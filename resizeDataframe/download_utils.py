import io
import zipfile
from io import BytesIO
import pandas as pd
import plotly.graph_objects as go
import platform
def get_japanese_font():
    """
    OSに応じて日本語フォントを返す
    """
    system = platform.system()
    if system == 'Windows':
        return 'Meiryo'  # Windows標準の日本語フォント
    elif system == 'Darwin':  # macOS
        return 'Hiragino Sans'  # または 'HirakakuProN-W3'
    else:  # Linux
        return 'IPAexGothic'  # または 'Noto Sans CJK JP'


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
            
            # グラフをPNG形式で保存
            if fig is not None:
                try:
                    # 明示的にライトテーマを設定して元の色を保持
                    fig_copy = go.Figure(fig)
                    fig_copy.update_layout(
                        template='plotly',  # デフォルトのカラフルなテーマを使用
                        paper_bgcolor='white',  # 背景を白に
                        plot_bgcolor='white',   # プロット領域も白に
                        font=dict(color='black',
                                family = get_japanese_font()),  # テキストを黒に
                        legend_font=dict(color='black',
                                family = get_japanese_font()),
                        
                    )
                    fig_copy.update_xaxes(
                        title_font=dict(color='black',
                                        family = get_japanese_font()),
                    )
                    fig_copy.update_yaxes(
                        color='black',
                        title_font=dict(color='black',
                                        family = get_japanese_font()),
                    )
                    img_bytes = fig_copy.to_image(format='png', width=1200, height=800)
                    zip_file.writestr(f'charts/{name}_chart.png', img_bytes)
                except Exception as e:
                    print(f"Error saving chart {name}: {e}")
            
            # データフレームをExcel形式で保存
            if df is not None and not df.empty:
                try:
                    excel_buffer = BytesIO()
                    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                        df.to_excel(writer, index=False, sheet_name=name[:31])  # Excelのシート名は31文字まで
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
