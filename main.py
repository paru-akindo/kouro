import streamlit as st
import requests

# JSONBin.io API設定
API_KEY = "YOUR_JSONBIN_API_KEY"  # JSONBin.ioのAPIキー
BIN_ID = "YOUR_BIN_ID"  # 作成したBinのID
BASE_URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"

HEADERS = {
    "Content-Type": "application/json",
    "X-Master-Key": API_KEY
}

# 場所の情報
locations = {
    1: "博多", 2: "開京", 3: "明州", 4: "泉州", 5: "広州",
    6: "淡水", 7: "安南", 8: "ボニ", 9: "タイ", 10: "真臘",
    11: "スル", 12: "三仏斉", 13: "ジョホール", 14: "大光国", 15: "天竺",
    16: "セイロン", 17: "ペルシャ", 18: "大食国", 19: "ミスル", 20: "末羅国"
}

# 初期データの設定（空のリストを各場所に設定）
def initialize_data():
    return {str(i): [] for i in range(1, 21)}  # 1から20の場所に空のリストを設定

# データを保存する関数
def save_data(data):
    response = requests.put(BASE_URL, headers=HEADERS, json=data)
    if response.status_code == 200:
        st.success("データを保存しました。")
    else:
        st.error(f"データの保存に失敗しました: {response.text}")

# データを読み込む関数
def load_data():
    response = requests.get(BASE_URL, headers=HEADERS)
    if response.status_code == 200:
        return response.json()["record"]
    else:
        st.error(f"データの読み込みに失敗しました: {response.text}")
        return initialize_data()

# アプリのタイトル
st.title("予約システム")

# 予約データの読み込み
reservations = load_data()

# 各場所の予約フォーム
for key in reservations:
    location_name = locations[key]  # 場所の名前を取得
    st.subheader(f"場所 {key} - {location_name}")  # 場所名を表示
    current_reservation = reservations[key]
    
    # 予約者追加用の入力欄
    new_reservation = st.text_input(f"場所 {location_name} に予約する名前を入力", key=f"input_{key}")
    
    # 予約者追加ボタン
    if st.button(f"予約する - 場所 {location_name}", key=f"book_{key}"):
        if new_reservation:
            current_reservation.append(new_reservation)
            save_data(reservations)
            st.success(f"{new_reservation} さんが場所 {location_name} に予約されました。")
        else:
            st.warning("名前を入力してください。")
    
    # 予約者表示
    if current_reservation:
        st.write("現在の予約者:", ", ".join(current_reservation))
        
        # 予約者削除用のセレクトボックス
        remove_reservation = st.selectbox(f"削除する予約者を選んでください (場所 {location_name})", options=[""] + current_reservation, key=f"remove_{key}")
        if remove_reservation:
            if st.button(f"削除する - {remove_reservation} (場所 {location_name})", key=f"remove_button_{key}"):
                current_reservation.remove(remove_reservation)
                save_data(reservations)
                st.success(f"{remove_reservation} さんが場所 {location_name} の予約から削除されました。")
