def cleaning_df(df):
    #locateデータがいらないtaskの時はlocateデータを削除する
    #該当するもの："委員会","勉強会参加","WG活動","1on1","業務調整","休憩",
    target_task = ["委員会","勉強会参加","WG活動","1on1","業務調整","休憩"]
    df.loc[df['task'].isin(target_task),'locate'] = None
    return df