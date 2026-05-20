import streamlit as st
from view.TASK_COLOR_MAP import TASK_COLOR_MAP
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import ast
def _get_data(filtered_data,combined_data):
    return filtered_data if filtered_data is not None else combined_data
    
def _calculate_time_from_count(df,time_column = "count"):
    df['time'] = df[time_column] * 15
    return df

def _calculate_time(count,to_hours = False):
    time_min = count * 15
    return time_min / 60 if to_hours else time_min


class ChartDataExtractor:
    def __init__(self,filtered_data,combined_data):
        self.df=_get_data(filtered_data,combined_data)
        
    def extract_task_data(self,task_name,to_hours = False):
        df = self.df[['phName','task']].copy()
        df = df[df['task'] ==task_name]
        df = df.groupby('phName').size().reset_index(name='count')
        time_label = 'time_hr' if to_hours else 'time_min'
        df[time_label] = _calculate_time(df['count'],to_hours)
        return df
    
    def _create_count_chart_data(self,task_name=False,colors=False):
        """件数付き集計のチャートデータを作成"""
        df = self.df[['phName','task','count']].copy()
        if task_name:
            df = df[df['task'] ==task_name]
        df = df.groupby(['phName','task']).agg(
            count_sum = ('count','sum'),
            size_count = ('task','size')
        ).reset_index()
        df['time'] = df['size_count']*15
        df['time_per_count'] = df['time'] / df['count_sum']
        
        fig = go.Figure(
            data=[
                go.Bar(name="件数(件)",x=df['phName'],y=df['count_sum'],marker_color=colors[0] if colors else None),
                go.Bar(name="1件あたりの時間(min)",x=df['phName'],y=df['time_per_count'],marker_color=colors[1] if colors else None)
            ]
        )
        fig.update_layout(
            xaxis_title="薬剤師名",
            yaxis_title="件数(件)/1件あたりの時間(min)",
        )
        """df['phName':薬剤師名,'count_sum','time','time_per_count']"""
        return fig,df
    

"""--各タスクの合計時間--"""
def create_total_time_per_task(filtered_data,combined_data):
    def _extract_data(df):
        df = df[['task','count']]
        df=df.groupby('task').size().reset_index(name='times')
        df['times'] = df['times']*15
        df['times'] =df['times']/60
        return df
    
    df =_extract_data(filtered_data if filtered_data is not None else combined_data)
    fig = px.bar(data_frame=df,x='task',y='times',labels={'task':'業務名','times':'総時間(hr)'})
    return fig,df

def total_time_per_task(filtered_data,combined_data):
    fig,df = create_total_time_per_task(filtered_data,combined_data)
    st.plotly_chart(fig,key="total_time_per_task_chart")
    
"""---業務内容ごとの件数と1件あたりの時間---"""
def count_task(filtered_data,combined_data):
    fig,df = ChartDataExtractor(filtered_data=filtered_data,combined_data=combined_data)._create_count_chart_data(
        task_name=False,colors=False
    )
    st.plotly_chart(fig,key="count_task_chart") 
    
"""--時間帯ごとに業務が記録された回数--"""
def create_task_heatmap(filtered_data,combined_data):
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
    return fig,df

def task_heatmap(filtered_data,combined_data):
    fig,df = create_task_heatmap(filtered_data,combined_data)
    st.plotly_chart(fig,key="task_heatmap_chart")

"""--その他コメント--"""
def create_comment_data(filtered_data,combined_data):
    df = _get_data(filtered_data, combined_data)
    df = df[['phName','comment','time','locate','date']]
    df = df[df['comment'].notnull() & (df['comment'] !='')]
    df['locate'] = df['locate'].apply(ast.literal_eval)
    df['locate'] = df['locate'].apply(lambda x: x[0] if len(x)>0 else 'Unknown')
    return df

def comment_data(filtered_data,combined_data):
    df = create_comment_data(filtered_data,combined_data)
    st.dataframe(df,column_config={'phName':'薬剤師名','comment':'コメント','time':'時間','locate':'病棟','date':'日付'})

"""--個人ごとの集計 ・業務割合--"""
def create_self_task_ratio(filtered_data,combined_data):
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
    return fig,df

