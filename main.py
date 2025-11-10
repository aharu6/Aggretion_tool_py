import streamlit as st
import pandas as pd
from widgets.folder_selector import FolderSelector
from widgets.join_files import JoinFiles
from view.main_view import View
st.set_page_config(layout="wide")
def main():
    View()

if __name__ == "__main__":  
    main()
