import subprocess
import time
import os
import re
import csv
import shutil
import textwrap
import urllib.parse
from types import SimpleNamespace
from dotenv import load_dotenv

from mitmproxy import ctx

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchWindowException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# ANSI Escape Codes for colored terminal formatting
ansi = SimpleNamespace(
    # Text colors
    BL="\033[30m", # BLACK
    R="\033[31m", # RED
    GR="\033[32m", # GREEN
    Y="\033[33m", # YELLOW
    B="\033[34m", # BLUE
    M="\033[35m", # MAGENTA
    C="\033[36m", # CYAN
    W="\033[37m", # WHITE
    RST="\033[39m", # RESET
    
    # Text colors (high intensity)
    HIR="\033[91m",
    HIG="\033[92m",
    HIY="\033[93m",
    HIB="\033[94m",
    HIM="\033[95m",
    HIC="\033[96m",
    HIW="\033[97m",
    
    # Background colors
    BGBL="\033[40m",
    BGR="\033[41m",
    BGGR="\033[42m",
    BGY="\033[43m",
    BGB="\033[44m",
    BGM="\033[45m",
    BGC="\033[46m",
    BGW="\033[47m",
    BGRST="\033[49m",
    
    # Background colors (high intensity)
    BGHIBL="\033[100m",
    BGHIR="\033[101m",
    BGHIGR="\033[102m",
    BGHIY="\033[103m",
    BGHIB="\033[104m",
    BGHIM="\033[105m",
    BGHIC="\033[106m",
    BGHIWH="\033[107m",
    
    # Text styles
    BD="\033[1m", # BOLD
    IT="\033[3m", # ITALIC
    ST="\033[9m", # STRIKETHROUGH
    D="\033[2m", # DIM
    U="\033[4m", # UNDERLINE
    BK="\x1b[5m", # BLINK
    RV="\033[7m", #REVERSE
    HDN="\033[8m", # HIDDEN
    RST_BK="\x1b[25m", # RESET BLINK
    RST_ALL="\033[0m", # RESET ALL
    
    # Cursor movements
    CURSOR_UP="\033[{n}A",
    CURSOR_DOWN="\033[{n}B",
    CURSOR_FORWARD="\033[{n}C",
    CURSOR_BACKWARD="\033[{n}D",
    CURSOR_POSITION="\033[{row};{column}H",
    SAVE_CURSOR_POSITION="\033[s",
    RESTORE_CURSOR_POSITION="\033[u",
    
    # Screen operations
    CLEAR_SCREEN="\033[2J",
    CLEAR_SCREEN_UP="\033[1J",
    CLEAR_SCREEN_DOWN="\033[J",
    CLEAR_LINE="\033[2K",
    CLEAR_LINE_START="\033[1K",
    CLEAR_LINE_END="\033[K",
    
    # Other
    SCROLL_UP="\033[{n}S",
    SCROLL_DOWN="\033[{n}T",
)

load_dotenv()
psw = os.getenv('password')
SCHEME = os.getenv('SCHEME')
MITMPROXY_HOST = os.getenv('MITMPROXY_HOST')
MITMPROXY_PORT = os.getenv('MITMPROXY_PORT')
MITMPROXY_CER = os.getenv('MITMPROXY_CER')
MITMPROXY_PEM = os.getenv('MITMPROXY_PEM')

# Optional
CHROMEDRIVER_ABS_PATH = os.getenv('CHROMEDRIVER_PATH')