def self_task_ratio(filtered_data,combined_data):
    """個人毎の業務割合チャート"""
    fig,df = create_self_task_ratio(filtered_data,combined_data)
    st.plotly_chart(fig,key='self_task_ratio_chart')
    
"""--個人ごとの集計 ・時間・件数・1件あたりの時間--"""
def create_time_count_avg(filtered_data,combined_data):
    fig,df  = ChartDataExtractor(filtered_data=filtered_data,combined_data=combined_data)._create_count_chart_data(
        task_name=False,colors=False
    )
    #record_countは不要なので削除
    df = df[['phName','task','count_sum','time','time_per_count']]
    
    #平均値dfを追加
    avg_df = df.groupby('task').agg(
        avg_total_count = ('count_sum','mean'),
        avg_total_time = ('time','mean'),
        avg_time_per_count = ('time_per_count','mean')
    ).reset_index()
    avg_df = avg_df[['task','avg_total_count','avg_total_time','avg_time_per_count']]
    avg_df = avg_df.rename(columns={
        'avg_total_count':'count_sum',
        'avg_total_time':'time',
        'avg_time_per_count':'time_per_count'
    })
    #phName列は不要なので削除
    avg_df = avg_df[['task','count_sum','time','time_per_count']]
    
    return df,avg_df

def time_count_avg(filtered_data,combined_data):
    df,avg_df = create_time_count_avg(filtered_data,combined_data)
    if (df['time_per_count'] == float('inf')).any():
        st.info("1件あたりの時間が算出できないデータがあります。件数が0の可能性があります。")
    st.dataframe(df,column_config={'phName':'薬剤師名','task':'業務内容','count_sum':'総件数','time':'総時間(min)','time_per_count':'1件あたりの時間(min)'})    

    st.markdown("業務別平均値")
    if (avg_df['time_per_count'] == float('inf')).any():
        st.info("1件あたりの時間が算出できないデータがあります。件数が0の可能性があります。")
    st.dataframe(avg_df,column_config={'task':'業務内容','count_sum':'総件数','time':'総時間(min)','time_per_count':'1件あたりの時間(min)'})


def collect_about_chart(filtered_data, combined_data):
    results = []
    PLOTLY_COLORS = ['#2B66C2',"#93C7FA"]
    """_summary_

            st.subheader("各タスクの合計時間")
            total_time_per_task(filtered_data,combined_data)
            st.markdown("業務内容ごとの件数と1件あたりの時間")
            count_task(filtered_data,combined_data)
            st.subheader("時間帯ごとに業務が記録された回数")
            task_heatmap(filtered_data,combined_data)
            st.subheader("その他コメント")
            comment_data(filtered_data,combined_data)
            st.subheader("個人ごとの集計")
            st.markdown("業務割合")
            self_task_ratio(filtered_data,combined_data)
            st.markdown("時間・件数・1件あたりの時間")
            time_count_avg(filtered_data,combined_data)
    """
    def get_total_time_per_task():
        fig,df = create_total_time_per_task(filtered_data,combined_data)
        return fig,df
    
    def get_count_task():
        fig,df = ChartDataExtractor(filtered_data=filtered_data,combined_data=combined_data)._create_count_chart_data(
        task_name=False,colors=False
    )
        return fig,df
    
    def get_task_heatmap():
        fig,df = create_task_heatmap(filtered_data,combined_data)
        return fig,df
    
    def get_comment_data():
        df = create_comment_data(filtered_data,combined_data)
        return None,df  # グラフは不要なのでNoneを返す
    
    def get_self_task_ratio():
        fig,df = create_self_task_ratio(filtered_data,combined_data)
        return fig,df
    
    def get_time_self_count():
        df,avg_df = create_time_count_avg(filtered_data,combined_data)
        return None,df  # グラフは不要なのでNoneを返す
    
    def get_time_count_avg():
        df,avg_df = create_time_count_avg(filtered_data,combined_data)
        return None,avg_df  # グラフは不要なのでNoneを返す
    
    data_functions = [
        ('各タスクの合計時間', get_total_time_per_task),
        ('業務内容ごとの件数と1件あたりの時間', get_count_task),
        ('時間帯ごとに業務が記録された回数', get_task_heatmap),
        ('その他コメント', get_comment_data),
        ('個人ごとの集計・業務割合', get_self_task_ratio),
        ('個人ごとの集計・時間・件数・1件あたりの時間', get_time_self_count),
        ('平均時間・件数・1件あたりの時間', get_time_count_avg),
    ]
    for name,func in data_functions:
        try:
            fig,df = func()
            results.append({'name': name, 'fig': fig, 'df': df})
        except Exception as e:
            st.warning(f"{name}のデータ収集中にエラーが発生しました: {e}")
            
    return results

    
