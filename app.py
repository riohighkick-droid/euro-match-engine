with open("app.py", "w", encoding="utf-8") as f:
    f.write("""
import streamlit as st
import pandas as pd
import random
import os
import base64

# ===== 本番エンジン STEP 1：カードデッキ =====
def make_deck():
    deck = []

    card_types = [
        "offense",
        "defense",
        "speed",
        "technique",
        "physical",
        "player_class"
    ]

    ability_map = {
        ("defense", 6): "god_hand",
        ("offense", 6): "hat_trick",
        ("speed", 6): "hat_trick",
        ("offense", 5): "doppel_back",
        ("speed", 5): "doppel_back",
        ("physical", 6): "doppel_back",
        ("technique", 6): "doppel_back",
        ("offense", 4): "super_goal",
        ("technique", 5): "super_goal",
    }

    for card_type in card_types:
        for number in range(1, 7):
            deck.append({
                "type": card_type,
                "number": number,
                "name": f"{card_type}{number}",
                "special": ability_map.get((card_type, number), "normal"),
                "power": number
            })

    for i in range(3):
        deck.append({
            "type": "yellow_card",
            "number": i + 1,
            "name": f"yellow_card{i + 1}",
            "special": "yellow_card",
            "power": 0
        })

    random.shuffle(deck)
    return deck

    # ===== 本番エンジン STEP 2：5すくみ判定 =====
def judge_card_battle(home_card, away_card):
    if home_card["type"] == "yellow_card" and away_card["type"] == "yellow_card":
        return "draw"

    if home_card["type"] == "yellow_card":
        return "away"

    if away_card["type"] == "yellow_card":
        return "home"
        
    win_map = {
        "offense": "defense",
        "defense": "speed",
        "speed": "technique",
        "technique": "physical",
        "physical": "offense"
    }

    h = home_card["type"]
    a = away_card["type"]

    # player_class は数値勝負
    if h == "player_class" or a == "player_class":

        if home_card["power"] > away_card["power"]:
            return "home"

        elif away_card["power"] > home_card["power"]:
            return "away"

        else:
            return "draw"

    # 同タイプは数値勝負
    if h == a:

        if home_card["power"] > away_card["power"]:
            return "home"

        elif away_card["power"] > home_card["power"]:
            return "away"

        else:
            return "draw"

    # 5すくみ判定
    if win_map.get(h) == a:
        return "home"

    elif win_map.get(a) == h:
        return "away"

    return "draw"

# ===== 本番エンジン STEP 3：選手バトル =====
def play_player_match(home_player, away_player, yellow_cards, red_card_players):

    home_wins = 0
    away_wins = 0
    battle_logs = []
    winning_card = None

    home_deck = make_deck()
    away_deck = make_deck()

    while home_wins < 3 and away_wins < 3:

        if len(home_deck) == 0:
            home_deck = make_deck()

        if len(away_deck) == 0:
            away_deck = make_deck()

        home_card = home_deck.pop(0)
        away_card = away_deck.pop(0)

        result = judge_card_battle(home_card, away_card)
        for card in [home_card, away_card]:

            if card["type"] == "yellow_card":

                player_name = home_player if card == home_card else away_player

                yellow_cards[player_name] = yellow_cards.get(player_name, 0) + 1

                battle_logs.append(
                    f"🟨 YELLOW CARD - {player_name} ({yellow_cards[player_name]}/2)"
                )

                if yellow_cards[player_name] >= 2:

                    red_card_players.append(player_name)

                    battle_logs.append(
                        f"🟥 RED CARD!! {player_name} SENT OFF!"
                    )

                    red_card_lines = [
                        f"実況：{player_name}、退場です！！試合が壊れました！！",
                        f"実況：ああっと！！ {player_name} にレッドカード！！これは痛すぎる！！",
                        f"実況：主審、迷いなくレッド！！ {player_name}、一発退場です！！",
                        f"実況：最悪の展開だ！！ {player_name}、ここで退場処分！！",
                        f"実況：チームに激震！！ {player_name}、無念のレッドカード！！",
                        f"実況：これは絶望的だ！！ {player_name} がピッチを去ります！！"
                    ]

                    battle_logs.append(random.choice(red_card_lines))

                    if player_name == home_player:
                        away_wins = 3
                    else:
                        home_wins = 3
                
        if result == "home":
            home_wins += 1
            winning_card = home_card

        elif result == "away":
            away_wins += 1
            winning_card = away_card

    if home_wins >= 3:
        return "home", away_player, winning_card, battle_logs

    return "away", home_player, winning_card, battle_logs

st.set_page_config(
    page_title="EURO MATCH ENGINE - TACTICAL SIX",
    page_icon="icon.jpeg",
    layout="wide"
)
st.markdown("<style>.stApp {background: linear-gradient(135deg, #050816 0%, #111827 55%, #020617 100%); color: white;} h1,h2,h3 {color:#FFD700;} label, .stMultiSelect label, .stSelectbox label {color:#ffffff !important; font-weight:800 !important; font-size:18px !important;} .stButton button {background: linear-gradient(135deg,#FFD700,#F59E0B); color:black; font-weight:900; border:none; border-radius:14px; height:60px; font-size:34px; letter-spacing:2px; box-shadow:0 0 18px rgba(255,215,0,0.35);} .stSelectbox div[data-baseweb='select'] > div {background-color:#1f2937; color:white; border:2px solid #FFD700; border-radius:12px; min-height:50px; font-weight:700; display:flex; align-items:center; justify-content:center;} .stSelectbox input {text-align:center;} </style>", unsafe_allow_html=True)
st.markdown("<style>.goal {font-size:56px; font-weight:900; background:linear-gradient(90deg,#ff0000,#ff9900,#ffee00,#33ff00,#00ccff,#6633ff,#ff00cc); background-size:400% 400%; -webkit-background-clip:text; -webkit-text-fill-color:transparent; animation:rainbow 3s ease infinite;} @keyframes rainbow {0% {background-position:0% 50%;} 50% {background-position:100% 50%;} 100% {background-position:0% 50%;}}</style>", unsafe_allow_html=True)
st.markdown("<style>.stMarkdown {text-align:center;}</style>", unsafe_allow_html=True)
st.markdown("<style>.live {background:rgba(15,23,42,0.88); border-left:5px solid #FFD700; border-radius:14px; padding:14px 18px; margin:12px 0; font-size:18px; line-height:1.7; box-shadow:0 0 12px rgba(255,215,0,0.08); text-align:center;}</style>", unsafe_allow_html=True)
st.markdown("<style>.goal {text-align:center;}</style>", unsafe_allow_html=True)

# ===== ロゴ表示 =====
try:
        st.image("logo.jpeg", use_container_width=True)
except:
    st.markdown('<div class="main-title">EURO MATCH ENGINE</div>', unsafe_allow_html=True)


df = pd.read_csv("players.csv", encoding="utf-8-sig")
df.columns = df.columns.str.strip().str.replace(" ", "_")
team_df = pd.read_csv("teams.csv", encoding="utf-8-sig")
team_df.columns = team_df.columns.str.strip().str.replace(" ", "_")

teams = {}
def team_value(team, key, default=""):
    try:
        value = teams[team][key]
        if pd.isna(value):
            return default
        return str(value)
    except:
        return default


def logo_path(short_name):
    return f"logos/{short_name}.svg"


def svg_img_tag(short_name, size=70):
    path = logo_path(short_name)

    if not os.path.exists(path):
        return f'<span style="font-size:28px; font-weight:900;">{short_name}</span>'

    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    return (
        f'<img src="data:image/svg+xml;base64,{encoded}" '
        f'style="width:{size}px; height:{size}px; object-fit:contain; vertical-align:middle;">'
    )

for _, row in team_df.iterrows():
    teams[row["team_name"]] = {
        "short_name": row["short_name"],
        "nickname": row["nickname"],
        "stadium": row["stadium"],
        "team_color": row["team_color"],
        "sub_color": row["sub_color"],
        "league": row["league"],
        "country": row["country"]
    }

teams_by_country = {}

for country in team_df["country"].unique():
    teams_by_country[country] = sorted(
        team_df[team_df["country"] == country]["team_name"].tolist()
    )

def get_teams(country):
    return teams_by_country.get(country, [])
def get_player_position(team, player_name):
    row = df[(df["team"] == team) & (df["name"] == player_name)]
    if len(row) == 0:
        return ""
    return row.iloc[0]["position"]

def player_label(team, player_name):

    pos = get_player_position(team, player_name)

    row = df[
        (df["team"] == team) &
        (df["name"] == player_name)
    ]

    if row.empty:
        return f"[{pos}] {player_name}"

    total = int(row.iloc[0]["total"])
    role = row.iloc[0]["role"]

    return f"[{pos}] {player_name} | {total} | {role}"


    
def pick_side(side_label, side_icon):
    st.markdown(f"## {side_icon} {side_label}")

    league_list = sorted(team_df["league"].dropna().unique().tolist())

    league = st.selectbox(
        f"{side_label} リーグを選択",
        league_list,
        key=f"{side_label}_league"
    )

    teams_list = sorted(
        team_df[team_df["league"] == league]["team_name"].dropna().tolist()
    )

    team = st.selectbox(
        f"{side_label} チームを選択",
        teams_list,
        key=f"{side_label}_team"
    )

    short_name = team_value(team, "short_name", team)
    logo_file = logo_path(short_name)

    if os.path.exists(logo_file):
        logo_col1, logo_col2, logo_col3 = st.columns([1,2,1])

        with logo_col2:
            st.empty()
            st.markdown("<div style='height:50px; display:flex; align-items:center; justify-content:center;'>", unsafe_allow_html=True)
            st.image(logo_file, width=250)
            st.markdown("</div>", unsafe_allow_html=True)
            st.empty()

        
    team_players = df[df["team"] == team]
    field = team_players[team_players["position"] != "GK"]
    gk = team_players[team_players["position"] == "GK"]
    memory_key = f"{side_label}_{team}_memory"
    if memory_key not in st.session_state:
        st.session_state[memory_key] = []
    
    starters = st.multiselect(
        f"{side_label} フィールド選手を6人選択",
        field["name"].tolist(),
        format_func=lambda name: player_label(team, name),
        max_selections=6,
        key=f"{side_label}_starters"
    )
    pickup_player = st.selectbox(
        f"{side_label} PICKUP選手を選択",
        starters,
        format_func=lambda name: player_label(team, name),
        key=f"{side_label}_pickup"
    )
    
    keeper = st.selectbox(
        f"{side_label} GKを選択",
        gk["name"].tolist(),
        key=f"{side_label}_gk"
    )

    return team, starters, keeper, pickup_player

left, right = st.columns(2)

with left:
    home_team, home_starters, home_gk, home_pickup = pick_side("HOME TEAM", "🏠")

with right:
    away_team, away_starters, away_gk, away_pickup = pick_side("AWAY TEAM", "🛫")

time_zones = [
    ("前半 12分", "立ち上がり、試合の流れをつかむ最初のホットポイント。"),
    ("後半 58分", "中盤以降、均衡を破る重要な攻防。"),
    ("後半 84分", "終盤、勝敗を決めるクライマックス。")
]

special_events = ["normal_goal", "save", "super_goal", "god_hand", "hat_trick", "doppel_back"]


def play_demo_match():

    score_home = 0
    score_away = 0
    logs = []
    mom_points = {}
    suspended_players = []

    yellow_cards = {}
    red_card_players = []

    def add_mom_points(player, pts):
        mom_points[player] = mom_points.get(player, 0) + pts

    home_short = team_value(home_team, "short_name", home_team)
    away_short = team_value(away_team, "short_name", away_team)
    home_nickname = team_value(home_team, "nickname", home_team)
    away_nickname = team_value(away_team, "nickname", away_team)
    stadium = team_value(home_team, "stadium", "")
    home_color = team_value(home_team, "team_color", "#FFD700")

    used_home_players = [home_pickup]
    used_away_players = [away_pickup]

    home_selected_players = [home_pickup]
    away_selected_players = [away_pickup]

    used_home_players = [home_pickup]
    used_away_players = [away_pickup]

    for i in range(2):

        available_home = [p for p in home_starters if p not in used_home_players]
        available_away = [p for p in away_starters if p not in used_away_players]

        home_player = random.choice(available_home)
        away_player = random.choice(available_away)

        used_home_players.append(home_player)
        used_away_players.append(away_player)

        home_selected_players.append(home_player)
        away_selected_players.append(away_player)

    random.shuffle(home_selected_players)
    random.shuffle(away_selected_players)

    selected_pairs = list(zip(home_selected_players, away_selected_players))

    logs.append(
        f'<div style="border:3px solid {home_color}; border-radius:22px; padding:24px; margin-top:20px; margin-bottom:25px; text-align:center; background:#111827;">'
        f'<div style="font-size:46px; font-weight:900; color:#FFD700; letter-spacing:3px;">MATCH START</div>'
        f'<div style="font-size:24px; font-weight:700; color:white; margin-top:10px;">{home_short} vs {away_short}</div>'
        f'<div style="font-size:20px; color:#CCCCCC; margin-top:12px;">🏟️ {stadium}</div>'
        f'</div>'
    )

    logs.append(f"実況：{home_nickname}、{home_team}！！対するは、{away_nickname}、{away_team}！！")
    logs.append("実況：運命の一戦、キックオフです！！")

    logs.append('<div style="text-align:center; font-size:30px; font-weight:bold; color:#FFD700; margin-top:30px;">TODAY’S HOT POINT</div>')
    logs.append("実況：今日の勝敗を分ける注目のホットポイントはこちら！！")

    for idx, pair in enumerate(selected_pairs, start=1):
        hp, ap = pair
        logs.append(f"{idx}. {player_label(home_team, hp)} vs {player_label(away_team, ap)}")

    for i, pair in enumerate(selected_pairs):

        minute, context = time_zones[i]
        home_player, away_player = pair

        winner, loser, winning_card, battle_logs = play_player_match(
            home_player,
            away_player,
            yellow_cards,
            red_card_players
        )

        if loser not in suspended_players:
            suspended_players.append(loser)

        event = winning_card["special"] if winning_card else "save"
        points = 0

        logs.append('<div style="height:18px;"></div>')
        logs.append(f'<div style="border-left:6px solid {home_color}; padding-left:14px; margin-top:18px; font-size:24px; font-weight:bold; color:#FFD700;">【{minute}】</div>')
        logs.append(context)
        logs.append(f"⚔️ {player_label(home_team, home_player)} vs {player_label(away_team, away_player)}")

        keeper_deck = make_deck()
        keeper_card = keeper_deck.pop(0)

        if winning_card is None:
            keeper_result = "save"
        else:
            keeper_result = judge_card_battle(
                winning_card,
                keeper_card
            )

        if winner == "home":
            attacker = home_player
            attacker_team = home_team
            keeper = away_gk
            side = "home"
            opponent = away_player
        else:
            attacker = away_player
            attacker_team = away_team
            keeper = home_gk
            side = "away"
            opponent = home_player

        attacker_pos = get_player_position(attacker_team, attacker)

        if attacker_pos in ["CB", "SB", "RB", "LB", "DF"] and event in ["hat_trick", "doppel_back"]:
            event = "normal_goal"

        duel_lines = [
            f"実況：{attacker}、{opponent}との戦いを制してGKと1対1を迎えます！！！",
            f"実況：注目の攻防を制したのは{attacker}！！残るは守護神のみ！！！",
            f"実況：{attacker}が{opponent}を上回った！！決定機到来です！！！",
            f"実況：勝負どころで抜け出したのは{attacker}！！GKとの一騎打ちへ！！！",
            f"実況：{attacker}、この局面を制しました！！さあ最後の砦はGK！！！"
        ]

        logs.append(random.choice(duel_lines))
        add_mom_points(attacker, 1)

        if event == "super_goal":

            if keeper_card["special"] == "god_hand":

                logs.append('<div class="goal">🧤 GOD HAND SAVE!! 🧤</div>')

                add_mom_points(keeper, 6)

                logs.append(
                    f"実況：止めたァァァ！！ {keeper}、まさに神の右手！！"
                )

            else:

                logs.append('<div class="goal">⚽ GOOOOOAL!! ⚽</div>')
                logs.append('<div class="goal">🧪 SUPER GOAL 🧪</div>')

                points = 1

                add_mom_points(attacker, 4)

                logs.append(
                    f"実況：これは理不尽！！ {attacker}、とんでもない一撃を突き刺しました！！！"
                )

        elif event == "hat_trick":
            if keeper_result == side:

                logs.append('<div class="goal">⚽ GOOOOOAL!! ⚽</div>')
                logs.append('<div class="goal">👑 HAT TRICK 👑</div>')

                points = 3

                add_mom_points(attacker, 6)

                logs.append(
                    f"実況：止まらない{attacker}！！完全にこの時間帯の主役です！！！"
                )

            else:

                logs.append('<div class="goal">🧤 GREAT SAVE!! 🧤</div>')

                add_mom_points(keeper, 5)

                logs.append(
                    f"実況：止めたァ！！ {keeper}、奇跡のスーパーセーブ！！！"
                )
                
        elif event == "doppel_back":
            if keeper_result == side:
                logs.append('<div class="goal">⚽ GOOOOOAL!! ⚽</div>')
                logs.append('<div class="goal">🔥 DOPPEL BACK!! 🔥</div>')
                points = 2
                add_mom_points(attacker, 5)
                logs.append(
                    f"実況：決まったぁぁぁ！！！ドッペルバック炸裂！！一気に2点を奪う！！！"
                )
            else:
                logs.append('<div class="goal">🧤 GREAT SAVE!! 🧤</div>')
                add_mom_points(keeper, 4)
                logs.append(
                    f"実況：止めたァァ！！ {keeper}、2点を阻止するビッグセーブ！！！"
                )
                
        elif event == "normal_goal" or event == "normal":

            if keeper_result == side:

                logs.append('<div class="goal">⚽ GOOOOOAL!! ⚽</div>')

                points = 1

                add_mom_points(attacker, 2)

                logs.append(
                    f"実況：{attacker}、冷静に流し込みました！！"
                )

            else:

                logs.append('<div class="goal">🧤 GREAT SAVE!! 🧤</div>')

                add_mom_points(keeper, 3)

                logs.append(
                    f"実況：{keeper}！！ ビッグセーブ！！ ゴールを許しません！！"
                )

        else:
            logs.append('<div class="goal">🧤 GREAT SAVE 🧤</div>')
            points = 0
            add_mom_points(keeper, 2)
            logs.append(f"実況：{keeper}がしっかり防いだ！！ここはノーゴール！！")

        if i == 2 and points > 0:
            add_mom_points(attacker, 1)

        if side == "home":
            score_home += points
        else:
            score_away += points

        logs.append(f"現在スコア：{home_short} {score_home} - {score_away} {away_short}")

    if len(mom_points) > 0:
        mom_player = max(mom_points, key=mom_points.get)
    else:
        all_players = home_starters + away_starters + [home_gk, away_gk]
        mom_player = random.choice(all_players)

    home_logo = svg_img_tag(home_short, 130)
    away_logo = svg_img_tag(away_short, 130)

    logs.append('<div style="height:35px;"></div>')

    logs.append(
        f'''
        <div style="
            border:3px solid {home_color};
            border-radius:22px;
            padding:26px;
            margin-top:35px;
            margin-bottom:24px;
            text-align:center;
            background:#111827;
        ">
            <div style="
                font-size:46px;
                font-weight:900;
                color:#FFD700;
                letter-spacing:3px;
                margin-bottom:20px;
            ">
                FULL TIME
            </div>

            <div style="
                display:flex;
                align-items:center;
                justify-content:center;
                gap:24px;
                width:100%;
            ">
                <div style="
                    width:150px;
                    height:150px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    flex-shrink:0;
                ">
                    {home_logo}
                </div>

                <div style="
                    font-size:52px;
                    font-weight:900;
                    color:white;
                    min-width:260px;
                    text-align:center;
                ">
                    {home_short} {score_home} - {score_away} {away_short}
                </div>

                <div style="
                    width:150px;
                    height:150px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    flex-shrink:0;
                ">
                    {away_logo}
                </div>
            </div>
        </div>
        '''
    )

    logs.append('<div style="text-align:center; font-size:42px; font-weight:bold; color:#FFD700; margin-top:30px;">⭐ MAN OF THE MATCH ⭐</div>')
    logs.append(f'<div style="text-align:center; font-size:54px; font-weight:bold; color:white; margin-bottom:30px;">{mom_player}</div>')

    mom_lines = [
        f"実況：今日は完全に{mom_player}が試合を支配しました！！！",
        f"実況：文句なしのMOM！！{mom_player}、圧巻のパフォーマンスです！！！",
        f"実況：攻守に輝いた{mom_player}！！今日の主役はこの男です！！！",
        f"実況：スタジアムを沸かせたのは{mom_player}でした！！！",
        f"実況：まさにゲームチェンジャー！！MOMは{mom_player}です！！！"
    ]

    logs.append(random.choice(mom_lines))

    if suspended_players:
        logs.append(
            f'<div style="text-align:center; font-size:16px; color:#BBBBBB; margin-top:25px;">次戦出場停止：{", ".join(suspended_players)}</div>'
        )
    if red_card_players:

        logs.append(
            f'<div style="text-align:center; font-size:16px; color:#ff4444; margin-top:10px;">🟥退場。三試合出場停止 → {", ".join(red_card_players)}</div>'
        )

    return score_home, score_away, logs
st.markdown('<div class="card">', unsafe_allow_html=True)

if st.button("⚽ MATCH START", use_container_width=True):
    if home_team is None or away_team is None:
        st.error("両チームを選択してください。")
    elif home_team == away_team:
        st.error("同じチーム同士は選べません。")
    elif len(home_starters) != 6 or len(away_starters) != 6:
        st.error("両チームともフィールド選手を6人選んでください。")
    else:
        home_score, away_score, logs = play_demo_match()

        st.subheader("📢 MATCH LIVE")

        for line in logs:

            if "<div" in line or "<img" in line or "<span" in line:
                st.markdown("\\n".join([x.strip() for x in line.splitlines()]), unsafe_allow_html=True)

            elif "GOOOOO" in line or "GOAL" in line:
                st.markdown(
                    f'<div class="goal">{line}</div>',
                    unsafe_allow_html=True
                )

            else:
               st.markdown(
                   f'<div class="live">{line}</div>',
                   unsafe_allow_html=True
             )

""")
