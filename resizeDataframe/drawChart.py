import streamlit as st
from view.TASK_COLOR_MAP import TASK_COLOR_MAP
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import ast
from models.task_list import Task_list

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
        """特定の業務に絞った、薬剤師ごとの時間を算出する関数"""
        df = self.df[['phName','task']].copy()
        df = df[df['task'] ==task_name]
        df = df.groupby('phName').size().reset_index(name='count')
        time_label = 'time_hr' if to_hours else 'time_min'
        df[time_label] = _calculate_time(df['count'],to_hours)
        return df
    
    def _create_count_chart_data(self,task_name=False,colors=False,
                                to_hours=False):
        """件数付き集計のチャートデータを作成"""
        df = self.df[['phName','task','count']].copy()
        if task_name:
            df = df[df['task'] ==task_name]
        df = df.groupby(['phName','task']).agg(
            count_sum = ('count','sum'),
            size_count = ('task','size')
        ).reset_index()
        df['time'] = df['size_count']*15
        if to_hours:
            df['time'] = df['time'] / 60
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


"""--汎用グラフ関数--"""
def simple_task_time_chart(filtered_data, combined_data, task_name, to_hours=False, chart_key=None):
    """extract_task_data + px.bar の共通処理をまとめた汎用関数"""
    df = ChartDataExtractor(filtered_data, combined_data).extract_task_data(
        task_name=task_name, to_hours=to_hours
    )
    time_col = 'time_hr' if to_hours else 'time_min'
    time_label = '総時間(hr)' if to_hours else '総時間(min)'
    fig = px.bar(
        data_frame=df,
        x='phName',
        y=time_col,
        labels={'phName': '薬剤師名', time_col: time_label},
    )
    key = chart_key if chart_key else f"simple_task_time_chart_{task_name}"
    st.plotly_chart(fig, key=key)


def count_task_chart(filtered_data, combined_data, task_name, chart_key=None, show_dataframe=False, show_total=False, chart=False,to_hours=False,):
    """_create_count_chart_data + 表示処理をまとめた汎用関数
    - task_name: 対象の業務名
    - chart_key: Streamlitのチャートに渡すキー（省略時は自動生成）
    - show_dataframe: データフレームを表示するか
    - show_total: 全薬剤師の合計行を表示するか
    - chart: チャートを表示するか
    - to_hours: 時間を時間単位で表示するか（デフォルトは分単位）
    
    """
    time_col = 'time_hr' if to_hours else 'time'
    time_label = '総時間(hr)' if to_hours else '総時間(min)'
    
    fig, df = ChartDataExtractor(filtered_data, combined_data)._create_count_chart_data(
        task_name=task_name, colors=False,to_hours=to_hours
    )
    key = chart_key if chart_key else f"count_task_chart_{task_name}"
    if chart:
        st.plotly_chart(fig, key=key)
    if df.empty:
        st.info("該当データが存在しません。")
        return
    if (df['time_per_count'] == float('inf')).any():
        st.info("1件あたりの時間が算出できないデータがあります。件数が0の可能性があります。")
    if show_dataframe:
        st.dataframe(
            df[['phName', 'count_sum', time_col, 'time_per_count']],
            column_config={
                'phName': '薬剤師名',
                'count_sum': '総件数',
                time_col: time_label,
                'time_per_count': '1件あたりの時間(min)',
            },
        )
            
    if show_total:
        total_df = df.agg({'count_sum': 'sum', time_col: 'sum'}).to_frame().T
        st.markdown("全薬剤師合計")
        st.dataframe(total_df, column_config={'count_sum': '総件数', time_col: time_label})
    
    if task_name=="TDM実施":
        #薬剤師名関係なく、件数の合計
        sumcount_df = df.agg({
            'count_sum':'sum',
            time_col:'sum'
        }).to_frame().T
        st.markdown("全薬剤師合計")
        st.dataframe(sumcount_df,column_config={
            'count_sum':'総件数',time_col:time_label})
        


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


def collect_all_charts_data(filtered_data, combined_data,task_list=None):
    """
    全てのグラフとデータフレームを収集する関数
    
    Returns:
        list: [{'name': str, 'fig': plotly.Figure, 'df': pd.DataFrame}, ...]
    """
    results = []
    
    PLOTLY_COLORS = [
        '#2B66C2',"#93C7FA"
    ]
    task_list = task_list if task_list is not None else combined_data['task'].unique()
    definitions = Task_list(filtered_data, combined_data).list()
    data_functions = []
    # 各関数からデータを抽出（表示はせずにデータのみ取得）
    for task in task_list:
        definition = definitions.get(task, {})
        print(f"Collecting data for task: {task}, definition: {definition}")  # デバッグ用ログ
        data_functions.append((definition.get('chart_key', f"chart_{task}"), 
                            lambda t=task: ChartDataExtractor(filtered_data, combined_data)._create_count_chart_data(
            task_name=t, colors=PLOTLY_COLORS,to_hours=definition.get('to_hours', False),
        )))

    for name, func in data_functions:
        try:
            fig, df, total_df = func()
            if df is not None and not df.empty:
                    results.append({'name': name, 'fig': fig, 'df': df,'total_df':total_df})
                
        except Exception as e:
            print(f"Error collecting data for {name}: {e}")
    
    return results