"""
###
# 業務別チャート関数群#
# ##
"""
def Calculate_1on1(filtered_data,combined_data):
    df=ChartDataExtractor(filtered_data,combined_data).extract_task_data(task_name='1on1',to_hours=False)
    fig = px.bar(data_frame=df,x='phName',y='time_min',labels={'phName':'薬剤師名','time_min':'総時間(min)'})
    st.plotly_chart(fig,key="Calculate_1on1_chart")

def Calculate_NST(filtered_data,combined_data):
    df=ChartDataExtractor(filtered_data,combined_data).extract_task_data(task_name='NST',to_hours=None)
    fig = px.bar(data_frame=df,x='phName',y='time_min',labels={'phName':'薬剤師名','time_min':'総時間(min)'})
    st.plotly_chart(fig,key="Calculate_NST_chart")

def Calculate_TDM(filtered_data,combined_data):
    fig,df = ChartDataExtractor(filtered_data,combined_data)._create_count_chart_data(
        task_name='TDM実施',colors=False
    )
    st.plotly_chart(fig)
    #size_countを除外
    df = df[['phName','count_sum','time','time_per_count']]
    st.dataframe(df,column_config={
        'phName':'薬剤師名','count_sum':'総件数','time':'総時間(min)','time_per_count':'1件あたりの時間(min)'})
    
    #薬剤師名関係なく、件数の合計
    sumcount_df =df.agg({
        'count_sum':'sum',
        'time':'sum'
    }).to_frame().T
    st.markdown("全薬剤師合計")
    st.dataframe(sumcount_df,column_config={
        'count_sum':'総件数','time':'総時間(min)'})
        

def Calculate_TPN(filtered_data,combined_data):
    fig,df=ChartDataExtractor(filtered_data,combined_data)._create_count_chart_data(
        task_name='TPN評価',colors=False
    )
    if (df['time_per_count'] == float('inf')).any():
        st.info("1件あたりの時間が算出できないデータがあります。件数が0の可能性があります。")
    st.dataframe(df,column_config={
        'phName':'薬剤師名','count_sum':'総件数','size_count':'記録回数',
        'time':'総時間(min)','time_per_count':'1件あたりの時間(min)'})

def Calculate_WG(filtered_data,combined_data):
    df=ChartDataExtractor(filtered_data,combined_data).extract_task_data(task_name='WG活動',to_hours=False)
    fig = px.bar(data_frame=df,x='phName',y='time_min',labels={'phName':'薬剤師名','time_min':'総時間(min)'},)
    st.plotly_chart(fig,key="Calculate_WG_chart")

def Calculate_confa(filtered_data,combined_data):
    df=ChartDataExtractor(filtered_data,combined_data).extract_task_data(task_name='カンファ・ラウンド',to_hours=True)
    fig = px.bar(data_frame=df,x='phName',y='time_hr',labels={'phName':'薬剤師名','time_hr':'総時間(hr)'})
    st.plotly_chart(fig,key="Calculate_confa_chart")

def Calculate_conference(filtered_data,combined_data):
    df=ChartDataExtractor(filtered_data,combined_data).extract_task_data(task_name='カンファレンス',to_hours=False)
    fig = px.bar(data_frame=df,x='phName',y='time_min',labels={'phName':'薬剤師名','time_min':'総時間(min)'})
    st.plotly_chart(fig,key="Calculate_conference_chart")


def Calculate_other_consultation(filtered_data,combined_data):
    fig,df = ChartDataExtractor(filtered_data=filtered_data,
                                combined_data=combined_data)._create_count_chart_data(
                                    task_name='その他の職種からの相談',colors=False
                                )
    st.plotly_chart(fig,key = "TDM_chart")

