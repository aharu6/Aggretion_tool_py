import streamlit as st
from view.TASK_COLOR_MAP import TASK_COLOR_MAP
import plotly.express as px
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
    st.bar_chart(data=df,x='phName',y='time',y_label='総時間(分)',x_label='薬剤師名')

def Calculate_NST(filtered_data,combined_data):
    def _extract_data(df):
        df=df[['phName','task']]
        df=df[df['task']=='NST']
        df=df.groupby('phName').size().reset_index(name='count')
        df['time'] = df['count']*15
        return df
    df=_extract_data(filtered_data if filtered_data is not None else combined_data)
    st.bar_chart(data=df,x='phName',y='time',y_label='総時間(分)',x_label='薬剤師名')

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
    st.dataframe(df)
        

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
    st.dataframe(df)

def Calculate_WG(filtered_data,combined_data):
    def _extract_data(df):
        df=df[['phName','task']]
        df=df[df['task']=='WG活動']
        df=df.groupby('phName').size().reset_index(name='count')
        df['time'] = df['count']*15
        return df
    df=_extract_data(filtered_data if filtered_data is not None else combined_data)
    st.bar_chart(data=df,x='phName',y='time',y_label='総時間(分)',x_label='薬剤師名')


def Calculate_confa(filtered_data,combined_data):
    def _extract_data(df):
        df=df[['phName','task']]
        df=df[df['task']=='カンファ・ラウンド']
        df=df.groupby('phName').size().reset_index(name='count')
        df['time'] = df['count']*15
        return df
    df=_extract_data(filtered_data if filtered_data is not None else combined_data)
    st.bar_chart(data=df,x='phName',y='time',y_label='総時間(分)',x_label='薬剤師名')

def Calculate_conference(filtered_data,combined_data):
    def _extract_data(df):
        df=df[['phName','task']]
        df=df[df['task']=='カンファレンス']
        df=df.groupby('phName').size().reset_index(name='count')
        df['time'] = df['count']*15
        return df
    df=_extract_data(filtered_data if filtered_data is not None else combined_data)
    st.bar_chart(data=df,x='phName',y='time',y_label='総時間(分)',x_label='薬剤師名')


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

    #TODO:１けんあたりの時間は必要か、データフレームで残すか、グラフを切り替えるか
    df=_extract_data(filtered_data if filtered_data is not None else combined_data)
    st.bar_chart(data=df,x='phName',y='time',y_label='総時間(分)',x_label='薬剤師名')

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
    st.dataframe(df,column_config={'phName':'薬剤師名','count_sum':'総件数','size_count':'記録回数','time':'総時間(分)','time_per_count':'1件あたりの時間(分)'})

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
    st.dataframe(df,column_config={'phName':'薬剤師名','count_sum':'総件数','size_count':'記録回数','time':'総時間(分)','time_per_count':'1件あたりの時間(分)'})


def time_per_task_chart(filtered_data,combined_data):
    def _extract_data(df):
        task_counts = df.groupby('task').size().reset_index(name='time')
        task_counts['time'] = task_counts['time']*15
        return task_counts
    
    task_counts=_extract_data(filtered_data if filtered_data is not None else combined_data)
    st.bar_chart(data=task_counts,x="task",y="time")

def counts_per_task_chart(filtered_data,combined_data):
    def _extract_data(df):
        task_counts = df[['task','count']]
        task_counts = task_counts.groupby('task').sum().reset_index()
        return task_counts
    
    task_counts=_extract_data(filtered_data if filtered_data is not None else combined_data)
    st.bar_chart(data=task_counts,x="task",y="count")
    
import ast
def time_per_locate_chart(filtered_data,combined_data):
    def _extract_locate_data(df):
        locate_data = df[['locate']].groupby('locate').size().reset_index(name='time')
        locate_data['time'] = locate_data['time']*15
        locate_data['locate']= locate_data['locate'].apply(ast.literal_eval)
        locate_data['locate'] = locate_data['locate'].apply(lambda x: x[0] if len(x)>0 else 'Unknown')
        return locate_data
    
    df=_extract_locate_data(filtered_data if filtered_data is not None else combined_data)
    st.bar_chart(data=df,x="locate",y="time")

def Medication_Guidance_Record_Creation(filtered_data,combined_data):
    def _extract_data(df):
        med_data = df[['phName','count','task']]
        med_data = med_data[med_data['task']=='服薬指導＋指導記録作成']
        med_data['time'] = 15
        med_data = med_data.groupby('phName',as_index =False).sum()
        med_data['time_per_task'] = med_data['time'] / med_data['count']
        return med_data
    med_data=_extract_data(filtered_data if filtered_data is not None else combined_data)
    st.bar_chart(med_data,y ='time_per_task',x = 'phName',x_label='薬剤師名',y_label='1件あたりの時間（分）')


def total_time_per_task(filtered_data,combined_data):
    def _extract_data(df):
        df = df[['task','count']]
        df=df.groupby('task').size().reset_index(name='times')
        df['times'] = df['times']*15
        df['times'] =df['times']/60
        return df
    
    df=_extract_data(filtered_data if filtered_data is not None else combined_data)
    try:
        st.bar_chart(df,y='times',x='task',y_label='総時間(hr)',x_label='業務名')
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

def drag_set_check(filtered_data,combined_data):
    def _extract_data(df):
        df = df[['phName','task']]
        df = df[df['task']=='薬剤セット・確認']
        df = df.groupby(['phName','task']).size().reset_index(name='count_sum')
        df['time'] = df['count_sum']*15
        return df
    df = _extract_data(filtered_data if filtered_data is not None else combined_data)
    st.bar_chart(data=df,x='phName',y='time',x_label='薬剤師名',y_label='総時間(分)')

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
                name="1件あたりの時間(分)",
                x=df['phName'],
                y=df['time_per_count'],
            )
        ]
    )
    fig.update_layout(
        xaxis_title="薬剤師名",
        yaxis_title="件数(件)/1件あたりの時間(分)",
    )
    st.plotly_chart(fig)

    df['time_per_counte'] = (df['size_count']*15) / df['count_sum']
    st.dataframe(df,column_config={'phName':'薬剤師名','count_sum':'総件数','size_count':'記録回数','time_per_counte':'1件あたりの時間(分)'})

def Jokusou_chart(filtered_data,combined_data):
    def _extract_data(df):
        df = df[['phName','task']]
        df = df[df['task']=='褥瘡']
        df = df.groupby(['phName','task']).size().reset_index(name='count_sum')
        df['time'] = df['count_sum']*15
        return df

    df = _extract_data(filtered_data if filtered_data is not None else combined_data)
    st.bar_chart(data=df,x='phName',y='time',x_label='薬剤師名',y_label='総時間(分)')
        

