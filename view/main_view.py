import streamlit as st
from widgets.folder_selector import FolderSelector
from widgets.join_files import JoinFiles
from dtgroupby.groupbytaskcount import GroupByTaskCount
from resizeDataframe.drawChart import (
    time_per_task_chart,
    counts_per_task_chart,
    time_per_locate_chart,
    Medication_Guidance_Record_Creation
)

def View():
    st.title("日誌集計ツール")
    st.markdown("このアプリケーションは複数のCSVファイルを結合し、集計を行うツールです。")
    st.markdown("最初にcsvファイルを含むフォルダをアップロードしてください")
    combined_data=None
    #フォルダを読み込む
    uploadfiles =st.sidebar.file_uploader(
        "フォルダを選択してください",accept_multiple_files='directory')
    #TODO:フォルダは複数選択できるようにする
    
    if uploadfiles:
        combined_data = JoinFiles(uploadfiles).join()

    # 前回slider値を追跡
    if 'prev_slider' not in st.session_state:
        st.session_state.prev_slider = None
    
    #TODO ファイル読み込み中のプログレスバーを表示、中に読み込んだデータを元に集計項目を作成する旨を記載
    slider = st.sidebar.pills("詳細な絞り込み",options=["あり","なし"])

    if st.session_state.prev_slider != slider:
        #前の選択をクリア
        if 'locate_select' in st.session_state:
            del st.session_state['locate_select']
        if 'name_select' in st.session_state:
            del st.session_state['name_select']
        st.session_state.prev_slider = slider
        st.rerun()

    if combined_data is not None:
        if slider == "あり":
            #日付以外に病棟名や個人名で絞り込みを行う
            #絞り込みありの場合
            locate_select =st.sidebar.multiselect(label="病棟の絞り込み",options=combined_data['locate'].unique())
            name_select = st.sidebar.multiselect(label="個人名の選択",options=combined_data["phName"].unique())

            st.sidebar.markdown("期間選択")
            date_range = st.sidebar.date_input("日付範囲を選択してください",[])
            #task_記録された回数
            #名前や期間で絞り込みあれば反映する
            filtered_data=GroupByTaskCount(combined_data).group_by_task_count(
                date_range=date_range,locate_select=locate_select,name_select=name_select)
            st.subheader("各タスクの合計時間")
            total_time_per_task(filtered_data,combined_data)
            st.subheader("病棟ごとの集計")
            componentChart_location(filtered_data,combined_data)
            st.subheader("個人ごとの集計")
            st.subheader("総件数と件数あたりの時間")
            st.subheader("業務内容ごとの件数")
            st.subheader("業務内容ごとの場所")
            st.subheader("時間帯ごとに業務が記録された回数")
            st.subheader("その他コメント")
            st.subheader("個人ごとの総時間数")
            st.subheader("個人ごとの時間数・件数・1件あたりの時間・平均値")



        elif slider == "なし":
            st.sidebar.markdown("期間選択")
            date_range = st.sidebar.date_input("日付範囲を選択してください",[])
            filtered_data= GroupByTaskCount(combined_data).group_by_task_count(
                date_range=date_range,locate_select=None,name_select=None)
            #絞り込みは日付のみ
            st.sidebar.markdown("結合結果のプレビュー")
            if filtered_data is not None:
                st.sidebar.dataframe(filtered_data.head(10))
            else:
                st.sidebar.dataframe(combined_data.head(10))    
            
            #barchart
            st.subheader("記録された時間")
            st.markdown("barchart")
            time_per_task_chart(filtered_data,combined_data)
            #plotly_chart
            st.markdown("plotly")
            
            st.subheader("件数の合計")
            counts_per_task_chart(filtered_data,combined_data)

            st.subheader("病棟別の業務割合表示")
            st.subheader("病棟ごとに記録された時間の合計")#TODO:locateごとに作成する
            time_per_locate_chart(filtered_data,combined_data)

            #TODO: taskごとに作成する
            st.markdown("1on1")
            Calculate_1on1(filtered_data,combined_data)
            st.markdown("NST")
            Calculate_NST(filtered_data,combined_data)
            st.markdown("TDM")
            Calculate_TDM(filtered_data,combined_data)
            st.markdown("TPN評価")
            Calculate_TPN(filtered_data,combined_data)
            st.markdown("WG活動")
            Calculate_WG(filtered_data,combined_data)
            st.markdown("カンファ・ラウンド")
            Calculate_confa(filtered_data,combined_data)
            st.markdown("カンファレンス")
            Calculate_conference(filtered_data,combined_data)
            st.markdown("その他の職種からの相談")
            Calculate_other_consultation(filtered_data,combined_data)
            st.markdown("医師からの相談")
            Calculate_doctor_consultation(filtered_data,combined_data)
            st.markdown("看護師からの相談")
            Calculate_nurse_consultation(filtered_data,combined_data)
            
            st.markdown("服薬指導+記録作成")
            Medication_Guidance_Record_Creation(filtered_data,combined_data)

            
