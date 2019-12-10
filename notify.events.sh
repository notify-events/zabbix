#!/bin/bash

set -eu

channel_token="$1"
subject="$2"
message="$3"

url="https://notify.events/api/channel/source/${channel_token}"

payload="payload={\"subject\":\"${subject//\"/\\\"}\",\"message\":\"${message//\"/\\\"}\"}"

curl -sm 5 --data-urlencode "${payload}" $url
