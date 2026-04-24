import streamlit as st
from widgets.join_files import JoinFiles
from dtgroupby.groupbytaskcount import GroupByTaskCount
from resizeDataframe.tidy_data import tidy_data
from resizeDataframe.drawChart import (
    Medication_Guidance_Record_Creation,
    count_task,
    task_heatmap,
    time_count_avg,
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
    Manegment_time,
    Adjustment_work,
    Check_Medication,
    Recept_Agent_Modification,
    clean_preparation,
    drag_set_check,
    research_info_chart,
    Jokusou_chart,
    self_task_ratio,
    collect_all_charts_data,
    collect_about_chart,
)
from resizeDataframe.location_charts import (
    collect_location_charts_data,
    componentChart_location,
    time_per_locate_chart,
    task_per_location,
)
from resizeDataframe.download_utils import (create_download_package,create_df_download_package)
import ast

#ユニークな病棟名の抽出
def extract_unique_locations(dataframe):
    if 'locate' not in dataframe.columns:
        return []
    df = dataframe.copy()
    df = df[df['locate'].notnull()]
    df['locate'] = df['locate'].apply(ast.literal_eval)
    df['locate'] = df['locate'].apply(lambda x: x[0] if len(x)>0 else '')
    df = df[['locate']].drop_duplicates().reset_index(drop=True)
    return df['locate'].tolist()

import hashlib
import pandas as pd
def get_dataframe_hash(df):
    return hashlib.md5(pd.util.hash_pandas_object(df,index=True).values).hexdigest()
from config.release_notes import get_release_notes


def downlad_handler(collected_data_handler,filtered_data,combined_data):
    # 一括ダウンロードボタン
        st.markdown("---")
        st.subheader("データ一括ダウンロード")
        if st.button("グラフとデータフレームを収集", key="collect_data_button"):
            with st.spinner("データを収集中..."):
                charts_and_data = collected_data_handler(filtered_data, combined_data)
                if charts_and_data:
                    zip_buffer = create_download_package(charts_and_data)
                    st.download_button(
                        label="📥 ZIPファイルをダウンロード",
                        data=zip_buffer,
                        file_name="業務分析レポート.zip",
                        mime="application/zip"
                    )
                    st.success(f"✅ {len(charts_and_data)}件のデータを収集しました")
                else:
                    st.warning("ダウンロード可能なデータが見つかりませんでした")
