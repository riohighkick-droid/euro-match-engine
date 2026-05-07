with open("app.py", "w", encoding="utf-8") as f:
    f.write("""
import streamlit as st
import pandas as pd
import random
import os
import base64

# ===== 本番エンジン STEP 1：カードデッキ =====
def make_deck():
    deck = [
        {"type": "offense", "special": "normal", "power": 6},
        {"type": "offense", "special": "super_goal", "power": 9},
        {"type": "offense", "special": "doppel_back", "power": 8},
        {"type": "defense", "special": "normal", "power": 6},
        {"type": "defense", "special": "god_hand", "power": 9},
        {"type": "speed", "special": "normal", "power": 6},
        {"type": "technique", "special": "normal", "power": 6},
        {"type": "physical", "special": "normal", "power": 6},
        {"type": "player_class", "special": "normal", "power": 6},
        {"type": "offense", "special": "hat_trick", "power": 7},
    ]
    random.shuffle(deck)
    return deck

    # ===== 本番エンジン STEP 2：5すくみ判定 =====
def judge_card_battle(home_card, away_card):
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
def play_player_match(home_player, away_player):

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
    page_icon="logo.jpeg",
    layout="wide"
)

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
    return f"[{pos}] {player_name}"
    
def pick_side(side_label, side_icon):
    st.markdown('<div class="card">', unsafe_allow_html=True)
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

    if len(teams_list) == 0:
        st.warning(f"{league} のチームはまだ登録されていません。")
        st.markdown("</div>", unsafe_allow_html=True)
        return None, [], None

    team = st.selectbox(
        f"{side_label} チームを選択",
        teams_list,
        key=f"{side_label}_team"
    )

    short_name = team_value(team, "short_name", team)

    logo_file = logo_path(short_name)
   def pick_side(side_label, side_icon):
    st.markdown('<div class="card">', unsafe_allow_html=True)
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

    if len(teams_list) == 0:
        st.warning(f"{league} のチームはまだ登録されていません。")
        st.markdown("</div>", unsafe_allow_html=True)
        return None, [], None

    team = st.selectbox(
        f"{side_label} チームを選択",
        teams_list,
        key=f"{side_label}_team"
    )

    short_name = team_value(team, "short_name", team)

    logo_file = logo_path(short_name)
    if os.path.exists(logo_file):
        st.image(logo_file, width=95)

    team_players = df[df["team"] == team]
    field = team_players[team_players["position"] != "GK"]
    gk = team_players[team_players["position"] == "GK"]

    starters = st.multiselect(
        f"{side_label} フィールド選手を6人選択",
        field["name"].tolist(),
        format_func=lambda name: player_label(team, name),
        max_selections=6,
        key=f"{side_label}_starters"
    )

    keeper = st.selectbox(
        f"{side_label} GKを選択",
        gk["name"].tolist(),
        key=f"{side_label}_gk"
    )

    st.markdown("</div>", unsafe_allow_html=True)

    return team, starters, keeper
    team_players = df[df["team"] == team]
    field = team_players[team_players["position"] != "GK"]
    gk = team_players[team_players["position"] == "GK"]

    starters = st.multiselect(
        f"{side_label} フィールド選手を6人選択",
        field["name"].tolist(),
        format_func=lambda name: player_label(team, name),
        max_selections=6,
        key=f"{side_label}_starters"
    )

    keeper = st.selectbox(
        f"{side_label} GKを選択",
        gk["name"].tolist(),
        key=f"{side_label}_gk"
    )

    st.markdown("</div>", unsafe_allow_html=True)

    return team, starters, keeper

left, right = st.columns(2)

with left:
    home_team, home_starters, home_gk = pick_side("HOME TEAM", "🏠")

with right:
    away_team, away_starters, away_gk = pick_side("AWAY TEAM", "🛫")

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

    def add_mom_points(player, pts):
        mom_points[player] = mom_points.get(player, 0) + pts

    home_short = team_value(home_team, "short_name", home_team)
    away_short = team_value(away_team, "short_name", away_team)

    home_nickname = team_value(home_team, "nickname", home_team)
    away_nickname = team_value(away_team, "nickname", away_team)

    stadium = team_value(home_team, "stadium", "")
    home_color = team_value(home_team, "team_color", "#FFD700")

    used_home_players = []
    used_away_players = []
    selected_pairs = []

    for i in range(3):
        available_home = [p for p in home_starters if p not in used_home_players]
        available_away = [p for p in away_starters if p not in used_away_players]

        home_player = random.choice(available_home)
        away_player = random.choice(available_away)

        used_home_players.append(home_player)
        used_away_players.append(away_player)

        selected_pairs.append((home_player, away_player))

    logs.append(
        f'<div style="border:3px solid {home_color}; border-radius:22px; padding:24px; margin-top:20px; margin-bottom:25px; text-align:center; background:#111827;">'
        f'<div style="font-family:Orbitron, sans-serif; font-size:46px; font-weight:900; color:#FFD700; letter-spacing:3px;">MATCH START</div>'
        f'<div style="font-family:Orbitron, sans-serif; font-size:24px; font-weight:700; color:white; margin-top:10px;">{home_short} vs {away_short}</div>'
        f'<div style="font-family:Orbitron, sans-serif; font-size:20px; color:#CCCCCC; margin-top:12px;">🏟️ {stadium}</div>'
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
            away_player
        )

        if loser not in suspended_players:
            suspended_players.append(loser)

        event = winning_card["special"] if winning_card else "save"

        logs.append('<div style="height:18px;"></div>')
        logs.append(f'<div style="border-left:6px solid {home_color}; padding-left:14px; margin-top:18px; font-size:24px; font-weight:bold; color:#FFD700;">【{minute}】</div>')
        logs.append(context)
        logs.append(f"⚔️ {player_label(home_team, home_player)} vs {player_label(away_team, away_player)}")

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

            logs.append('<div class="goal"><span>G</span><span>O</span><span>O</span><span>O</span><span>O</span><span>O</span><span>AL!!</span></div>')
            logs.append('<div class="goal">☄️ SUPER GOAL ☄️</div>')

            points = 1
            add_mom_points(attacker, 4)

            lines = [
                f"実況：これは理不尽！！{attacker}、とんでもない一撃を突き刺しました！！！",
                f"実況：スーパーゴール炸裂！！{attacker_team}、会場の空気を一変させました！！！",
                f"実況：これは止められない！！{keeper}も見送るしかありません！！！",
                f"実況：衝撃のフィニッシュ！！{attacker}、完璧に決め切りました！！！",
                f"実況：芸術的な一撃！！{attacker}が試合を動かします！！！"
            ]

            logs.append(random.choice(lines))

        elif event == "hat_trick":

            logs.append('<div class="goal"><span>G</span><span>O</span><span>O</span><span>O</span><span>O</span><span>O</span><span>AL!!</span></div>')
            logs.append('<div class="goal">👑 HAT TRICK 👑</div>')

            points = random.choice([2, 3])
            add_mom_points(attacker, 6)

            lines = [
                f"実況：止まらない{attacker}！！完全にこの時間帯の主役です！！！",
                f"実況：{attacker}、圧巻の大暴れ！！試合を支配しています！！！",
                f"実況：エースの仕事！！{attacker}が一気に流れを持っていきました！！！",
                f"実況：{attacker}が爆発！！相手守備陣、対応しきれません！！！",
                f"実況：これは大きい！！{attacker}が試合を一気に動かします！！！"
            ]

            logs.append(random.choice(lines))

        elif event == "doppel_back":

            logs.append('<div class="goal"><span>G</span><span>O</span><span>O</span><span>O</span><span>O</span><span>O</span><span>AL!!</span></div>')
            logs.append('<div class="goal">🔥 DOPPEL BACK!! 🔥</div>')

            points = 2
            add_mom_points(attacker, 5)

            lines = [
                f"実況：決まったぁぁぁ！！！ドッペルバック炸裂！！一気に2点を奪う！！！",
                f"実況：これはデカい！！{attacker}の一撃で試合が大きく動きます！！！",
                f"実況：まさかの2点級プレー！！{attacker_team}、ここで一気に突き放す！！！",
                f"実況：ドッペルバック発動！！この一撃はあまりにも重い！！！",
                f"実況：{attacker}が勝負を決めにきた！！流れを完全に掌握しました！！！"
            ]

            logs.append(random.choice(lines))

        elif event == "normal_goal" or event == "normal":

            logs.append('<div class="goal"><span>G</span><span>O</span><span>O</span><span>O</span><span>O</span><span>O</span><span>AL!!</span></div>')
            logs.append('<div class="goal">⚽ GOAL ⚽</div>')

            points = 1
            add_mom_points(attacker, 3)

            lines = [
                f"実況：{attacker}が冷静に決め切った！！！",
                f"実況：決めた！！{attacker}、落ち着いて流し込みました！！！",
                f"実況：最後はきっちり仕留めた！！{keeper}届きません！！！",
                f"実況：{attacker_team}、このチャンスを逃しませんでした！！！",
                f"実況：{attacker}が決め切った！！この一撃は大きい！！！"
            ]

            logs.append(random.choice(lines))

        elif event == "god_hand":

            logs.append('<div class="goal">🧤 GOD HAND 🧤</div>')

            points = 0
            add_mom_points(keeper, 5)

            lines = [
                f"実況：決まったかと思われたァァァ！！しかし{keeper}止めたァァァ！！！",
                f"実況：神セーブ炸裂！！{keeper}が失点濃厚の場面を救いました！！！",
                f"実況：{keeper}が立ちはだかる！！信じられない反応です！！！",
                f"実況：ゴッドハンド発動！！{attacker}の決定機を完全に封じました！！！",
                f"実況：守護神降臨！！{keeper}、ここでビッグセーブ！！！"
            ]

            logs.append(random.choice(lines))

        else:

            logs.append('<div class="goal">🧤 GREAT SAVE 🧤</div>')

            points = 0
            add_mom_points(keeper, 2)

            lines = [
                f"実況：{keeper}がしっかり防いだ！！ここはノーゴール！！",
                f"実況：抜け出した{attacker}！！しかし{keeper}が冷静に対応しました！！",
                f"実況：これは決めきれない！！{keeper}が落ち着いて処理！！！",
                f"実況：{keeper}、正面でキャッチ！！このチャンスは得点ならず！！！",
                f"実況：守護神が止めた！！{attacker_team}、追加点ならず！！！"
            ]

            logs.append(random.choice(lines))

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

    home_logo = svg_img_tag(home_short, 58)
    away_logo = svg_img_tag(away_short, 58)

    logs.append('<div style="height:35px;"></div>')
    logs.append(
        f'<div style="border:3px solid {home_color}; border-radius:22px; padding:28px; margin-top:35px; margin-bottom:20px; text-align:center; background:#111827;">'
        f'<div style="font-size:52px; font-weight:900; color:#FFD700; letter-spacing:3px;">FULL TIME</div>'
        f'<div style="display:flex; justify-content:center; align-items:center; gap:16px; font-size:56px; font-weight:900; color:white; margin-top:16px;">'
        f'<span style="width:68px; height:68px; display:flex; align-items:center; justify-content:center;">{home_logo}</span>'
        f'<span>{home_short}</span>'
        f'<span>{score_home} - {score_away}</span>'
        f'<span>{away_short}</span>'
        f'<span style="width:68px; height:68px; display:flex; align-items:center; justify-content:center;">{away_logo}</span>'
        f'</div>'
        f'</div>'
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

            if line.startswith("<div"):
                st.markdown(line, unsafe_allow_html=True)

            else:
                st.markdown(
                    f'<div class="live">{line}</div>',
                    unsafe_allow_html=True
                )

st.markdown('</div>', unsafe_allow_html=True)
""")
