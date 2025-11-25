import streamlit as st
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
    if filtered_data is not None:
        #服薬指導＋記録作成のみの業務内容で、個人ごとに集計、coutsの合計から、１けんあたりに要した時間を算出
        med_data = filtered_data[['phName','count','task']]
        med_data = med_data[med_data['task']=='服薬指導＋指導記録作成']
        med_data['time'] = 15
        med_data = med_data.groupby('phName',as_index =False).sum()
        med_data['time_per_task'] = med_data['count'] / med_data['time']
        st.bar_chart(med_data,y ='time_per_task',x = 'phName',x_label='薬剤師名',y_label='1件あたりの時間（分）')

    else:
        med_data = combined_data[['phName','count','task']]
        med_data = med_data[med_data['task']=='服薬指導＋指導記録作成']
        med_data['time'] = 15
        med_data = med_data.groupby('phName',as_index =False).sum()
        med_data['time_per_task'] = med_data['count'] / med_data['time']
        st.bar_chart(med_data,y ='time_per_task',x = 'phName',x_label='薬剤師名',y_label='1件あたりの時間（分）')