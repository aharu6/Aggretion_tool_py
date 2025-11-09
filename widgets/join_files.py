import dask.dataframe as dd
import pandas as pd
from io import StringIO


class JoinFiles:
    def __init__(self, files):
        self.files = files

    def join(self):
        print(f"{self.files}")
        combined_df = None

        for file in self.files:
            if hasattr(file,"read"):
                content=StringIO(file.getvalue().decode("utf-8"))
                #csvファイルを縦に結合していく
                df =pd.read_csv(content)
                combined_df =dd.from_pandas(df,npartitions = 1)
                
            else:
                df = dd.read_csv(file)
            
            if combined_df is None:
                combined_df=df
            else:
                combined_df=dd.concat([combined_df,df],axis=0,interleave_partitions=True)
        print(combined_df.head(6))
        return combined_df