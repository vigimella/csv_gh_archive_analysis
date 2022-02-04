This tool allows merging multiple CSV, and after, if you want, to execute an analysis that give as output CSV merged, a report in TXT
format, and a set of charts obtained from the analysis. **Remember to change the CSV structure to avoid malfunctions**.

# CSV Upload
Before start, you have to create a folder with name “elm” where you are going to insert all CSV files to merge.
# Installation
In order to install all requirements, you can use  the following command.
```bash
pip install -r requirements.txt
```
In order to use the function to remove stop words, you have to install NLTK.
```bash
pip install nltk
```

After that remember to install en_core_web_lg. This is necessary in order to execute a similarity calculation.

```bash
python -m spacy download en_core_web_lg
```

#License
Using are welcome, remember to quote me.

Vigimella - 2022.