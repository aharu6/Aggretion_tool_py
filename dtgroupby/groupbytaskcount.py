import dask.dataframe as dd
import pandas as pd
class GroupByTaskCount:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def group_by_task_count(self, locate_select=None, name_select=None, date_range=None):
        df = self.dataframe

        conditions = []
        if locate_select:
            df = df[df['locate'].isin(locate_select)]
        
        if name_select:
            df = df[df['phName'].isin(name_select)]

        #date_range[0]:start date
        #date_range[1]:end date
        if date_range and len(date_range) ==2:
            start_date = pd.Timestamp(date_range[0])
            end_date = pd.Timestamp(date_range[1])
            conditions.append((df['date'] >= start_date) & (df['date'] <= end_date))

        if conditions:
            combined_condition = conditions[0]
            for condition in conditions[1:]:
                combined_condition &= condition
            df = df[combined_condition]
                    
        return df
            