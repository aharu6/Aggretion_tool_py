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