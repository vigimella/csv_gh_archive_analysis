import merge_csv, csv_analysis
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# Creation of directory elm where you can store all CSV files to merge

elm = os.path.join(APP_ROOT, 'elm')
outputs = os.path.join(APP_ROOT, 'outputs')

if __name__ == '__main__':

    # Choose the name of your output file

    output_file_name = 'gh_archive_merged'
    output_path = os.path.join(outputs, output_file_name + '.csv')

    # Merge CSV files in elm directory

    if not os.path.exists(output_path):
        merge_csv.merge_csv_file(elm, outputs, output_file_name)
    else:
        print('CSV merged already exists...')

    # Start analysis form CSV merged

    #csv_analysis.analysis(output_path, outputs)



    


