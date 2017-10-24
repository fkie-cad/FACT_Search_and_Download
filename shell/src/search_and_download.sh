#!/bin/bash

FACT_URL=https://faf.caad.fkie.fraunhofer.de

TMPQUERY=search_query.json
TMPSEARCH=search.txt
TMPBIN=tmp_binary.txt
TMPDWNLOAD=download.json
TMPUID=tmp_uid.json
TMPUIDLIST=tmp_uids.txt

read -p "Please enter your username " USRNAME
read -p "Please enter your password " -s -r PASS
printf "\n"
read -p "Please enter your search query " -r QUERY

echo $QUERY
echo $QUERY | python -m json.tool

while [[ $? != 0 ]]; do
    read -p "Please enter your search query. Example: {\"search_query\": \"{\\\"device_class\\\": \\\"Printer\\\"}\"} " -r QUERY
    echo $QUERY
    echo $QUERY | python -m json.tool
done

echo "$USRNAME downloading all data for search query $QUERY"
echo $QUERY | python -m json.tool > "$TMPQUERY"

SEARCH=$(curl  $FACT_URL/rest/search -u "$USRNAME:$PASS" -X GET --data-urlencode data@"$TMPQUERY")

echo "$SEARCH" > "$TMPSEARCH"

if [[ $(cat "$TMPSEARCH" | grep html) ]]; then
    printf "Something went wrong. Please try again.\n"
    exit 1
fi

#Extract only a list of uids from the returned json dictionary
UIDLIST=$( cat search.txt | cut -f2 -d: | cut -f1 -d\} )
echo "$UIDLIST" > "$TMPUIDLIST"

#Turn the extracted uids into an array, so they can be iterated over
UIDARRAY=$(sed 's/\[//g;s/\]//g;s/"//g;s/,/\n/g' "$TMPUIDLIST")

while read -r line; do

    echo "Downloading image with uid $line"

    DATA="{\"uid\": \"$line\"}"

    echo $DATA | python -m json.tool > "$TMPUID"

    DWNLOAD=$(curl $FACT_URL/rest/download -u "$USRNAME:$PASS" -X GET --data-urlencode data@"$TMPUID")

    echo "$DWNLOAD" > "$TMPDWNLOAD"

    #Extract the part of the returned json that contains the binary and the part that contains the name
    BIN=$(cat "$TMPDWNLOAD" | cut -f4 -d: | cut -f2 -d\")
    NAME=$(cat "$TMPDWNLOAD" | cut -f3 -d: | cut -f1 -d, | cut -f2 -d\")

    echo "$BIN" > "$TMPBIN"

    python -m base64 -d "$TMPBIN" > "data/$NAME"

done <<< "$UIDARRAY"

rm "$TMPQUERY"
rm "$TMPSEARCH"
rm "$TMPBIN"
rm "$TMPDWNLOAD"
rm "$TMPUID"
rm "$TMPUIDLIST"

exit 0