def Calculate_doctor_consultation(filtered_data,combined_data):
    fig,df = ChartDataExtractor(filtered_data=filtered_data,
                                combined_data=combined_data)._create_count_chart_data(
                                    task_name='医師からの相談',colors=False
                                )
    st.plotly_chart(fig,key = "doctor_consultation_chart")


def Calculate_nurse_consultation(filtered_data,combined_data):
    fig,df = ChartDataExtractor(filtered_data=filtered_data,combined_data=combined_data)._create_count_chart_data(
        task_name='看護師からの相談',colors=False
    )
    st.plotly_chart(fig,key="nurse_consultation_chart")



def Manegment_time(filtered_data,combined_data):
    df = ChartDataExtractor(filtered_data=filtered_data,
                            combined_data=combined_data).extract_task_data(task_name='管理業務',to_hours=True)
    fig = px.bar(data_frame=df,x='phName',y='time_hr',labels={'phName':'薬剤師名','time_hr':'時間(hr)'})
    st.plotly_chart(fig,key="Manegment_time_chart")


def Adjustment_work(filtered_data,combined_data):    
    df = ChartDataExtractor(filtered_data=filtered_data,
                            combined_data=combined_data).extract_task_data(task_name='業務調整',to_hours=True)
    fig = px.bar(data_frame=df,x='phName',y='time_hr',labels={'phName':'薬剤師名','time_hr':'時間(hr)'})
    st.plotly_chart(fig,key="Adjustment_work_chart")

def Check_Medication(filtered_data,combined_data):
    fig,df=ChartDataExtractor(filtered_data=filtered_data,combined_data=combined_data)._create_count_chart_data(
        task_name='持参薬を確認',colors=False
    )
    st.plotly_chart(fig,key = "Check_Medication_chart")


def Recept_Agent_Modification(filtered_data,combined_data): #件数、総時間、１けんあたりの時間、グラフ描画
    fig,df =ChartDataExtractor(filtered_data=filtered_data,combined_data=combined_data)._create_count_chart_data(
        task_name='処方代理修正',colors=False
    )
    st.plotly_chart(fig,key="Recept_Agent_Modification_chart")
    
#TODO:病棟関係ない業務を排除できるボタンを作成、グラフ表示をきりかえる
def Medication_Guidance_Record_Creation(filtered_data,combined_data,task_name=None):
    if task_name is None:
        task_name = '服薬指導＋指導記録作成'
    fig,df=ChartDataExtractor(filtered_data=filtered_data,combined_data=combined_data)._create_count_chart_data(
        task_name=task_name,colors=False
    )
    st.plotly_chart(fig,key=f"Medication_Guidance_Record_Creation_chart_{task_name}")
    if df.empty:
        st.info("該当データが存在しません。")
        return
    
    if (df['time_per_count'] == float('inf')).any():
        st.info("1件あたりの時間が算出できないデータがあります。件数が0の可能性があります。")
    st.dataframe(df[['phName','count_sum','time_per_count']],column_config={'phName':'薬剤師名','count_sum':'総件数','time_per_count':'1件あたりの時間(min)'})


def normal_chart(filtered_data,combined_data,task_name=None):#台車鑑査,件数 、1件あたりの時間、グラフ描画
    fig,df = ChartDataExtractor(filtered_data=filtered_data,combined_data=combined_data)._create_count_chart_data(
        task_name='注射台車鑑査',colors=False
    )
    st.plotly_chart(fig,key="Trolley_check_chart")
    if df.empty:
        st.info("該当データが存在しません。")
        return

    if (df['time_per_count'] == float('inf')).any():
        st.info("1件あたりの時間が算出できないデータがあります。件数が0の可能性があります。")
    st.dataframe(df[['phName','count_sum','time_per_count']],column_config={'phName':'薬剤師名','count_sum':'総件数','time_per_count':'1件あたりの時間(min)'})

import plotly.express as px
import pandas as pd

def clean_preparation(filtered_data,combined_data,task_name=None):
    if task_name is None:
        task_name = '無菌調製関連業務'
    df = ChartDataExtractor(filtered_data,combined_data).extract_task_data(
        task_name=task_name,to_hours=False)
    fig = px.bar(data_frame=df,x='phName',y='time_min',labels={'phName':'薬剤師名','time_min':'総時間(min)'})
    st.plotly_chart(fig,key="clean_preparation_chart")

