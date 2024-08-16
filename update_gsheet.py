'''
    add in an actual description
    '''

import pandas as pd
import gspread
from process_strava_data import get_new_run_data

GSHEET_KEY = '1d2Qla44umefW7gR5jW1LrK_7RreIreyk6CeGNI6ffnw'

# load current google sheet
gc = gspread.service_account()
gsheet = gc.open_by_key(GSHEET_KEY)
wsheet = gsheet.worksheet('run_data')

# load updated running data
updated_run_data = get_new_run_data()

# move any new data into a new dataframe
current_run_data = pd.DataFrame(wsheet.get_all_records())
new_data = updated_run_data[~updated_run_data.index.isin(current_run_data.index)]

# update google sheet with new rows if necessary
if new_data.empty:
    print('Google Drive csv is already up to date.')
else:
    try:
        if current_run_data.empty:
            gsheet.values_append('run_data', {'valueInputOption': 'USER_ENTERED'}, {'values': [updated_run_data.columns.tolist()]})
        values = new_data.values.tolist()
        gsheet.values_append('run_data', {'valueInputOption': 'USER_ENTERED'}, {'values': values})
    except Exception as e:
        print('Could not update Google Drive csv.')
        print(e)
    else:
        print('Updated Google Drive csv successfully.')