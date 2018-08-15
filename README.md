# FACT Search and Download

[![Build Status](https://travis-ci.org/fkie-cad/FACT_Search_and_Download.svg?branch=master)](https://travis-ci.org/fkie-cad/FACT_Search_and_Download)
[![codecov](https://codecov.io/gh/fkie-cad/FACT_Search_and_Download/branch/master/graph/badge.svg)](https://codecov.io/gh/fkie-cad/FACT_Search_and_Download)

This program utilizes the [FACT](https://fkie-cad.github.io/FACT_core/) REST API to find and download all files matching a specific query.
If used with '*-F*' parameter it downloads all firmware image that include files matching the query.

This tool is intended to create a ground truth matching specific parameters for scientific research on firmware.

## Usage

Write a mongodb query into a json file and execute the following command

```sh
src/fact_search_and_download.py -H http://YOUR_FACT_INSTALLATION -Q PATH_TO_JSON_FILE_WITH_MONGO_QUERY -d STORE_FILES_TO_THIS_DIR
```

Alternatively you can write the query right to the command line if you use '*-q*' instead of '*-Q*'.  

### Example
This line downloads all ELF executables that are larger than 4kb from a local FACT installation to the current working directory.

```sh
src/fact_search_and_download.py -q {"$and": [{"processed_analysis.file_type.mime": "application/x-executable"}, {"size": {"$gte" : 4096}}]}
```

## Install Requrirements
```sh
sudo -EH pip3 install -r requirements.txt
```

## Limitations
At the moment the tool does not support FACT installations with authentication enabled. 

## License
```
    FACT Search and Download
    Copyright (C) 2017-2018  Fraunhofer FKIE

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
```