def drag_set_check(filtered_data,combined_data,task_name=None):
    if task_name is None:
        task_name = '薬剤セット・確認'
    df =ChartDataExtractor(filtered_data=filtered_data,
                        combined_data=combined_data).extract_task_data(task_name=task_name,to_hours=False)
    fig = px.bar(data_frame=df,x='phName',y='time_min',labels={'phName':'薬剤師名','time_min':'総時間(min)'})
    st.plotly_chart(fig,key="drag_set_check_chart")

import plotly.graph_objects as go

def research_info_chart(filtered_data,combined_data):
    fig,df =ChartDataExtractor(filtered_data=filtered_data,combined_data=combined_data)._create_count_chart_data(
        task_name='薬剤使用状況の把握等（情報収集）',colors=False
    )
    st.plotly_chart(fig,key="research_info_chart")
    if (df['time_per_count'] == float('inf')).any():
        st.info("1件あたりの時間が算出できないデータがあります。件数が0の可能性があります。")
    st.dataframe(df,column_config={
        'phName':'薬剤師名','count_sum':'総件数','size_count':'記録回数','time_per_count':'1件あたりの時間(min)',
        'time':'総時間(min)'
        })

def Jokusou_chart(filtered_data,combined_data):
    df = ChartDataExtractor(filtered_data,combined_data).extract_task_data(task_name='褥瘡',to_hours=False)
    fig = px.bar(data_frame=df,x='phName',y='time_min',labels={'phName':'薬剤師名','time_min':'総時間(min)'})
    st.plotly_chart(fig,key="Jokusou_chart")
        
