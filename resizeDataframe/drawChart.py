import streamlit as st
from view.TASK_COLOR_MAP import TASK_COLOR_MAP
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import ast
def _get_data(filtered_data,combined_data):
    return filtered_data if filtered_data is not None else combined_data

def _calculate_time_by_group(data,group_by_column):
    counts = data.groupby(group_by_column).size().reset_index(name='time')
    counts['time'] *= 15
    return counts

def _filter_and_aggregate_task(data,task_name):
    task_data = data[['phName','count','task']]
    task_data = data[data['task'] ==task_name]
    task_data['time'] = 15
    task_data = task_data.groupby('phName',as_index =False)[['time','count']].sum()
    return task_data
    
def Calculate_1on1(filtered_data,combined_data):
    def _extract_data(df):
        df=df[['phName','task']]
        df=df[df['task']=='1on1']
        df=df.groupby('phName').size().reset_index(name='count')
        df['time'] = df['count']*15
        return df
    df=_extract_data(filtered_data if filtered_data is not None else combined_data)
    fig = px.bar(data_frame=df,x='phName',y='time',labels={'phName':'薬剤師名','time':'総時間(min)'})
    st.plotly_chart(fig,key="Calculate_1on1_chart")

def Calculate_NST(filtered_data,combined_data):
    def _extract_data(df):
        df=df[['phName','task']]
        df=df[df['task']=='NST']
        df=df.groupby('phName').size().reset_index(name='count')
        df['time'] = df['count']*15
        return df
    df=_extract_data(filtered_data if filtered_data is not None else combined_data)
    fig = px.bar(data_frame=df,x='phName',y='time',labels={'phName':'薬剤師名','time':'総時間(min)'})
    st.plotly_chart(fig,key="Calculate_NST_chart")

def Calculate_TDM(filtered_data,combined_data):
    def _extract_data(df):
        df=df[['phName','task',"count"]]
        df=df[df['task']=='TDM実施']
        df=df.groupby(['phName','task']).agg(
            count_sum =('count','sum'),
            size_count =('task','size')
        ).reset_index()
        df['time'] = df['size_count']*15
        df['time_per_count'] = df['time'] / df['count_sum']
        return df
    df=_extract_data(filtered_data if filtered_data is not None else combined_data)
    fig = go.Figure(
        data=[
            go.Bar(
                name="件数(件)",
                x=df['phName'],
                y=df['count_sum']
            ),
            go.Bar(
                name="1件あたりの時間(min)",
                x=df['phName'],
                y=df['time_per_count']
            )
        ]
    )
    fig.update_layout(
        xaxis_title="薬剤師名",
        yaxis_title="件数(件)/1件あたりの時間(min)",
    )
    st.plotly_chart(fig)
        

def Calculate_TPN(filtered_data,combined_data):
    def _extract_data(df):
        df=df[['phName','task',"count"]]
        df=df[df['task']=='TPN評価']
        df=df.groupby(['phName','task']).agg(
            count_sum =('count','sum'),
            size_count =('task','size')
        ).reset_index()
        df['time'] = df['size_count']*15
        df['time_per_count'] = df['time'] / df['count_sum']
        return df
    df=_extract_data(filtered_data if filtered_data is not None else combined_data)
    st.dataframe(df,column_config={
        'phName':'薬剤師名','count_sum':'総件数','size_count':'記録回数',
        'time':'総時間(min)','time_per_count':'1件あたりの時間(min)'})

def Calculate_WG(filtered_data,combined_data):
    def _extract_data(df):
        df=df[['phName','task']]
        df=df[df['task']=='WG活動']
        df=df.groupby('phName').size().reset_index(name='count')
        df['time'] = df['count']*15
        return df
    df=_extract_data(filtered_data if filtered_data is not None else combined_data)
    fig = px.bar(data_frame=df,x='phName',y='time',labels={'phName':'薬剤師名','time':'総時間(min)'},)
    st.plotly_chart(fig,key="Calculate_WG_chart")


def Calculate_confa(filtered_data,combined_data):
    def _extract_data(df):
        df=df[['phName','task']]
        df=df[df['task']=='カンファ・ラウンド']
        df=df.groupby('phName').size().reset_index(name='count')
        df['time'] = df['count']*15
        df['time'] = df['time']/60
        return df
    df=_extract_data(filtered_data if filtered_data is not None else combined_data)
    fig = px.bar(data_frame=df,x='phName',y='time',labels={'phName':'薬剤師名','time':'総時間(hr)'})
    st.plotly_chart(fig,key="Calculate_confa_chart")

def Calculate_conference(filtered_data,combined_data):
    def _extract_data(df):
        df=df[['phName','task']]
        df=df[df['task']=='カンファレンス']
        df=df.groupby('phName').size().reset_index(name='count')
        df['time'] = df['count']*15
        return df
    df=_extract_data(filtered_data if filtered_data is not None else combined_data)
    fig = px.bar(data_frame=df,x='phName',y='time',labels={'phName':'薬剤師名','time':'総時間(min)'})
    st.plotly_chart(fig,key="Calculate_conference_chart")


