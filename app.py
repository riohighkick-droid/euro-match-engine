with open("app.py", "w", encoding="utf-8") as f:
    f.write("""
import streamlit as st
import pandas as pd
import random

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

    home_deck = make_deck()
    away_deck = make_deck()

    home_wins = 0
    away_wins = 0

    battle_logs = []
    losers = []

    for i in range(3):

        home_card = home_deck[i]
        away_card = away_deck[i]

        result = judge_card_battle(home_card, away_card)

        battle_logs.append(
            f"{home_player} [{home_card['type']}:{home_card['power']}] "
            f"vs "
            f"{away_player} [{away_card['type']}:{away_card['power']}]"
        )

        if result == "home":
            home_wins += 1
            .append(f"→ {home_player} WIN!")
            losers.append(away_player)

        elif result == "away":
            away_wins += 1
            .append(f"→ {away_player} WIN!")
            losers.append(home_player)

        else:
            .append("→ DRAW")

    if home_wins > away_wins:
        return "home", , home_card, losers

    elif away_wins > home_wins:
        return "away", , away_card, losers

    else:
        return "draw", , None, losers

st.set_page_config(
    page_title="EURO MATCH ENGINE - TACTICAL SIX",
    page_icon="logo.jpeg",
    layout="wide"
)

st.markdown(\"\"\"
<style>
.stApp {
    background: #050505;
    color: #f8fafc;
}

div[role="listbox"] {
    background-color: white !important;
}

div[role="option"] {
    color: black !important;
    background-color: white !important;
    font-size: 18px !important;
    font-weight: 700 !important;
}

div[role="option"]:hover {
    background-color: #facc15 !important;
    color: black !important;
}


.logo-area {
    text-align: center;
    margin-top: 10px;
    margin-bottom: 20px;
}

.main-title {
    text-align: center;
    font-size: 64px;
    font-weight: 900;
    letter-spacing: 4px;
    color: #ffffff;
    margin-bottom: 0px;
}

.sub-title {
    text-align: center;
    font-size: 24px;
    color: #facc15;
    letter-spacing: 4px;
    margin-bottom: 35px;
}

.card {
    background: transparent;
    border: none;
    border-radius: 18px;
    padding: 0px;
    margin-bottom: 26px;
}

h1, h2, h3, p, label,  {
    color: #f8fafc !important;
}

.stSelectbox label,
.stMultiSelect label {
    font-size: 18px !important;
    font-weight: 800 !important;
    color: #facc15 !important;
}

.stSelectbox div[data-baseweb="select"] > div {
    color: black !important;
    background-color: white !important;
    font-weight: 700 !important;
}

.stMultiSelect div[data-baseweb="select"] > div {
    color: black !important;
    background-color: white !important;
    font-weight: 700 !important;
}

.score {
    text-align: center;
    font-size: 54px;
    font-weight: 900;
    color: #facc15;
    margin: 24px 0;
}

.result {
    text-align: center;
    font-size: 34px;
    font-weight: 900;
    color: #ffffff;
    margin-bottom: 30px;
}

.live {
    background: #020617;
    border-left: 6px solid #facc15;
    padding: 16px 20px;
    margin: 12px 0;
    border-radius: 10px;
    font-size: 20px;
    line-height: 1.7;
}

div.stButton > button {
    background: linear-gradient(90deg, #facc15, #f59e0b);
    color: #050505 !important;
    font-size: 28px;
    font-weight: 900;
    border-radius: 14px;
    padding: 18px 30px;
    border: none;
    box-shadow: 0 0 24px rgba(250, 204, 21, 0.45);
}

div.stButton > button:hover {
    background: linear-gradient(90deg, #fde047, #facc15);
    color: #000000 !important;
    transform: scale(1.02);
}

div[data-baseweb="select"] input {
    color: black !important;
}

input {
    color: black !important;
}

textarea {
    color: black !important;
}

.goal {
    text-align: center;
    font-size: 42px;
    font-weight: 900;
    letter-spacing: 4px;
    margin: 18px 0;
    padding: 18px;
    border-radius: 18px;
    background: #000000;
    animation: pulse 0.8s infinite alternate;
}

.goal span:nth-child(1) { color: #3b82f6; }
.goal span:nth-child(2) { color: #22c55e; }
.goal span:nth-child(3) { color: #84cc16; }
.goal span:nth-child(4) { color: #eab308; }
.goal span:nth-child(5) { color: #f97316; }
.goal span:nth-child(6) { color: #ef4444; }
.goal span:nth-child(7) { color: #ffffff; }

@keyframes pulse {
    from {
        transform: scale(1);
        text-shadow: 0 0 8px #facc15;
    }
    to {
        transform: scale(1.04);
        text-shadow: 0 0 24px #facc15;
    }
}

</style>
\"\"\", unsafe_allow_html=True)

# ===== ロゴ表示 =====
try:
        st.image("logo.jpeg", use_container_width=True)
except:
    st.markdown('<div class="main-title">EURO MATCH ENGINE</div>', unsafe_allow_html=True)


df = pd.read_csv("players.csv", encoding="utf-8-sig")
df.columns = df.columns.str.strip().str.replace(" ", "_")

teams_by_country = {
    "イングランド": sorted(df["team"].unique().tolist()),
    "イタリア": [],
    "ドイツ": [],
    "スペイン": []
}

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

    country = st.selectbox(
        f"{side_label} 国を選択",
        ["イングランド", "イタリア", "ドイツ", "スペイン"],
        key=f"{side_label}_country"
    )

    teams = get_teams(country)

    if len(teams) == 0:
        st.warning(f"{country}のチームはまだ登録されていません。")
        st.markdown('</div>', unsafe_allow_html=True)
        return None, [], None

    team = st.selectbox(
        f"{side_label} チームを選択",
        teams,
        key=f"{side_label}_team"
    )

    team_df = df[df["team"] == team]
    field = team_df[team_df["position"] != "GK"]
    gk = team_df[team_df["position"] == "GK"]

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

    st.markdown('</div>', unsafe_allow_html=True)
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

    def add_mom_points(player, pts):
        mom_points[player] = mom_points.get(player, 0) + pts

    used_home_players = []
    used_away_players = []
    selected_pairs = []
    suspended_players = []

    for i in range(3):

        available_home = [p for p in home_starters if p not in used_home_players]
        available_away = [p for p in away_starters if p not in used_away_players]

        if not available_home:
            used_home_players = []
            available_home = home_starters

        if not available_away:
            used_away_players = []
            available_away = away_starters

        home_player = random.choice(available_home)
        away_player = random.choice(available_away)

        used_home_players.append(home_player)
        used_away_players.append(away_player)

        selected_pairs.append((home_player, away_player))

    logs.append('<div style="text-align:center; font-size:34px; font-weight:bold; color:#FFD700; margin-top:20px;">MATCH START</div>')
    logs.append(f"実況：{home_team}！！対するは、{away_team}！！")
    logs.append("実況：運命の一戦、キックオフです！！")

    logs.append('<div style="text-align:center; font-size:30px; font-weight:bold; color:#FFD700; margin-top:30px;">TODAY’S HOT POINT</div>')
    logs.append("実況：今日の勝敗を分ける注目のホットポイントはこちら！！")

    for idx, pair in enumerate(selected_pairs, start=1):
        hp, ap = pair
        logs.append(f"{idx}. {player_label(home_team, hp)} vs {player_label(away_team, ap)}")

    for i, pair in enumerate(selected_pairs):

        minute, context = time_zones[i]
        home_player, away_player = pair

        winner, battle_logs, winning_card, losers = play_player_match(
            home_player,
            away_player
        )

        event = winning_card["special"] if winning_card else "save"

        logs.append('<div style="height:18px;"></div>')
        logs.append(f"【{minute}】")
        logs.append(context)
        logs.append(f"⚔️ {player_label(home_team, home_player)} vs {player_label(away_team, away_player)}")

        if winner == "home":
            attacker = home_player
            attacker_team = home_team
            keeper = away_gk
            side = "home"

            suspended_players.append(away_player)

        elif winner == "away":
            attacker = away_player
            attacker_team = away_team
            keeper = home_gk
            side = "away"

            suspended_players.append(home_player)

        else:
            draw_lines = [
                "実況：注目の攻防は互いに譲らず、ここは決着つかず！！",
                "実況：激しいぶつかり合い！！しかし最後まで崩し切れません！！",
                "実況：一進一退の攻防！！ここは両者痛み分けです！！",
                "実況：勝負は紙一重！！このホットポイントはノーゴール！！",
                "実況：互いに意地を見せましたが、ここはスコア動かず！！"
            ]
            logs.append(random.choice(draw_lines))
            logs.append(f"現在スコア：{home_team} {score_home} - {score_away} {away_team}")
            continue

        duel_lines = [
            f"実況：激しい競り合いを制したのは、、、{attacker}だァァァ！！！",
            f"実況：注目の攻防、最後に上回ったのは{attacker}！！！",
            f"実況：ここで抜け出したのは、、、{attacker}だァァァ！！！",
            f"実況：この局面をものにしたのは{attacker}！！流れを引き寄せます！！！",
            f"実況：勝負どころで強さを見せたのは{attacker}！！！"
        ]

        logs.append(random.choice(duel_lines))
        add_mom_points(attacker, 1)

        if event == "super_goal":

            logs.append('<div class="goal"><span>G</span><span>O</span><span>O</span><span>O</span><span>O</span><span>O</span><span>AL!!</span></div>')
            logs.append('<div class="goal">☄️ SUPER GOAL ☄️</div>')

            points = 1
            add_mom_points(attacker, 4)

            super_goal_lines = [
                f"実況：これは理不尽！！{attacker}、とんでもない一撃を突き刺しました！！！",
                f"実況：スーパーゴール炸裂！！{attacker_team}、会場の空気を一変させました！！！",
                f"実況：{attacker}が魅せた！！まさに試合を切り裂く一撃です！！！",
                f"実況：これは止められない！！{keeper}も見送るしかありません！！！",
                f"実況：衝撃のフィニッシュ！！{attacker}、完璧に決め切りました！！！"
            ]

            logs.append(random.choice(super_goal_lines))

        elif event == "hat_trick":

            logs.append('<div class="goal"><span>G</span><span>O</span><span>O</span><span>O</span><span>O</span><span>O</span><span>AL!!</span></div>')
            logs.append('<div class="goal">👑 HAT TRICK 👑</div>')

            points = random.choice([2, 3])
            add_mom_points(attacker, 6)

            hat_trick_lines = [
                f"実況：止まらない{attacker}！！完全にこの時間帯の主役です！！！",
                f"実況：{attacker}、圧巻の大暴れ！！試合を支配しています！！！",
                f"実況：エースの仕事！！{attacker}が一気に流れを持っていきました！！！",
                f"実況：{attacker}が爆発！！相手守備陣、対応しきれません！！！",
                f"実況：これは大きい！！{attacker}が試合を一気に動かします！！！"
            ]

            logs.append(random.choice(hat_trick_lines))

        elif event == "doppel_back":

            logs.append('<div class="goal"><span>G</span><span>O</span><span>O</span><span>O</span><span>O</span><span>O</span><span>AL!!</span></div>')
            logs.append('<div class="goal">🔥 DOPPEL BACK!! 🔥</div>')

            points = 2
            add_mom_points(attacker, 5)

            doppel_back_lines = [
                f"実況：決まったぁぁぁ！！！ドッペルバック炸裂！！一気に2点を奪う！！！",
                f"実況：これはデカい！！{attacker}の一撃で試合が大きく動きます！！！",
                f"実況：まさかの2点級プレー！！{attacker_team}、ここで一気に突き放す！！！",
                f"実況：ドッペルバック発動！！この一撃はあまりにも重い！！！",
                f"実況：{attacker}が勝負を決めにきた！！流れを完全に掌握しました！！！"
            ]

            logs.append(random.choice(doppel_back_lines))

        elif event == "normal_goal" or event == "normal":

            logs.append('<div class="goal"><span>G</span><span>O</span><span>O</span><span>O</span><span>O</span><span>O</span><span>AL!!</span></div>')
            logs.append('<div class="goal">⚽ GOAL ⚽</div>')

            points = 1
            add_mom_points(attacker, 3)

            normal_goal_lines = [
                f"実況：{attacker}が冷静に決め切った！！！",
                f"実況：決めた！！{attacker}、落ち着いて流し込みました！！！",
                f"実況：最後はきっちり仕留めた！！{keeper}届きません！！！",
                f"実況：{attacker_team}、このチャンスを逃しませんでした！！！",
                f"実況：{attacker}が決め切った！！この一撃は大きい！！！"
            ]

            logs.append(random.choice(normal_goal_lines))

        elif event == "god_hand":

            logs.append('<div class="goal">🧤 GOD HAND 🧤</div>')

            points = 0
            add_mom_points(keeper, 5)

            god_hand_lines = [
                f"実況：決まったかと思われたァァァ！！しかし{keeper}止めたァァァ！！！",
                f"実況：神セーブ炸裂！！{keeper}が失点濃厚の場面を救いました！！！",
                f"実況：{keeper}が立ちはだかる！！信じられない反応です！！！",
                f"実況：ゴッドハンド発動！！{attacker}の決定機を完全に封じました！！！",
                f"実況：守護神降臨！！{keeper}、ここでビッグセーブ！！！"
            ]

            logs.append(random.choice(god_hand_lines))

        else:

            logs.append('<div class="goal">🧤 GREAT SAVE 🧤</div>')

            points = 0
            add_mom_points(keeper, 2)

            save_lines = [
                f"実況：{keeper}がしっかり防いだ！！ここはノーゴール！！",
                f"実況：抜け出した{attacker}！！しかし{keeper}が冷静に対応しました！！",
                f"実況：これは決めきれない！！{keeper}が落ち着いて処理！！！",
                f"実況：{keeper}、正面でキャッチ！！このチャンスは得点ならず！！！",
                f"実況：守護神が止めた！！{attacker_team}、追加点ならず！！！"
            ]

            logs.append(random.choice(save_lines))

        if i == 2 and points > 0:
            add_mom_points(attacker, 1)

        if side == "home":
            score_home += points
        else:
            score_away += points

        logs.append(f"現在スコア：{home_team} {score_home} - {score_away} {away_team}")

    if len(mom_points) > 0:
        mom_player = max(mom_points, key=mom_points.get)
    else:
        all_players = home_starters + away_starters + [home_gk, away_gk]
        mom_player = random.choice(all_players)

    logs.append('<div style="height:35px;"></div>')
    logs.append('<div style="text-align:center; font-size:52px; font-weight:bold; color:#FFD700; margin-top:40px; margin-bottom:20px;">FULL TIME</div>')
    logs.append(f'<div style="text-align:center; font-size:64px; font-weight:bold; color:#FFD700; margin-bottom:40px;">{home_team} {score_home} - {score_away} {away_team}</div>')
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