def operoom_chart(filtered_data,combined_data):
    df = ChartDataExtractor(filtered_data=filtered_data).extract_task_data(task_name='手術室サテライト薬剤定数確認',to_hours=False)
    fig = px.bar(data_frame=df,x='phName',y='time_min',labels={'phName':'薬剤師名','time_min':'総時間(min)'})
    st.plotly_chart(fig,key="operroom_count_chart")


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
        df =ChartDataExtractor(filtered_data,combined_data).extract_task_data(task_name='1on1',to_hours=False)
        fig = px.bar(data_frame=df, x='phName', y='time_min', 
                    labels={'phName':'薬剤師名','time_min':'総時間(min)'},
                    color_discrete_sequence=[PLOTLY_COLORS[0]])
        total_df = df.agg({'time_min':'sum'}).to_frame().T
        df = df.rename(columns={'time_min':'総時間(min)','phName':'薬剤師名','count':'記録回数'})
        total_df = total_df.rename(columns={'time_min':'総時間(min)'})
        return fig, df[["総時間(min)","薬剤師名"]],total_df[["総時間(min)"]]
    
    def get_nst_data():
        df =ChartDataExtractor(filtered_data,combined_data).extract_task_data(task_name='NST',to_hours=False)
        fig = px.bar(data_frame=df, x='phName', y='time_min', 
                    labels={'phName':'薬剤師名','time_min':'総時間(min)'},color_discrete_sequence=[PLOTLY_COLORS[0]])
        total_df = df.agg({'time_min':'sum'}).to_frame().T
        df = df.rename(columns={'time_min':'総時間(min)','phName':'薬剤師名'})
        total_df =total_df.rename(columns={'time_min':'総時間(min)'})
        return fig, df[["総時間(min)","薬剤師名"]],total_df[["総時間(min)"]]
    
    def get_tdm_data():
        fig ,df = ChartDataExtractor(filtered_data=filtered_data,combined_data=combined_data)._create_count_chart_data(
            task_name='TDM実施', colors=PLOTLY_COLORS
        )
        total_df = df.agg({
            'count_sum':'sum',
            'time':'sum'
        }).to_frame().T
        
        df = df.rename(columns={'count_sum':'総件数','time':'総時間(min)','phName':'薬剤師名','time_per_count':'1件あたりの時間(min)'}) #薬剤師名ごとのデータフレーム
        total_df = total_df.rename(columns = {'count_sum':'総件数', 'time':'総時間(min)'})#全薬剤師合計のデータフレーム
        return fig, df[["総件数","総時間(min)","薬剤師名","1件あたりの時間(min)"]],total_df[["総件数","総時間(min)"]]
    
    def get_tpn_data():
        fig,df = ChartDataExtractor(filtered_data, combined_data)._create_count_chart_data(
            task_name='TPN評価', colors=False
        )
        total_df = df.agg({'count_sum':'sum','time':'sum'}).to_frame().T
        df=df.rename(columns={'count_sum':'総件数','size_count':'記録回数','time':'総時間(min)','time_per_count':'1件あたりの時間(min)','phName':'薬剤師名'})
        total_df = total_df.rename(columns={'count_sum':'総件数','time':'総時間(min)'})
        return None, df[["総件数","記録回数","総時間(min)","1件あたりの時間(min)","薬剤師名"]], total_df[["総件数","総時間(min)"]]  # TPNはグラフがないのでNone
    
    def get_wg_data():
        df = ChartDataExtractor(filtered_data,combined_data).extract_task_data(task_name='WG活動',to_hours=False)
        fig = px.bar(data_frame=df, x='phName', y='time_min', 
                    labels={'phName':'薬剤師名','time_min':'総時間(min)'},
                    color_discrete_sequence=[PLOTLY_COLORS[0]])
        total_df = df.agg({'time_min':'sum'}).to_frame().T
        df = df.rename(columns={'time_min':'総時間(min)','phName':'薬剤師名'})
        total_df = total_df.rename(columns={'time_min':'総時間(min)'})
        return fig, df[["総時間(min)","薬剤師名"]],total_df[["総時間(min)"]]
    
    def get_confa_data():
        df = ChartDataExtractor(filtered_data,combined_data).extract_task_data(task_name='カンファ・ラウンド',to_hours=True)
        fig = px.bar(data_frame=df, x='phName', y='time_hr', 
                    labels={'phName':'薬剤師名','time_hr':'総時間(hr)'},
                    color_discrete_sequence=[PLOTLY_COLORS[0]])
        total_df = df.agg({'time_hr':'sum'}).to_frame().T
        df = df.rename(columns={'time_hr':'総時間(hr)','phName':'薬剤師名'})
        total_df = total_df.rename(columns={'time_hr':'総時間(hr)'})
        return fig, df[["総時間(hr)","薬剤師名"]],total_df[["総時間(hr)"]]
    
    def get_conference_data():
        df = ChartDataExtractor(filtered_data=filtered_data,
                                combined_data=combined_data).extract_task_data(task_name='カンファレンス',to_hours=False)
        fig = px.bar(data_frame=df, x='phName', y='time_min', 
                    labels={'phName':'薬剤師名','time_min':'総時間(min)'},
                    color_discrete_sequence=[PLOTLY_COLORS[0]])
        total_df = df.agg({'time_min':'sum'}).to_frame().T
        df = df.rename(columns={'time_min':'総時間(min)','phName':'薬剤師名'})
        total_df = total_df.rename(columns={'time_min':'総時間(min)'})
        return fig, df[["総時間(min)","薬剤師名"]], total_df[["総時間(min)"]]
    
    def get_other_consultation_data():
        fig,df = ChartDataExtractor(filtered_data=filtered_data,
                                    combined_data=combined_data)._create_count_chart_data(
                                        task_name='その他の職種からの相談', colors=PLOTLY_COLORS
                                    )
                                    
        total_df =df.agg({'count_sum':'sum','time':'sum'}).to_frame().T
        df = df.rename(columns={'count_sum':'総件数','time':'総時間(min)','phName':'薬剤師名','time_per_count':'1件あたりの時間(min)'})
        total_df = total_df.rename(columns={'count_sum':'総件数','time':'総時間(min)'})
        return fig, df[["総件数","総時間(min)","薬剤師名","1件あたりの時間(min)"]],total_df[["総件数","総時間(min)"]]
    
    def get_doctor_consultation_data():
        fig,df = ChartDataExtractor(filtered_data=filtered_data,
                                    combined_data=combined_data)._create_count_chart_data(
                                        task_name='医師からの相談', colors=PLOTLY_COLORS
                                    )
        total_df=df.agg({'count_sum':'sum','time':'sum'}).to_frame().T
        df = df.rename(columns={'count_sum':'総件数','time':'総時間(min)','phName':'薬剤師名','time_per_count':'1件あたりの時間(min)'})
        total_df = total_df.rename(columns={'count_sum':'総件数','time':'総時間(min)'})
        return fig, df[["総件数","総時間(min)","薬剤師名","1件あたりの時間(min)"]],total_df[["総件数","総時間(min)"]]
    
    def get_nurse_consultation_data():
        fig,df = ChartDataExtractor(filtered_data=filtered_data,combined_data=combined_data)._create_count_chart_data(
            task_name='看護師からの相談', colors=PLOTLY_COLORS
        )
        total_df = df.agg({'count_sum':'sum','time':'sum'}).to_frame().T
        df = df.rename(columns={'count_sum':'総件数','time':'総時間(min)','phName':'薬剤師名','time_per_count':'1件あたりの時間(min)'})
        total_df = total_df.rename(columns={'count_sum':'総件数','time':'総時間(min)'})
        return fig, df[["総件数","総時間(min)","薬剤師名","1件あたりの時間(min)"]], total_df[["総件数","総時間(min)"]]
    
    def get_management_time_data():
        df = ChartDataExtractor(filtered_data,combined_data).extract_task_data(task_name='管理業務',to_hours=True)
        fig = px.bar(data_frame=df, x='phName', y='time_hr', 
                    labels={'phName':'薬剤師名','time_hr':'時間(hr)'},
                    color_discrete_sequence=[PLOTLY_COLORS[0]])
        total_df = df.agg({'time_hr':'sum'}).to_frame().T
        df =df.rename(columns={'time_hr':'時間(hr)','phName':'薬剤師名','count':'記録回数'})
        total_df = total_df.rename(columns={'time_hr':'総時間(hr)'})
        return fig, df[['時間(hr)','薬剤師名']],total_df[['総時間(hr)']]
    
    def get_adjustment_work_data():
        df = ChartDataExtractor(filtered_data,combined_data).extract_task_data(task_name='業務調整',to_hours=True)
        fig = px.bar(data_frame=df, x='phName', y='time_hr', 
                    labels={'phName':'薬剤師名','time_hr':'時間(hr)'},
                    color_discrete_sequence=[PLOTLY_COLORS[0]])
        total_df = df.agg({'time_hr':'sum'}).to_frame().T
        df = df.rename(columns={'time_hr':'時間(hr)','phName':'薬剤師名'})
        total_df = total_df.rename(columns={'time_hr':'総時間(hr)'})
        return fig, df[['時間(hr)','薬剤師名']], total_df[['総時間(hr)']]
    
    def get_check_medication_data():
        fig,df = ChartDataExtractor(filtered_data=filtered_data,combined_data=combined_data)._create_count_chart_data(
            task_name='持参薬を確認', colors=PLOTLY_COLORS
        )
        total_df = df.agg({'count_sum':'sum','time':'sum'}).to_frame().T
        df = df.rename(columns={'count_sum':'総件数','time':'総時間(min)','phName':'薬剤師名','time_per_count':'1件あたりの時間(min)'})
        total_df = total_df.rename(columns={'count_sum':'総件数','time':'総時間(min)'})
        return fig, df[["総件数","総時間(min)","薬剤師名","1件あたりの時間(min)"]], total_df[["総件数","総時間(min)"]]
    
    def get_recept_agent_modification_data():
        fig,df =ChartDataExtractor(filtered_data=filtered_data,combined_data=combined_data)._create_count_chart_data(
            task_name='処方代理修正', colors=PLOTLY_COLORS
        )
        total_df = df.agg({'count_sum':'sum','time':'sum'}).to_frame().T
        df = df.rename(columns={'count_sum':'総件数','time':'総時間(min)','phName':'薬剤師名','time_per_task':'1件あたりの時間(min)'})
        total_df = total_df.rename(columns={'count_sum':'総件数','time':'総時間(min)'})
        return fig, df[["総件数","総時間(min)","薬剤師名","1件あたりの時間(min)"]],total_df[["総件数","総時間(min)"]]
    
    def get_medication_guidance_data():
        fig,df = ChartDataExtractor(filtered_data=filtered_data,combined_data=combined_data)._create_count_chart_data(
            task_name='服薬指導＋指導記録作成', colors=PLOTLY_COLORS
        )
        total_df = df.agg({'count_sum':'sum','time':'sum'}).to_frame().T
        
        df = df.rename(columns={'count_sum':'総件数','time':'総時間(min)','phName':'薬剤師名','time_per_task':'1件あたりの時間(min)'})
        total_df = total_df.rename(columns={'count_sum':'総件数','time':'総時間(min)'})
        return fig, df[['薬剤師名','総件数','1件あたりの時間(min)']], total_df[["総件数","総時間(min)"]]
    
    def get_clean_preparation_data():
        df = ChartDataExtractor(filtered_data=filtered_data,
                                combined_data=combined_data).extract_task_data(task_name='無菌調製関連業務',to_hours=False)
        fig = px.bar(data_frame=df, x='phName', y='time_min', 
                    labels={'phName':'薬剤師名','time_min':'総時間(min)'},
                    color_discrete_sequence=[PLOTLY_COLORS[0]])
        total_df = df.agg({
            'time':'sum'
        }).to_frame().T
        df = df.rename(columns={'count_sum':'総記録回数','time_min':'総時間(min)','phName':'薬剤師名'})
        total_df = total_df.rename(columns={'time':'総時間(min)'})
        return fig, df[["総時間(min)","薬剤師名"]], total_df[["総時間(min)"]]   
    
    def get_drag_set_check_data():
        df = ChartDataExtractor(filtered_data=filtered_data,
                                combined_data=combined_data).extract_task_data(task_name='薬剤セット・確認',to_hours=False)
        fig = px.bar(data_frame=df, x='phName', y='time_min', 
                    labels={'phName':'薬剤師名','time_min':'総時間(min)'},
                    color_discrete_sequence=[PLOTLY_COLORS[0]])
        total_df = df.agg({
            'time':'sum'
        }).to_frame().T
        
        df = df.rename(columns={'count_sum':'総記録回数','time_min':'総時間(min)','phName':'薬剤師名'})
        total_df = total_df.rename(columns={'time':'総時間(min)'})
        return fig, df[["総時間(min)","薬剤師名"]], total_df[["総時間(min)"]]
    
    def get_research_info_data():
        fig,df =ChartDataExtractor(filtered_data=filtered_data,combined_data=combined_data)._create_count_chart_data(
            task_name='薬剤使用状況の把握等（情報収集）', colors=PLOTLY_COLORS
        )
        total_df = df.agg({
            'count_sum':'sum',
            'time':'sum'
        }).to_frame().T
        df = df.rename(columns={'count_sum':'総件数','size_count':'記録回数','time_per_count':'1件あたりの時間(min)',
                                'time':'総時間(min)','phName':'薬剤師名'})
        total_df = total_df.rename(columns = {'count_sum':'総件数','time':'総時間(min)'})
        
        return fig, df[["薬剤師名","総件数","記録回数","総時間(min)","1件あたりの時間(min)"]], total_df[["総件数","総時間(min)"]]
    
    def get_jokusou_data():
        df = ChartDataExtractor(filtered_data=filtered_data,
                                combined_data=combined_data).extract_task_data(task_name='褥瘡',to_hours=False)
        fig = px.bar(data_frame=df, x='phName', y='time_min', 
                    labels={'phName':'薬剤師名','time_min':'総時間(min)'},
                    color_discrete_sequence=[PLOTLY_COLORS[0]])
        total_df = df.agg({
            'time':'sum'
        }).to_frame().T
        df = df.rename(columns={'count_sum':'総記録回数','time_min':'総時間(min)','phName':'薬剤師名'})
        total_df = total_df.rename(columns = {'time':'総時間(min)'})
        return fig, df[["総時間(min)","薬剤師名"]], total_df[["総時間(min)"]]
    
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
            fig, df, total_df = func()
            if df is not None and not df.empty:
                    results.append({'name': name, 'fig': fig, 'df': df,'total_df':total_df})
                
        except Exception as e:
            print(f"Error collecting data for {name}: {e}")
    
    return results