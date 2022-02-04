import matplotlib.pyplot as plt
import csv, re, spacy, os, nltk, nltk.corpus
import pandas as pd
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from nltk.corpus import stopwords

os.environ['SPACY_WARNING_IGNORE'] = 'W007'


def cleanhtml(raw_html):
    cleaner = re.sub(r'<.*?>', ' ', raw_html)
    cleaner = re.sub(r'(\r\n|\n|\r|\t)', ' ', cleaner)
    return cleaner


def remove_stop_words(df_column):
    nltk.download('punkt')
    nltk.download('stopwords')
    stop_words = stopwords.words('english')
    df_column = df_column.apply(lambda x: ' '.join([word for word in x.split() if word not in (stop_words)]))


def similarity_calc(df_column, word_to_check, list):
    nlp = spacy.load("en_core_web_sm")

    for elm in df_column:
        doc1 = nlp(elm)
        doc2 = nlp(word_to_check)
        list.append(doc1.similarity(doc2))


def analysis(input_csv, path_outputs_folder):
    df = pd.read_csv(input_csv)

    # defining lists to use

    # list of date yyyy-dd-mm
    date_list_full = []
    # list of years yyyy
    date_list_year = []
    # list of month mm
    date_list_month = []
    # list of hours hh
    time_list_h = []
    # list of hours and minutes hh:mm
    time_list_minutes = []
    # list affinity with differential privacy
    similarity_dp_list = []
    # list affinity with machine learning
    similarity_ml_list = []
    # general data list
    general_data_list = []

    # cleaning unused columns

    df.drop(['Unnamed: 0', 'Unnamed: 0.1', 'file'], axis=1, inplace=True)

    # list population in specific format

    for c_date in df['commit_date']:
        c_date = c_date.split('T')
        date = c_date[0]
        time = c_date[1]

        date_y = date[:4]
        date_m = date.split('-')[2]

        time = time.replace('Z', '')
        time_hm = time[:-3]
        time_h = time[:-6]

        date_list_full.append(date)
        date_list_year.append(date_y)
        date_list_month.append(date_m)
        time_list_minutes.append(time_hm)
        time_list_h.append(time_h)

    # adding two new columns: date and time.
    df['commit_full_date'] = date_list_full
    df['commit_year'] = date_list_year
    df['commit_month'] = date_list_month
    df['commit_time_h'] = time_list_h
    df['commit_time_hm'] = time_list_minutes

    # remove commit_date

    df.drop(['commit_date'], axis=1, inplace=True)

    # cleaning commit_message column

    df['commit_message'] = df['commit_message'].apply(cleanhtml)

    # remove_stop_words

    remove_stop_words(df['commit_message'])

    # calculating similarity with differential privacy and machine learning

    similarity_calc(df['commit_message'], 'differential privacy', similarity_dp_list)
    similarity_calc(df['commit_message'], 'machine learning', similarity_ml_list)

    # adding similarity columns

    df['similarity_dp'] = similarity_dp_list
    df['similarity_ml'] = similarity_ml_list

    print('Similarities have been calculated...')

    # filtering data frame searching if inside commit message there is something related to differential privacy

    df_filtered = df[df['commit_message'].str.contains('diff privacy | differential privacy | d privacy | dif. privacy | differential priv. | diff priv.')]

    # Drop items duplicated by commit_message and commit_time_hm

    df_filtered = df_filtered.drop_duplicates(subset=['commit_message', 'commit_time_hm'])

    # general information

    # stats pre-filter

    commits_number = 'Number of commits is : ' + str(df['commit_message'].count())
    mean_commits_day = 'Mean of commits by day is : ' + str((df['commit_message'].count()) / 24)
    number_of_projects = 'Number of projects analyzed: ' + str(len(set(df['repository'])))
    num_repo_2020 = 'Number of repos in 2020 is : ' + str(df[df['commit_year'].str.contains('2020')].count()[0])
    num_repo_2021 = 'Number of repos in 2021 is : ' + str(df[df['commit_year'].str.contains('2021')].count()[0])
    num_occurences_dp = 'Number of occurences "Differential Privacy: " ' + str(df['commit_message'].str.count(
        'diff privacy | differential privacy | d privacy | dif. privacy | differential priv. | diff priv.').sum())
    num_occurences_ml = 'Number of occurences "Machine Learning: " ' + str(df['commit_message'].str.count(
        'machine learning | m learning | machine l | ml | m. learning | m.l. | machine l | machine l.').sum())

    # stats post-filter

    f_commits_number = 'After filter number of commits is : ' + str(df_filtered['commit_message'].count())
    f_mean_commits_day = 'After filter mean of commits by day is : ' + str((df_filtered['commit_message'].count()) / 24)
    f_number_of_projects = 'After filter number of projects analyzed: ' + str(len(set(df_filtered['repository'])))
    f_num_repo_2020 = 'After filter number of repos in 2020 is : ' + str(
        df_filtered[df_filtered['commit_year'].str.contains('2020')].count()[0])
    f_num_repo_2021 = 'After filter number of repos in 2021 is : ' + str(
        df_filtered[df_filtered['commit_year'].str.contains('2021')].count()[0])
    f_num_occurences_dp = 'After filter number of occurences "Differential Privacy: " ' + str(
        df_filtered['commit_message'].str.count(
            'diff privacy | differential privacy | d privacy | dif. privacy | differential priv. | diff priv.').sum())
    f_num_occurences_ml = 'After filter number of occurences "Machine Learning: " ' + str(
        df_filtered['commit_message'].str.count(
            'machine learning | m learning | machine l | ml | m. learning | m.l. | machine l | machine l.').sum())

    general_data_list.append(commits_number)
    general_data_list.append(mean_commits_day)
    general_data_list.append(number_of_projects)
    general_data_list.append(num_repo_2020)
    general_data_list.append(num_repo_2021)
    general_data_list.append(num_occurences_dp)
    general_data_list.append(num_occurences_ml)

    general_data_list.append(f_commits_number)
    general_data_list.append(f_mean_commits_day)
    general_data_list.append(f_number_of_projects)
    general_data_list.append(f_num_repo_2020)
    general_data_list.append(f_num_repo_2021)
    general_data_list.append(f_num_occurences_dp)
    general_data_list.append(f_num_occurences_ml)

    # charts generation

    # general stats

    # number of repositories by days
    num_repos_days = df.pivot_table(columns=['commit_full_date'], aggfunc='size')
    # number of repositories by years
    num_repos_years = df.pivot_table(columns=['commit_year'], aggfunc='size')

    # stats after filtering

    # number of repositories by days
    f_num_repos_days = df_filtered.pivot_table(columns=['commit_full_date'], aggfunc='size')
    # number of repositories by years
    f_num_repos_years = df_filtered.pivot_table(columns=['commit_year'], aggfunc='size')

    # plot to show number of repositories for each year

    num_repos_years.T[:5].plot(kind='bar', ylabel='Number of commits')
    plt.title('Number of commits for each year')
    plt_no_filtered_year = os.path.join(path_outputs_folder, 'number_repos_by_year.png')
    plt.savefig(plt_no_filtered_year)

    num_repos_days.T[:5].plot(kind='bar', ylabel='Number of commits')
    plt.title('Top 5 months with the higher number of commit')
    plt_no_filtered_day = os.path.join(path_outputs_folder, 'number_repos_by_day.png')
    plt.savefig(plt_no_filtered_day)

    f_num_repos_years.T[:5].plot(kind='bar', ylabel='Number of commits')
    plt.title('Number of commits for each year about differential privacy')
    plt_filtered_year = os.path.join(path_outputs_folder, 'number_repos_by_year_dp.png')
    plt.savefig(plt_filtered_year)

    f_num_repos_days.T[:5].plot(kind='bar', ylabel='Number of commits')
    plt.title('Top 5 days with the higher number of commit about differential privacy')
    plt_filtered_day = os.path.join(path_outputs_folder, 'number_repos_by_day_dp.png')
    plt.savefig(plt_filtered_day)

    print('All charts have been created...')

    # Word cloud generation

    # Start with one review:

    f_text = ''
    text = ''

    for cm_message in df['commit_message']:
        text = text + ' ' + cm_message

    for f_cm_message in df_filtered['commit_message']:
        f_text = f_text + ' ' + f_cm_message

    # Create and generate a word cloud image no dataset filtered:
    wordcloud = WordCloud(background_color="white").generate(text)

    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title('Word cloud before filtering')
    plt.axis("off")
    plt_no_filtered_wc = os.path.join(path_outputs_folder, 'no_filtered_wc.png')
    plt.savefig(plt_no_filtered_wc)

    # Create and generate a word cloud image from dataset filtered:

    wordcloud = WordCloud(background_color="white").generate(f_text)

    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title('Word cloud after filtering')
    plt.axis("off")
    plt_filtered_wc = os.path.join(path_outputs_folder, 'filtered_wc.png')
    plt.savefig(plt_filtered_wc)

    df_filtered_sorted_dp = df_filtered.sort_values(by=['similarity_dp'], ascending=False)

    df_filtered_sorted_ml = df_filtered.sort_values(by=['similarity_ml'], ascending=False)

    # report file generation

    report_txt = os.path.join(path_outputs_folder, 'report.txt')
    textfile = open(report_txt, "w")

    for element in general_data_list:
        textfile.write(element + "\n")
    textfile.close()

    print('Report has been created...')
