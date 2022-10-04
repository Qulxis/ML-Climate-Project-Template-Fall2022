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