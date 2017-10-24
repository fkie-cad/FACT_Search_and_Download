# FACT - Search and Download

This is a tool to automatically download all images from the database of FACT for a search query you specify. 

## Usage
The current (preliminary) tool consists of just one bash-script that does not support any additional parameters.  
Enter your username, password and search query as promted.  
Example:
```bash
$ ./search_and_download.sh
Please enter your username XXX
Please enter your password XXX
Please enter your search query {"search_query": "{\"device_class\": \"Printer\"}", "firmware_flag": true}
```
If you want to download all firmwares including a file matching your search, set "firmware_flag" to *true*.