def Calculate_other_consultation(filtered_data,combined_data):
    def _extract_data(df):
        df=df[['phName','task','count']]
        df=df[df['task']=='その他の職種からの相談']
        df=df.groupby(['phName','task']).agg(
            count_sum =('count','sum'),
            size_count =('task','size')
        ).reset_index()
        df['time'] = df['size_count']*15
        df['time_per_count'] = df['time'] / df['count_sum']
        return df

    df=_extract_data(filtered_data if filtered_data is not None else combined_data)
    fig = go.Figure(
        data=[
            go.Bar(
                name="件数(件)",
                x=df['phName'],
                y=df['count_sum']
            ),
            go.Bar(
                name="1件あたりの時間(min)",
                x=df['phName'],
                y=df['time_per_count']
            )
        ]
    )
    fig.update_layout(
        xaxis_title="薬剤師名",
        yaxis_title="件数(件)/1件あたりの時間(min)",
    )
    st.plotly_chart(fig,key = "TDM_chart")

def Calculate_doctor_consultation(filtered_data,combined_data):
    def _extract_data(df):
        df=df[['phName','task','count']]
        df=df[df['task']=='医師からの相談']
        df=df.groupby(['phName','task']).agg(
            count_sum =('count','sum'),
            size_count =('task','size')
        ).reset_index()
        df['time'] = df['size_count']*15
        df['time_per_count'] = df['time'] / df['count_sum']
        return df
    df=_extract_data(filtered_data if filtered_data is not None else combined_data)
    fig = go.Figure(
        data = [
            go.Bar(
                name="件数(件)",
                x=df['phName'],
                y=df['count_sum']
            ),
            go.Bar(
                name="1件あたりの時間(min)",
                x=df['phName'],
                y=df['time_per_count']
            )
        ]
    )
    fig.update_layout(
        xaxis_title="薬剤師名",
        yaxis_title="件数(件)/1件あたりの時間(min)",
    )
    st.plotly_chart(fig,key = "doctor_consultation_chart")


def Calculate_nurse_consultation(filtered_data,combined_data):
    def _extract_data(df):
        df=df[['phName','task','count']]
        df=df[df['task']=='看護師からの相談']
        df=df.groupby(['phName','task']).agg(
            count_sum =('count','sum'),
            size_count =('task','size')
        ).reset_index()
        df['time'] = df['size_count']*15
        df['time_per_count'] = df['time'] / df['count_sum']
        return df
    df=_extract_data(filtered_data if filtered_data is not None else combined_data)
    fig = go.Figure(
        data=[
            go.Bar(
                name = "件数(件)",
                x= df['phName'],
                y= df['count_sum']
            ),
            go.Bar(
                name="1件あたりの時間(min)",
                x=df['phName'],
                y=df['time_per_count']
            )
        ]
    )
    fig.update_layout(
        xaxis_title="薬剤師名",
        yaxis_title="件数(件)/1件あたりの時間(min)",
    )
    st.plotly_chart(fig,key="nurse_consultation_chart")



import ast
def time_per_locate_chart(filtered_data,combined_data):
    def _extract_locate_data(df):
        df = df[['locate']].copy()
        df = df[df['locate'].notnull()]
        df['locate']= df['locate'].apply(ast.literal_eval)
        df['locate'] = df['locate'].apply(lambda x: x[0] if len(x)>0 else 'Unknown')
        df = df[df['locate'] != 'Unknown']
        df = df.groupby('locate').size().reset_index(name='time')
        df['time'] = df['time']*15
        df['time'] = df['time']/60
        return df
    
    df=_extract_locate_data(filtered_data if filtered_data is not None else combined_data)
    fig =px.bar(
        data_frame=df,
        x='locate',
        y='time',
        labels={'locate':'病棟','time':'総時間(hr)'}
    )
    fig.update_layout(
        xaxis_title="病棟",
        yaxis_title="総時間(hr)",
    )
    st.plotly_chart(fig,key="time_per_locate_chart")


def Manegment_time(filtered_data,combined_data):
    def _extract_data(df):
        df = df[['phName','task']]
        df = df[df['task']=="管理業務"]
        df = df.groupby('phName').size().reset_index(name = "task_count")
        df['total_time'] =df['task_count']*15
        df['total_time'] = df['total_time']/60
        return df
    
    df = _extract_data(filtered_data if filtered_data is not None else combined_data)
    fig = px.bar(data_frame=df,x='phName',y='total_time',labels={'phName':'薬剤師名','total_time':'時間(hr)'})
    st.plotly_chart(fig,key="Manegment_time_chart")


def Adjustment_work(filtered_data,combined_data):
    def _extract_data(df):
        df = df[['phName',"task"]]
        df = df[df['task'] =="業務調整"]
        df = df.groupby('phName').size().reset_index(name = "task_count")
        df['total_time'] = df['task_count']*15
        df['total_time'] = df['total_time']/60
        return df
    
    df = _extract_data(filtered_data if filtered_data is not None else combined_data)
    fig = px.bar(data_frame=df,x='phName',y='total_time',labels={'phName':'薬剤師名','total_time':'時間(hr)'})
    st.plotly_chart(fig,key="Adjustment_work_chart")

def Check_Medication(filtered_data,combined_data):
    def _extract_data(df):
        df = df[['phName','task','count']]
        df = df[df['task'] =='持参薬を確認']
        df = df.groupby(['phName','task']).agg(
            count_sum =('count','sum'),
            task_count = ('task','size')
        ).reset_index()
        df['time'] = df['task_count']*15
        df['time_per_task'] = df['time'] / df['count_sum']
        return df
    df=_extract_data(filtered_data if filtered_data is not None else combined_data)
    fig = go.Figure(
        data = [
            go.Bar(
                name = "件数(件)",
                x = df['phName'],
                y = df['count_sum']
            ),
            go.Bar(
                name="1件あたりの時間(min)",
                x=df['phName'],
                y=df['time_per_task']
            )
        ]
    )
    fig.update_layout(xaxis_title="薬剤師名",yaxis_title="件数(件)/1件あたりの時間(min)",)
    st.plotly_chart(fig,key = "Check_Medication_chart")


