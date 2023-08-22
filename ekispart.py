import streamlit as st
import requests

# Streamlitアプリのタイトルを設定
st.title('ルート検索アプリ')

# 駅名の入力フィールドを表示
station_name = st.text_input('駅名を入力してください')

# APIキーとURL
api_key = "test_J9XQ9fXTgaw"
api_url = "https://api.ekispert.jp/v1/json/search/course/extreme"

# グループに含まれる駅の情報
groups = {
    'A': ['渋谷', '三軒茶屋', '下高井戸'],
    'B': ['中目黒', '田園調布', '目黒'],
    'C': ['武蔵小杉', '新横浜', '菊名', '横浜'],
    'D': ['大井町', '五反田', '蒲田'],
    'E': ['自由が丘', '二子玉川', '溝の口'],
    'F': ['鷺沼', '青葉台', '長津田']
}

# get_travel_info 関数を定義
def get_travel_info(from_station, to_station):
    params = {
        'key': api_key,
        'viaList': f'{from_station}:{to_station}',
        'date': '20230818',
        'time': '0800',
        'searchType': 'departure',
    }

    res = requests.get(api_url, params=params)
    result = res.json()
    return result['ResultSet']['Course'][0]

# ルート情報を表示する関数を定義
def print_route_info(route_info):
    display_route = route_info['Teiki']['DisplayRoute']

    st.write(f"Display Route: {display_route}")
    st.write("-----")

# メインの実行部分
def main():
    if station_name:
        from_station = station_name

        min_travel_time = float('inf')
        min_travel_station = None
        min_travel_group = None

        user_station_group = None
        for group, stations in groups.items():
            if from_station in stations:
                user_station_group = group
                break

        for group, to_stations in groups.items():
            if group == user_station_group:
                continue

            for to_station in to_stations:
                travel_info = get_travel_info(from_station, to_station)
                travel_time = float(travel_info['Route']['timeOnBoard'])

                if travel_time < min_travel_time:
                    min_travel_time = travel_time
                    min_travel_station = to_station
                    min_travel_group = group

        if min_travel_station:
            route_info = get_travel_info(from_station, min_travel_station)
            print_route_info(route_info)

            excluded_groups = {min_travel_group}

            for _ in range(len(groups) - 1):
                min_to_next_time = float('inf')
                min_to_next_station = None
                min_to_next_group = None

                for group, to_stations in groups.items():
                    if group not in excluded_groups:
                        for to_station in to_stations:
                            travel_info_to_next = get_travel_info(min_travel_station, to_station)
                            travel_time_to_next = float(travel_info_to_next['Route']['timeOnBoard'])

                            if travel_time_to_next < min_to_next_time:
                                min_to_next_time = travel_time_to_next
                                min_to_next_station = to_station
                                min_to_next_group = group

                if min_to_next_station:
                    route_info_to_next = get_travel_info(min_travel_station, min_to_next_station)
                    print_route_info(route_info_to_next)
                    excluded_groups.add(min_to_next_group)
                    min_travel_station = min_to_next_station

# Streamlitアプリを実行
if __name__ == '__main__':
    main()
