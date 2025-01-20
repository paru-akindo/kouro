import streamlit as st

# 初期設定
if "reservations" not in st.session_state:
    st.session_state["reservations"] = {
        1: None, 2: None, 3: None, 4: None, 5: None, 
        6: None, 7: None, 8: None, 9: None, 10: None,
        11: None, 12: None, 13: None, 14: None, 15: None, 
        16: None, 17: None, 18: None, 19: None, 20: None
    }

# 場所リスト
locations = {
    1: "博多", 2: "開京", 3: "明州", 4: "泉州", 5: "広州",
    6: "淡水", 7: "安南", 8: "ボニ", 9: "タイ", 10: "真臘",
    11: "スル", 12: "三仏斉", 13: "ジョホール", 14: "大光国", 15: "天竺",
    16: "セイロン", 17: "ペルシャ", 18: "大食国", 19: "ミスル", 20: "末羅国"
}

st.title("予約ページ")

# 各場所の予約管理
for key, location in locations.items():
    col1, col2, col3, col4 = st.columns([2, 3, 3, 2])
    
    # 場所名表示
    col1.write(f"{key}. {location}")
    
    # 名前入力欄
    name_input = col2.text_input(f"名前を入力 ({location})", key=f"input_{key}")
    
    # 現在の予約者表示
    current_reservation = st.session_state["reservations"][key]
    col3.write(f"現在の予約者: {current_reservation if current_reservation else 'なし'}")
    
    # 決定ボタン
    if col4.button("決定", key=f"decide_{key}"):
        if name_input:
            st.session_state["reservations"][key] = name_input
            st.success(f"{location} の予約者を {name_input} に設定しました。")
        else:
            st.warning("名前を入力してください。")
    
    # 削除ボタン
    if col4.button("削除", key=f"delete_{key}"):
        if st.session_state["reservations"][key]:
            st.session_state["reservations"][key] = None
            st.success(f"{location} の予約者を削除しました。")
        else:
            st.warning(f"{location} は既に予約されていません。")
