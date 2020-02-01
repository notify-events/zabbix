#!/bin/bash

set -eu

to="$1"
subject="$2"
message="$3"
severity="$4"
status="$5"

url="https://notify.events/api/v1/channel/source/${to}/execute"

curl -sm 5 -d "subject=${subject}" -d "message=${message}" -d "severity=${severity}" -d "status=${status}" $url
