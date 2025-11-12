import dask.dataframe as dd
import pandas as pd
from io import StringIO
import chardet

class JoinFiles:
    def __init__(self, files):
        self.files = files


    def join(self):
        def safe_decode(file_bytes):
            encodings = ['utf-8', 'shift_jis', 'euc_jp', 'utf-16']
            """複数のエンコーディングを試してファイルをデコード"""
            detected =chardet.detect(file_bytes)
            if detected['encoding']:
                encodings.insert(0, detected['encoding'])

                for encoding in encodings:
                    try:
                        return file_bytes.decode(encoding)
                    except UnicodeDecodeError:
                        continue
            raise UnicodeDecodeError("すべてのエンコーディングでデコードに失敗しました。")
        
        
        combined_df = None

        for file in self.files:
            if hasattr(file,"read"):
                content=StringIO(safe_decode(file.getvalue()))
                #csvファイルを縦に結合していく
                df =pd.read_csv(content)
                df =dd.from_pandas(df,npartitions = 1)
                
            else:
                df = dd.read_csv(file).compute()
            
            if combined_df is None:
                combined_df=df
            else:
                combined_df=dd.concat([combined_df,df]).compute()

        return combined_df