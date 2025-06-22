import streamlit as st
import json
import os

DATA_FILE = "dictionary_data.json"

# --- 📚 データベース的な辞書定義（ジャンル付き） ---
INITIAL_DATA = {
    "permutations": {
        "ジャンル": "itertools",
        "説明": "順列（並び順をすべて出す）",
        "例": "from itertools import permutations\nlist(permutations([1,2,3]))"
    },
    "combinations": {
        "ジャンル": "itertools",
        "説明": "組み合わせ（順番は関係ない）",
        "例": "from itertools import combinations\nlist(combinations([1,2,3], 2))"
    },
    "product": {
        "ジャンル": "itertools",
        "説明": "直積（全ての要素の組み合わせ）",
        "例": "from itertools import product\nlist(product([0,1], repeat=2))"
    },
    "zip": {
        "ジャンル": "組込み関数",
        "説明": "複数のリストを並列に処理",
        "例": "for a, b in zip([1,2], ['a','b']):\n    print(a, b)"
    },
    "enumerate": {
        "ジャンル": "組込み関数",
        "説明": "リストの要素とインデックスを同時に取得",
        "例": "for i, val in enumerate(['a','b']):\n    print(i, val)"
    },
    "read_csv": {
        "ジャンル": "pandas",
        "説明": "CSVファイルをDataFrameとして読み込む",
        "例": "import pandas as pd\ndf = pd.read_csv('data.csv')"
    },
    "plot": {
        "ジャンル": "matplotlib",
        "説明": "折れ線グラフなどを描画する基本関数",
        "例": "import matplotlib.pyplot as plt\nplt.plot([1,2,3], [4,5,6])\nplt.show()"
    },
    "array": {
        "ジャンル": "numpy",
        "説明": "数値計算やベクトル処理に使う配列型",
        "例": "import numpy as np\na = np.array([1,2,3])"
    },
    "st.write": {
        "ジャンル": "Streamlit",
        "説明": "テキストや変数などを画面に出力",
        "例": "import streamlit as st\nst.write('Hello, Streamlit')"
    },
    "datetime": {
        "ジャンル": "標準ライブラリ",
        "説明": "日付や時間の操作ができる",
        "例": "import datetime\ntoday = datetime.date.today()"
    },
    "open": {
        "ジャンル": "ファイル操作",
        "説明": "ファイルの読み書きに使う基本関数",
        "例": "with open('file.txt', 'r') as f:\n    content = f.read()"
    }
}
# --- JSONファイルから読み込む or 初期化して保存 ---
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        dictionary = json.load(f)
else:
    dictionary = INITIAL_DATA.copy()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(dictionary, f, ensure_ascii=False, indent=2)


# --- 🎨 UI構成 ---
st.set_page_config(page_title="Python辞書アプリ", layout="centered")
st.title("🧠 Python構文・ライブラリ辞書")

query = st.text_input("🔍 キーワードを検索", "")

if query:
    entry = dictionary.get(query)
    if entry:
        st.subheader(f"🔎 {query}")
        st.write("📂 ジャンル:", entry.get("ジャンル", "未分類"))
        st.write("📘 説明:", entry["説明"])
        st.code(entry["例"], language="python")
    else:
        st.warning("そのキーワードは辞書に登録されていません。")


# --- 既存の辞書表示処理ここまで ---

# --- 🔧 新しい辞書エントリを追加（←これを最上部に移動） ---
with st.expander("➕ 新しい言葉を追加"):
    with st.form("new_entry_form"):
        key = st.text_input("🔑 キーワード")
        explanation = st.text_area("📖 説明")
        example = st.text_area("💻 例（Pythonコード）")
        genre = st.text_input("📁 ジャンル（例: itertools, pandas, numpy など）", value="未分類")
        submitted = st.form_submit_button("登録")

    if submitted:
        if key in dictionary:
            st.warning(f"⚠️ '{key}' はすでに登録されています。")
        else:
            dictionary[key] = {
                "説明": explanation,
                "例": example,
                "ジャンル": genre
            }
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(dictionary, f, ensure_ascii=False, indent=2)
            st.success(f"✅ '{key}' を辞書に登録しました！")
            st.rerun()

# --- 🔁 全表示 & 削除処理 ---
st.subheader("📂 ジャンル別で表示")
all_genres = sorted(set(entry.get("ジャンル", "未分類") for entry in dictionary.values()))
selected_genre = st.selectbox(
    "ジャンルを選択", 
    ["すべて"] + all_genres, 
    key="genre_select"
)


delete_key = None  # ← 削除対象を覚える

delete_key = None  # ← 削除対象を記憶

# 辞書をリスト化して順番固定（動的削除でも安全）
for key, val in list(dictionary.items()):
    if selected_genre != "すべて" and val.get("ジャンル", "未分類") != selected_genre:
        continue

    st.markdown(f"### 🧩 {key}")
    st.write("📂 ジャンル:", val.get("ジャンル", "未分類"))
    st.write("📘 説明:", val["説明"])
    st.code(val["例"], language="python")

    if st.button(f"🗑 {key} を削除", key=f"delete_{key}"):
        delete_key = key
    # 編集対象を保持（セッションで管理）
    if "edit_key" not in st.session_state:
        st.session_state["edit_key"] = None

    # 編集ボタンの処理
    if st.button(f"✏️ {key} を編集", key=f"edit_{key}"):
        st.session_state["edit_key"] = key
        st.rerun()

    # 編集フォームの表示
    if st.session_state["edit_key"] == key:
        with st.form(f"edit_form_{key}"):
            new_key = st.text_input("🔑 キーワード", value=key)
            new_explanation = st.text_area("📖 説明", value=val["説明"])
            new_example = st.text_area("💻 例（Pythonコード）", value=val["例"])
            new_genre = st.selectbox("📁 ジャンル", ["未分類", "標準", "itertools", "pandas"], index=0)

            save = st.form_submit_button("保存")
            if save:
                # キー名が変わっていたら削除→追加
                if new_key != key:
                    dictionary[new_key] = dictionary.pop(key)
                dictionary[new_key].update({
                    "説明": new_explanation,
                    "例": new_example,
                    "ジャンル": new_genre
                })
                with open(DATA_FILE, "w", encoding="utf-8") as f:
                    json.dump(dictionary, f, ensure_ascii=False, indent=2)
                st.session_state["edit_key"] = None
                st.success(f"✅ '{new_key}' を更新しました！")
                st.rerun()

    st.markdown("---")

# --- 実際に削除実行 ---
if delete_key:
    del dictionary[delete_key]
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(dictionary, f, ensure_ascii=False, indent=2)
    st.success(f"✅ '{delete_key}' を削除しました！")
    st.rerun()
