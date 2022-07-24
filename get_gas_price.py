import os
import pandas as pd
import re

"""
Get the gas price for 2019 und 2022 from https://dev.azure.com/tankerkoenig/_git/tankerkoenig-data?path=/prices/2022/01
The files are prices of different gas stations, get median gas price for day
Store the result in csv
"""

def get_median_gas_prices(path_data_folder, years, months):

    # Get number of files (only for progress tracking)
    num_files = 0
    for y in years:
        for m in months:
            path_data = os.path.join(path_data_folder, str(y), str(m))
            for file in os.listdir(path_data):
                num_files += 1

    # Get data for each day by looping through years and months
    data_all = []
    files_processed = 0
    for y in years:
        for m in months:
            path_data = os.path.join(path_data_folder, str(y), str(m))
            for file in os.listdir(path_data):
                f = os.path.join(path_data,file)
                if os.path.isfile(f):
                    # Get date from file name
                    file_name = os.path.basename(f)
                    date = re.sub('-prices.csv', '', file_name)

                    # Read csv for one day and calculate median
                    df_day = pd.read_csv(f)
                    median = df_day.median(numeric_only=True)

                    # Make input for one day for final df
                    data_day = [date, median['e5'], median['e10'], median['diesel']]
                    data_all.append(data_day)
                    
                    # Get number of currently processed files (only for progress tracking)
                    files_processed += 1
                    print('Processed', files_processed, 'of', num_files, 'files.')

    # Create output df
    df = pd.DataFrame(data_all, columns=['Date', 'E5', 'E10', 'Diesel'])
    return df


if __name__ == '__main__':
    
    # Input
    years = ['2019', '2022']
    months = ['04', '05', '06']
    path_data_folder = os.path.join(os.getcwd(), 'data')

    # Call function
    df = get_median_gas_prices(path_data_folder, years, months)
    print(df)

    # Create csv
    df.to_csv(os.path.join(os.getcwd(), 'output_gas_prices.csv'), encoding='utf-8', index=False)