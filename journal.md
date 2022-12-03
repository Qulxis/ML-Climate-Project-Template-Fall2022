## 10/4/2022:
Attempted to access datasets. UI is a little hard to follow because NASA is serving as an intermediate between users and data sources, but doesn't allow downloading of the datasets unless it owns them. Original dataset for solar radiation/insolation is not longer viable as only way to access is through ordering and because time frame available only goes back to 3/1/2022 on sourcing site. Other options could be using NASA's png/cvs files on their website, but limited resolution. Thinking of switching to cloud cover dataset rather than solar insolation. 

New dataset sources:
- land temp: https://lpdaac.usgs.gov/products/mod11c1v006/#tools
- All the above? https://nsrdb.nrel.gov/data-viewer

nsrdb has good potential as would include both data for temperature AND solar radiation metrics. Issue is that data can only meaniningfully be accessed via API.
- API KEY: KGQPxhHwezmhBj96AirFO6eKuzfP5DvQI7gFDWOk
- Example use: https://developer.nrel.gov/api/alt-fuel-stations/v1.json?fuel_type=E85,ELEC&state=CA&limit=2&api_key=KGQPxhHwezmhBj96AirFO6eKuzfP5DvQI7gFDWOk

Sample using single location data is downloaded currently
Observations: 
- GHI is the most important predictor for solar panel output: https://blog.globalweathercorp.com/global-horizontal-irradiance-solar-panel-efficiency
"Global horizontal irradiance (GHI) is a measurement of the total solar electromagnetic radiation above a horizontal surface at a given location and time. It is the most useful metric for predicting solar panel output. It accounts for 71.6% of PV performance variations. "
- Temperature and GHI are both localized and arranged accordingly. This dataset is very promising, will proceed to research API usage to extract data for other data locations.
- Time series prediction on single location could be viable: RNN model using historical prediction, transformer arch/LSTM model also would be good approaches. 
- File format is csv, 1 measurement per hour per day, around 8000+ data points per year

Conclusion: nsrdb is much more optimal than the original datasets. It's model for GHI is based on predicitions using the initially listed datasets (MERRA 2, MODIS, NASA database sets) and localizes the measurements of temperature and GHI, the main factors of our prediction. From here, I will move forward with data extraction via API, and then move towards creating a predictive model using location information (various attributes are open on nsrdb website, such as wind, dew point, etc). The key will actually be looking for correlation between other attributes to predict temperature and GHI outside of the autoregressive time model information.

##  10/11/2022
Sick, emailed Professor about extentions and delay in progress

## 10/18/2022
Missed progress last week as was sick for its entirety.

Current work: Get data via API. Not a lot of documentation available, so experimention is needed. However, I should be able to do some basic experimentation on the current set of data. 
TODO:
[x] Gather data using API as current extraction through GUI limits to only one location at a time due to download size limits.
[x] Define a usibility metric. Cold is good, but sunlight is likely more important. The weighting of these needs to be considered. 
[x] Filtering data down and cleaning. Option 1: GHI should be looked at as a summation over time, while temperature should be viewed as a condition that needs to be met a minimum of x hours a day. Option 2: combine GHI and temperature for each hour to get a score. The best way to combine this is a research task
[x] Research the way energy generation depends on temperature and GHI to determine exactly how much each should be considered.
[ ] Consider regression for predictions overtime (predict usability score)
[ ] Consider classification for location choice (more like manual, but also related). Will require multiple location analysis.

API python example: https://developer.nrel.gov/docs/solar/nsrdb/guide/

Conclusions: datapoint example loaded successfully as a usable pandas df. I will next look into baseline predictions using basic regression models for both temperature and GHI using time. I will also look into defining a metric to mark good locations vs bad locations.

## 10/25/2022 + 11/1/2022
API is uncooperative and dataset is absolutely massive. It is extremely granular, by the hour. This could be a case study where we look at if high GHI occurances actually overlap in the day with a lower temperature. However, to actually make this useful, we would need to expand this to multiple areas to search for. Too much data for my abilities (and seemingly the API). As such, will instead user raster data of the global GHI and temperature to observe global points of interest in which a grandular search might be useful. I have introduced both into this repo and has begun analysis of the local dataset in a notebook in src. 

To determine the effect temperature has on solar panels imperically, I start with this article:
https://www.mahindrateqo.com/blog/impact-of-temperature-on-solar-panels-efficiency/#:~:text=So%2C%20for%20every%20degree%20rise,more%20efficient%20in%20cooler%20temperature.

Which states, "for every degree rise, the maximum power of the solar panel will fall by 0.258% and for every degree fall it will increase by the same percentage. This means, no matter where you are, your panels will be affected by seasonal variation and also that solar panels are more efficient in cooler temperature."

This is in celsius, and thus taking the max and min land temperatures, I get a range of 146 degrees (-88c to 58c), equivalent to 37.66% of efficiency different just from temperature alone in an earth-like conditions. This will be justification for my research as well.

I will use a simple metric to calculate my "goodness of placement" score and that is a sum of products of GHI and temperature efficiency over a day/month/year. I first will look at each day by looking at GHI and temperature every 30 minutes (more local) which is the best estimation of power generation effect based on just temperature and GHI that I do. I will do this for a multiple months and then compare results with if I calculate my score on just the monthly GHI and temperature averages. This is to see at what scale do we see sufficient accuracy in power prediction. I can scale this process out to years as well. By doing this, I will know what time step I need to work with, though I realistically can only go by month due to the scale of the data. 

Goodness_metric = GHI*abs(100-Temp). GHI: Watts/m^2 , Temp = degrees celsius. Note this scale is relative to itself and cannot be combined in its present state so far. It is a relative metric to help compare locations.

