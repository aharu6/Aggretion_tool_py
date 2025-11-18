import dask.dataframe as dd
import pandas as pd
from io import StringIO
import chardet
import re
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

        dataframes=[]
        for file in self.files:
            #ファイル名の日付データを取得する'2025-4-1三浦 太一.csv' '2025-4-1小林 京助.csv'
            #数字の部分でファイル名を切れば日付になる
            date_part=re.search(r'(\d{4}-\d{1,2}-\d{1,2})',file.name)
            if date_part is None:
                print(f"ファイル名から日付を取得できませんでした: {file.name}")
                break

            if hasattr(file,"read"):
                content=StringIO(safe_decode(file.getvalue()))
                #csvファイルを縦に結合していく
                df =pd.read_csv(content)
                df =dd.from_pandas(df,npartitions = 1)
                df["date"]=date_part.group(0)
                
                
            else:
                df = dd.read_csv(file)
                #日付列を加える
                df["date"]=date_part.group(0)
            df["date"] = dd.to_datetime(df["date"],format="%Y-%m-%d")
            dataframes.append(df)
                
            if dataframes:
                combined_df = dd.concat(dataframes,ignore_index=True)
                return combined_df.compute()
            
            else:
                return None
