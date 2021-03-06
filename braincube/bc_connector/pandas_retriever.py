#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pandas as pd
from datetime import datetime
from braincube.bc_connector.data_formatting import data_to_dataframe
from braincube.bc_connector.raw_retriever import RawRetriever
from braincube.bc_connector.entities.braincube import Braincube
from braincube.bc_connector.entities.memorybase import Memorybase
from braincube.bc_connector.entities.variable_set import VariableSet
from braincube.bc_connector.braincube_requests import get_references, get_data_defs


class PandasRetriever(RawRetriever):  # Class giving access to functions communicating with the braincube API
    def __init__(self, token, sso_token, braincubes):
        RawRetriever.__init__(self, token, sso_token, braincubes)
        self.__token = token
        self.__sso_token = sso_token
        self.__braincubes = braincubes

    def get_token(self):
        # Display the token to the user
        return self.__token

    def get_braincube_list(self):
        # Return a dataframe containing the braincubes accessible
        try:
            bc_id = []
            bc_name = []

            for i in self.__braincubes:
                if i['product']['type'] == 'braincube':
                    bc_id.append(i['product']['productId'])
                    bc_name.append(i['product']['name'])
            return pd.DataFrame({'product_id': bc_id, 'name': bc_name})
        except TypeError:
            print("No data retrieved")
        return

    def get_memorybase_list(self, braincube_name):
        # Return a dataframe containing the memorybases available for the braincube selected
        try:
            mb_name = []
            mb_nb_var = []
            mb_id = []
            print('Braincube selected : ' + braincube_name)
            memorybases = super(PandasRetriever, self).get_memorybase_list(braincube_name)
            for i in memorybases:
                if not i['quickStudy']:
                    mb_id.append(i['bcId'])
                    mb_name.append(i['name'])
                    mb_nb_var.append(i['numberOfVariables'])
            return pd.DataFrame({'id': mb_id, 'name': mb_name, 'number_of_variable': mb_nb_var})
        except TypeError:
            print("No data retrieved")

    def get_memorybase_order_variable(self, braincube_name, mb_id):
        # Return the id of the variable which is used to order the memorybase
        ref = super(PandasRetriever, self).get_memorybase_references(braincube_name, mb_id)
        return ref['referenceDate'].split('/d')[1]

    def get_variable_list(self, braincube_name, mb_id):
        # Return a dataframe containing the variables available for the memorybase selected
        try:
            var_name = []
            var_id = []
            data_def = super(PandasRetriever, self).get_variable_list(braincube_name, mb_id)
            for i in data_def:
                var_id.append(i['id'])
                var_name.append(i['local'])
            return pd.DataFrame({'id': var_id, 'name': var_name})
        except TypeError:
            print("No data retrieved")

    def retrieve_all_variables_from_memory_base(self, braincube_name, mb_id, start_date, end_date=datetime.now()):
        # Return a dataframe containing the datas of all the variables of the selected memorybase
        # Indexed with the order variable, a column represents a variable
        variable_list = self.get_variable_list(braincube_name, mb_id)
        selected_variables = []
        for var in variable_list.itertuples():
            selected_variables.append(var.id)
        return self.retrieve_data(braincube_name, mb_id, selected_variables, start_date, end_date)

    def retrieve_data(self, braincube_name, mb_id, variable_list, start_date, end_date=datetime.now()):
        # Return a dataframe containing the datas of the seelcted variables for the selected memorybase
        # Indexed with the order variable, a column represents a variable
        try:
            ref = get_references(braincube_name, mb_id, self.__sso_token)
            data = super(PandasRetriever, self)\
                .retrieve_data(braincube_name, mb_id, variable_list, start_date, end_date)
            print('Format the data')
            data_def = get_data_defs(braincube_name, mb_id, self.__sso_token)
            return data_to_dataframe(data, data_def, ref)
        except TypeError:
            print("No data retrieved")

    def create_braincube(self, braincube_name):
        return Braincube(braincube_name, self)

    def create_memorybase(self, braincube_name, mb_id):
        return Memorybase(braincube_name, mb_id, self)

    def create_variable_set(self, braincube_name, mb_id, variable_list):
        return VariableSet(braincube_name, mb_id, variable_list, self)
