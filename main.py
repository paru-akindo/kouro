import streamlit as st
import pandas as pd
import requests
import json

# JSONBin.io API設定
API_KEY = "$2a$10$wkVzPCcsW64wR96r26OsI.HDd3ijLveJn6sxJoSjfzByIRyODPCHq"  # JSONBin.ioのAPIキー
BIN_ID = "678e24e2ad19ca34f8f14fa2"  # 作成したBinのID
BASE_URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"

HEADERS = {
    "Content-Type": "application/json",
    "X-Master-Key": API_KEY
}

# 初期データ
def initialize_data():
    return {i: None for i in range(1, 21)}

# データをロード
def load_data():
    response = requests.get(BASE_URL, headers=HEADERS)
    if response.status_code == 200:
        return response.json()["record"]
    else:
        st.error("データの読み込みに失敗しました。")
        return initialize_data()

# データを保存
def save_data(data):
    # データをJSON形式でダンプして確認
    response = requests.put(BASE_URL, headers=HEADERS, json=data)
    
    if response.status_code == 200:
        st.success("データを保存しました。")
    else:
        st.error("データの保存に失敗しました。")
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
    current_reservation = st.session_state["reservations"].get(str(key), "なし")
    data.append([key, location, current_reservation])

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
            st.session_state["reservations"][str(selected_id)] = name_input
            save_data(st.session_state["reservations"])  # JSONBin.ioに保存
            st.success(f"{locations[selected_id]} の予約者を {name_input} に設定しました。")
        else:
            st.warning("名前を入力してください。")

    if st.button("削除"):
        if st.session_state["reservations"].get(str(selected_id)):
            st.session_state["reservations"][str(selected_id)] = None
            save_data(st.session_state["reservations"])  # JSONBin.ioに保存
            st.success(f"{locations[selected_id]} の予約者を削除しました。")
        else:
            st.warning(f"{locations[selected_id]} は既に予約されていません。")
