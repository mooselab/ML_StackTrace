![](https://www.polymtl.ca/create-seed/sites/create-seed.amigow2020.polymtl.ca/files/uni_poly_fr.png)![](https://www.hengli.org/images/logo_final_smallest.png)

## SOTorrent Queries:

On [this](https://github.com/ghadesi/db-scripts/tree/master/sotorrent) repository, we mentioned completely all queries that we used for generating the data.

## Fast Run (Approach 1):
Running just the result code.
## Structure
```bash
├── CSV_data/
├── Excel_data/                     <~~~~ All the sheets related to the empirical studies
├── Pickle_data/
├── Result/                         <~~~~ Result plots
├── Project_1_hugh_v2.ipynb         =|
├── Project_1_keras_v2.ipynb         |
├── Project_1_nltk_v2.ipynb          |
├── Project_1_pt_v2.ipynb            | <~~~~ All library codes: The structure of all files. 
├── Project_1_sklearn_v2.ipynb       |       However, there are some small changes in each library. 
├── Project_1_spark.ipynb            |       (For checking you can check the Spark file.)
├── Project_1_tf_v2.ipynb           =|
├── README.md
├── Results.ipynb                   <~~~~ You can find all information that helps us to generate plots and tables.
└── requirements.txt                <~~~~ Requirement packages
```
## Complete Run (Approach 2): 
Running the project with the whole dependency files: [Downlaod Link](https://zenodo.org/record/7839032#.ZD3G6-xudgc)
## Structure
```bash
├── README.md
├── anaconda3.tar.gz                <~~~~ Virtual environment
├── code_output_csv/
├── db_results/                     <~~~~ ML libraries information 
├── project_1_codes                 <~~~~ Source codes
│   ├── CSV_data/
│   ├── Excel_data/
│   ├── Pickle_data/
│   ├── Project_1_hugh_v2.ipynb
│   ├── Project_1_keras_v2.ipynb
│   ├── Project_1_nltk_v2.ipynb
│   ├── Project_1_pt_v2.ipynb
│   ├── Project_1_sklearn_v2.ipynb
│   ├── Project_1_spark.ipynb
│   ├── Project_1_tf_v2.ipynb
│   ├── Result/
│   └── Results.ipynb                <~~~~ Output plots
├── question_tag.csv                 <~~~~ Posts information
├── SOTorrent
│   ├── README.md                    <~~~~ Extract posts from SOTorrent
│   └── sotorrent 
```
0. Please, change your directory to the place that you downlowded the file.
 ```console
 Linux$ cd [Downloade directory]
 ```

1. Unzip the project file 
 ```console
 Linux$ unzip archive-project-1.zip
 ```

2. Change your directory to the root of the project.
 ```console
 Linux$ cd ./archive-project-1
 ```
3. Make a directory for for the "anaconda3" environment and unpack that. 
```console
 Linux$ mkdir -p anaconda3
 Linux$ tar -xzf anaconda3.tar.gz -C anaconda3
 ```
4. Active the virtual environment.
```console
 Linux$ source ./anaconda3/bin/activate
 ```
5. Run the project
```console
 (anaconda3) Linux$ jupyter-lab .
 ```

> :warning: ** The binary files of the python language are cloned from a system that you can find the information of that in the below box; if you use another processor architecture, you have to install the jupyter-lab on your PC again!
```console
          conda version : 4.13.0
    conda-build version : 3.21.9
         python version : 3.9.12.final.0
       virtual packages : __linux=3.10.0=0
                          __glibc=2.17=0
                          __unix=0=0
                          __archspec=1=x86_64
  conda av metadata url : None
           channel URLs : https://repo.anaconda.com/pkgs/main/linux-64
                          https://repo.anaconda.com/pkgs/main/noarch
                          https://repo.anaconda.com/pkgs/r/linux-64
                          https://repo.anaconda.com/pkgs/r/noarch
               platform : linux-64
             user-agent : conda/4.13.0 requests/2.27.1 CPython/3.9.12 Linux/3.10.0-1160.49.1.el7.x86_64 centos/7.9.2009 glibc/2.17
                UID:GID : 1312:1055
             netrc file : None
           offline mode : False
```
