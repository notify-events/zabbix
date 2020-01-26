#!/bin/bash

set -eu

token="$1"
subject="$2"
message="$3"
severity="$4"

url="https://notify.events/api/v1/channel/source/${token}/execute"

curl -sm 5 -d "subject=${subject}" -d "message=${message}" -d "severity=${severity}" $url
