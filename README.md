## faf_search_and_download

This is a tool to automatically download all images from the database of FAF for a search query you specify. 

### Usage
The current (preliminary) tool consists of just one bash-script that does not support any additional parameters.  
Enter your username, password and search query as promted.  
Example:
```bash
$ ./search_and_download.sh
Please enter your username geierhaas
Please enter your password 
Please enter your search query {"search_query": "{\"device_class\": \"Printer\"}", "firmware_flag": true}
```
If the returned data is supposed to be only full images, the firmware flag must be set to true.
