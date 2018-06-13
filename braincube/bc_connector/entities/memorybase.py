#!/usr/bin/env python
# -*- coding:utf-8 -*-
from datetime import datetime


class Memorybase:
    def __init__(self, braincube_name, mb_id, retriever):
        self.__retriever = retriever
        self.__braincube = braincube_name
        self.__mb_id = mb_id

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

    def retrieve_all_variables_from_memory_base(self, start_date, end_date=datetime.now()):
        # Return a dataframe containing the datas of all the variables of the selected memorybase
        # Indexed with the order variable, a column represents a variable
        return self.__retriever.retrieve_all_variables_from_memory_base(self.__braincube, self.__mb_id, start_date,
                                                                        end_date)

    def retrieve_data(self, variable_list, start_date, end_date=datetime.now()):
        # Return a dataframe containing the datas of the seelcted variables for the selected memorybase
        # Indexed with the order variable, a column represents a variable
        return self.__retriever.retrieve_data(self.__braincube, self.__mb_id, variable_list,
                                              start_date, end_date)

    def create_variable_set(self, variable_list):
        return self.__retriever.create_variable_set(self.__braincube, self.__mb_id, variable_list)
