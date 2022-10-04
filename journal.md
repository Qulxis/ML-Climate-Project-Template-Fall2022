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
- 
