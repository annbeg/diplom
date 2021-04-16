from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from os.path import join, dirname, realpath

import pickle


from flask_cors import CORS

from user import *
from nominatim import *
from NER import NER



app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

@app.route('/')
def index():
    return 'Hello World'

@app.route('/user/<username>')
def getUserInformation(username):
    resp = getUserInfo(username)
    # print(resp)
    return jsonify(resp)

@app.route('/subscriptions/<username>')
def getUserSubscriptions(username):
    userRestId = getUserInfo(username)['rest_id']
    resp = getUserFollowing(userRestId)

    return resp.to_json()

@app.route('/upload', methods=['GET','POST'])
def uploadFiles():
    # get the uploaded file
    # print(request.files['myFile'])
    uploaded_file = request.files['myFile']
    abbHistoryDict = pd.read_pickle('abbHistoryDict.p')

    df = pd.read_csv(uploaded_file, header=None, names = ['username','location'])
    df = df.fillna('')
    df.location = df.apply(lambda row: getUserInfo(row['username'])['location'],axis = 1)


    obviousDF, changed_locations_percent, empty_locations_percent, abbHistoryDict = formatObviousLocations(df, abbHistoryDict)
    NERresDF, changed_with_NER_percent, abbHistoryDict = NER(obviousDF, abbHistoryDict)

    countries_codes_df = pd.read_pickle('alpha2_alpha3_dict.p')

    counted_unique_df = NERresDF.groupby('location')['username'].nunique()
    counted_unique_df = counted_unique_df.loc[pd.Series(counted_unique_df.keys()).apply(lambda x: x in abbHistoryDict).to_list()]
    counted_unique_df = pd.DataFrame(counted_unique_df)
    counted_unique_df = counted_unique_df.assign(ISO3=pd.Series(counted_unique_df.index).apply(lambda x: countries_codes_df[x.upper()]).values)
    counted_unique_df = counted_unique_df.assign(proportion=pd.Series(counted_unique_df['username'].apply(lambda x: x/counted_unique_df['username'].sum())).values)
    # if uploaded_file.filename != '':
    #    file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
    #   # set the file path
    #    uploaded_file.save(file_path)
    #   # save the file
    pickle.dump(abbHistoryDict, open('abbHistoryDict.p', 'wb'))
    return jsonify({'count': counted_unique_df.to_dict(orient='records'),'df': NERresDF.to_dict(orient='records'), 'changed_locations_percent': changed_locations_percent})
    # return redirect(url_for('index'))
    # return render_template('indexo.html',data=Todos.query.all())

if __name__ == "__main__":
    app.run()
