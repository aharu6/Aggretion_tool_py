import dask.dataframe as dd
import pandas as pd
from models.datamodel import Datamodel
class GroupByTaskCount:
    def __init__(self, dataframe):
        self.dataframe = dataframe
        self.model = Datamodel().old_new_taskname_map()

    def group_by_task_count(self, locate_select, name_select, date_range,taskname_tydir):
        df = self.dataframe
        conditions = []
        if locate_select:
            df = df[df['locate'].apply(lambda x:any(loc in x for loc in locate_select))]

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
                    
        if taskname_tydir==True:
            #新データの業務名を旧データの業務名へ統一
            df['task'] = df['task'].map(self.model).fillna(df['task'])
        return df
            