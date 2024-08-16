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
    runs_df = process_run_data(df.loc[df['type'] == 'Run'])
    return runs_df


def process_run_data(df):
    '''
    add in an actual description
    '''
    
    # load in strava running data
    #runs_df = load_run_data()

    # create consistent column names
    df = rename_columns(df)

    # date fields
    df['date'] = pd.to_datetime(df['date'], format='mixed')
    df['year'] = df['date'].dt.year
    df['year_month'] = df['date'].dt.to_period('M')
    df['season'] = df['date'].apply(date_to_season)
    df['time_of_day'] = df['name'].str.lower().str.split(' ').str[0]
    df['time_of_day'] = df['time_of_day'].replace({'lunch': 'afternoon'}).astype('category')
    
    # create fields based on pace
    df['moving_time_s'] = pd.to_timedelta(df['moving_time_s'], unit='s')
    df['pace_per_mile'] = df['moving_time_s'] / df['distance_mi']
    # runs_df['pace_per_mile_dt'] = pd.to_datetime(runs_df['pace_per_mile'].apply(format_timedelta), format='%M:%S')
    # runs_df['formatted_pace_per_mile'] = runs_df['pace_per_mile_dt'].dt.time

    # create fields based on heartrate zones
    df['average_zone'] = df['average_heartrate'].apply(find_zone)
    df['max_zone']  = df['max_heartrate'].apply(find_zone)
    df['ratio_avg_hr_to_max_hr'] = df['average_heartrate'] / df['max_heartrate']

    return  df