def Recept_Agent_Modification(filtered_data,combined_data): #件数、総時間、１けんあたりの時間、グラフ描画
    def _extract_data(df):
        df = df[['phName','count','task']]
        df = df[df['task'] =='処方代理修正']
        df = df.groupby(['phName','task']).agg(
            count_sum=('count','sum'),
            task_count=('task','size')
        ).reset_index()
        df['time'] = df['task_count']*15
        df['time_per_task'] = df['time'] / df['count_sum']
        return df
    df=_extract_data(filtered_data if filtered_data is not None else combined_data)
    fig = go.Figure(
        data = [
            go.Bar(
                name="件数(件)",
                x=df['phName'],
                y=df['count_sum']
            ),
            go.Bar(
                name="1件あたりの時間(min)",
                x=df['phName'],
                y=df['time_per_task']
            )
        ]
    )
    fig.update_layout(
        xaxis_title="薬剤師名",
        yaxis_title="件数(件)/1件あたりの時間(min)",
    )
    st.plotly_chart(fig,key="Recept_Agent_Modification_chart")
    
#TODO:病棟関係ない業務を排除できるボタンを作成、グラフ表示をきりかえる
def Medication_Guidance_Record_Creation(filtered_data,combined_data):
    def _extract_data(df):
        med_data = df[['phName','count','task']]
        med_data = med_data[med_data['task']=='服薬指導＋指導記録作成']
        med_data = med_data.groupby(['phName','task']).agg(
            count_sum = ('count','sum'),
            time = ('task','size')
        ).reset_index()
        med_data['total_time'] = med_data['time']*15
        med_data['time_per_task'] = med_data['total_time'] / med_data['count_sum']
        return med_data
    med_data=_extract_data(filtered_data if filtered_data is not None else combined_data)
    fig = go.Figure(
        data = [
            go.Bar(
                name = "件数(件)",
                x = med_data['phName'],
                y = med_data['count_sum']
            ),
            go.Bar(
                name = "1件あたりの時間(min)",
                x = med_data['phName'],
                y = med_data['time_per_task']
            )
        ]
    )
    fig.update_layout(
        xaxis_title="薬剤師名",
        yaxis_title="件数(件)/1件あたりの時間(min)",
    )
    st.plotly_chart(fig,key="Medication_Guidance_Record_Creation_chart")
    if med_data.empty:
        st.info("該当データが存在しません。")
        return
    
    if (med_data['time_per_task'] == float('inf')).any():
        st.info("1件あたりの時間が算出できないデータがあります。件数が0の可能性があります。")

    st.dataframe(med_data[['phName','count_sum','time_per_task']],column_config={'phName':'薬剤師名','count_sum':'総件数','time_per_task':'1件あたりの時間(min)'})


def total_time_per_task(filtered_data,combined_data):
    def _extract_data(df):
        df = df[['task','count']]
        df=df.groupby('task').size().reset_index(name='times')
        df['times'] = df['times']*15
        df['times'] =df['times']/60
        return df
    
    df=_extract_data(filtered_data if filtered_data is not None else combined_data)
    try:
        fig = px.bar(data_frame=df,x='task',y='times',labels={'task':'業務名','times':'総時間(hr)'})
        st.plotly_chart(fig,key="total_time_per_task_chart")
    except:
        pass

import plotly.express as px
import pandas as pd
def componentChart_location(filtered_data,combined_data):
    def _extract_data(df):
        df = df[['locate','task']]
        df=df.groupby(['locate','task']).size().reset_index(name='count')
        #複数病棟記載されている場合は強制的に先頭の病棟へ統一
        df['locate'] = df['locate'].apply(ast.literal_eval)
        df['locate'] = df['locate'].apply(lambda x: x[0] if len(x)>0 else 'Unknown')
        return df
    
    df = _extract_data(filtered_data if filtered_data is not None else combined_data)
    chart_list = []
    try:
        for locate in df['locate'].unique():
            filtered_data=df[df['locate'] ==locate]
            fig = px.pie(filtered_data,values='count',names='task')
            chart_list.append((locate,fig))

        for locate,fig in chart_list:
            st.markdown(f"### 場所: {locate}")
            st.plotly_chart(fig)
    except Exception as e:
        st.warning(f"チャートの作成中にエラーが発生しました: {e}")

    #TODO:データが存在しない場合はst.infoで通知

def clean_preparation(filtered_data,combined_data):
    def _extract_data(df):
        df = df[['phName','task']]
        df = df[df['task']=='無菌調製関連業務']
        df = df.groupby(['phName','task']).size().reset_index(name='count_sum')
        df['time'] = df['count_sum']*15
        return df
    df = _extract_data(filtered_data if filtered_data is not None else combined_data)
    fig = px.bar(data_frame=df,x='phName',y='time',labels={'phName':'薬剤師名','time':'総時間(min)'})
    st.plotly_chart(fig,key="clean_preparation_chart")

