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
    task_data = task_data.groupby('phName',as_index =False).sum()
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
    st.bar_chart(med_data,y ='count',x = 'phName',x_label='薬剤師名',y_label='1件あたりの時間（分）')


def Calculate_1on1(filtered_data,combined_data):
    
    if filtered_data is not None:
        one_on_one_data = filtered_data[['phName','count','task']]
        one_on_one_data = one_on_one_data[one_on_one_data['task']=='1on1']
        one_on_one_data['time'] = 15
        one_on_one_data = one_on_one_data.groupby('phName',as_index =False).sum()
        st.bar_chart(one_on_one_data,y = 'time',x ='phName',x_label='薬剤師名',y_label='1on1に要した時間（分）')
    else:
        one_on_one_data = combined_data[['phName','count','task']]
        one_on_one_data = one_on_one_data[one_on_one_data['task']=='1on1']
        one_on_one_data['time'] = 15
        one_on_one_data = one_on_one_data.groupby('phName',as_index =False).sum()
        st.bar_chart(one_on_one_data,y = 'time',x ='phName',x_label='薬剤師名',y_label='1on1に要した時間（分）')

def Calculate_NST(filtered_data,combined_data):
    if filtered_data is not None:
        nst_data = filtered_data[['phName','count','task']]
        nst_data = nst_data[nst_data['task']=='NST']
        nst_data['time'] = 15
        nst_data = nst_data.groupby('phName',as_index =False).sum()
        st.bar_chart(nst_data,y = 'time',x ='phName',x_label='薬剤師名',y_label='NSTに要した時間（分）')
    else:
        nst_data = combined_data[['phName','count','task']]
        nst_data = nst_data[nst_data['task']=='NST']
        nst_data['time'] = 15
        nst_data = nst_data.groupby('phName',as_index =False).sum()
        st.bar_chart(nst_data,y = 'time',x ='phName',x_label='薬剤師名',y_label='NSTに要した時間（分）')

def Calculate_TDM(filtered_data,combined_data):
    if filtered_data is not None:
        tdm_data = filtered_data[['phName','count','task']]
        tdm_data = tdm_data[tdm_data['task']=='TDM実施']
        tdm_data['time'] = 15
        tdm_data = tdm_data.groupby('phName',as_index =False).sum()
        tdm_data["task_per_time"] = tdm_data['time'] / tdm_data['count']
        st.dataframe(tdm_data)
    else:
        tdm_data = combined_data[['phName','count','task']]
        tdm_data = tdm_data[tdm_data['task']=='TDM実施']
        tdm_data['time'] = 15
        tdm_data = tdm_data.groupby('phName',as_index =False).sum()
        tdm_data["task_per_time"] = tdm_data['time'] / tdm_data['count']
        st.dataframe(tdm_data)

def Calculate_TPN(filtered_data,combined_data):
    if filtered_data is not None:
        tpn_data = filtered_data[['phName','count','task']]
        tpn_data = tpn_data[tpn_data['task']=='TPN評価']
        tpn_data['time'] = 15
        tpn_data = tpn_data.groupby('phName',as_index =False).sum()
        tpn_data["task_per_time"] = tpn_data['time'] / tpn_data['count'] 
        st.dataframe(tpn_data)
    else:
        tpn_data = combined_data[['phName','count','task']]
        tpn_data = tpn_data[tpn_data['task']=='TPN評価']
        tpn_data['time'] = 15
        tpn_data = tpn_data.groupby('phName',as_index =False).sum()
        tpn_data["task_per_time"] = tpn_data['time'] / tpn_data['count'] 
        st.dataframe(tpn_data)

def Calculate_WG(filtered_data,combined_data):
    if filtered_data is not None:
        wg_data = filtered_data[['phName','count','task']]
        wg_data = wg_data[wg_data['task']=='WG活動']
        wg_data['time'] = 15
        wg_data = wg_data.groupby('phName',as_index =False).sum()
        st.bar_chart(wg_data,y = 'time',x ='phName',x_label='薬剤師名',y_label='WG活動に要した時間（分）')
    else:
        wg_data = combined_data[['phName','count','task']]
        wg_data = wg_data[wg_data['task']=='WG活動']
        wg_data['time'] = 15
        wg_data = wg_data.groupby('phName',as_index =False).sum()
        st.bar_chart(wg_data,y = 'time',x ='phName',x_label='薬剤師名',y_label='WG活動に要した時間（分）')

def Calculate_confa(filtered_data,combined_data):
    if filtered_data is not None:
        confa_data = filtered_data[['phName','count','task']]
        confa_data = confa_data[confa_data['task']=='カンファ・ラウンド']
        confa_data['time'] = 15
        confa_data = confa_data.groupby('phName',as_index =False).sum()
        st.bar_chart(confa_data,y = 'time',x ='phName',x_label='薬剤師名',y_label='カンファ・ラウンドに要した時間（分）')
    else:
        confa_data = combined_data[['phName','count','task']]
        confa_data = confa_data[confa_data['task']=='カンファ・ラウンド']
        confa_data['time'] = 15
        confa_data = confa_data.groupby('phName',as_index =False).sum()
        st.bar_chart(confa_data,y = 'time',x ='phName',x_label='薬剤師名',y_label='カンファ・ラウンドに要した時間（分）')

def Calculate_conference(filtered_data,combined_data):
    if filtered_data is not None:
        conference_data = filtered_data[['phName','count','task']]
        conference_data = conference_data[conference_data['task']=='カンファレンス']
        conference_data['time'] = 15
        conference_data = conference_data.groupby('phName',as_index =False).sum()
        st.bar_chart(conference_data,y = 'time',x ='phName',x_label='薬剤師名',y_label='カンファレンスに要した時間（分）')
    else:
        conference_data = combined_data[['phName','count','task']]
        conference_data = conference_data[conference_data['task']=='カンファレンス']
        conference_data['time'] = 15
        conference_data = conference_data.groupby('phName',as_index =False).sum()
        st.bar_chart(conference_data,y = 'time',x ='phName',x_label='薬剤師名',y_label='カンファレンスに要した時間（分）')


def Calculate_other_consultation(filtered_data,combined_data):
    if filtered_data is not None:
        other_consultation_data = filtered_data[['phName','count','task']]
        other_consultation_data = other_consultation_data[other_consultation_data['task']=='その他の職種からの相談']
        other_consultation_data['time'] = 15
        other_consultation_data = other_consultation_data.groupby('phName',as_index =False).sum()
        st.dataframe(other_consultation_data)
    else:
        other_consultation_data = combined_data[['phName','count','task']]
        other_consultation_data = other_consultation_data[other_consultation_data['task']=='その他の職種からの相談']
        other_consultation_data['time'] = 15
        other_consultation_data = other_consultation_data.groupby('phName',as_index =False).sum()
        st.dataframe(other_consultation_data)

def Calculate_doctor_consultation(filtered_data,combined_data):
    pass