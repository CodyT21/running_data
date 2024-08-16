'''
    add in an actual description
    '''

import pandas as pd
import gspread
from process_strava_data import load_run_data
from helper_functions import convert_cols_to_strs

GSHEET_KEY = '1d2Qla44umefW7gR5jW1LrK_7RreIreyk6CeGNI6ffnw' #run_data spreadsheet

# load current google sheet
gc = gspread.service_account()
gsheet = gc.open_by_key(GSHEET_KEY)
wsheet = gsheet.worksheet('run_data')

# load updated running data
updated_run_data = convert_cols_to_strs(load_run_data())

# move any new data into a new dataframe
current_run_data = pd.DataFrame(wsheet.get_all_records())
new_data = updated_run_data[~updated_run_data.index.isin(current_run_data.index)]

# update google sheet with new rows if necessary
if new_data.empty:
    print('The run_data spreadsheet is already up to date on the Google Drive.')
else:
    try:
        if current_run_data.empty:
            gsheet.values_append('run_data', {'valueInputOption': 'USER_ENTERED'}, {'values': [updated_run_data.columns.tolist()]})
            print('The run_data spreadsheet was empty.\nHeader row added successfully.')
        values = new_data.values.tolist()
        gsheet.values_append('run_data', {'valueInputOption': 'USER_ENTERED'}, {'values': values})
        print(f'{len(values)} new runs added.')
    except Exception as e:
        print('Could not update the run_data spreadsheet.')
        print(e)
    else:
        print('Updated the run_data spreadsheet on the Google Drive successfully.')