def drag_set_check(filtered_data,combined_data):
    def _extract_data(df):
        df = df[['phName','task']]
        df = df[df['task']=='薬剤セット・確認']
        df = df.groupby(['phName','task']).size().reset_index(name='count_sum')
        df['time'] = df['count_sum']*15
        return df
    df = _extract_data(filtered_data if filtered_data is not None else combined_data)
    fig = px.bar(data_frame=df,x='phName',y='time',labels={'phName':'薬剤師名','time':'総時間(min)'})
    st.plotly_chart(fig,key="drag_set_check_chart")

import plotly.graph_objects as go

def research_info_chart(filtered_data,combined_data):
    def _extract_data(df):
        df = df[['phName','task','count']]
        df = df[df['task']=='薬剤使用状況の把握等（情報収集）']
        df = df.groupby(['phName','task']).agg(
            count_sum =('count','sum'),
            size_count =('task','size'),
        ).reset_index()
        df['time'] = df['size_count']*15
        df['time_per_count'] = df['time'] / df['count_sum']
        return df
    df = _extract_data(filtered_data if filtered_data is not None else combined_data)
    fig = go.Figure(
        data=[
            go.Bar(
                name="件数(件)",
                x=df['phName'],
                y=df['count_sum'],
            ),
            go.Bar(
                name="1件あたりの時間(min)",
                x=df['phName'],
                y=df['time_per_count'],
            )
        ]
    )
    fig.update_layout(
        xaxis_title="薬剤師名",
        yaxis_title="件数(件)/1件あたりの時間(min)",
    )
    st.plotly_chart(fig,key="research_info_chart")

    df['time_per_counte'] = (df['size_count']*15) / df['count_sum']
    st.dataframe(df,column_config={
        'phName':'薬剤師名','count_sum':'総件数','size_count':'記録回数','time_per_count':'1件あたりの時間(min)',
        'time':'総時間(min)'
        })

def Jokusou_chart(filtered_data,combined_data):
    def _extract_data(df):
        df = df[['phName','task']]
        df = df[df['task']=='褥瘡']
        df = df.groupby(['phName','task']).size().reset_index(name='count_sum')
        df['time'] = df['count_sum']*15
        return df

    df = _extract_data(filtered_data if filtered_data is not None else combined_data)
    fig = px.bar(data_frame=df,x='phName',y='time',labels={'phName':'薬剤師名','time':'総時間(min)'})
    st.plotly_chart(fig,key="Jokusou_chart")
        

def self_task_ratio(filtered_data,combined_data):
    def _extract_data(df):
        df = df[['phName','task']]
        df = df.groupby(['phName','task']).size().reset_index(name='count')
        total_counts = df.groupby('phName')['count'].sum().reset_index(name='total_count')
        merged_df = pd.merge(df, total_counts, on='phName')
        merged_df['task_ratio'] = merged_df['count'] / merged_df['total_count']
        return merged_df

    df = _extract_data(filtered_data if filtered_data is not None else combined_data)

    fig = px.bar(
        df,
        x='task_ratio',
        y='phName',
        color='task',
        orientation='h',
        color_discrete_map=TASK_COLOR_MAP,
        labels={'phName':'薬剤師名','task_ratio':'業務割合','task':'業務内容'},
            )
    fig.update_layout(
        barmode='stack',
    )
    st.plotly_chart(fig,key='self_task_ratio_chart')

def comment_data(filtered_data,combined_data):
    def _extract_data(df):
        df = df[['phName','comment','time','locate','date']]
        df = df[df['comment'].notnull() & (df['comment'] !='')]
        df['locate'] = df['locate'].apply(ast.literal_eval)
        df['locate'] = df['locate'].apply(lambda x: x[0] if len(x)>0 else 'Unknown')
        return df
    
    df = _extract_data(filtered_data if filtered_data is not None else combined_data)
    st.dataframe(df,column_config={'phName':'薬剤師名','comment':'コメント','time':'時間','locate':'病棟','date':'日付'})


def task_heatmap(filtered_data,combined_data):
    def _extract_data(df):
        df = df[['phName','time','task']]
        df = df.groupby(['task','time']).size().reset_index(name = "count")
        df['sort_time'] = df["time"].astype(str).fillna("")
        df["sort_time"]=df["sort_time"].str.strip().str.split(" ").str[0]
        df["sort_time"]=pd.to_datetime(df["sort_time"],format="%H:%M",errors="coerce")
        df.sort_values("sort_time")
        return df
    
    df = _extract_data(filtered_data if filtered_data is not None else combined_data)
    
    fig = px.density_heatmap(
        data_frame=df,
        x="time",
        y="task",
        z="count",
        labels={'time':'時間','task':'業務内容','count':'記録回数'}
    )
    fig.update_layout(
        xaxis_title="時間",
        yaxis_title="業務内容",
    )
    st.plotly_chart(fig,key="task_heatmap_chart")


def task_per_location(filtered_data,combined_data):
    def _extract_data(df):
        df = df[['locate','task']]
        df = df[df['locate'].notnull()]
        df['locate'] = df['locate'].apply(ast.literal_eval)
        df['locate'] = df['locate'].apply(lambda x: x[0] if len(x)>0 else 'Unknown')
        df = df.groupby(['locate','task']).size().reset_index(name='count')
        df['time'] = df['count']*15
        df['time'] = df['time']/60
        return df
    
    df = _extract_data(filtered_data if filtered_data is not None else combined_data)

    fig = px.bar(
        data_frame=df,
        x = 'locate',
        y = 'time',
        color= 'task',
        labels={'locate':'病棟','time':'総時間(hr)','task':'業務内容'},
        color_discrete_map=TASK_COLOR_MAP,
        barmode='stack',
        hover_data={'task':True,'time':True,'locate':True}
    )
    fig.update_layout(
        xaxis_title="病棟",
        yaxis_title="総時間(hr)",
    )
    st.plotly_chart(fig,key="task_per_location_chart")

