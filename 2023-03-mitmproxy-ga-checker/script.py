from dotenv import load_dotenv
import os
import time
from mitmproxy import ctx, flow
from mitmproxy.http import HTTPFlow
from mitmproxy.script import concurrent

from be_data import (
    url_test_list1 as list1,
    url_test_list3 as list3,
    be_hostname,
    be_path_list,
)
from tools.functions import (
    ansi,
    enable_proxies,
    disable_proxies,
    url_set_builder,
    write_url_list,
    compare_url_lists
)

# Initialize .env
load_dotenv()
psw = os.getenv('password')

# Initialize empty set for URLs that are detected to have target query string parameters with 'google-analytics.com' as domain
ga_urls = set()

"""
Type in the name of this script to run it with mitmproxy; command in the line below
    `mitmproxy -s script.py --listen-host $(ipconfig getifaddr en0) -p 8081 --anticache`
    
- Selenium script to automate URL visitation must be ran separately, after mitmproxy has been activated and is listening.
- Do not exit the script while mitmproxy is active or else it will disrupt the process and the compare_url_list function will export an inaccurate output.
"""



class GoogleAnalyticsInterceptor:
    def __init__(self):
        # Prompt messages and web proxy enabling
        print(f'{ansi.Y}{ansi.BD}Initializing mitmproxy...{ansi.RST_ALL}')
        enable_proxies(psw, False)
        time.sleep(1)
        print(f'\n{ansi.B}{ansi.BD}Opening mitmproxy...{ansi.RST_ALL}\n')
        time.sleep(1)
        
        # Build unique url set from host name and list of paths.
        # url_set = url_set_builder(be_hostname, be_path_list) 
        # url_set = url_set_builder(be_hostname, list3) 
        url_set = list1 # Test with smaller set/list
        
        # Write unique URL set to CSV file to be compared later.
        write_url_list(url_set)
    
    
    @concurrent
    def request(self, flow: HTTPFlow) -> None:
        # Set variables for different values contained in HTTP requests
        request, meth, url, host, path, q = (
            flow.request,
            flow.request.method,
            flow.request.pretty_url,
            flow.request.pretty_host,
            flow.request.path,
            dict(flow.request.query),
        )
        
        # Conditions to meet to add to Google Analytics URL, `ga_urls` list to be compared against entire `url_set`
        http_method = 'POST'
        ga_domain1 = 'google-analytics.com'
        ga_domain2 = 'analytics.google.com'
        ga_path_lead = '/g/collect?v'
        url_key = 'dl'
        qsp_key = 'en' # qsp (query string parameter)
        value = 'view_item'
        
        if (meth == http_method and
            ga_domain1 or ga_domain2 in host and
            ga_path_lead in path):
            if q.get(qsp_key) == value:
                ctx.log.warn(f"Adding '{q.get(url_key)}' to 'ga_urls' set()")
                ga_urls.add(f"{q.get(url_key)}")
        # Ignore and go on to the next flow                
        else:
            pass

    @concurrent
    def response(self, flow: HTTPFlow) -> None:
        pass
    
    # General messages for error
    @concurrent
    def error(self, flow: HTTPFlow) -> None:
        # ctx.log.error("An HTTP error has occured.")
        pass

    # When the exiting mitmproxy is finished, compare `url_set` against `ga_urls`, outputting differences into CSV files.
    # 02-...csv shows all URLs. Green met the condition. Orange did not and need to be looked at.
    # 03-...csv shows all that were orange in 02-...csv without the orange marker prepended.
    @concurrent
    def done(self):
        if not ga_urls:
            print('nothing in ga_urls')
            print(ga_urls)
            pass
        else:
            print('running compare_url_lists(ga_urls)')
            compare_url_lists(ga_urls)
        
        # Disable proxies
        time.sleep(1)
        disable_proxies(psw, False)
        time.sleep(1)


addons = [GoogleAnalyticsInterceptor()]
