# Aggretion_tool_py

業務記録データ(CSV/Excel)を読み込み、業務名ごとの件数・時間を集計して可視化する Streamlit アプリです。

## 主な機能

- 複数ファイルの結合(結合済みデータのダウンロード)
- 病棟・担当者・期間で絞り込んだ業務名ごとの集計
- 新旧ツールの業務名の統一(旧ツールの業務名への変換、重複件数の整理)
- グラフ描画(件数、総時間、平均時間、ヒートマップ、病棟別グラフなど)
- 名前の番号変換と、名前・番号の対応表の作成
- グラフ画像(タイトル付き)とデータフレーム(Excel)の一括ダウンロード

更新履歴は `config/release_notes.py` を参照してください。

## ディレクトリ構成

| パス | 内容 |
| --- | --- |
| `main.py` | アプリのエントリーポイント |
| `view/` | 画面(UI)と業務ごとの配色定義 |
| `widgets/` | ファイル選択・ファイル結合などのウィジェット |
| `dtgroupby/` | 業務件数の集計処理 |
| `resizeDataframe/` | データ整形、グラフ描画、ダウンロード処理 |
| `models/` | 業務名リスト・新旧業務名の対応モデル |
| `config/` | リリースノートなどの設定 |

## セットアップ

Python 3.12 以上が必要です。

```bash
pip install -r requirements.txt
# または uv を使用
uv sync
```

グラフ画像の保存(kaleido)と日本語表示のため、`packages.txt` の日本語フォントと Chromium が必要です。

```bash
sudo apt install $(cat packages.txt)
```

## 起動

```bash
streamlit run main.py
```

## 主な使用ライブラリ

Streamlit, pandas, Dask, Plotly, Altair, kaleido, openpyxl, chardet