Based on graphing GHI vs Temperature over just a day with 30 minutue interveral, while most of the time temperature and GHI increase and decrease together, occations GHI has extremely irregular patterns. This is likely to cloud cover varition and irregular weather patterns. Regardless of cause, this leads the motivation to look at GHI vs Temp at such a fine scale before looking at monthly averages.

I am using gdal to explore the raster data which requires installation work. https://opensourceoptions.com/blog/how-to-install-gdal-for-python-with-pip-on-windows/
data: https://www.nrel.gov/gis/solar-resource-maps.html


## 11/08/2022:
No commits last week due to academic holiday

## 11/15/2022:
Moving to modeling:

Gdal success, can deal with raster data now but data may be difficult to deal with. GDAL version used: GDAL‑3.4.3‑cp39‑cp39‑win_amd64.whl from https://www.lfd.uci.edu/~gohlke/pythonlibs/. 
Tasks Completed:
[x] Read and displayed data as np array. 
[x] Filtered points so only best GHI spots are shown. Best spots for april are in mexico for example.
[x] Accessed data via api openning access to all datapoints
Issues: 
- Convert x,y corrd to Lat. and Long for raster case
- Need to finalize which data source type is the best (Raster vs. Location data over year)


NSRDB Notebook for reference found:
https://github.com/NREL/hsds-examples/blob/master/notebooks/03_NSRDB_introduction.ipynb
https://developer.nrel.gov/docs/solar/nsrdb/python-examples/
https://sam.nrel.gov/


Moving forwards:
- From EDA, I can see that temperature and GHI are NOT correlated hourly due to previously mentioned reasons. As such, I will take the average Goodness_score over the day.
- Model is a time series models. Thus: https://machinelearningmastery.com/time-series-forecasting-methods-in-python-cheat-sheet/ <-- Choose one of these to start
- Data is already sorted into time series form, just need to squash to not be every 30 minutes lol

## Final Approach:
[ ] 1. Generate predictive model for one random location in USA to prove efficacy
    - Squash data to have time step of daily rather hourly and extract "Goodness score"
    - Move process to personal API for use future use in step 3.
    - Split into train, val, test split. Augment data if not enough 
    - Train model and observe results (acc, precision etc)
[x] 2. Use raster data to identify locations with GHI to help limit our search space.
    - Convert x,y coord to long and lat coord
    - Filter locations by hard threshold of GHI values
    - Filter locations by temp if possible, missing dataset for this.
    - Record filtered location for step 3
[ ] 3. Select n number of locations within the area's filtered by raster data search and perform predictive modelling for each location
[ ] 4. Observe results and select locations with best likelihood of having good score over next 3-5 years


## 11/28/2022
Cleaning up repo and organizing notebooks into follow-along format. Below are notes on Power Output calculation methods that I want to keep. Look through Notebooks to see progress :)

More concrete scoring:
PV = Photovoltaic system

Many ways to calculate the PV output:
1. https://photovoltaic-software.com/principle-ressources/how-calculate-solar-energy-power-pv-systems
Power is given by:
E = A * r * H * PR

E = Energy (kWh)
A = Total solar panel Area (m2)
r = solar panel yield or efficiency(%) 
H = Annual average solar radiation on tilted panels (shadings not included)
PR = Performance ratio, coefficient for losses (range between 0.5 and 0.9, default value = 0.75)

Assume A is fixed, H is GHI. 

For PR:
- Inverter losses (4% to 10 %)
- Temperature losses (5% to 20%)
- DC cables losses (1 to 3 %)
- AC cables losses (1 to 3 %)
- Shadings 0 % to 80% !!! (specific to each site)
- Losses at weak radiation 3% to 7%
- Losses due to dust, snow... (2%)
- Other Losses (?)

2. Homer
https://www.homerenergy.com/products/pro/docs/3.11/how_homer_calculates_the_pv_array_power_output.html
PV caculation explicit:
$P = Y_{pv}f_{pv}(\frac{G_T}{G_{SD}})[1+\alpha*(T_c - T_{c,STC})]$
https://www.homerenergy.com/products/pro/docs/latest/how_homer_calculates_the_pv_cell_temperature.html
Solar panel efficiency depends on temperature of the cell, not ambience. According to Homer's second link, this cell temperature is calcuatable. It also is very difficult and requires data I do not have.

[x] Updated Notebook and strcture to be suitable for presentation and follow along
[x] Added explicit explaination of preprocessing and calcualtion justifications 

## 11/30/2022
Finishing $T_c calculations$
Nrel is in W/m^2 rather than kW/m^2. While this factor should scale evenly in the calculation regardless, I am unsure if it will affect my results. Should be fine.

Conflicting results on range of Wattage for PV cells:https://www.solar.com/learn/how-much-energy-does-a-solar-panel-produce/
vshttps://www.solaris-shop.com/hanwha-q-cells-q-pro-bfr-g4-260-260w-poly-solar-panel/
https://www.sciencedirect.com/science/article/pii/S0360544219305729 
Example calculation:
https://sinovoltaics.com/solar-basics/measuring-the-temperature-coefficients-of-a-pv-module/
https://climatebiz.com/peak-sun-hours-united-states/
https://www.solar.com/learn/how-much-energy-does-a-solar-panel-produce/

Finished PV output calculations and cross referenced with online resources listed above!

## 12/1/2022
Apply score and then train linear regression model from prediction!
Steps:
1. Apply scores for one instance to test and aggragate to be in final data state.  [x]
2. Move process to API section. [x]
3. Call API for all years from 1998-2021. [x]
4. Create data-output paris. Features are data from last 5-7 years and output is the PV (kWh/year and/or kWh/month) [x]

## 12/2/2022
Modeling and data preprocessing completed.
Ready for presentations! Last step is to let data collection run for all points and then impliment train-test split to validate results.

