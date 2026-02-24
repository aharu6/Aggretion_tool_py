#ダウンロード用のデータを加工する
#名前を数字に変換する
import pandas as pd
def tidy_data(filtered_df,combined_df,change_name):
    """_summary_

    Args:
        filtered_df (_type_): _description_
        combined_df (_type_): _description_
        change_name (_type_): 1なら名前を数字に変換、0ならそのまま
    """
    df = filtered_df if filtered_df is not None else combined_df
    if change_name == 1:
        name_mapping = {name: idx for idx,name in enumerate(df["phName"].unique())}
        df["phName"] = df["phName"].map(name_mapping)
        #名前と番号の対応表を作成
        name_mapping_df = pd.DataFrame(list(name_mapping.items()),columns=["薬剤師名","対応番号"])
        return df, name_mapping_df
    else:
        return df, None
    
    