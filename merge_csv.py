import os
import pandas as pd


def merge_csv_file(path_dir_input, path_dir_output, csv_name):
    # Sort file in directory by name

    # Check if directory called "elm" exists

    if not os.path.exists(path_dir_input):

        os.makedirs(path_dir_input)

    if not os.path.exists(path_dir_output):

        os.makedirs(path_dir_output)

    if not os.listdir(path_dir_input):

        print('Empty folder, pleas insert some CSV file inside...')

    else:

        print('Some CSV files has been found...')

        sorted_file = sorted(os.listdir(path_dir_input))

        csv_files = []
        all_csv = []

        for file in sorted_file:

            if file.endswith('.csv'):
                csv_files.append(os.path.join(path_dir_input, file))

        for csv_file in csv_files:

            if os.path.getsize(csv_file) > 0:

                df = pd.read_csv(csv_file, sep=',')
                df['file'] = csv_file.split('/')[-1]
                all_csv.append(df)

            else:

                print(str(csv_file) + ' is empty. You are not going to find it in the merged file!')

        merged_df = pd.concat(all_csv, ignore_index=True, sort=True)
        csv_output = os.path.join(path_dir_output, csv_name + '.csv')
        print(csv_output)
        merged_df.to_csv(csv_output)

        print('CSV file merged has been created with the name: ' + csv_name + '.csv')
