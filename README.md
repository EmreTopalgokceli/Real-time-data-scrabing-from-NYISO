# Data Extraction and Transformation from NYISO

This repository contains a script that extracts and transforms data from the New York Independent System Operator (NYISO) website.

**Requirements**
* Python 3.x
* Pandas library
* Zipfile library
* Urllib library

**Usage**
To use the script, simply run the nyiso_extraction.py file. The script will extract data from NYISO website and save the output as a csv file named "data_EMRE_TOPALGOKCELI.csv" in the same directory.

**Description**
The script extracts data from NYISO's public data repository for the first twelve months of 2005, which are stored as zip files containing CSV files. The script iterates through the zip files and reads all the CSV files after removing the zipped structure. The data is then combined into a single Pandas DataFrame.

After combining the data, the script performs some data cleaning and manipulation. The unnecessary columns are dropped, and the "Time Stamp" column is converted from an object to a datetime data type. The timestamp column is then converted to UTC time with daylight saving adjustment. Finally, the column names are changed as requested and a source column is added with a value of "NYISO".