def count_task(filtered_data,combined_data):
    def _extract_data(df):
        df = df[['task','count']]
        df = df.groupby(['task','count']).agg(
            total_count = ('count','sum'),
            record_count = ('task','size')
        ).reset_index()
        df['time'] = df['record_count']*15
        df['time_per_count'] = df['time'] / df['total_count']
        return df
    df = _extract_data(filtered_data if filtered_data is not None else combined_data)
    fig = go.Figure(
        data=[
            go.Bar(
                name="件数(件)",
                x=df['task'],
                y=df['total_count']
            ),
            go.Bar(
                name="1件あたりの時間(min)",
                x=df['task'],
                y=df['time_per_count']
            )
        ]
    )
    fig.update_layout(
        xaxis_title="業務内容",
        yaxis_title="件数(件)/1件あたりの時間(min)",
    )
    st.plotly_chart(fig,key="count_task_chart") 

def time_count_avg(filtered_data,combined_data):
    def _extract_data(df):#時間・件数・1件あたりの時間・平均値
        df = df[['phName','task','count']]
        df = df.groupby(['phName','task']).agg(
            total_count = ('count','sum'),
            record_count = ('task','size')
        ).reset_index()
        df['total_time'] = df['record_count']*15
        df['time_per_count'] = df['total_time'] / df['total_count']
        return df
    df = _extract_data(filtered_data if filtered_data is not None else combined_data)
    #record_countは不要なので削除
    df = df[['phName','task','total_count','total_time','time_per_count']]
    st.dataframe(df,column_config={'phName':'薬剤師名','task':'業務内容','total_count':'総件数','total_time':'総時間(min)','time_per_count':'1件あたりの時間(min)'})    

    #平均値dfを追加
    avg_df = df.groupby('task').agg(
        avg_total_count = ('total_count','mean'),
        avg_total_time = ('total_time','mean'),
        avg_time_per_count = ('time_per_count','mean')
    ).reset_index()
    avg_df = avg_df[['task','avg_total_count','avg_total_time','avg_time_per_count']]
    avg_df = avg_df.rename(columns={
        'avg_total_count':'total_count',
        'avg_total_time':'total_time',
        'avg_time_per_count':'time_per_count'
    })
    #phName列は不要なので削除
    avg_df = avg_df[['task','total_count','total_time','time_per_count']]
    st.markdown("業務別平均値")
    st.dataframe(avg_df,column_config={'task':'業務内容','total_count':'総件数','total_time':'総時間(min)','time_per_count':'1件あたりの時間(min)'})


