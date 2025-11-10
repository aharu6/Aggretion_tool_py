import streamlit as st

def View():
    st.title("Hello from aggretion-tool-py!")
    combined_data=None
    #フォルダを読み込む
    st.markdown("フォルダ選択")
    uploadfiles =st.file_uploader("フォルダを選択してください",accept_multiple_files='directory')
    
    if uploadfiles:
        combined_data = JoinFiles(uploadfiles).join()

    #データを縦にまとめる　これでメモリいっぱいになるようなら、集計結果の表示は別ウィンドウに変更する
    if combined_data is not None:
        st.markdown("結合結果のプレビュー")
        st.markdown("先頭10行を表示")
        st.dataframe(combined_data.head(10))

        st.markdown("全体の集計")
        st.markdown("病棟ごとの集計")
        st.markdown("個人ごとの集計")
        #個人を選択するチェックボックスを表示
        if st.checkbox("個人ごとの集計を表示"):
            # TODO: 個人ごとの集計処理を実装
            pass
