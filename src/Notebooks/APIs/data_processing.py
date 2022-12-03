import sys, os
import pandas as pd
import numpy as np

"""
calcPV
Inputs: ghi (float), temp (float), cell_rating (int)
Ouput: t_c (float), PV outage in kW (float)

This function calculates the PV outage for a given GHI level in kW, the ambient temperature (temp), and the cell rating (cell_rating) in kW
GHI: Watts (not in kW!)
temp: Celcius
Cell Rating: kW
"""
def calcPV(ghi, temp, cell_rating):
    #ghi: W/m^2
    #temp: Ambient temperature Celcius 
    #returns cell temp and PV output 
    ghi = ghi/1000 #this is because nrel return GHI W/m^2, https://nsrdb.nrel.gov/data-sets/us-data
    t_c = temp+(ghi*(45-20)/0.8)*(1-20/90)
    return t_c, cell_rating*ghi*(1-.0048*(t_c-25))

"""
addPV
Inpits: df (pandas dataframe), cell_rating (int)
Ouputs: df (pandas dataframe)

Note that cell_rating is in kW, not W!
This function adds the PV rating to the df assuming time interval is hourly. 

"""
def addPV(df,cell_rating=400):
    pv = []
    ghi_hist = df["GHI"].tolist()
    temp_hist = df["Temperature"].tolist()
    for index in range(len(ghi_hist)):
        t_c, out = calcPV(ghi_hist[index],temp_hist[index],cell_rating=cell_rating)
        pv.append(out)
    df["pv"] = pv #update df
    return df

"""
getData
Inputs: api_key (string), your_name (string), your_affiliation (string), your_email (string), lat (float), long (float), year (int), api_key (str)
Outputs: df (pandas dataframe)

Return the dataframe containing the GHI and temp values for the paramters given
"""
def getData(api_key, your_name, your_affiliation, your_email, lat=33.2164, lon =-118.2437, year=2010):
    # Declare all variables as strings. Spaces must be replaced with '+', i.e., change 'John Smith' to 'John+Smith'.
    # Define the lat, long of the location and the year
    lat, lon, year = lat, lon, year #Long is always negative Los Angeles USA: 33.2164, -118.2437
    # You must request an NSRDB api key from the link above
    api_key = api_key # 
    # Set the attributes to extract (e.g., dhi, ghi, etc.), separated by commas.
    attributes = 'ghi,air_temperature'
    # Choose year of data
    year = str(year)
    # Set leap year to true or false. True will return leap day data if present, false will not.
    leap_year = 'false'
    # Set time interval in minutes, i.e., '30' is half hour intervals. Valid intervals are 30 & 60.
    interval = '60'
    # Specify Coordinated Universal Time (UTC), 'true' will use UTC, 'false' will use the local time zone of the data.
    # NOTE: In order to use the NSRDB data in SAM, you must specify UTC as 'false'. SAM requires the data to be in the
    # local time zone.
    utc = 'false'
    # Your full name, use '+' instead of spaces.
    your_name =  your_name #'andrew+xavier'
    # Your reason for using the NSRDB.
    reason_for_use = 'beta+testing'
    # Your affiliation
    your_affiliation = your_affiliation #
    # Your email address
    your_email = your_email #
    # Please join our mailing list so we can keep you up-to-date on new developments.
    mailing_list = 'true'

    # Declare url string
    url = 'https://developer.nrel.gov/api/nsrdb/v2/solar/psm3-download.csv?wkt=POINT({lon}%20{lat})&names={year}&leap_day={leap}&interval={interval}&utc={utc}&full_name={name}&email={email}&affiliation={affiliation}&mailing_list={mailing_list}&reason={reason}&api_key={api}&attributes={attr}'.format(year=year, lat=lat, lon=lon, leap=leap_year, interval=interval, utc=utc, name=your_name, email=your_email, mailing_list=mailing_list, affiliation=your_affiliation, reason=reason_for_use, api=api_key, attr=attributes)
    # Return just the first 2 lines to get metadata:
    info = pd.read_csv(url, nrows=1)
    # See metadata for specified properties, e.g., timezone and elevation
    timezone, elevation = info['Local Time Zone'], info['Elevation']
    # Return all but first 2 lines of csv to get data:
    df = pd.read_csv('https://developer.nrel.gov/api/nsrdb/v2/solar/psm3-download.csv?wkt=POINT({lon}%20{lat})&names={year}&leap_day={leap}&interval={interval}&utc={utc}&full_name={name}&email={email}&affiliation={affiliation}&mailing_list={mailing_list}&reason={reason}&api_key={api}&attributes={attr}'.format(year=year, lat=lat, lon=lon, leap=leap_year, interval=interval, utc=utc, name=your_name, email=your_email, mailing_list=mailing_list, affiliation=your_affiliation, reason=reason_for_use, api=api_key, attr=attributes), skiprows=2)

    # Set the time index in the pandas dataframe:
    df = df.set_index(pd.date_range('1/1/{yr}'.format(yr=year), freq=interval+'Min', periods=525600/int(interval)))
    return df



