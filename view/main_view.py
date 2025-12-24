import streamlit as st
from widgets.folder_selector import FolderSelector
from widgets.join_files import JoinFiles
from dtgroupby.groupbytaskcount import GroupByTaskCount
from resizeDataframe.drawChart import (
    time_per_locate_chart,
    Medication_Guidance_Record_Creation,
    count_task,
    task_per_location,
    task_heatmap,
    comment_data,

    Calculate_1on1,
    Calculate_NST,
    Calculate_TDM,
    Calculate_TPN,
    Calculate_WG,
    Calculate_confa,
    Calculate_conference,
    Calculate_other_consultation,
    Calculate_doctor_consultation,
    Calculate_nurse_consultation,
    total_time_per_task,
    componentChart_location,
    Manegment_time,
    Adjustment_work,
    Check_Medication,
    Recept_Agent_Modification,
    clean_preparation,
    drag_set_check,
    research_info_chart,
    Jokusou_chart,

    self_task_ratio,

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
    slider = st.sidebar.pills("表示モード",options=["概要","業務別分析"])

    if st.session_state.prev_slider != slider:
        #前の選択をクリア
        if 'locate_select' in st.session_state:
            del st.session_state['locate_select']
        if 'name_select' in st.session_state:
            del st.session_state['name_select']
        st.session_state.prev_slider = slider
        st.rerun()

    if combined_data is not None:
        if slider == "概要":
            #日付以外に病棟名や個人名で絞り込みを行う
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
            st.markdown("時間の合計")#TODO:locateごとに作成する
            time_per_locate_chart(filtered_data,combined_data)

            st.markdown("業務内容ごとの件数と1件あたりの時間")
            count_task(filtered_data,combined_data)
            st.markdown("記録された業務内容と回数")
            task_per_location(filtered_data,combined_data)            
            st.subheader("時間帯ごとに業務が記録された回数")
            task_heatmap(filtered_data,combined_data)
            st.subheader("その他コメント")
            comment_data(filtered_data,combined_data)

            st.subheader("個人ごとの集計")
            st.markdown("業務割合")
            self_task_ratio(filtered_data,combined_data)
            st.markdown("時間・件数・1件あたりの時間・平均値")




        elif slider == "業務別分析":
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
            
            

            

            st.markdown("1on1")
            Calculate_1on1(filtered_data,combined_data)
            st.markdown("NST")
            Calculate_NST(filtered_data,combined_data)
            st.markdown("TDM実施")
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
            st.markdown("管理業務")#TODO:個人ごとの総時間グラフ
            Manegment_time(filtered_data,combined_data)
            st.markdown("業務調整")#個人ごとの総時間グラフ
            Adjustment_work(filtered_data,combined_data)
            st.markdown("持参薬を確認")#件数、総時間、１けんあたりの時間、グラフ描画必要
            Check_Medication(filtered_data,combined_data)
            st.markdown("処方代理修正")#件数、総時間、１けんあたりの時間、グラフ描画
            Recept_Agent_Modification(filtered_data,combined_data)
            st.markdown("服薬指導+記録作成")
            Medication_Guidance_Record_Creation(filtered_data,combined_data)#グラフとデータフレーム
            #データフレームは件数と１けんあたりの時間のみ
            st.markdown("無菌調整関連業務")#個人ごとの時間
            clean_preparation(filtered_data,combined_data)
            st.markdown("薬剤セット確認")#個人ごとの、総時間、グラフ描画
            drag_set_check(filtered_data,combined_data)
            st.markdown("薬剤使用状況の把握等(情報収集)")#個人ごとの件数と１けんあたりの時間を並列棒グラフ
            research_info_chart(filtered_data,combined_data)
            #TODO:別途データフレームで件数、総時間、１件あたりの時間
            st.markdown("褥瘡")#個人ごとの、総時間、グラフ描画
            Jokusou_chart(filtered_data,combined_data)