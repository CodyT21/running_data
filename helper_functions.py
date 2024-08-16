AGE = 29
MAX_HEART_RATE = 220 - AGE

def rename_columns(df):
    new_column_names = {col: col.strip().lower().replace(' ', '_').replace('.1', '') for col in df.columns}
    return df.rename(columns=new_column_names)


# determine average running zone based on averagee heart rate   
def find_zone(avg_heart_rate):
    if avg_heart_rate < 0.6 * MAX_HEART_RATE:
        return 1
    elif avg_heart_rate < 0.7 * MAX_HEART_RATE:
        return 2
    elif avg_heart_rate < 0.8 * MAX_HEART_RATE:
        return 3
    elif avg_heart_rate < 0.9 * MAX_HEART_RATE:
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