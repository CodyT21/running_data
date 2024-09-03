AGE = 29
MAX_HEART_RATE = 208 - (0.7 * AGE) # forumla comes from the Mayo Clininc
RESTING_HEART_RATE = 55

def rename_columns(df):
    new_column_names = {col: col.strip().lower().replace(' ', '_').replace('.1', '') for col in df.columns}
    return df.rename(columns=new_column_names)


# determine average running zone based on averagee heart rate   
def find_zone(avg_heart_rate):
    
    # Using the Karnonen method
    hrr = MAX_HEART_RATE - RESTING_HEART_RATE # heart rate reserve
    
    if avg_heart_rate < (0.6 * hrr) + RESTING_HEART_RATE:
        return 1
    elif avg_heart_rate < (0.7 * hrr) + RESTING_HEART_RATE:
        return 2
    elif avg_heart_rate < (0.8 * hrr) + RESTING_HEART_RATE:
        return 3
    elif avg_heart_rate < (0.9 * hrr) + RESTING_HEART_RATE:
        return 4
    else:
        return 5


def format_timedelta(dlt):
    minutes, seconds = divmod(int(dlt.total_seconds()), 60)
    return f'{minutes:02}:{seconds:02}'


def date_to_season(date):
    seasons = {'winter': [12, 1, 2],
               'spring': [3, 4, 5],
               'summer': [6, 7, 8],
               'fall': [9, 10, 11]}
    
    for season, months in seasons.items():
        if date.month in months:
            return season


def cols_to_str(df):
    for col in df.columns:
        
        # format timedelta columns
        if df[col].dtype == '<m8[ns]':
            df[col] = df[col].astype('str')
            df[col] = df[col].apply(lambda x:x.split(' ')[2])
        else:
            df[col] = df[col].astype('str')
    
    return df

def convert_cols_to_strs(df):
    for col in df.columns:
        
        # format timedelta columns
        if df[col].dtype == '<m8[ns]':
            df[col] = df[col].astype('str')
            df[col] = df[col].apply(lambda x:x.split(' ')[2])
        else:
            df[col] = df[col].astype('str')
    
    return df

def categorize_run_by_distance(distance):
    short_run_cutoff_distance = 4
    medium_run_cutoff_distance = 10

    if distance < short_run_cutoff_distance:
        return 'short'
    elif distance < medium_run_cutoff_distance:
        return 'medium'
    else:
        return 'long'

def categorize_run_type(distance):
    # ranges are used to account for any gps inconistencies between phone app and watch gps tracking
    if distance > 3 and distance <= 3.2:
        return '5k'
    elif distance > 6 and distance <= 6.4:
        return '10k'
    elif distance > 12.7 and distance <= 13.5:
        return 'half marathon'
    else:
        return 'other'