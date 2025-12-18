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
        task_counts = task_counts.groupby('task').sum().reset_index(name='count_sum')
        return task_counts
    
    task_counts=_extract_data(filtered_data if filtered_data is not None else combined_data)
    st.bar_chart(data=task_counts,x="task",y="count_sum")
    
import ast
def time_per_locate_chart(filtered_data,combined_data):
    def _extract_locate_data(df):
        locate_data = df[['locate']].groupby('locate').size().reset_index(name='time')
        locate_data['time'] = locate_data['time']*15
        locate_data['locate']= locate_data['locate'].apply(ast.literal_eval)
        locate_data['locate'] = locate_data['locate'].apply(lambda x: x[0] if len(x)>1 else x[0])
        return locate_data
    
    df=_extract_locate_data(filtered_data if filtered_data is not None else combined_data)
    st.bar_chart(data=df,x="locate",y="time")

def Medication_Guidance_Record_Creation(filtered_data,combined_data):
    if filtered_data is not None:
        #服薬指導＋記録作成のみの業務内容で、個人ごとに集計、coutsの合計から、１けんあたりに要した時間を算出
        med_data = filtered_data[['phName','count','task']]
        med_data = med_data[med_data['task']=='服薬指導＋指導記録作成']
        med_data['time'] = 15
        med_data = med_data.groupby('phName',as_index =False).sum()
        med_data['time_per_task'] = med_data['count'] / med_data['time']
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
        df['locate'] = df['locate'].apply(lambda x: x[0] if len(x)>1 else x[0])
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

