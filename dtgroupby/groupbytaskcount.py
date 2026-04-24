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

        def has_location(value, target):
            if isinstance(value, (list, tuple, set)):
                return target in value
            if pd.isna(value):
                return False
            if isinstance(value, str):
                if value == target:
                    return True
                # 例: "['DI']" のような文字列化リストも判定できるようにする
                return f"'{target}'" in value or f'"{target}"' in value
            return False

        if locate_select:
            df = df[df['locate'].apply(lambda x: any(has_location(x, loc) for loc in locate_select))]

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
            di_mask = df['locate'].apply(lambda x: has_location(x, 'DI'))
            normalize_task_mask = df['task'].isin(['問い合わせ業務', 'その他の職種からの相談'])
            df.loc[di_mask & normalize_task_mask,'task'] = '問い合わせ応需'
            df['task'] = df['task'].map(self.model).fillna(df['task'])
            #locate=DIにおけるtask=="問い合わせ業務"をtask=="問い合わせ応需"へ変更
            print(df)
        return df
            