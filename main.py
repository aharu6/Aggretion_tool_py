import streamlit as st
import pandas as pd
from widgets.folder_selector import FolderSelector
from widgets.join_files import JoinFiles
def main():
    st.title("Hello from aggretion-tool-py!")
    #フォルダを読み込む
    st.markdown("フォルダ選択")
    uploadfiles =st.file_uploader("フォルダを選択してください",accept_multiple_files='directory')
    
    if uploadfiles:
        st.button("集計準備開始",on_click = lambda: JoinFiles(uploadfiles).join())#データを縦にまとめる　これでメモリいっぱいになるようなら、集計結果の表示は別ウィンドウに変更する

if __name__ == "__main__":  
    main()