def View():
    st.title("日誌集計ツール")
    st.markdown("このアプリケーションは複数のCSVファイルを結合し、集計を行うツールです。")
    st.markdown("最初にcsvファイルを含むフォルダをアップロードしてください")
    with st.expander("リリースノート",expanded=False):
        st.markdown(get_release_notes())
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
    slider = st.sidebar.pills("表示モード",options=["概要","病棟別分析","業務別分析","データ加工"])

    if st.session_state.prev_slider != slider:
        #前の選択をクリア
        if 'locate_select' in st.session_state:
            del st.session_state['locate_select']
        if 'name_select' in st.session_state:
            del st.session_state['name_select']
        st.session_state.prev_slider = slider
        st.rerun()



    if combined_data is not None:
        #ハッシュ値で変更を検知、変更ある場合のみ。select_locate_listを更新
        current_hash = get_dataframe_hash(combined_data)
        if 'combined_data_hash' not in st.session_state:
            st.session_state.select_locate_list = extract_unique_locations(combined_data)
            st.session_state.combined_data_hash = current_hash

        select_locate_list = st.session_state.select_locate_list

        if slider == "概要":
            #日付以外に病棟名や個人名で絞り込みを行う
            locate_select =st.sidebar.multiselect(label="病棟の絞り込み",options=select_locate_list,key='locate_select')
            name_select = st.sidebar.multiselect(label="個人名の選択",options=combined_data["phName"].unique(),key='name_select')


            st.sidebar.markdown("期間選択")
            date_range = st.sidebar.date_input("日付範囲を選択してください",[])
            #task_記録された回数
            #名前や期間で絞り込みあれば反映する
            #TODO:旧ツールの業務名で新ツールのデータを統一する
            taskname_tydir=st.toggle(label="旧ツールの業務名で統一",key="taskname_tpggle",value=False)
            filtered_data=GroupByTaskCount(combined_data).group_by_task_count(
                date_range=date_range,locate_select=locate_select,name_select=name_select,taskname_tydir=taskname_tydir)
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
            # 一括ダウンロードボタン
            downlad_handler(collect_about_chart,filtered_data,combined_data)
        elif slider == "病棟別分析":
            #日付以外に病棟名や個人名で絞り込みを行う
            locate_select =st.sidebar.multiselect(label="病棟の絞り込み",options=select_locate_list)
            name_select = st.sidebar.multiselect(label="個人名の選択",options=combined_data["phName"].unique())

            st.sidebar.markdown("期間選択")
            date_range = st.sidebar.date_input("日付範囲を選択してください",[])
            #task_記録された回数
            #名前や期間で絞り込みあれば反映する
            taskname_tydir=st.toggle(label="旧ツールの業務名で統一",key="taskname_tpggle",value=False)
            filtered_data=GroupByTaskCount(combined_data).group_by_task_count(
                date_range=date_range,locate_select=locate_select,name_select=name_select,taskname_tydir=taskname_tydir )
            
            st.subheader("病棟ごとの集計")
            componentChart_location(filtered_data,combined_data)
            st.markdown("時間の合計")#locateごとに作成する
            time_per_locate_chart(filtered_data,combined_data)
            st.markdown("記録された業務内容と総時間")
            task_per_location(filtered_data,combined_data)     
            
            downlad_handler(collect_location_charts_data,filtered_data,combined_data)

        elif slider == "業務別分析":
            st.sidebar.markdown("期間選択")
            date_range = st.sidebar.date_input("日付範囲を選択してください",[])
            taskname_tydir=st.toggle(label="旧ツールの業務名で統一",key="taskname_tpggle",value=False)
            filtered_data= GroupByTaskCount(combined_data).group_by_task_count(
                date_range=date_range,locate_select=None,name_select=None,taskname_tydir=taskname_tydir )
            #絞り込みは日付のみ
            st.sidebar.markdown("結合結果のプレビュー")
            if filtered_data is not None:
                st.sidebar.dataframe(filtered_data.head(10))
            else:
                st.sidebar.dataframe(combined_data.head(10))    
            
            st.divider()
            st.markdown("1on1")
            Calculate_1on1(filtered_data,combined_data)
            st.divider()
            st.markdown("NST")
            Calculate_NST(filtered_data,combined_data)
            st.divider()
            st.markdown("TDM実施")
            Calculate_TDM(filtered_data,combined_data)
            st.divider()
            st.markdown("TPN評価")
            Calculate_TPN(filtered_data,combined_data)
            st.divider()
            st.markdown("WG活動")
            Calculate_WG(filtered_data,combined_data)
            st.divider()
            st.markdown("カンファ・ラウンド")
            Calculate_confa(filtered_data,combined_data)
            st.divider()
            st.markdown("カンファレンス")
            Calculate_conference(filtered_data,combined_data)
            st.divider()
            st.markdown("その他の職種からの相談")
            Calculate_other_consultation(filtered_data,combined_data)
            st.divider()
            st.markdown("医師からの相談")
            Calculate_doctor_consultation(filtered_data,combined_data)
            st.divider()
            st.markdown("看護師からの相談")
            Calculate_nurse_consultation(filtered_data,combined_data)
            st.divider()
            st.markdown("管理業務")#TODO:個人ごとの総時間グラフ
            Manegment_time(filtered_data,combined_data)
            st.divider()
            st.markdown("業務調整")#個人ごとの総時間グラフ
            Adjustment_work(filtered_data,combined_data)
            st.divider()
            st.markdown("持参薬を確認")#件数、総時間、１けんあたりの時間、グラフ描画必要
            Check_Medication(filtered_data,combined_data)
            st.divider()
            st.markdown("処方代理修正")#件数、総時間、１けんあたりの時間、グラフ描画
            Recept_Agent_Modification(filtered_data,combined_data)
            st.divider()
            st.markdown("服薬指導+記録作成")
            Medication_Guidance_Record_Creation(filtered_data,combined_data)#グラフとデータフレーム
            #データフレームは件数と１けんあたりの時間のみ
            st.divider()
            st.markdown("無菌調整関連業務")#個人ごとの時間
            clean_preparation(filtered_data,combined_data)
            st.divider()
            st.markdown("薬剤セット確認")#個人ごとの、総時間、グラフ描画
            drag_set_check(filtered_data,combined_data)
            st.divider()
            st.markdown("薬剤使用状況の把握等(情報収集)")#個人ごとの件数と１けんあたりの時間を並列棒グラフ
            research_info_chart(filtered_data,combined_data)
            #TODO:別途データフレームで件数、総時間、１件あたりの時間
            st.divider()
            st.markdown("褥瘡")#個人ごとの、総時間、グラフ描画
            Jokusou_chart(filtered_data,combined_data)
            
            # 一括ダウンロードボタン
            downlad_handler(collect_all_charts_data,filtered_data,combined_data)
        elif slider == "データ加工":
            st.markdown("統合データの保存・加工")
            st.text("結合されたデータフレームを加工してダウンロードできます")
            
            st.divider()
            st.markdown("オうプションを選択してください")
            st.divider()
            
            st.sidebar.markdown("期間選択")
            date_range = st.sidebar.date_input("日付範囲を選択してください",[])
            taskname_tydir=st.toggle(label="旧ツールの業務名で統一",key="taskname_tpggle",value=False)
            filtered_data= GroupByTaskCount(combined_data).group_by_task_count(
                date_range=date_range,locate_select=None,name_select=None,taskname_tydir=taskname_tydir )
            
            change_name = 0
            st.write("名前を番号へ変換し、匿名化を行います")
            st.toggle(label="名前の匿名化",key="rename_toggle",value=False)
            if st.session_state.rename_toggle:
                change_name = 1
            st.markdown("加工データの作成とダウンロード")
            if st.button("加工データを作成",key="create_tidy_data"):
                with st.spinner("データを加工中..."):
                    tidy_df,name_mapping_df = tidy_data(filtered_data,combined_data,change_name)
                    st.dataframe(tidy_df.head())
                    if tidy_df is not None and not tidy_df.empty:
                        zip_buffer = create_df_download_package(tidy_df,name_mapping_df)
                        st.download_button(
                            label="📥 加工データをダウンロード",
                            data=zip_buffer,
                            file_name="加工データ.zip",
                            mime="application/zip"
                        )
                        st.success("✅ データを作成しました")
                    else:
                        st.warning("データの作成に失敗しました")