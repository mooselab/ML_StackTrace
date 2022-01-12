#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import re
from pathlib import Path
from typing import Tuple, List, Optional, Union
from pprint import pprint

# pd.options.display.max_colwidth = 999
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# .csv configuration
encoding = "utf-8"
delimiter = None
working_directory_path = "/home/amin/Desktop/DevOps_final_projecct/"


# ## Loading Dataset

pure_data = working_directory_path + "question_tag.csv"
path = Path(pure_data)

if path.suffix == ".csv":
    df = pd.read_csv(path, encoding=encoding)
else:
    raise ValueError("{data_file_path.suffix} extensions are not supported")


def tag_filter(pref_tags: List, tags: str) -> bool:
    regex = ""
    for tag in pref_tags:
        regex += '(?=.*\\b'+ tag +'([+-]?([0-9]*[.])?[0-9]*)\\b)'
    regex = r"^" + regex + ".*$"
    tags = tags.strip().lower()
    match_result = re.match(regex, tags, re.MULTILINE | re.IGNORECASE)
    if match_result is None:
        return 0
    else:
        return 1


tags = ["tensorflow", "python"]
df['HasPreferableTags'] = df['Tags'].apply(lambda row_tags: tag_filter(tags, row_tags))


df_w_tags = df[df['HasPreferableTags']==True]


# The new dataset that has a specific tag/s reduced to:

print("The orginal DB: ", df.shape[0])
print("The new DB: ", df_w_tags.shape[0])
print("The difference is: ", df.shape[0] - df_w_tags.shape[0])


df_w_tags = df_w_tags.drop(['HasPreferableTags'], axis='columns')


# ## Extracting the Code Parts from Body


def extract_code_blocks(body: str) -> List:
    regex = r"<pre><code>((.*?)|(\n)*)*(<\/code><\/pre>|</pre></code>)"
    matches = re.finditer(regex, body, re.MULTILINE | re.IGNORECASE)
    result=[]
    
    try:
        for matchNum, match in enumerate(matches):
            code = match.group()
            code = code.replace("<pre><code>", "")
            code = code.replace("</pre></code>", "")
            code = code.replace("</code></pre>", "")
            result.append(code)
    except:
        print("\n Error(1): ")
        print(body)
        return None

    return result

df_w_tags['Code'] = df_w_tags['Body'].apply(lambda row_body: extract_code_blocks(row_body))


# For testing:
df_w_tags = df_w_tags.reset_index(drop=True)


df_w_tags.to_csv('/home/amin/Desktop/DevOps_final_projecct/amin_result_v1.csv', encoding='utf-8')


# ## Find the Regular Expressions for Unix and Windows base Pathnames

# ### 1) Absolute and Relative Pathnames in UNIX OS

# Stack/trace example: https://stackoverflow.com/questions/37337728/tensorflow-internalerror-blas-sgemm-launch-failed

# Find the restrictions and limitations related to the Unix pathnames: https://www.cyberciti.biz/faq/linuxunix-rules-for-naming-file-and-directory-names/

# Online regular expression environment for testing: https://regex101.com/r/ZyEx5u/4

# > Regular Expression: "[^\n\&\:\|\>\<\/\ \"\;\&]*(\/[^\n\&\:\|\>\<\/]+)+\/([^\n\&\:\|\>\<\/]+)(\.pyc|\.py)"

# ### 1) Pathnames in Windows OS

# Stack/trace example: https://stackoverflow.com/questions/49434031/tensorflow-on-windows-cpu-version-importerror-no-module-named-pywrap-tensorf

# Find the restrictions and limitations related to the Windows pathnames: <br /> 
# https://docs.microsoft.com/en-us/dotnet/standard/io/file-path-formats <br />
# https://docs.microsoft.com/en-us/windows/win32/fileio/naming-a-file

# Online regular expression environment for testing: https://regex101.com/r/L6xmCa/1

# > Regular Expression: "[a-zA-Z]:\\?([^\<\>\:\"\\\/\/\|\?\*\n]+\\)+([^\<\>\:\"\\\/\/\|\?\*\n]+)(\.pyc|\.py)"

