#!/bin/zsh

yellow='\033[33m'
green='\033[32m'
reset='\033[0m'

# 🚧
IPADDR=$(ipconfig getifaddr en0)
PORT=8081

# Default path. Can change to yaml in project root
CONFPATH=~/.mitmproxy/config.yaml

echo "${yellow}Enabling web proxies...${reset}"
echo $psw | sudo -S networksetup -setwebproxy "Wi-Fi" ${IPADDR} ${PORT}
echo $psw | sudo -S networksetup -setsecurewebproxy "Wi-Fi" ${IPADDR} ${PORT}
echo "${green}Web proxies enabled...${reset}\n"

read -q "REPLY?Would you like to include a script? (y/n) "
echo "\n"

if [[ $REPLY =~ ^[Yy]$ ]]
then
  read "SCRIPT_NAME?Enter the name of the Python script to use with mitmproxy: "
  echo "\n"

  echo "${green}Starting mitmproxy with script $SCRIPT_NAME.py...${reset}"
  # mitmproxy -s "$SCRIPT_NAME.py" --console-layout single --listen-host ${IPADDR} --listen-port ${PORT} --anticache
  mitmproxy -s "$SCRIPT_NAME.py" --console-layout single --listen-host ${IPADDR} --listen-port ${PORT} --conf ${CONFPATH}
else
  echo "${green}Starting mitmproxy...${reset}"
  mitmproxy --listen-host ${IPADDR} --listen-port ${PORT} --anticache
fi

echo "To exit mitmproxy, press Ctrl-C"
wait &

echo "${yellow}\nDisabling web proxies...${reset}"
echo $psw | sudo -S networksetup -setwebproxystate "Wi-Fi" off
echo $psw | sudo -S networksetup -setsecurewebproxystate "Wi-Fi" off 

echo "${yellow}\nChecking web proxies...${reset}\n"
zsh ~/.local-scripts/proxy_check.sh

echo "\n${green}Done.${reset}"
