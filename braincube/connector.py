#!/usr/bin/env python
# -*- coding:utf-8 -*-
import webbrowser as __browser
import json as __json
import requests as __requests
import re as __research
from flask import Flask as __Flask
from flask import request as __request
from flask import redirect as __redirect
from flask_cors import CORS as __CORS
from flask_cors import cross_origin as __cross_origin
from gevent.pywsgi import WSGIServer as __WSGIServer
from braincube.bc_connector.braincube_requests import request_data as __request_data
from braincube.bc_connector.data_formatting import data_to_dataframe as __data_to_dataframe
from braincube.bc_connector.braincube_requests import get_sso_token as __get_sso_token
from braincube.bc_connector.pandas_retriever import PandasRetriever as __PandasRetriever
from braincube.bc_connector.raw_retriever import RawRetriever as __RawRetriever
__app = __Flask(__name__)
__app.config['CORS_HEADERS'] = 'Content-Type'
__server = __WSGIServer(('localhost', 5000), __app, log=None)
__cors = __CORS(__app, resources={r"/*": {"origins": "https://mybraincube.com/*"}})

__authorize_uri = "https://mybraincube.com/sso-server/vendors/braincube/authorize.jsp"
__token_uri = "https://mybraincube.com/sso-server/ws/oauth2/token"
__redirect_uri = "http://localhost:5000/token"
__client_id = "975d984d-2995-3a1d-8174-2a26c4fdd941"
__client_secret = "7152b2fd-689c-32e9-9f3a-dd2ae4eaa4b0"
__scopes = "BASE%20API"


@__app.route('/')
@__cross_origin()
# Code executed when launching the local server
# Opens the Braincube authorization page or the React page according to the parameter passed in query
def __launch_connector():
    if __request.args.get('from_web'):
        url = "https://mybraincube.com/connectors/tableau/?pandas=True"
    else:
        url = __authorize_uri\
              + '?client_id=' + __client_id\
              + '&response_type=code' \
              + '&scope=' + __scopes\
              + '&redirect_uri=' + __redirect_uri
    return __redirect(url)


@__app.route('/token')
@__cross_origin()
# Code executed when returning from the Braincube authorization page
# Allows to recover a token thanks to the received code
def __get_token_from_code():
    code = __research.search('code=(.*)', __request.url).group(1)
    content = {"grant_type": "authorization_code",
               "code": code,
               "redirect_uri": __redirect_uri,
               "client_id": __client_id,
               "client_secret": __client_secret
               }
    print("Pending recovery attempt, please wait")
    retrieve_token = __requests.post(__token_uri, data=content)
    global TOKEN  # The only way to return a result from a flask app
    TOKEN = __json.loads(retrieve_token.text)['access_token']
    # To close the flask app and execute the code after
    __server.close()
    return '<h1 style="text-align:center">Data successfully retrieved</h1>' \
           '<h3 style="text-align:center">You can now close this page</h3>'


@__app.route('/data', methods=['POST'])
@__cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
# Code executed when the local server receives information from the react page
# Get this info and call the REST API to retrieve the data
def __get_data():
    print("Variables selected, recovery in progress")
    data = __request.get_json(force=True)
    __format_data(data)
    return "OK"


@__app.route('/close')
@__cross_origin(origin='localhost')
# Code executed when the react page successfully transmits data to the bc_connector
# Closes the local server to execute the rest of the code
def __close_app():
    __server.close()
    return 'OK'


def __format_data(data):
    # Read the received info and call the REST API to retrieve the desired data
    selected_variables = data['selectedVariableList']
    start_date = data['startDate']
    end_date = data['endDate']
    braincube_name = data['braincubeName']
    sso_token = data['ssoToken']
    global MEMORY_BASE_SELECTED
    MEMORY_BASE_SELECTED = data['memoryBaseSelected']
    global DATADEFS
    DATADEFS = data['listOfDatadefs']
    global DATA
    DATA = __request_data(MEMORY_BASE_SELECTED, selected_variables, braincube_name, start_date, end_date, sso_token)
    print("Formatting your data")


def connect(token=0, format_type='pandas'):
    # Function called by the user to access to flask_the python API
    # if the user call this function with a token, check it's validity and return an object object to manipulate the API
    if token != 0:
        data = __get_sso_token(token)
    # redirect the user to the braincube autorisation page to get a token and return an object to manipulate the API
    else:
        __browser.open('http://localhost:5000/')
        try:
            __server.serve_forever()
        except OSError:
            print('The port 5000 of the machine is already open, please close your activity before restarting it')
        token = TOKEN
        data = __get_sso_token(token)
    if format_type == 'raw':
        return __RawRetriever(token, data['token'], data['accessList'])
    else:
        return __PandasRetriever(token, data['token'], data['accessList'])


def retrieve_data_from_web():
    # Function called by the user to access to the React page and select the wanted data
    # Launch the local serveur, which runs the react page
    __browser.open('http://localhost:5000/?from_web=True')
    try:
        __server.serve_forever()
    except OSError:
        print('The port 5000 of the machine is already open, please close your activity before restarting it')

    # When the user have selected his data, format it and return a Dataframe with all the data in it
    try:
        global DATA
        d = __data_to_dataframe(DATA['datadefs'], DATADEFS, MEMORY_BASE_SELECTED)
        del DATA
        return d
    except NameError:
        print("No data retrieved, process stopped before the end")
    return None
