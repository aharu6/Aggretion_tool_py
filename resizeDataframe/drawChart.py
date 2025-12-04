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
    if filtered_data is not None:
            task_counts = filtered_data.groupby('task').size().reset_index(name='time')
            task_counts['time'] = task_counts['time']*15
    else:
        task_counts = combined_data.groupby('task').size().reset_index(name='time')
        task_counts['time'] = task_counts['time']*15
    if filtered_data is not None:
        bar_chart = px.bar(data_frame=task_counts,x="task",y="time",color='task',
            color_discrete_map=TASK_COLOR_MAP)        
        st.plotly_chart(bar_chart)
    else:
        bar_chart = px.bar(data_frame=task_counts,x="task",y="time",color='task',
            color_discrete_map=TASK_COLOR_MAP)      
        st.plotly_chart(bar_chart)

def counts_per_task_chart(filtered_data,combined_data):
    if filtered_data is not None:
        task_counts = filtered_data.groupby('task')
        task_counts = task_counts['count'].sum().reset_index(name='count_sum')
        bar_chart = px.bar(data_frame=task_counts,x="task",y="count_sum",color='task',
            color_discrete_map=TASK_COLOR_MAP)
        st.plotly_chart(bar_chart)
    else:
        task_counts = combined_data.groupby('task')
        task_counts = task_counts['count'].sum().reset_index(name='count_sum')
        bar_chart = px.bar(data_frame=task_counts,x="task",y="count_sum",color='task',
            color_discrete_map=TASK_COLOR_MAP)
        st.plotly_chart(bar_chart)
import ast
def time_per_locate_chart(filtered_data,combined_data):
    if filtered_data is not None:
        time_per_locate = filtered_data[['locate']].groupby('locate').size().reset_index(name='time')
        time_per_locate['time'] = time_per_locate['time']*15
        time_per_locate['locate']= time_per_locate['locate'].apply(ast.literal_eval)
        time_per_locate = time_per_locate[time_per_locate['locate'].apply(lambda x:len(x) <=1)]
        st.bar_chart(data=time_per_locate,x="locate",y="time")
    else:
        time_per_locate = combined_data[['locate']].groupby('locate').size().reset_index(name='time')
        time_per_locate['time'] = time_per_locate['time']*15
        #locateのデータが複数ある場合には削除 ["",""]リストのながさが２以上の場合
        time_per_locate['locate'] = time_per_locate['locate'].apply(ast.literal_eval)
        time_per_locate = time_per_locate[time_per_locate['locate'].apply(lambda x:len(x) <=1)]
        st.bar_chart(data=time_per_locate,x="locate",y="time")

import plotly.express as px
def time_per_locate_piechart(filtered_data,combined_data):
    data = _get_data(filtered_data,combined_data)
    locate_data = data[['locate','task']]
    #locateごと。taskごとに集計する
    locate_data = locate_data.groupby(['locate','task']).size().reset_index(name='time')
    locate_data['locate'] = locate_data['locate'].apply(ast.literal_eval)
    locate_data = locate_data[locate_data['locate'].apply(lambda x:len(x) <=1)]
    locate_data['locate'] = locate_data['locate'].apply(lambda x:x[0] if len(x)==1 else '不明')
    #llocateごとにループを作成、時間を合計、taskごとにかかった割合を抽出し、円グラフを作成する
    for locate in locate_data['locate'].unique():
        locate_subset = locate_data[locate_data['locate'] == locate]
        total_time = locate_subset['time'].sum()
        locate_subset['percentage'] = locate_subset['time'] / total_time * 100
        fig = px.pie(data_frame=locate_subset, values="percentage",names = 'task',
                    title=f"{locate}の業務割合",labels={'percentage':'割合 (%)','task':'業務内容'},
                    color='task',
                    color_discrete_map=TASK_COLOR_MAP)
        st.plotly_chart(fig)

    st.dataframe(locate_data)