"""
hoursToDays:
Inputs: df (pandas dataframe)
Outputs: df_days (pandas dataframe)

This function takes in a df with hour level granularity and returns a dataframe with day level granularity.
It includes PV in kWh/day, average ghi and temperature. 
Columns in outputs are: Year, Month, Day, Temp mean, GHI mean, and PV kWh/day

Typically run this on ouput of addPV!


"""
def hoursToDays(df):   
    ghi_hist = df["GHI"].tolist()
    temp_hist = df["Temperature"].tolist()
    num_days = len(df)//24
    year_days = [df["Year"][0]]*num_days
    month_days = []
    pv_days = []
    temp_days = []
    ghi_days = []
    day_days = []
    for day in range(len(df["pv"])//24):
        month_days.append(df["Month"][day*24])
        pv_days.append(np.sum(df["pv"][day*24:day*24+24]))
        ghi_days.append(np.mean(ghi_hist[day*24:day*24+24]))
        temp_days.append(np.mean(temp_hist[day*24:day*24+24]))
        day_days.append(df["Day"][day*24])
    dic_days = {
        "Year":year_days,
        "Month": month_days,
        "Day": day_days,
        "Temp mean": temp_days,
        "GHI mean": ghi_days,
        "PV kWh/day": pv_days
    }
    df_days = pd.DataFrame.from_dict(dic_days)
    return df_days


"""
Runs on output of hoursToDays.
"""
def daysToMonths(df):
    year_month = [df["Year"][0]]*12
    month_month = []
    pv_month = []
    temp_month = []
    ghi_month = []
    for i in range(12):
        i += 1 #to match month counter
        df_month = df.loc[df['Month'] == i]
        month_month.append(i)
        pv_month.append(np.sum(df_month["PV kWh/day"]))
        temp_month.append(np.mean(df_month["Temp mean"]))
        ghi_month.append(np.mean(df_month["GHI mean"]))
    dic_month = {
        "Year":year_month,
        "Month": month_month,
        "Temp mean": temp_month,
        "GHI mean": ghi_month,
        "PV kWh/month": pv_month
    }
    df_month = pd.DataFrame.from_dict(dic_month)
    return df_month

"""
Runs on output of addPV.
"""
def hoursToMonths(df):
    year_month = [df["Year"][0]]*12
    month_month = []
    pv_month = []
    temp_month = []
    ghi_month = []
    for i in range(12):
        i += 1 #to match month counter
        df_month = df.loc[df['Month'] == i]
        month_month.append(i)
        pv_month.append(np.sum(df_month["pv"]))
        temp_month.append(np.mean(df_month["Temperature"]))
        ghi_month.append(np.mean(df_month["GHI"]))
    dic_month = {
        "Year":year_month,
        "Month": month_month,
        "Temp mean": temp_month,
        "GHI mean": ghi_month,
        "PV kWh/month": pv_month
    }
    df_month = pd.DataFrame.from_dict(dic_month)
    return df_month
""""
dataByLocation
Inputs: api_key (string), your_name (string), your_affiliation (string), your_email (string), lat (float), lon (float), cell_rating (float)
end_year (int)
Ouput: 
This lets the function run in one line
"""
def dataByLocation(api_key, your_name, your_affiliation, your_email, lat, lon, cell_rating, end_year):
    dates = list(range(1998, end_year)) #years 1998-2020. Online states 1998-2021 but error when I try to make a request
    df_all = pd.DataFrame(columns=["Year", "Month", "Temp mean", "GHI mean", "PV kWh/month"]) #final df
    for date in dates:
        df = getData(api_key, your_name, your_affiliation, your_email, lat=lat, lon = lon, year=date) #get raw data from nrel
        df_pv = addPV(df,cell_rating=cell_rating) #Add PV calculated column
        df_pv_month = hoursToMonths(df_pv)
        df_all = pd.concat([df_all, df_pv_month])
        df_all["lat"] = [lat]*len(df_all)
        df_all["lon"] = [lon]*len(df_all)
    return df_all