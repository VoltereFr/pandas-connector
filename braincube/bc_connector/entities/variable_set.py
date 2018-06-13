#!/usr/bin/env python
# -*- coding:utf-8 -*-
from datetime import datetime
import pandas as pd


class VariableSet:
    def __init__(self, braincube_name, mb_id, variable_list, retriever):
        self.__retriever = retriever
        self.__braincube = braincube_name
        self.__mb_id = mb_id
        self.__variables = variable_list

    def get_braincube_list(self):
        # Return a dataframe containing the braincubes accessible
        return self.__retriever.get_memorybase_list()

    def get_memorybase_list(self):
        # Return a dataframe containing the memorybases available for the braincube selected
        return self.__retriever.get_memorybase_list(self.__braincube)

    def get_memorybase_order_variable(self):
        # Return the id of the variable which is used to order the memorybase
        return self.__retriever.get_memorybase_order_variable(self.__braincube, self.__mb_id)

    def get_variable_list(self):
        # Return a dataframe containing the variables available for the memorybase selected
        return self.__retriever.get_variable_list(self.__braincube, self.__mb_id)

    def get_selected_variables(self):
        try:
            bc_id = []
            bc_name = []
            for i in self.get_variable_list().itertuples():
                if i.id in self.__variables:
                    bc_id.append(i.id)
                    bc_name.append(i.name)
            return pd.DataFrame({'product_id': bc_id, 'name': bc_name})
        except NameError:
            print("No data retrieved, process stopped before the end")

    def retrieve_data(self, start_date, end_date=datetime.now()):
        # Return a dataframe containing the datas of the seelcted variables for the selected memorybase
        # Indexed with the order variable, a column represents a variable
        return self.__retriever.retrieve_data(self.__braincube, self.__mb_id,
                                              self.__variables, start_date, end_date)