def self_barchart(filtered_data,combined_data):
    data = _get_data(filtered_data,combined_data)
    self_data = data[['phName','task']]
    self_data = self_data.groupby(['phName','task']).size().reset_index(name='time')
    total_by_phName = self_data.groupby('phName')['time'].sum().reset_index(name='total_time')
    self_data = self_data.merge(total_by_phName,on='phName')
    self_data['task_per_time'] = self_data['time'] /self_data['total_time'] *100
    bar_chart = px.bar(data_frame=self_data,orientation='h',x = "task_per_time",y="phName",color = 'task',
        color_discrete_map=TASK_COLOR_MAP)
    st.plotly_chart(bar_chart)

def Medication_Guidance_Record_Creation(filtered_data,combined_data):
    data = _get_data(filtered_data,combined_data)
    med_data = _filter_and_aggregate_task(data,'服薬指導＋指導記録作成')
    med_data["task_per_time"] = med_data['time'] / med_data['count']
    st.bar_chart(med_data,y ='task_per_time',x = 'phName',x_label='薬剤師名',y_label='1件あたりの時間（分）')


def Calculate_1on1(filtered_data,combined_data):
    data = _get_data(filtered_data,combined_data)
    one_on_one_data = _filter_and_aggregate_task(data,'1on1')
    st.bar_chart(one_on_one_data,y = 'time',x ='phName',x_label='薬剤師名',y_label='1on1に要した時間（分）')

def Calculate_NST(filtered_data,combined_data):
    data = _get_data(filtered_data,combined_data)
    nst_data = _filter_and_aggregate_task(data,'NST')
    st.bar_chart(nst_data,y = 'time',x ='phName',x_label='薬剤師名',y_label='NSTに要した時間（分）')

def Calculate_TDM(filtered_data,combined_data):
    data = _get_data(filtered_data,combined_data)
    tdm_data = _filter_and_aggregate_task(data,'TDM実施')
    tdm_data["task_per_time"] = tdm_data['time'] / tdm_data['count']
    st.dataframe(tdm_data)

def Calculate_TPN(filtered_data,combined_data):
    data = _get_data(filtered_data,combined_data)
    tpn_data = _filter_and_aggregate_task(data,'TPN評価')
    tpn_data["task_per_time"] = tpn_data['time'] / tpn_data['count']
    st.dataframe(tpn_data)

def Calculate_WG(filtered_data,combined_data):
    data = _get_data(filtered_data,combined_data)
    wg_data = _filter_and_aggregate_task(data,'WG活動')
    st.bar_chart(wg_data,y = 'time',x ='phName',x_label='薬剤師名',y_label='WG活動に要した時間（分）')

def Calculate_confa(filtered_data,combined_data):
    data = _get_data(filtered_data,combined_data)
    confa_data = _filter_and_aggregate_task(data,'カンファ・ラウンド')
    st.bar_chart(confa_data,y = 'time',x ='phName',x_label='薬剤師名',y_label='カンファ・ラウンドに要した時間（分）')

def Calculate_conference(filtered_data,combined_data):
    data = _get_data(filtered_data,combined_data)
    conference_data = _filter_and_aggregate_task(data,'カンファレンス')
    st.bar_chart(conference_data,y = 'time',x ='phName',x_label='薬剤師名',y_label='カンファレンスに要した時間（分）')

def Calculate_other_consultation(filtered_data,combined_data):
    data = _get_data(filtered_data,combined_data)
    other_consultation_data = _filter_and_aggregate_task(data,'その他の職種からの相談')
    other_consultation_data["task_per_time"] = other_consultation_data['time'] / other_consultation_data['count']
    st.dataframe(other_consultation_data)

def Calculate_doctor_consultation(filtered_data,combined_data):
    data = _get_data(filtered_data,combined_data)
    doctor_consultation_data = _filter_and_aggregate_task(data,'医師からの相談')
    doctor_consultation_data["task_per_time"] = doctor_consultation_data['time'] / doctor_consultation_data['count']
    st.dataframe(doctor_consultation_data)

def Calculate_nurse_consultation(filtered_data,combined_data):
    data = _get_data(filtered_data,combined_data)
    nurse_consultation_data = _filter_and_aggregate_task(data,'看護師からの相談')
    nurse_consultation_data["task_per_time"] = nurse_consultation_data['time'] / nurse_consultation_data['count']
    st.dataframe(nurse_consultation_data)
    