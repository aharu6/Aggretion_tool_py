import streamlit as st

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
        st.bar_chart(data=task_counts,x="task",y="time")        
    else:
        st.bar_chart(data=task_counts,x="task",y="time")

def counts_per_task_chart(filtered_data,combined_data):
    if filtered_data is not None:
        task_counts = filtered_data.groupby('task')
        task_counts = task_counts['count'].sum().reset_index(name='count_sum')
        st.bar_chart(data=task_counts,x="task",y="count_sum")
    else:
        task_counts = combined_data.groupby('task')
        task_counts = task_counts['count'].sum().reset_index(name='count_sum')
        st.bar_chart(data=task_counts,x="task",y="count_sum")

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
    pass