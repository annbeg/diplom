import spacy
from nominatim import *

def NER(dataframe,abbHistoryDict):
    df = dataframe.copy()

    nlp_xx = spacy.load('xx_ent_wiki_sm')
    ner_xx = nlp_xx.get_pipe("ner")
    useful_NER_labels = ['LOC']
    changed_values_count = 0
    for i,row in df.iterrows() :
        if row.location == '':
            continue
        if row.location in abbHistoryDict:
            continue

        doc_xx = nlp_xx(row.location)
        processed_xx = ner_xx(doc_xx)

        for ent in processed_xx.ents:
            if (ent.label_ in useful_NER_labels):
                formatted_location = nominatimQueryToCountryCode(str(ent))
                if formatted_location :

                    abbHistoryDict[formatted_location] = formatted_location
                    abbHistoryDict[str(ent)] = formatted_location

                    df.iloc[i].location = formatted_location
                    changed_values_count += 1
                    break

    changed_values_percent = changed_values_count/len(df)
    return df , changed_values_percent, abbHistoryDict
