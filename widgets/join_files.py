import dask.dataframe as dd
import pandas as pd
from io import StringIO
import chardet
import re
import os
from concurrent.futures import ThreadPoolExecutor,as_completed
from resizeDataframe.creaningDataframe import cleaning_df
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

        def process_single_file(file):
            date_part = re.search(r'(\d{4}-\d{1,2}-\d{1,2})', file.name)
            if date_part is None:
                print(f"ファイル名から日付を取得できませんでした: {file.name}")
                return None
            try:
                if hasattr(file,"read"):
                    content = StringIO(safe_decode(file.getvalue()))
                    df = pd.read_csv(content) 
                    cleaned_df = cleaning_df(df)
                    if cleaned_df is not None:
                        df = cleaned_df
                else:
                    df = pd.read_csv(file)
                    cleaned_df = cleaning_df(df)
                    if cleaned_df is not None:
                        df = cleaned_df

                df["date"] = pd.to_datetime(date_part.group(0), format="%Y-%m-%d")
                return df
            except Exception as e:
                print(f"ファイルの処理中にエラーが発生しました: {file.name}, エラー: {e}")
                return None
        
        check_folders = [f for f in os.listdir('.') if os.path.isdir(f)]
        if check_folders:
            for subfolder in check_folders:
                with ThreadPoolExecutor(max_workers=4) as executor:
                    future_to_file = {executor.submit(process_single_file,os.path.join(subfolder,f)):f for f in os.listdir(subfolder) if f.endswith('.csv')}
                    for future in as_completed(future_to_file):
                        df = future.result()
                        if df is not None:
                            if combined_df is None:
                                combined_df = df
                            else:
                                combined_df = pd.concat([combined_df,df],ignore_index=True)
                                
        dataframes=[] 
        with ThreadPoolExecutor(max_workers=4) as executor:
            future_to_file = {executor.submit(process_single_file,file):file for file in self.files}

            for future in as_completed(future_to_file):
                df = future.result()
                if df is not None:
                    dataframes.append(df)

                
        if dataframes:
            total_rows = sum(len(df) for df in dataframes)

            if total_rows < 100000:
                combined_df = pd.concat(dataframes,ignore_index=True)
            else:
                dask_dfs = [dd.from_pandas(df,npartitions=1) for df in dataframes]
                combined_df = dd.concat(dask_dfs,ignore_index=True).compute()
                
            return combined_df
        
        else:
            return None