def check_proxy_states(psw):
    # Build the commands as a list of arguments
    cmd1 = ["echo", psw]
    cmd2 = ["sudo", "-S", "scutil", "--proxy"]
    cmd3 = ["grep", "HTTPEnable :"]
    cmd4 = ["awk", "{print $3}"]
    cmd5 = ["sudo", "scutil", "--proxy"]
    cmd6 = ["grep", "HTTPSEnable :"]
    cmd7 = ["awk", "{print $3}"]

    # Run the commands using subprocess
    p1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE)
    p2 = subprocess.Popen(cmd2, stdin=p1.stdout, stdout=subprocess.PIPE)
    p3 = subprocess.Popen(cmd3, stdin=p2.stdout, stdout=subprocess.PIPE)
    p4 = subprocess.Popen(cmd4, stdin=p3.stdout, stdout=subprocess.PIPE)
    http_enabled = p4.communicate()[0].decode().strip()
    p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits
    p2.stdout.close()  # Allow p2 to receive a SIGPIPE if p3 exits
    p3.stdout.close()  # Allow p3 to receive a SIGPIPE if p4 exits

    p5 = subprocess.Popen(cmd5, stdout=subprocess.PIPE)
    p6 = subprocess.Popen(cmd6, stdin=p5.stdout, stdout=subprocess.PIPE)
    p7 = subprocess.Popen(cmd7, stdin=p6.stdout, stdout=subprocess.PIPE)
    https_enabled = p7.communicate()[0].decode().strip()
    p5.stdout.close()  # Allow p5 to receive a SIGPIPE if p6 exits
    p6.stdout.close()  # Allow p6 to receive a SIGPIPE if p7 exits

    # Check if HTTP Proxy is enabled or disabled
    if int(http_enabled) == 0:
        print(f"⨯ {ansi.R}HTTP Proxy is disabled.{ansi.RST}")
    else:
        print(f"✓ {ansi.GR}HTTP Proxy enabled.{ansi.RST}")

    # Check if HTTPS Proxy is enabled or disabled
    if int(https_enabled) == 0:
        print(f"⨯ {ansi.R}HTTPS Proxy is disabled.{ansi.RST}")
    else:
        print(f"✓ {ansi.GR}HTTPS Proxy enabled.{ansi.RST}")

