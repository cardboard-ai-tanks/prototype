#!/bin/sh
sleep 15

_IP=$(hostname -I) || true
if [ "$_IP" ]; then
  printf "My IP address is %s\n" "$_IP"
  curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"content": "hello from '"$_IP"'"}' 'https://discordapp.com/api/webhooks/588040369124671546/d-ENUy_43IVypKqUz-UHsI-CNzKJbEdX7YYAKMXm4jRVhXPquUM7It_QBYBoveZp9HZm'
fi

