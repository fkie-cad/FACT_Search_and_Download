#!/bin/bash

FACT_URL=https://faf.caad.fkie.fraunhofer.de

TMPSEARCH=search.txt
TMPBIN=tmp_binary.txt
TMPDWNLOAD=download.json
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

SEARCH=$(curl "$FACT_URL/rest/firmware?" -u "$USRNAME:$PASS" -X GET -G --data-urlencode "query=$QUERY")

echo "$SEARCH" > "$TMPSEARCH"

if [[ $(cat "$TMPSEARCH" | grep html) ]]; then
    printf "Something went wrong. Please try again.\n"
    exit 1
fi

#Extract only a list of uids from the returned json dictionary
UIDLIST=$(cat "$TMPSEARCH" | grep -Eio '("uids": \[.*\])' | cut -f2 -d:)
echo "$UIDLIST" > "$TMPUIDLIST"

#Turn the extracted uids into an array, so they can be iterated over
UIDARRAY=$(sed 's/ \[//g;s/\]//g;s/"//g;s/, /\n/g' "$TMPUIDLIST")

while read -r line; do

    echo "Downloading image with uid $line"

    DWNLOAD=$(curl "$FACT_URL/rest/binary/$line" -u "$USRNAME:$PASS" -X GET)

    echo "$DWNLOAD" > "$TMPDWNLOAD"

    #Extract the part of the returned json that contains the binary and the part that contains the name
    BIN=$(cat "$TMPDWNLOAD" | grep -Eio '("binary": .*")' | cut -f2 -d: | cut -f2 -d\" )

    NAME=$(cat "$TMPDWNLOAD" | grep -Eio '("file_name": .*")' | cut -f2 -d: | cut -f2 -d\" )

    echo "$BIN" > "$TMPBIN"

    python -m base64 -d "$TMPBIN" > "$NAME"

done <<< "$UIDARRAY"

rm "$TMPSEARCH"
rm "$TMPBIN"
rm "$TMPDWNLOAD"
rm "$TMPUIDLIST"

exit 0
