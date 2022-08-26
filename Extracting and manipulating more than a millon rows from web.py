import pandas as pd
from io import BytesIO
import zipfile
import datetime

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

my_dict = {}    # An empty dict. is needed to add dataframes.

# Since the targets are zip/zip file, we need a function itterating until making open all the zipped folder.
# With the below function, I converted all files name to lower case to avoid leaving data out because folder's name mismatch.
# The zip_opener function will not stop until all zipped folder is opened.

def zip_opener(data):
    zip_file = zipfile.ZipFile(BytesIO(data))
    for i in zip_file.namelist():
        if i.lower().endswith(".csv"):
            my_list[i] = pd.read_csv(zip_file.open(i))
        elif i.lower().endswith(".zip"):
            zip_opener(zip_file.open(i).read())


# The below function helps us to reach the data sources and read all after removing zipped structure.
def get_data_from_url(url):
    req = urlopen(url)
    zip_opener(req.read())


# Soruce locations
source_list = ["http://mis.nyiso.com/public/csv/pal/20050101pal_csv.zip",
               "http://mis.nyiso.com/public/csv/pal/20050201pal_csv.zip",
               "http://mis.nyiso.com/public/csv/pal/20050301pal_csv.zip",
               "http://mis.nyiso.com/public/csv/pal/20050401pal_csv.zip",
               "http://mis.nyiso.com/public/csv/pal/20050501pal_csv.zip",
               "http://mis.nyiso.com/public/csv/pal/20050601pal_csv.zip",
               "http://mis.nyiso.com/public/csv/pal/20050701pal_csv.zip",
               "http://mis.nyiso.com/public/csv/pal/20050801pal_csv.zip",
               "http://mis.nyiso.com/public/csv/pal/20050901pal_csv.zip",
               "http://mis.nyiso.com/public/csv/pal/20051001pal_csv.zip",
               "http://mis.nyiso.com/public/csv/pal/20051101pal_csv.zip",
               "http://mis.nyiso.com/public/csv/pal/20051201pal_csv.zip"]


# Importing data from the source.
for link in source_list:
    get_data_from_url(link)
    print(link)     # Check if all of them is read.

# Bring all dataframes together. You could check the outcome by dfs.shape, or dfs.info for both first and last 5 observations.
dfs = pd.concat(my_list)

dfs.reset_index(inplace=True)      # We should to reset index to drop columns that we do not need.

dfs.drop(["level_0", "level_1", "Time Zone", "PTID"], axis=1, inplace=True)     # Drop unnecessary columns.

# When I checked the data, I realized that Time Stamp variable seems as an object. I changed its type as datatime.
dfs["Time Stamp"] = pd.to_datetime(dfs["Time Stamp"], format="%m/%d/%Y %H:%M:%S")   # It seems okay now.

# to UTC with daylight saving adjustment.
dfs["Time Stamp"] = dfs["Time Stamp"].dt.tz_localize("EST", ambiguous="infer").dt.tz_convert(None)

# Rename the columns as requested.
dfs.columns = ["timestamp", "pca_abbrev", "load_mw"]

dfs["source"] = "NYISO"         # Add a source column for all.

dfs.info()        # For last check.

# Write to a csv file.
dfs.to_csv("Codding_Assessment_EMRE_TOPALGOKCELI.csv")