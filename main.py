import streamlit as st
import pandas as pd
import json
import os

# ファイルパス
DATA_FILE = "reservations.json"

# データをロード
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        return {i: None for i in range(1, 21)}

# データを保存
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# 初期設定
if "reservations" not in st.session_state:
    st.session_state["reservations"] = load_data()

# 場所リスト
locations = {
    1: "博多", 2: "開京", 3: "明州", 4: "泉州", 5: "広州",
    6: "淡水", 7: "安南", 8: "ボニ", 9: "タイ", 10: "真臘",
    11: "スル", 12: "三仏斉", 13: "ジョホール", 14: "大光国", 15: "天竺",
    16: "セイロン", 17: "ペルシャ", 18: "大食国", 19: "ミスル", 20: "末羅国"
}

st.title("予約ページ")

# データをテーブル形式で表示
data = []
for key, location in locations.items():
    current_reservation = st.session_state["reservations"].get(key)  # 修正: 辞書キーの扱いを統一
    data.append([key, location, current_reservation if current_reservation else "なし"])

df = pd.DataFrame(data, columns=["ID", "場所", "現在の予約者"])
st.table(df)

# 入力欄と操作ボタン
col1, col2, col3 = st.columns([2, 2, 2])

with col1:
    selected_id = st.selectbox("場所を選択", options=list(locations.keys()), format_func=lambda x: f"{x}. {locations[x]}")

with col2:
    name_input = st.text_input("名前を入力", key="name_input")

with col3:
    if st.button("決定"):
        if name_input:
            st.session_state["reservations"][selected_id] = name_input
            save_data(st.session_state["reservations"])  # 保存
            st.success(f"{locations[selected_id]} の予約者を {name_input} に設定しました。")
        else:
            st.warning("名前を入力してください。")

    if st.button("削除"):
        if st.session_state["reservations"].get(selected_id):
            st.session_state["reservations"][selected_id] = None
            save_data(st.session_state["reservations"])  # 保存
            st.success(f"{locations[selected_id]} の予約者を削除しました。")
        else:
            st.warning(f"{locations[selected_id]} は既に予約されていません。")
