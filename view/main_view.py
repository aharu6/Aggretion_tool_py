import streamlit as st
from widgets.folder_selector import FolderSelector
from widgets.join_files import JoinFiles

def View():
    st.title("Hello from aggretion-tool-py!")
    st.markdown("ようこそ。このアプリケーションは複数のCSVファイルを結合し、集計を行うツールです。")
    st.markdown("最初にcsvファイルを含むフォルダをアップロードしてください")
    combined_data=None
    #フォルダを読み込む
    st.markdown("フォルダ選択")
    uploadfiles =st.file_uploader("フォルダを選択してください",accept_multiple_files='directory')
    
    if uploadfiles:
        combined_data = JoinFiles(uploadfiles).join()
    #TODO ファイル読み込み中のプログレスバーを表示、中に読み込んだデータを元に集計項目を作成する旨を記載
    if combined_data is not None:
        st.markdown("結合結果のプレビュー")
        st.markdown("先頭10行を表示")
        st.dataframe(combined_data.head(n=10))    

        st.multiselect(label="病棟の絞り込み",options=combined_data['locate'].unique())
        st.multiselect(label="個人名の選択",options=combined_data["phName"].unique())

        st.markdown("期間選択")

        st.markdown("全体の集計")
        #barchart

        st.markdown("病棟ごとの集計")
        if st.checkbox("病棟の選択"):
            pass  # TODO
        st.markdown("個人ごとの集計")
        #個人を選択するチェックボックスを表示
        if st.checkbox("個人ごとの集計を表示"):
            # TODO: 個人ごとの集計処理を実装 読み込んだデータから名前データを抽出してチェックボックスを生成する
            pass
        #TODO グラフの表示
        #主計に使用したデータフレームの表示
