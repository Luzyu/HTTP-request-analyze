# Google Analytics Query String Parameter Checker

Uses mitmproxy to analyze and intercept target network traffic and Selenium to visit target URLs that initiate target network traffic.

## Choose your package manager relative to your system. For macOS users, use [homebrew](https://www.homebrew.sh)
mitmproxy 9.0.1: `brew install mitmproxy`
Python 3.11.x: `brew install python@3.11`
google-chrome: `brew install --cask chromedriver`
chromedriver: `brew install --cask chromedriver`
firefox: `brew install --cask firefox`
geckodriver: `brew install --cask geckodriver`

## Python3 Requirements
Major packages are mitmproxy, selenium, and python-dotenv. Others are needed, check the requirements.txt file.

```zsh
virtualenv -p python3.11 .venv
pip3 install --update pip
pip3 install --update setuptools
pip3 install --update wheel
pip3 install -r requirements.txt
```

## Shell commands to run this application:

### Add your local password to the `.sh` files in the `scripts/` folder

Inside of most or all of the `.sh`, you'll see a line that states `psw="yourpassword"`. You need to insert your local user password in these in order for the scripts to work without trouble. This should be the password you use to log into your computer. It is needed to execute any commands that are initialized with `sudo`.

### Moving the `config.yaml` for `mitmproxy` file to its proper location
If you do not already have a config.yaml ready, then rename config.example.yaml to config.yaml and then run this command:

```zsh
# Move the config.yaml file to ~/.mitmproxy. Create the folder if it doesn't already exist.
mv config.yaml ~/.mitmproxy/config.yaml
```

Modify the config.yaml as needed. If you're not using `bash` or `zsh`, then change the script commands accordingly to your terminal shell.

### Running mitmproxy and loading it with a script
You'll need to have two terminal shell screens running. For both, don't forget to activate your virtual environment. For the script name, do not add the extension. Just the name. So, don't put `script.py` when prompted with *"What is the name of the script?"*, put `script` or whatever you may rename the file. Moreover, if you're using `bash`, then replace `zsh start-mitmproxy.sh` with `bash start-mitmproxy.sh`. If this doesn't work, then execute the `.sh` file's logic in a way that conforms to your system's shell.

Screen 1:

```zsh
source .venv/bin/activate
zsh start-mitmproxy.sh
	Would you like to add a script (y/n) y
	What is the name of the script? script
```
Running Selenium

Screen 2:

```zsh
source .venv/bin/activate
python3 selen.py
```