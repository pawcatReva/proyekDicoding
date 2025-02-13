# Project Bike Sharing Dataset
  This repository is about the results of the Bike Sharing Dataset analysis.
  ## Background
  The bike sharing system is a new generation of traditional bicycle rental where the entire process starts from membership, rental and return.
  Therefore, it is expected to be the most important thing events in the city can be detected through monitoring this data.
  ## Dataset
  The following data sets were analyzed, including:
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
      - 1: Clear, Few clouds, Partly cloudy, Partly cloudy
      - 2: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist
      - 3: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds
      - 4: Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog
  - temp : Normalized temperature in Celsius. The values are derived via (t-t_min)/(t_max-t_min), t_min=-8, t_max=+39 (only in hourly scale)
  - atemp: Normalized feeling temperature in Celsius. The values are derived via (t-t_min)/(t_max-t_min), t_min=-16, t_max=+50 (only in hourly scale)
  - hum: Normalized humidity. The values are divided to 100 (max)
  - windspeed: Normalized wind speed. The values are divided to 67 (max)
  - casual: count of casual users
  - registered: count of registered users
  - cnt: count of total rental bikes including both casual and registered


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
├── notebooks.ipynb
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

You can install all dependencies using the ```requirements.txt``` file by running the command:
 ```
 pipenv install
 pipreqs C:\coding\proyekDicoding
 pip install -r requirements.txt
```

## Running the Dashboard
1. Clone Repository
```
git clone https://github.com/pawcatReva/proyekDicoding.git
cd proyekDicoding
```
2. Run the Streamlit dashboard:
```
streamlit run C:\coding\proyekDicoding\dashboard\dashboardd.py
```

## Conclusion
1. Comparison of bicycle use on holidays and non-holidays.
- Weekdays (No Holidays): Bicycle usage is higher on weekdays. Bicycles are used as the main means of transportation for commuting to work, with borrowing volumes tending to be higher.
- Holidays: On holidays, loan amounts tend to be lower. This may be because many people choose to rest at home or use other modes of transportation while on holiday.
2. Bicycle Usage Patterns on Certain Days
- On weekdays, especially during morning rush hours (07:00-09:00) and afternoon (17:00-19:00), bicycle rentals tend to be high because many people use them to travel to and from work.
- On holidays, bicycle use tends to be more distributed throughout the day without significant peaks in use. Users are more likely to use bicycles for leisure activities, exercise or traveling.
3. Bicycle Usage Patterns in Certain Seasons.
- Summer and Fall: The number of bike rentals is highest during the summer and fall, when the weather tends to be more friendly for cycling. This season favors outdoor activities, so people are more likely to choose bicycles.
- Spring and Winter: In spring, which tends to be cooler or the weather is cold at certain times, bicycle rentals may decrease because the weather is not always comfortable for cycling. In cold or rainy weather, people prefer to use covered transportation or choose to stay at home.
4. Time (Hour) with Highest Borrowing by Hour
- Bicycle rentals peak during peak hours between 07:00-09:00 and 17:00-19:00. This shows patterns of bicycle use that are directly related to commuting to and from work or other routine activities.
5. Manual Clustering Approach – User Segmentation Based on Number of Bikes Borrowed
- In this approach, users can be divided into several groups based on the frequency of borrowing bicycles, such as:
    - Low Users: Bicycle rentals < 1,000 times per period (eg per month).
    - Medium Users: Bike rentals between 1,000 to 4,000 times per period.
    - High Users: Bike borrowed more than 4,500 times per period.