#!/bin/bash

TMPBIN=tmp_binary.txt

TMPDWNLOAD=Download.json

read -p "Please enter your username " USRNAME

read -p "Please enter your search query " -r QUERY

echo $QUERY
echo $QUERY | python -m json.tool

while [[ $? != 0 ]]; do
    read -p "Please enter your search query. Example: {\"search_query\": \"{\\\"device_class\\\": \\\"Printer\\\"}\"} " -r QUERY
    echo $QUERY
    echo $QUERY | python -m json.tool
done

echo "$USRNAME searching for $QUERY"

echo $QUERY | python -m json.tool > searchQuery.json

SEARCH=$(curl  https://faf.caad.fkie.fraunhofer.de/rest/search -u "$USRNAME" -X GET --data-urlencode data@searchQuery.json)

echo "$SEARCH"

DWNLOAD=$(curl https://faf.caad.fkie.fraunhofer.de/rest/download -u geierhaas -X GET -d data='{"uid": "b25ced5e73f8d823c523d01f406894c2f46e941d83afbb574d439d43be85011d_14725369"}')

echo "$DWNLOAD" > "$TMPDWNLOAD"

BIN=$(cat "$TMPDWNLOAD" | cut -f4 -d: | cut -f2 -d\")

NAME=$(cat "$TMPDWNLOAD" | cut -f2 -d: | cut -f1 -d, | cut -f2 -d\")

echo "$BIN" > "$TMPBIN"

python -m base64 -d "$TMPBIN" > "$NAME"

rm "$TMPBIN"
rm "$TMPDWNLOAD"

exit 0
