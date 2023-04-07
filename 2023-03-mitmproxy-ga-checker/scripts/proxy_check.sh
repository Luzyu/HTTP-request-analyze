#!/bin/zsh

# 🚧
psw="yourpassword"
red="${red}"
gr="${gr}"
rst="${rst}"

# Check if HTTP Proxy is enabled or disabled
http_enabled=$(echo $psw | sudo -S scutil --proxy | grep "HTTPEnable :" | awk '{print $3}')

if [[ $http_enabled -eq 0 ]]; then
  echo -e "⨯ \${red}HTTP Proxy is disabled.${rst}"
else
  echo -e "✓ ${gr}HTTP Proxy enabled.${rst}"
fi

# Check if HTTPS Proxy is enabled or disabled
https_enabled=$(sudo scutil --proxy | grep "HTTPSEnable :" | awk '{print $3}')

if [[ $https_enabled -eq 0 ]]; then
  echo -e "⨯ ${red}HTTPS Proxy is disabled.${rst}"
else
  echo -e "✓ ${gr}HTTPS Proxy enabled.${rst}"
fi
