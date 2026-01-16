import pandas as pd
import plotly.express as px
import streamlit as st
from view.TASK_COLOR_MAP import TASK_COLOR_MAP

"""描画関数"""

"""--病棟毎の集計--"""
def create_componentChart_location(filtered_data,combined_data):
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
    except Exception as e:
        st.warning(f"チャートの作成中にエラーが発生しました: {e}")

    return chart_list


def componentChart_location(filtered_data,combined_data):
    chart_list = create_componentChart_location(filtered_data, combined_data)
    try:
        for locate,fig in chart_list:
            st.markdown(f"### 場所: {locate}")
            st.plotly_chart(fig)
    except Exception as e:
        st.warning(f"チャートの表示中にエラーが発生しました: {e}")

    #TODO:データが存在しない場合はst.infoで通知

"""--時間の合計--"""
import ast

def create_fig_time_per_location(filtered_data, combined_data, colormap=None):
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
        labels={'locate':'病棟','time':'総時間(hr)'},
        color_discrete_sequence=colormap if colormap else None,
    )
    fig.update_layout(
        xaxis_title="病棟",
        yaxis_title="総時間(hr)",
    )
    return fig,df

def time_per_locate_chart(filtered_data,combined_data):
    fig,df = create_fig_time_per_location(filtered_data, combined_data,colormap=None)
    st.plotly_chart(fig,key="time_per_locate_chart")


"""--記録された回数と総時間--"""
def create_fig_task_per_location(filtered_data, combined_data):
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
        hover_data={'task':True,'time':True,'locate':True},
    )
    fig.update_layout(
        xaxis_title="病棟",
        yaxis_title="総時間(hr)",
        legend = dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            font=dict(size=10)
        ),
        margin=dict(r=150)
    )
    return fig,df

def task_per_location(filtered_data,combined_data):
    fig, df = create_fig_task_per_location(filtered_data, combined_data)    
    st.plotly_chart(fig,key="task_per_location_chart")


"""収集関数"""

def collect_location_charts_data(filtered_data,combined_data):
    """病棟別分析のグラフとデータフレームを収集する"""
    
    results = []
    
    PLOTLY_COLORS = [ '#2B66C2',"#93C7FA"]
    
    """st.subheader("病棟ごとの集計")
            componentChart_location(filtered_data,combined_data)
            st.markdown("時間の合計")#locateごとに作成する
            time_per_locate_chart(filtered_data,combined_data)
            st.markdown("記録された業務内容と総時間")
            task_per_location(filtered_data,combined_data)   
    """
    def get_componentChart_location():
        chart_list = create_componentChart_location(filtered_data, combined_data)
        return chart_list, None  # データフレームは不要
    
    def get_time_per_locate_chart():
        fig,df = create_fig_time_per_location(filtered_data, combined_data,colormap=PLOTLY_COLORS)
        return fig,df
    
    def get_task_per_location():
        fig ,df = create_fig_task_per_location(filtered_data, combined_data)
        df = df.rename(columns={'locate':'病棟','task':'業務内容','time':'総時間(hr)'})
        return fig,df
    
    
    list_chart_functions = [
        ('病棟毎の集計',get_componentChart_location),
    ]
    data_functions = [
        ('時間の合計',get_time_per_locate_chart),
        ('記録された業務内容と総時間',get_task_per_location),
    ]
    for name,func in list_chart_functions:
        try:
            chart_list ,_ = func()
            for locate,fig in chart_list:
                results.append({'name': f"{name}_{locate}", 'fig': fig, 'df': None})
        except Exception as e:
            st.warning(f"{name}のチャート作成中にエラーが発生しました: {e}")
            
    for name,func in data_functions:
        try:
            fig,df = func()
            if df is not None and not df.empty:
                results.append({'name': name, 'fig': fig, 'df': df})
        except Exception as e:
            st.warning(f"{name}のデータ収集中にエラーが発生しました: {e}")

    return results
