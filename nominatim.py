import pandas as pd
import requests
import json


def nominatimQueryToCountryCode(q):
    response_search = requests.request("GET", f"https://nominatim.openstreetmap.org/search?q={q.replace('#', '')}&format=json")
    response_search_json = json.loads(response_search.text)
    if response_search_json:
        try:
            response_details = requests.request("GET", f"https://nominatim.openstreetmap.org/details?osmtype=R&osmid={response_search_json[0]['osm_id']}&format=json")
        except KeyError:
            return None
    else:
        return None
    response_details_json = json.loads(response_details.text)
    if 'error' in response_details_json:
        return None
    return response_details_json['country_code']

def formatObviousLocations(df, abbHistoryDict):
    dataframe = df.copy()
    changed_locations_count = 0
    empty_locations_count = 0
    for i,row in dataframe.iterrows():

        if row.location == '':
            empty_locations_count += 1
            continue
        if not row.location:
            empty_locations_count += 1
            continue

        if not row.location in abbHistoryDict:
            formatted_location = nominatimQueryToCountryCode(row.location)
            if formatted_location:
                abbHistoryDict[formatted_location] = formatted_location
                abbHistoryDict[row.location] = formatted_location

                dataframe.iloc[i].location = formatted_location
                changed_locations_count += 1
        else:
            dataframe.iloc[i].location = abbHistoryDict[row.location]
            changed_locations_count += 1

    changed_locations_percent = changed_locations_count/len(dataframe)
    empty_locations_percent = empty_locations_count/len(dataframe)

    return dataframe, changed_locations_percent, empty_locations_percent, abbHistoryDict
