import streamlit as st
import pandas as pd
from widgets.folder_selector import FolderSelector
from widgets.join_files import JoinFiles
def main():
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


if __name__ == "__main__":  
    main()
