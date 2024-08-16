import numpy as np
import pandas as pd
import gspread
import matplotlib.dates as mdates
from helper_functions import rename_columns, find_zone, format_timedelta, date_to_season, cols_to_str  
from datetime import datetime

GSHEET_STRAVA_KEY = '1T5ScOCSiojB0lUUky9NgyVeH6IpYQboACxh4HOAxO8o'

def load_strava_data():
    gc = gspread.service_account()
    gsheet = gc.open_by_key(GSHEET_STRAVA_KEY)
    wsheet = gsheet.worksheet('Sheet1')
    return pd.DataFrame(wsheet.get_all_records())


def load_run_data():
    df = load_strava_data()
    return df.loc[df['type'] == 'Run']


def get_new_run_data():
    df = process_run_data()
    return cols_to_str(df)


def process_run_data():
    '''
    add in an actual description
    '''
    
    # load in strava running data
    runs_df = load_run_data()

    # create consistent column names
    runs_df = rename_columns(runs_df)

    # date fields
    runs_df['date'] = pd.to_datetime(runs_df['date'], format='mixed')
    runs_df['year'] = runs_df['date'].dt.year
    runs_df['year_month'] = runs_df['date'].dt.to_period('M')
    runs_df['season'] = runs_df['date'].apply(date_to_season)
    runs_df['time_of_day'] = runs_df['name'].str.lower().str.split(' ').str[0]
    runs_df['time_of_day'] = runs_df['time_of_day'].replace({'lunch': 'afternoon'}).astype('category')
    
    # create fields based on pace
    runs_df['moving_time_s'] = pd.to_timedelta(runs_df['moving_time_s'], unit='s')
    runs_df['pace_per_mile'] = runs_df['moving_time_s'] / runs_df['distance_mi']
    # runs_df['pace_per_mile_dt'] = pd.to_datetime(runs_df['pace_per_mile'].apply(format_timedelta), format='%M:%S')
    # runs_df['formatted_pace_per_mile'] = runs_df['pace_per_mile_dt'].dt.time

    # create fields based on heartrate zones
    runs_df['average_zone'] = runs_df['average_heartrate'].apply(find_zone)
    runs_df['max_zone']  = runs_df['max_heartrate'].apply(find_zone)
    runs_df['ratio_avg_hr_to_max_hr'] = runs_df['average_heartrate'] / runs_df['max_heartrate']

    return  runs_df