import streamlit as st
import requests

# JSONBin.io API設定
API_KEY = "$2a$10$wkVzPCcsW64wR96r26OsI.HDd3ijLveJn6sxJoSjfzByIRyODPCHq"  # JSONBin.ioのAPIキー
BIN_ID = "678e24e2ad19ca34f8f14fa2"  # 作成したBinのID
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
st.title("最後どこ行く？")

# 場所の選択
location_choice = st.selectbox("予約する場所を選択してください", options=[locations[i] for i in range(1, 21)])

# 選択された場所のキーを取得
selected_location_key = [key for key, name in locations.items() if name == location_choice][0]

# 予約者追加の入力欄
new_reservation = st.text_input(f"場所 {location_choice} に予約する名前を入力")

# 予約者追加ボタン
if st.button(f"予約する - 場所 {location_choice}"):
    # 最新の予約データを再取得
    reservations = load_data()
    current_reservation = reservations[str(selected_location_key)]

    if new_reservation:
        if new_reservation in current_reservation:
            st.warning(f"{new_reservation} さんはすでに場所 {location_choice} に予約済みです。")
        else:
            current_reservation.append(new_reservation)
            save_data(reservations)
            st.success(f"{new_reservation} さんが場所 {location_choice} に予約されました。")
    else:
        st.warning("名前を入力してください。")

# 予約者削除用のセレクトボックス
reservations = load_data()  # 最新データを取得
current_reservation = reservations[str(selected_location_key)]
if current_reservation:
    remove_reservation = st.selectbox(f"削除する予約者を選んでください (場所 {location_choice})", options=[""] + current_reservation)
    if remove_reservation:
        if st.button(f"削除する - {remove_reservation} (場所 {location_choice})"):
            current_reservation.remove(remove_reservation)
            save_data(reservations)
            st.success(f"{remove_reservation} さんが場所 {location_choice} の予約から削除されました。")

# すべての場所の予約状況を表形式で表示
st.subheader("すべての場所の予約状況")
reservations = load_data()  # 最新データを取得
table_data = []

for key in locations:
    location_name = locations[key]
    current_reservation = reservations[str(key)]
    # 「絽呂」「ろろ」「ロロ」を「女神様」に変換して表示
    display_reservations = [
        "女神様" if name in {"絽呂", "ろろ", "ロロ"} else name for name in current_reservation
    ]
    reservation_list = ", ".join(current_reservation) if current_reservation else "予約者はいません"
    table_data.append([location_name, reservation_list])

# 表形式で表示
st.table(table_data)

# すべての予約をリセットするボタン
if st.button("すべての予約をリセット"):
    reservations = initialize_data()  # 初期化
    save_data(reservations)
    st.success("すべての予約をリセットしました。")