def extract_pathnames_from_code_column(code_sec: List) -> Tuple[str, List]: 
    try:
        result_post_file_names = []
        OS_flag = None
        
        for code in code_sec:
            regex_unix    = r"[^\n\&\:\|\>\<\/\ \"\;\&]*(\/[^\n\&\:\|\>\<\/]+)+\/([^\n\&\:\|\>\<\/]+)(\.pyc|\.py)"
            regex_windows = r"[a-zA-Z]:\\?([^\<\>\:\"\\\/\/\|\?\*\n]+\\)+([^\<\>\:\"\\\/\/\|\?\*\n]+)(\.pyc|\.py)"
            pattern_unix  = re.compile(regex_unix)
            pattern_windows  = re.compile(regex_windows)
            if pattern_unix.search(code):
                OS_flag = "unix"
                break
            elif pattern_windows.search(code):
                OS_flag = "windows"
                break
        
        if OS_flag == "unix":
            for code in code_sec:
                regex = r"[^\n\&\:\|\>\<\/\ \"\;\&]*(\/[^\n\&\:\|\>\<\/]+)+\/([^\n\&\:\|\>\<\/]+)(\.pyc|\.py)"
                code = code.replace("\\n", "\n")
                matches = re.finditer(regex, code, re.MULTILINE)
                file_names_for_each_code_part = []

                for matchNum, match in enumerate(matches, start=1):
                    file_names_for_each_code_part.append(match.groups()[1])
                    # print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
                    # for groupNum in range(0, len(match.groups())):
                        # groupNum = groupNum + 1
                        # print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
                file_names_for_each_code_part = [s.strip() for s in file_names_for_each_code_part]  # Strip the list
                file_names_for_each_code_part = list(set(file_names_for_each_code_part))            # Create a unique list
                if file_names_for_each_code_part:                                                   # Ignore the empty list
                    result_post_file_names.append(file_names_for_each_code_part)
                    
        elif OS_flag == "windows":
            for code in code_sec:
                regex = r"[a-zA-Z]:\\?([^\<\>\:\"\\\/\/\|\?\*\n]+\\)+([^\<\>\:\"\\\/\/\|\?\*\n]+)(\.pyc|\.py)"
                code = code.replace('&lt;', '<')
                code = code.replace('&gt;', '>')
                code = code.replace('&quot;', '"')
                matches = re.finditer(regex, code, re.MULTILINE)                            
                file_names_for_each_code_part = []

                for matchNum, match in enumerate(matches, start=1):
                    file_names_for_each_code_part.append(match.groups()[1])
                    # print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
                    # for groupNum in range(0, len(match.groups())):
                        # groupNum = groupNum + 1
                        # print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
                file_names_for_each_code_part = [s.strip() for s in file_names_for_each_code_part]  # Strip the list
                file_names_for_each_code_part = list(set(file_names_for_each_code_part))            # create a unique list
                if file_names_for_each_code_part:                                                   # Ignore the empty list
                    result_post_file_names.append(file_names_for_each_code_part)
            
    except:
        print("\n Error(2): \n", code_sec)
        return None, None

    return OS_flag, result_post_file_names



# #### Apply to code column 

df_w_tags['bugy_py_files'] = df_w_tags['Code'].apply(lambda row_code_ex: extract_pathnames_from_code_column(row_code_ex))


df_w_tags['bugy_py_files'].to_csv('/home/amin/Desktop/DevOps_final_projecct/amin_result_v2.csv', encoding='utf-8')



counter_win  = 0
counter_unix = 0
dim_win  = []
dim_unix = []

for tuple in df_w_tags["bugy_py_files"]:
    if tuple[0] == "windows":
        counter_win += 1
        np_array = np.array(tuple[1], dtype=object)
        dim_win.append(np_array.shape)
        
    elif tuple[0] == "unix":
        counter_unix += 1
        np_array = np.array(tuple[1], dtype=object)
        dim_unix.append(np_array.shape)

print(f"Table has {counter_win} windows labels.")
print(f"Table has {counter_unix} unix labels.")
print("The dimensions of Windows labels is: ", set(dim_win))
print("The dimensions of Unix labels is: ", set(dim_unix))


# ### Creating a string matrix based on the buggy python file names

# https://stackoverflow.com/questions/32037893/numpy-fix-array-with-rows-of-different-lengths-by-filling-the-empty-elements-wi

def numpy_fillna(data: List) -> np.ndarray:
    # Get lengths of each row of data
    lens = np.array([len(i) for i in data])

    # Mask of valid places in each row
    mask = np.arange(lens.max()) < lens[:, None]

    # Setup output array and put elements from data into masked positions
    out = np.zeros(mask.shape, dtype='object')
    out[mask] = np.concatenate(data)
    
    return out

_2D_array = []
for row_tuple in df_w_tags['bugy_py_files']:
    for element in row_tuple[1]:
        _2D_array.append(element)
_2D_array_pad = numpy_fillna(_2D_array)

# ### Creating a numerical matrix based on the buggy python file names

# https://www.geeksforgeeks.org/python-pandas-factorize/

# #### Creating a dictionary based on the name of files and assigning a unique number to that


dic = {} 
specific_val = 1
for row in _2D_array_pad:
    for element in row:
        if element not in dic:
            dic[element] = specific_val
            specific_val += 1


print("The number of files that we considered is: ", max(dic.values()))

for i, row in enumerate(_2D_array_pad):
    for j in range(len(row)):
        _2D_array_pad[i][j] = dic[_2D_array_pad[i][j]]


# ## Sequential Pattern Mining

# https://www.cc.gatech.edu/~hic/CS7616/pdf/lecture13.pdf

# ### Approach (1):

# The shortest yet efficient implementation of the famous frequent sequential pattern mining algorithm PrefixSpan, the famous frequent closed sequential pattern mining algorithm BIDE (in closed.py), and the frequent generator sequential pattern mining algorithm FEAT (in generator.py), as a unified and holistic algorithm framework.

# https://github.com/chuanconggao/PrefixSpan-py

# ## Approach (2): 

# pymining is a small collection of data mining algorithms implemented in Python. I did not design any of the algorithms, but I use them in my own research so I thought other developers might be interested to use them as well.

# https://github.com/bartdag/pymining


from prefixspan import PrefixSpan


ps = PrefixSpan(_2D_array_pad)

# print(ps.frequent(30))

print(ps.topk(15, closed=True))