def collect_all_charts_data(filtered_data, combined_data):
    """
    全てのグラフとデータフレームを収集する関数
    
    Returns:
        list: [{'name': str, 'fig': plotly.Figure, 'df': pd.DataFrame}, ...]
    """
    results = []
    
    PLOTLY_COLORS = [
        '#2B66C2',"#93C7FA"
    ]
    
    # 各関数からデータを抽出（表示はせずにデータのみ取得）
    def get_1on1_data():
        df = filtered_data if filtered_data is not None else combined_data
        df = df[['phName','task']]
        df = df[df['task']=='1on1']
        df = df.groupby('phName').size().reset_index(name='count')
        df['time'] = df['count']*15
        fig = px.bar(data_frame=df, x='phName', y='time', 
                    labels={'phName':'薬剤師名','time':'総時間(min)'},
                    color_discrete_sequence=[PLOTLY_COLORS[0]])
        df = df.rename(columns={'time':'総時間(min)','phName':'薬剤師名','count':'記録回数'})
        return fig, df[["総時間(min)","薬剤師名"]]
    
    def get_nst_data():
        df = filtered_data if filtered_data is not None else combined_data
        df = df[['phName','task']]
        df = df[df['task']=='NST']
        df = df.groupby('phName').size().reset_index(name='count')
        df['time'] = df['count']*15
        fig = px.bar(data_frame=df, x='phName', y='time', 
                    labels={'phName':'薬剤師名','time':'総時間(min)'},color_discrete_sequence=[PLOTLY_COLORS[0]])
        df = df.rename(columns={'time':'総時間(min)','phName':'薬剤師名'})
        return fig, df[["総時間(min)","薬剤師名"]]
    
    def get_tdm_data():
        df = filtered_data if filtered_data is not None else combined_data
        df = df[['phName','task',"count"]]
        df = df[df['task']=='TDM実施']
        df = df.groupby(['phName','task']).agg(
            count_sum =('count','sum'),
            size_count =('task','size')
        ).reset_index()
        df['time'] = df['size_count']*15
        df['time_per_count'] = df['time'] / df['count_sum']
        fig = go.Figure(
            data=[
                go.Bar(name="件数(件)", x=df['phName'], y=df['count_sum'],
                    marker=dict(color=PLOTLY_COLORS[0])),
                go.Bar(name="1件あたりの時間(min)", x=df['phName'], y=df['time_per_count'],
                    marker=dict(color=PLOTLY_COLORS[1]))
            ]
        )
        fig.update_layout(xaxis_title="薬剤師名", yaxis_title="件数(件)/1件あたりの時間(min)")
        df = df.rename(columns={'count_sum':'総件数','time':'総時間(min)','phName':'薬剤師名','time_per_count':'1件あたりの時間(min)'})
        return fig, df[["総件数","総時間(min)","薬剤師名","1件あたりの時間(min)"]]
    
    def get_tpn_data():
        df = filtered_data if filtered_data is not None else combined_data
        df = df[['phName','task',"count"]]
        df = df[df['task']=='TPN評価']
        df = df.groupby(['phName','task']).agg(
            count_sum =('count','sum'),
            size_count =('task','size')
        ).reset_index()
        df['time'] = df['size_count']*15
        df['time_per_count'] = df['time'] / df['count_sum']
        df=df.rename(columns={'count_sum':'総件数','size_count':'記録回数','time':'総時間(min)','time_per_count':'1件あたりの時間(min)','phName':'薬剤師名'})
        return None, df[["総件数","記録回数","総時間(min)","1件あたりの時間(min)"]]  # TPNはグラフがないのでNone
    
    def get_wg_data():
        df = filtered_data if filtered_data is not None else combined_data
        df = df[['phName','task']]
        df = df[df['task']=='WG活動']
        df = df.groupby('phName').size().reset_index(name='count')
        df['time'] = df['count']*15
        fig = px.bar(data_frame=df, x='phName', y='time', 
                    labels={'phName':'薬剤師名','time':'総時間(min)'},
                    color_discrete_sequence=[PLOTLY_COLORS[0]])
        df = df.rename(columns={'time':'総時間(min)','phName':'薬剤師名'})
        return fig, df[["総時間(min)","薬剤師名"]]
    
    def get_confa_data():
        df = filtered_data if filtered_data is not None else combined_data
        df = df[['phName','task']]
        df = df[df['task']=='カンファ・ラウンド']
        df = df.groupby('phName').size().reset_index(name='count')
        df['time'] = df['count']*15
        df['time'] = df['time']/60
        fig = px.bar(data_frame=df, x='phName', y='time', 
                    labels={'phName':'薬剤師名','time':'総時間(hr)'},
                    color_discrete_sequence=[PLOTLY_COLORS[0]])
        df = df.rename(columns={'time':'総時間(hr)','phName':'薬剤師名'})
        return fig, df[["総時間(hr)","薬剤師名"]]
    
    def get_conference_data():
        df = filtered_data if filtered_data is not None else combined_data
        df = df[['phName','task']]
        df = df[df['task']=='カンファレンス']
        df = df.groupby('phName').size().reset_index(name='count')
        df['time'] = df['count']*15
        fig = px.bar(data_frame=df, x='phName', y='time', 
                    labels={'phName':'薬剤師名','time':'総時間(min)'},
                    color_discrete_sequence=[PLOTLY_COLORS[0]])
        df = df.rename(columns={'time':'総時間(min)','phName':'薬剤師名'})
        return fig, df[["総時間(min)","薬剤師名"]]
    
    def get_other_consultation_data():
        df = filtered_data if filtered_data is not None else combined_data
        df = df[['phName','task','count']]
        df = df[df['task']=='その他の職種からの相談']
        df = df.groupby(['phName','task']).agg(
            count_sum =('count','sum'),
            size_count =('task','size')
        ).reset_index()
        df['time'] = df['size_count']*15
        df['time_per_count'] = df['time'] / df['count_sum']
        fig = go.Figure(
            data=[
                go.Bar(name="件数(件)", x=df['phName'], y=df['count_sum'],
                    marker=dict(color=PLOTLY_COLORS[0])),
                go.Bar(name="1件あたりの時間(min)", x=df['phName'], y=df['time_per_count'],
                    marker=dict(color=PLOTLY_COLORS[1]))
            ],
        )
        fig.update_layout(xaxis_title="薬剤師名", yaxis_title="件数(件)/1件あたりの時間(min)")
        df = df.rename(columns={'count_sum':'総件数','time':'総時間(min)','phName':'薬剤師名','time_per_count':'1件あたりの時間(min)'})
        return fig, df[["総件数","総時間(min)","薬剤師名","1件あたりの時間(min)"]]
    
    def get_doctor_consultation_data():
        df = filtered_data if filtered_data is not None else combined_data
        df = df[['phName','task','count']]
        df = df[df['task']=='医師からの相談']
        df = df.groupby(['phName','task']).agg(
            count_sum =('count','sum'),
            size_count =('task','size')
        ).reset_index()
        df['time'] = df['size_count']*15
        df['time_per_count'] = df['time'] / df['count_sum']
        fig = go.Figure(
            data=[
                go.Bar(name="件数(件)", x=df['phName'], y=df['count_sum'],
                    marker=dict(color=PLOTLY_COLORS[0])),
                go.Bar(name="1件あたりの時間(min)", x=df['phName'], y=df['time_per_count'],
                    marker=dict(color=PLOTLY_COLORS[1]))
            ]
        )
        fig.update_layout(xaxis_title="薬剤師名", yaxis_title="件数(件)/1件あたりの時間(min)")
        df = df.rename(columns={'count_sum':'総件数','time':'総時間(min)','phName':'薬剤師名','time_per_count':'1件あたりの時間(min)'})
        return fig, df[["総件数","総時間(min)","薬剤師名","1件あたりの時間(min)"]]
    
    def get_nurse_consultation_data():
        df = filtered_data if filtered_data is not None else combined_data
        df = df[['phName','task','count']]
        df = df[df['task']=='看護師からの相談']
        df = df.groupby(['phName','task']).agg(
            count_sum =('count','sum'),
            size_count =('task','size')
        ).reset_index()
        df['time'] = df['size_count']*15
        df['time_per_count'] = df['time'] / df['count_sum']
        fig = go.Figure(
            data=[
                go.Bar(name="件数(件)", x=df['phName'], y=df['count_sum'],
                    marker=dict(color=PLOTLY_COLORS[0])),
                go.Bar(name="1件あたりの時間(min)", x=df['phName'], y=df['time_per_count'],
                    marker=dict(color=PLOTLY_COLORS[1]))
            ]
        )
        fig.update_layout(xaxis_title="薬剤師名", yaxis_title="件数(件)/1件あたりの時間(min)")
        df = df.rename(columns={'count_sum':'総件数','time':'総時間(min)','phName':'薬剤師名','time_per_count':'1件あたりの時間(min)'})
        return fig, df[["総件数","総時間(min)","薬剤師名","1件あたりの時間(min)"]]
    
    def get_management_time_data():
        df = filtered_data if filtered_data is not None else combined_data
        df = df[['phName','task']]
        df = df[df['task']=="管理業務"]
        df = df.groupby('phName').size().reset_index(name = "task_count")
        df['total_time'] =df['task_count']*15
        df['total_time'] = df['total_time']/60
        fig = px.bar(data_frame=df, x='phName', y='total_time', 
                    labels={'phName':'薬剤師名','total_time':'時間(hr)'},
                    color_discrete_sequence=[PLOTLY_COLORS[0]])
        df =df.rename(columns={'total_time':'時間(hr)','phName':'薬剤師名','task_count':'記録回数'})
        return fig, df[['時間(hr)','薬剤師名']]
    
    def get_adjustment_work_data():
        df = filtered_data if filtered_data is not None else combined_data
        df = df[['phName',"task"]]
        df = df[df['task'] =="業務調整"]
        df = df.groupby('phName').size().reset_index(name = "task_count")
        df['total_time'] = df['task_count']*15
        df['total_time'] = df['total_time']/60
        fig = px.bar(data_frame=df, x='phName', y='total_time', 
                    labels={'phName':'薬剤師名','total_time':'時間(hr)'},
                    color_discrete_sequence=[PLOTLY_COLORS[0]])
        df = df.rename(columns={'total_time':'時間(hr)','phName':'薬剤師名'})
        return fig, df[['時間(hr)','薬剤師名']]
    
    def get_check_medication_data():
        df = filtered_data if filtered_data is not None else combined_data
        df = df[['phName','task','count']]
        df = df[df['task'] =='持参薬を確認']
        df = df.groupby(['phName','task']).agg(
            count_sum =('count','sum'),
            task_count = ('task','size')
        ).reset_index()
        df['time'] = df['task_count']*15
        df['time_per_task'] = df['time'] / df['count_sum']
        fig = go.Figure(
            data=[
                go.Bar(name="件数(件)", x=df['phName'], y=df['count_sum'],
                    marker=dict(color=PLOTLY_COLORS[0])),
                go.Bar(name="1件あたりの時間(min)", x=df['phName'], y=df['time_per_task'],
                    marker=dict(color=PLOTLY_COLORS[1]))
            ]
        )
        fig.update_layout(xaxis_title="薬剤師名", yaxis_title="件数(件)/1件あたりの時間(min)")
        df = df.rename(columns={'count_sum':'総件数','time':'総時間(min)','phName':'薬剤師名','time_per_task':'1件あたりの時間(min)'})
        return fig, df[["総件数","総時間(min)","薬剤師名","1件あたりの時間(min)"]]
    
    def get_recept_agent_modification_data():
        df = filtered_data if filtered_data is not None else combined_data
        df = df[['phName','count','task']]
        df = df[df['task'] =='処方代理修正']
        df = df.groupby(['phName','task']).agg(
            count_sum=('count','sum'),
            task_count=('task','size')
        ).reset_index()
        df['time'] = df['task_count']*15
        df['time_per_task'] = df['time'] / df['count_sum']
        fig = go.Figure(
            data=[
                go.Bar(name="件数(件)", x=df['phName'], y=df['count_sum'],
                    marker=dict(color=PLOTLY_COLORS[0])),
                go.Bar(name="1件あたりの時間(min)", x=df['phName'], y=df['time_per_task'],
                    marker=dict(color=PLOTLY_COLORS[1]))
            ]
        )
        fig.update_layout(xaxis_title="薬剤師名", yaxis_title="件数(件)/1件あたりの時間(min)")
        df = df.rename(columns={'count_sum':'総件数','time':'総時間(min)','phName':'薬剤師名','time_per_task':'1件あたりの時間(min)'})
        return fig, df[["総件数","総時間(min)","薬剤師名","1件あたりの時間(min)"]]
    
    def get_medication_guidance_data():
        df = filtered_data if filtered_data is not None else combined_data
        med_data = df[['phName','count','task']]
        med_data = med_data[med_data['task']=='服薬指導＋指導記録作成']
        med_data = med_data.groupby(['phName','task']).agg(
            count_sum = ('count','sum'),
            time = ('task','size')
        ).reset_index()
        med_data['total_time'] = med_data['time']*15
        med_data['time_per_task'] = med_data['total_time'] / med_data['count_sum']
        fig = go.Figure(
            data=[
                go.Bar(name="件数(件)", x=med_data['phName'], y=med_data['count_sum'],
                    marker=dict(color=PLOTLY_COLORS[0])),
                go.Bar(name="1件あたりの時間(min)", x=med_data['phName'], y=med_data['time_per_task'],
                    marker=dict(color=PLOTLY_COLORS[1]))
            ]
        )
        fig.update_layout(xaxis_title="薬剤師名", yaxis_title="件数(件)/1件あたりの時間(min)")
        med_data = med_data.rename(columns={'count_sum':'総件数','time':'総時間(min)','phName':'薬剤師名','time_per_task':'1件あたりの時間(min)'})
        return fig, med_data[['薬剤師名','総件数','1件あたりの時間(min)']]
    
    def get_clean_preparation_data():
        df = filtered_data if filtered_data is not None else combined_data
        df = df[['phName','task']]
        df = df[df['task']=='無菌調製関連業務']
        df = df.groupby(['phName','task']).size().reset_index(name='count_sum')
        df['time'] = df['count_sum']*15
        fig = px.bar(data_frame=df, x='phName', y='time', 
                    labels={'phName':'薬剤師名','time':'総時間(min)'},
                    color_discrete_sequence=[PLOTLY_COLORS[0]])
        df = df.rename(columns={'count_sum':'総記録回数','time':'総時間(min)','phName':'薬剤師名'})
        return fig, df[["総時間(min)","薬剤師名"]]
    
    def get_drag_set_check_data():
        df = filtered_data if filtered_data is not None else combined_data
        df = df[['phName','task']]
        df = df[df['task']=='薬剤セット・確認']
        df = df.groupby(['phName','task']).size().reset_index(name='count_sum')
        df['time'] = df['count_sum']*15
        fig = px.bar(data_frame=df, x='phName', y='time', 
                    labels={'phName':'薬剤師名','time':'総時間(min)'},
                    color_discrete_sequence=[PLOTLY_COLORS[0]])
        df = df.rename(columns={'count_sum':'総記録回数','time':'総時間(min)','phName':'薬剤師名'})
        return fig, df[["総時間(min)","薬剤師名"]]
    
    def get_research_info_data():
        df = filtered_data if filtered_data is not None else combined_data
        df = df[['phName','task','count']]
        df = df[df['task']=='薬剤使用状況の把握等（情報収集）']
        df = df.groupby(['phName','task']).agg(
            count_sum =('count','sum'),
            size_count =('task','size'),
        ).reset_index()
        df['time'] = df['size_count']*15
        df['time_per_count'] = df['time'] / df['count_sum']
        fig = go.Figure(
            data=[
                go.Bar(name="件数(件)", x=df['phName'], y=df['count_sum'],
                    marker=dict(color=PLOTLY_COLORS[0])),
                go.Bar(name="1件あたりの時間(min)", x=df['phName'], y=df['time_per_count'],
                    marker=dict(color=PLOTLY_COLORS[1]))
            ]
        )
        fig.update_layout(xaxis_title="薬剤師名", yaxis_title="件数(件)/1件あたりの時間(min)")
        df = df.rename(columns={'count_sum':'総件数','size_count':'記録回数','time_per_count':'1件あたりの時間(min)',
                                'time':'総時間(min)','phName':'薬剤師名'})
        return fig, df[["総件数","記録回数","総時間(min)","1件あたりの時間(min)"]]
    
    def get_jokusou_data():
        df = filtered_data if filtered_data is not None else combined_data
        df = df[['phName','task']]
        df = df[df['task']=='褥瘡']
        df = df.groupby(['phName','task']).size().reset_index(name='count_sum')
        df['time'] = df['count_sum']*15
        fig = px.bar(data_frame=df, x='phName', y='time', 
                    labels={'phName':'薬剤師名','time':'総時間(min)'},
                    color_discrete_sequence=[PLOTLY_COLORS[0]])
        df = df.rename(columns={'count_sum':'総記録回数','time':'総時間(min)','phName':'薬剤師名'})
        return fig, df[["総時間(min)","薬剤師名"]]
    
    # 各関数を実行してデータを収集
    data_functions = [
        ('1on1', get_1on1_data),
        ('NST', get_nst_data),
        ('TDM実施', get_tdm_data),
        ('TPN評価', get_tpn_data),
        ('WG活動', get_wg_data),
        ('カンファ・ラウンド', get_confa_data),
        ('カンファレンス', get_conference_data),
        ('その他の職種からの相談', get_other_consultation_data),
        ('医師からの相談', get_doctor_consultation_data),
        ('看護師からの相談', get_nurse_consultation_data),
        ('管理業務', get_management_time_data),
        ('業務調整', get_adjustment_work_data),
        ('持参薬を確認', get_check_medication_data),
        ('処方代理修正', get_recept_agent_modification_data),
        ('服薬指導+記録作成', get_medication_guidance_data),
        ('無菌調製関連業務', get_clean_preparation_data),
        ('薬剤セット確認', get_drag_set_check_data),
        ('薬剤使用状況の把握等', get_research_info_data),
        ('褥瘡', get_jokusou_data),
    ]
    
    for name, func in data_functions:
        try:
            fig, df = func()
            if df is not None and not df.empty:
                results.append({'name': name, 'fig': fig, 'df': df})
        except Exception as e:
            print(f"Error collecting data for {name}: {e}")
    
    return results