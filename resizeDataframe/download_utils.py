import io
import zipfile
from io import BytesIO
from io import StringIO
import pandas as pd
import plotly.graph_objects as go
import platform
def get_japanese_font():
    """
    OSに応じて日本語フォントを返す
    """
    system = platform.system()
    if system == 'Windows':
        print("Detected OS: Windows")
        return 'Yu Gothic, Meiryo, MS Gothic, sans-serif'
    elif system == 'Darwin':  # macOS
        print("Detected OS: macOS")
        return 'Hiragino Sans, Hiragino Kaku Gothic ProN, Arial Unicode MS, sans-serif'
    else:  # Linux
        print("Detected OS: Linux/Other")
        return 'Noto Sans CJK JP, IPAexGothic, sans-serif'


def create_df_download_package(df,name_mapping_df=None):
    """
    データフレームをZIPファイルにまとめる
    excel形式とcsv形式両方を保存する
    """
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer,'w',zipfile.ZIP_DEFLATED) as zip_file:
        if df is not None and not df.empty:
            try:
                excel_buffer = BytesIO()
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                    df.to_excel(writer,index =False,sheet_name='結合データ')
                excel_buffer.seek(0)
                zip_file.writestr('結合データ.xlsx', excel_buffer.getvalue())
                
                ccsv_buffer = StringIO()
                df.to_csv(ccsv_buffer, index=False)
                zip_file.writestr('結合データ.csv', ccsv_buffer.getvalue())
                
                if name_mapping_df is not None and not name_mapping_df.empty:
                    name_mapping_df_buffer = BytesIO()
                    with pd.ExcelWriter(name_mapping_df_buffer,engine='openpyxl') as write:
                        name_mapping_df.to_excel(write,index=False,sheet_name='名前と番号の対応表')
                    name_mapping_df_buffer.seek(0)
                    zip_file.writestr('名前と番号の対応表.xlsx', name_mapping_df_buffer.getvalue())
                    
            except Exception as e:
                print(f"Error saving dataframe: {e}")
    zip_buffer.seek(0)
    return zip_buffer
    
def create_download_package(charts_and_data):
    """
    グラフとデータフレームをZIPファイルにまとめる
    
    Args:
        charts_and_data: list of dict with keys 'name', 'fig' (plotly figure), 'df' (pandas dataframe)
        例: [
            {'name': '1on1', 'fig': fig1, 'df': df1},
            {'name': 'NST', 'fig': fig2, 'df': df2}
        ]
    
    Returns:
        BytesIO: ZIPファイルのバイナリデータ
    """
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for item in charts_and_data:
            name = item.get('name', 'unknown')
            fig = item.get('fig')
            df = item.get('df')
            total_df = item.get('total_df')
            
            # グラフをPNG形式で保存
            if fig is not None:
                try:
                    # 明示的にライトテーマを設定して元の色を保持
                    fig_copy = go.Figure(fig)
                    japanese_font = get_japanese_font()
                    fig_copy.update_layout(
                        template='plotly',  # デフォルトのカラフルなテーマを使用
                        paper_bgcolor='white',  # 背景を白に
                        plot_bgcolor='white',   # プロット領域も白に
                        font=dict(color='black',
                                family = japanese_font),  # テキストを黒に
                        legend_font=dict(color='black',
                                family = japanese_font),
                        title=dict(text=name,font = dict(size=30)),
                        title_font_family=japanese_font,
                    )
                    fig_copy.update_xaxes(
                        title_font=dict(color='black',
                                        family = japanese_font),
                        tickfont=dict(color='black',
                                    family = japanese_font),
                    )
                    fig_copy.update_yaxes(
                        color='black',
                        title_font=dict(color='black',
                                        family = japanese_font),
                        tickfont=dict(color='black',
                                    family = japanese_font),
                    )
                    img_bytes = fig_copy.to_image(format='png', width=1920, height=1080,scale=2,engine='kaleido')
                    zip_file.writestr(f'charts/{name}_chart.png', img_bytes)
                except Exception as e:
                    print(f"Error saving chart {name}: {e}")
                    import traceback
                    traceback.print_exc()
            
            # データフレームをExcel形式で保存
            if df is not None and not df.empty:
                if total_df is not None and not total_df.empty:
                    try:
                        excel_buffer = BytesIO()
                        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                            df.to_excel(writer, index=False, sheet_name=name[:31])  # Excelのシート名は31文字まで
                            total_df.to_excel(writer, index=False, sheet_name=f"{name[:27]}_総件数・総時間")
                        excel_buffer.seek(0)
                        zip_file.writestr(f'data/{name}_data.xlsx', excel_buffer.getvalue())
                    except Exception as e:
                        print(f"Error saving dataframe {name}: {e}")
    zip_buffer.seek(0)
    return zip_buffer


def create_combined_excel(charts_and_data):
    """
    全てのデータフレームを1つのExcelファイルにまとめる
    
    Args:
        charts_and_data: list of dict with keys 'name' and 'df'
    
    Returns:
        BytesIO: Excelファイルのバイナリデータ
    """
    excel_buffer = BytesIO()
    
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        for item in charts_and_data:
            name = item.get('name', 'unknown')
            df = item.get('df')
            
            if df is not None and not df.empty:
                try:
                    # Excelのシート名は31文字まで、特殊文字を除去
                    safe_name = name[:31].replace('/', '_').replace('\\', '_')
                    df.to_excel(writer, index=False, sheet_name=safe_name)
                except Exception as e:
                    print(f"Error adding sheet {name}: {e}")
    
    excel_buffer.seek(0)
    return excel_buffer
