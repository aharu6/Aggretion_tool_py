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
            #問い合わせ応需カウンターはそのまま
            di_mask = df['locate'].apply(lambda x: has_location(x, 'DI'))
            normalize_task_mask = df['task'].isin(['問い合わせ業務', 'その他の職種からの相談'])
            df.loc[di_mask & normalize_task_mask,'task'] = '問い合わせ応需'
            """新→旧へ直した時の件数の統一"""
            #"服薬指導":"服薬指導＋指導記録作成", "指導記録作成": "服薬指導＋指導記録作成",
            #件数は指導記録作成の方で統一する,服薬指導の方は0にする
            df.loc[df['task']=='服薬指導','count'] = 0
            
            #"無菌調製(調製者)": "無菌調製関連業務",E "無菌調製補助業務（準備、鑑査）": "無菌調製関連業務",
            #件数は無菌調製(調製者)の方で統一する
            df.loc[df['task']=='無菌調製補助業務（準備、鑑査）','count'] = 0
            
            #"薬剤セット": "薬剤セット・確認", "薬剤セット確認": "薬剤セット・確認",
            #件数は薬剤セットの方で統一する
            df.loc[df['task']=='薬剤セット確認','count'] = 0
            
            
            df['task'] = df['task'].map(self.model).fillna(df['task'])
            #locate=DIにおけるtask=="問い合わせ業務"をtask=="問い合わせ応需"へ変更
            print(df)
        return df
            