def enable_proxies(password, quiet=False):
    password = "password"
    
    cmd1 = ["echo", password]
    cmd2 = ["sudo", "-S", "networksetup", "-setwebproxy", "Wi-Fi", "192.168.1.70", "8081"]
    cmd3 = ["echo", password]
    cmd4 = ["sudo", "-S", "networksetup", "-setsecurewebproxy", "Wi-Fi", "192.168.1.70", "8081"]
    
    if quiet == True:
      pass
    elif quiet == False:
      print(f"{ansi.Y}Enabling web proxies...{ansi.RST}")
    
    p1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE)
    p2 = subprocess.Popen(cmd2, stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()
    p3 = subprocess.Popen(cmd3, stdout=subprocess.PIPE)
    p4 = subprocess.Popen(cmd4, stdin=p3.stdout, stdout=subprocess.PIPE)
    p3.stdout.close()
    output, error = p2.communicate()
    print(output.decode())
    output, error = p4.communicate()
    print(output.decode())
    
    if quiet == True:
      pass
    elif quiet == False:
      print(f"{ansi.Y}\nChecking web proxies...{ansi.RST}\n")
      check_proxy_states(password)
      
      print(f"\n{ansi.GR}Web proxies enabled...{ansi.RST}\n")
    
    del password

def disable_proxies(password, quiet=False):
    cmd1 = ["echo", password]
    cmd2 = ["sudo", "-S", "networksetup", "-setwebproxystate", "Wi-Fi", "off"]
    cmd3 = ["echo", password]
    cmd4 = ["sudo", "-S", "networksetup", "-setsecurewebproxystate", "Wi-Fi", "off"]

    p1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE)
    p2 = subprocess.Popen(cmd2, stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()
    p3 = subprocess.Popen(cmd3, stdout=subprocess.PIPE)
    p4 = subprocess.Popen(cmd4, stdin=p3.stdout, stdout=subprocess.PIPE)
    p3.stdout.close()
    
    if quiet == True:
      pass
    elif quiet == False:
      output, error = p2.communicate()
      print(f"{ansi.Y}\nDisabling web proxies...{ansi.RST}")
      print(output.decode())
      output, error = p4.communicate()
      print(output.decode())

      print(f"{ansi.Y}\nChecking web proxies...{ansi.RST}\n")
      check_proxy_states(password)

      print(f"\n{ansi.GR}Web proxies disabled.{ansi.RST}\n")
      
    del password

# Generate URLs array
def url_set_builder(host, path_list):
  url_list = [f"{host}{path}" for path in path_list]
  return set(url_list)


# Go to a single URL
def go_to_url(url, quiet=False, proxy='proxy-off', headless='headless-off'):
  try:
    chrome_options = Options()
    # ua_str = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    
    if headless == 'headless-on':
      chrome_options.add_argument('--headless')
    elif headless == 'headless-off':
      pass
    
    if proxy == 'proxy-off':
      chrome_options.add_argument('--no-proxy-server')
    elif proxy == 'proxy-on':
      chrome_options.add_argument(f'--proxy-server={SCHEME}://{MITMPROXY_HOST}:{MITMPROXY_PORT}')
    elif proxy == 'proxy-auto':
      chrome_options.add_argument('--proxy-auto-detect')
    else:
      pass
    # chrome_options.add_argument(f'--cert-server-certificate={MITMPROXY_CER}')
    # chrome_options.add_argument(f'--cert-client-key={MITMPROXY_PEM}')
    chrome_options.add_argument('--disable-popup-blocking')
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--enable-automation')
    chrome_options.add_argument('--test-type=webdriver')
    chrome_options.add_argument('--disable-sync')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-background-networking')
    chrome_options.add_argument('--disable-client-side-phishing-detection')
    # chrome_options.add_argument('--acceptInsecureCerts=true')
    # chrome_options.add_argument('--ignore-certificate-errors')

    # initialize the Chrome driver
    driver = webdriver.Chrome(options=chrome_options)

    # go to the URL
    driver.get(url)

    # wait for 10 seconds for the google-analytics element to be present
    wait = WebDriverWait(driver, 6)

    # Start a timer timer
    if quiet == True:
       pass
    elif quiet == False:
      start_time = time.time()
      pattern = re.compile(r'sit-gaLoaded')
    

    try:
      wait.until(EC.presence_of_element_located((By.XPATH, "//script[contains(text(),'sit-gaLoaded')]")))
      element = wait.until(EC.presence_of_element_located((By.XPATH, "//script[contains(text(),'sit-gaLoaded')]")))

      if quiet == True:
        pass
      elif quiet == False:
        print(f"{ansi.GR}{ansi.BD}✓ 'sit-gaLoaded'{ansi.RST} detected in <script> tag:")
        print(f"Tag name: {element.tag_name}")
        print(f"Script content:")
        print("-"*50)
        print(f'<script type="text/javascript" id>')
        inner_html = element.get_attribute('innerHTML')
        highlighted_html = pattern.sub(f"{ansi.GR}{ansi.BD}sit-gaLoaded{ansi.RST}", inner_html)
        print(f"{highlighted_html}")
        print(f'</script>')
        print("-"*50)
        print("\n")

    except TimeoutException:
        print(f"{ansi.R}{ansi.BD}⨯ Timed out waiting for google-analytics element{ansi.RST}\n")
    except WebDriverException as e:
          if isinstance(e, NoSuchWindowException):
              print(f"{ansi.R}{ansi.BD}⨯ Browser window was closed prematurely{ansi.RST}\n")
              print(f"{ansi.Y}Exiting the script.")
              exit(1)
          else:
              raise e
    finally:
        # Stop the timer and print the execution time
        end_time = time.time()
        if quiet == True:
          pass
        elif quiet == False:
          print(f"Script execution time: {end_time - start_time:.2f} seconds")

        # close the browser window
        driver.close()
        time.sleep(2)
        driver.quit()
  except KeyboardInterrupt:
    print(f"\n{ansi.R}{ansi.BD}⨯ Terminated with a KeyboardInterrupt.{ansi.RST}\n")
    exit(1)

def visit_all_urls(urls_array, quiet=False, proxy='proxy-off', headless='headless-off'):
    for i, url in enumerate(urls_array):
      if quiet == True:
        pass
      elif quiet == False:
        iteration_num = f'#{i+1:03d}'
        wrapped_url = (f'\n {" "*4}').join(textwrap.wrap(url, width=31))
        print(f'{ansi.Y}{ansi.BD}\n ✦✦✦ {ansi.BK}⎨Running Iteration {iteration_num}{ansi.RST_BK}⎬ ✦✦✦{ansi.RST}\n')
        print(f'{" "*2}{ansi.B}{ansi.BD}{wrapped_url}{ansi.RST_ALL}\n')
      
      go_to_url(url, quiet, proxy, headless)
      
      if quiet == True:
        pass
      elif quiet == False:
        print(f'{ansi.GR}{ansi.BD} Script finished for:{ansi.RST}\n{ansi.B}{url}{ansi.RST}\n\n')


def parse_ga_key(path, key):
  decoded_path = urllib.parse.unquote_plus(path)
  decoded_path = decoded_path.replace("%2F", "/").replace('%3A', ':').replace('%25', '%').replace('%3B', ';').replace('%7C', '|').replace('%20', ' ')
  decoded_path = decoded_path.split(f"{key}=")[1].split('&')[0]
  return decoded_path

def print_all_ga_keys(path):
  ga_qsp_keys = {
      'version': parse_ga_key(path, 'v'),
      'tracking_id': parse_ga_key(path, 'tid'),
      'gtm_id': parse_ga_key(path, 'gtm'),
      'ga_anon_cid': parse_ga_key(path, '_p'),
      'user_ucid': parse_ga_key(path, 'cid'), # cid = client id
      'ulang': parse_ga_key(path, 'ul'),
      'uarch': parse_ga_key(path, 'uaa'),
      'ubrowser_bitness': parse_ga_key(path, 'uab'),
      'uagent_browser': parse_ga_key(path, 'uafvl'),
      'avail_mem_ubrowser': parse_ga_key(path, 'uamb'),
      'uplaansiorm': parse_ga_key(path, 'uap'),
      'uwindow_env': parse_ga_key(path, 'uaw'), # windowed environment?
      'ev_update': parse_ga_key(path, '_eu'), # see whether a hit is the first in a session or a subsequent hit
      'sess_ctrl': parse_ga_key(path, '_s'),
      'currency': parse_ga_key(path, 'cu'),
      'sess_id': parse_ga_key(path, 'sid'),
      'sess_hits': parse_ga_key(path, 'sct'), # number of hits in the current session
      'hit_segment': parse_ga_key(path, 'seg'), # the user segment to which the hit belongs
      'tracked_url': parse_ga_key(path, 'dl'), # the URL of the page being tracked
      'tracked_title': parse_ga_key(path, 'dt'), # the title of the page being tracked
      'event_name': parse_ga_key(path, 'en'), # identify the type of user interaction being tracked, like viewing a product, adding an item to the cart, checkout, etc.
      'prod_info1': parse_ga_key(path, 'pr1'), # product information for an ecommerce transaction
      'price': parse_ga_key(path, 'ep.value') # ep stands for ecommerce parameters -- ep. is about the whole ecommerce transaction, so it won't appear in front of sth like pr1
  }
  for key, value in ga_qsp_keys.items():
      print(f"{ansi.B}{key}{ansi.RST}: {ansi.Y}{value}{ansi.RST}")

def write_url_list(url_list, filename='output'):
  print(f'{ansi.Y}Writing to 01-{filename}.csv{ansi.RST}.')
  with open(f'01-{filename}.csv', 'w') as csvfile:
      csvwriter = csv.writer(csvfile)
      for url in url_list:
          csvwriter.writerow([url])
  print(f'{ansi.GR}Finished writing to 01-{filename}.csv{ansi.RST_ALL}.')  
  
def compare_url_lists(url_list_comparand, filename='output'):
    shutil.copyfile(f'01-{filename}.csv', f'02-{filename}_compared.csv')
    copied_file = f'{filename}_compared'
    
    print(f'{ansi.Y}Reading 02-{copied_file}.csv{ansi.RST_ALL}. Finding rows.')
    with open(f'02-{copied_file}.csv', 'r') as csvfile:
      rows = list(csv.reader(csvfile))
      non_list = []
      for i in range(0, len(rows)):
        if rows[i][0] in url_list_comparand:
          rows[i][0] = f'🟢 {rows[i][0]}'
        else:
          non_list.append(rows[i][0])
          rows[i][0] = f'🟠 {rows[i][0]}'
    
    print(f'{ansi.Y} Prepending "🟢" to matching URLs in {ansi.IT}"02-{copied_file}.csv"{ansi.RST_ALL}')
    with open(f'02-{copied_file}.csv', 'w', newline='') as csvfile:
      csvwriter = csv.writer(csvfile)
      csvwriter.writerows(rows)
      
    print(f'{ansi.Y} Writing URLs not present in both lists to {ansi.IT}"03-{filename}_non_list.csv"{ansi.RST_ALL}')
    with open(f'03-{filename}_non_list.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for url in non_list:
            csvwriter.writerow([url]) 

# from be_data import url_test_list1, url_test_list2
# write_url_list(url_test_list1, 'playground_output')
# compare_url_lists(url_test_list2, 'playground_output')

def countdown(duration, type=None):
  if type == 'mitm':
    for i in range(duration, 0, -1):
      ctx.log.warn(f"\n\nTime left: {i} seconds\n\n")
      time.sleep(1)
      ctx.log.alert(f"\n\nTime's up!\n\n")
  elif type==None:
    for i in range(duration, 0, -1):
      print(f"{ansi.Y}Time left: {i} seconds{ansi.RST}")
      time.sleep(1)
    print(f"{ansi.GR}{ansi.BK}Time's up!{ansi.RST_ALL}")
