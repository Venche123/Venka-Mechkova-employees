import pandas as pd
from datetime import date

#upload the csv file
df = pd.read_csv('input_data.csv')
all_empl_worked_together = {}

#use fillna to replace all NaN with today date
today = date.today()
df[['DateFrom', 'DateTo']] = df[['DateFrom', 'DateTo']].fillna(today)
#use to_datetime to change all dates to same format
df['DateFrom'] = pd.to_datetime(df['DateFrom'])
df['DateTo'] = pd.to_datetime(df['DateTo'])

all_projects_set = set(df['ProjectID']) #to get all unique project numbers

#start checking project by project
for project in all_projects_set:
    current_project = df.loc[(df['ProjectID']) == project] #filter the df with current project
    number_of_rows = len(current_project.axes[0])
    for row in range(number_of_rows): #for each row in all lines
        for i in range(row, number_of_rows): #for each row from current row until the end of the rows
            if row + i < number_of_rows:
                next_row = int(row + 1)
                #with iat - to access the value in particular cell
                start_day_current_row = current_project.iat[row, 2]
                end_day_current_row = current_project.iat[row, 3]
                start_day_next_row = current_project.iat[next_row, 2]
                end_day_next_row = current_project.iat[next_row, 3]
                #between 2 rows to find the bigger start day and the smaller end day
                if start_day_current_row <= end_day_next_row or start_day_next_row <= end_day_current_row:
                    if start_day_current_row < start_day_next_row:
                        bigger_start_day = start_day_next_row
                    else:
                        bigger_start_day = start_day_current_row
                    if end_day_current_row < end_day_next_row:
                        smaller_end_day = end_day_current_row
                    else:
                        smaller_end_day = end_day_next_row

                    # to find exactly how many days both employees worked together
                    worked_together = (smaller_end_day - bigger_start_day).days
                    worked_together_int = int(worked_together) + 1 #to add one more day


                    #to find in both ways the 2 employes for later check
                    key_name = str(current_project.iat[row, 0]) + ' and ' + str(current_project.iat[next_row, 0])
                    key_name_swaped = str(current_project.iat[next_row, 0]) + ' and ' + str(current_project.iat[row, 0])

                    #check if one of the above pairs exist in the dictionary where I collect the info for working together empls
                    if key_name in all_empl_worked_together:
                        all_empl_worked_together[key_name] += worked_together_int
                    elif key_name_swaped in all_empl_worked_together:
                        all_empl_worked_together[key_name_swaped] += worked_together_int
                    else:
                        all_empl_worked_together[key_name] = worked_together_int
                else:
                    continue

#find the biggest key value and the name of the biggest key value
worked_together_the_most = max(all_empl_worked_together)
total_days_worked_together = max(all_empl_worked_together.values())

print(f'The two employees: {worked_together_the_most} worked the longest together - {total_days_worked_together} days.')