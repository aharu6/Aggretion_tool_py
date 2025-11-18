import dask.dataframe as dd
import pandas as pd
class GroupByTaskCount:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def group_by_task_count(self, locate_select=None, name_select=None, date_range=None):
        df = self.dataframe
        if locate_select:
            df = df[df['locate'].isin(locate_select)]
        
        if name_select:
            df = df[df['phName'].isin(name_select)]

        #date_range[0]:start date
        #date_range[1]:end date
        if date_range and len(date_range) ==2:
            start_date = pd.to_datetime(date_range[0])
            print("start_date:",start_date)
            print("end_date:",date_range[1])
            
            end_date = pd.to_datetime(date_range[1])
            df = df[(df['date'] >= start_date)&(df['date']<= end_date)]
        
        return df
            