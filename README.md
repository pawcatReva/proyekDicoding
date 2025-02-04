# Proyek Bike Sharing Dataset
  This repository is about the results of the Bike Sharing Dataset analysis.
  ## Background
  The bike sharing system is a new generation of traditional bicycle rental where the entire process starts from membership, rental and return.
  Therefore, it is expected to be the most important thing events in the city can be detected through monitoring this data.
  ## Dataset
  - instant: record index
  - dteday : date
  -  season : season (1:springer, 2:summer, 3:fall, 4:winter)
  - yr : year (0: 2011, 1:2012)
  -mnth : month ( 1 to 12)
  - hr : hour (0 to 23)
  - holiday : weather day is holiday or not (extracted from [Web Link])
  - weekday : day of the week
  - workingday : if day is neither weekend nor holiday is 1, otherwise is 0.
  - weathersit :
           -1: Clear, Few clouds, Partly cloudy, Partly cloudy

    ## Folder Structure

```
📂 Proyek
├── 📁 dashboard
│   ├── dashboardd.py
│   ├── day_cleaned.csv
│   ├── hour_cleaned.csv
├── 📁 data
│   ├── day.csv
│   ├── hour.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

## Running
# Prerequisite
In this project I use Python version 3.13.1 and use several libraries as follows:
- matplotlib==3.10.0
- numpy==2.2.2
- pandas==2.2.3
- seaborn==0.13.2
- streamlit==1.41.1



