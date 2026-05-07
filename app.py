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
    winning_card = None

    for i in range(5):

        if len(home_deck) == 0 or len(away_deck) == 0:
            break

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
            loser = away_player
            return "home", loser, winning_card, battle_logs

        if away_wins >= 3:
            loser = home_player
            return "away", loser, winning_card, battle_logs

    if home_wins > away_wins:
        loser = away_player
        return "home", loser, winning_card, battle_logs

    elif away_wins > home_wins:
        loser = home_player
        return "away", loser, winning_card, battle_logs

    else:
        return "draw", None, None, battle_logs

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
team_df = pd.read_csv("teams.csv", encoding="utf-8-sig")
team_df.columns = team_df.columns.str.strip().str.replace(" ", "_")

teams = {}

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
    suspended_players = []

    def add_mom_points(player, pts):
        mom_points[player] = mom_points.get(player, 0) + pts

    used_home_players = []
    used_away_players = []
    selected_pairs = []

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

    home_short = teams[home_team]["short_name"]
    away_short = teams[away_team]["short_name"]

    home_nickname = teams[home_team]["nickname"]
    away_nickname = teams[away_team]["nickname"]

    stadium = teams[home_team]["stadium"]

    home_color = teams[home_team]["team_color"]
    sub_color = teams[home_team]["sub_color"]

    text_color = "#FFFFFF"

    logs.append(
        f'''
        <div style="
            background: linear-gradient(135deg, {home_color}, {sub_color});
            border-radius: 24px;
            padding: 35px;
            margin-top: 20px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 0 30px rgba(0,0,0,0.35);
        ">

            <div style="
                font-size: 54px;
                font-weight: 900;
                color: {text_color};
                letter-spacing: 4px;
                margin-bottom: 15px;
            ">
                MATCH START
            </div>

            <div style="
                font-size: 26px;
                font-weight: bold;
                color: {text_color};
                margin-bottom: 10px;
            ">
                🏟️ {stadium}
            </div>

            <div style="
                font-size: 30px;
                font-weight: bold;
                color: {text_color};
                margin-top: 20px;
            ">
                {home_nickname}　{home_team}
            </div>

            <div style="
                font-size: 22px;
                font-weight: bold;
                color: {text_color};
                margin-top: 8px;
                margin-bottom: 8px;
            ">
                VS
            </div>

            <div style="
                font-size: 30px;
                font-weight: bold;
                color: {text_color};
            ">
                {away_nickname}　{away_team}
            </div>

        </div>
        '''
    )

    logs.append(
        f"実況：{home_nickname}、{home_team}！！対するは、{away_nickname}、{away_team}！！"
    )

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

        if loser is not None and loser not in suspended_players:
            suspended_players.append(loser)

        event = winning_card["special"] if winning_card else "save"

        logs.append('<div style="height:18px;"></div>')
        stadium = teams[home_team]["stadium"]
        logs.append(
            f'<div style="text-align:center; font-size:30px; color:#CCCCCC; margin-top:10px; margin-bottom:25px;">🏟️ {stadium}</div>'
        )
        logs.append(f"【{minute}】")
        logs.append(context)
        logs.append(f"⚔️ {player_label(home_team, home_player)} vs {player_label(away_team, away_player)}")

        if winner == "home":
            attacker = home_player
            attacker_team = home_team
            keeper = away_gk
            side = "home"

        elif winner == "away":
            attacker = away_player
            attacker_team = away_team
            keeper = home_gk
            side = "away"

        else:
            draw_lines = [
                "実況：注目の攻防は互いに譲らず、ここは決着つかず！！",
                "実況：激しいぶつかり合い！！しかし最後まで崩し切れません！！",
                "実況：一進一退の攻防！！ここは両者痛み分けです！！",
                "実況：勝負は紙一重！！このホットポイントはノーゴール！！",
                "実況：互いに意地を見せましたが、ここはスコア動かず！！",
                "実況：両者一歩も引かない！！緊張感が張り詰めています！！",
                "実況：守備と攻撃が激突！！ここは互角のまま終了！！",
                "実況：素晴らしい読み合い！！互いに決定打を許しません！！",
                "実況：ここは完全に五分！！両者譲りません！！！",
                "実況：白熱の攻防！！しかし最後まで均衡破れず！！"
            ]

            logs.append(random.choice(draw_lines))
            logs.append(f"現在スコア：{home_team} {score_home} - {score_away} {away_team}")
            continue

        attacker_pos = get_player_position(attacker_team, attacker)

        if attacker_pos in ["CB", "SB", "RB", "LB", "DF"] and event in ["hat_trick", "doppel_back"]:
            event = "normal_goal"

        duel_lines = [
            f"実況：激しい競り合いを制したのは、、、{attacker}だァァァ！！！",
            f"実況：注目の攻防、最後に上回ったのは{attacker}！！！",
            f"実況：ここで抜け出したのは、、、{attacker}だァァァ！！！",
            f"実況：この局面をものにしたのは{attacker}！！流れを引き寄せます！！！",
            f"実況：勝負どころで強さを見せたのは{attacker}！！！",
            f"実況：{attacker}、この局面で圧倒的な強さを見せつけたァァァ！！！",
            f"実況：会場どよめく！！{attacker}が流れを強引に引き寄せます！！！",
            f"実況：ここで魅せた！！{attacker}、完全に主導権を握りました！！！",
            f"実況：激戦を制したのは{attacker}！！この勝負強さは本物です！！！",
            f"実況：ぶつかり合いを制圧！！{attacker}が試合を動かしました！！！"
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
                f"実況：衝撃のフィニッシュ！！{attacker}、完璧に決め切りました！！！",
                f"実況：スタジアム騒然！！{attacker}の一撃がネットを揺らしました！！！",
                f"実況：常識外れのゴール！！これは誰にも止められません！！！",
                f"実況：{attacker}、まさに一発回答！！試合を動かすスーパーゴールです！！！",
                f"実況：芸術点まで満点！！{attacker}、鮮烈なフィニッシュ！！！",
                f"実況：これはスーパー！！{attacker_team}にとって値千金の一撃です！！！"
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
                f"実況：これは大きい！！{attacker}が試合を一気に動かします！！！",
                f"実況：大暴れです！！{attacker}、止める術がありません！！！",
                f"実況：完全にゾーンに入っています！！{attacker}が試合を破壊します！！！",
                f"実況：これはエースの証明！！{attacker}が主役の座を奪いました！！！",
                f"実況：守備陣を切り裂く連続攻撃！！{attacker}が魅せます！！！",
                f"実況：今日の{attacker}は危険すぎる！！完全に止まりません！！！"
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
                f"実況：{attacker}が勝負を決めにきた！！流れを完全に掌握しました！！！",
                f"実況：これは試合の流れを壊す一撃！！ドッペルバック炸裂！！！",
                f"実況：一気に持っていった！！{attacker_team}、大きな追加点です！！！",
                f"実況：衝撃の2点プレー！！相手ベンチも呆然です！！！",
                f"実況：ドッペルバック！！これは勝敗に直結するビッグプレー！！！",
                f"実況：{attacker}、ここで特大の仕事！！試合を大きく傾けます！！！"
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
                f"実況：{attacker}が決め切った！！この一撃は大きい！！！",
                f"実況：冷静沈着！！{attacker}、きっちりゴールへ流し込みます！！！",
                f"実況：勝負強い！！{attacker}、ここでネットを揺らしました！！！",
                f"実況：チャンスを逃さない！！{attacker_team}、貴重なゴールです！！！",
                f"実況：最後の局面で落ち着いていたのは{attacker}でした！！！",
                f"実況：きましたゴール！！{attacker}、完璧な仕事です！！！"
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
                f"実況：守護神降臨！！{keeper}、ここでビッグセーブ！！！",
                f"実況：これは止めたというより消した！！{keeper}、驚異の反応！！！",
                f"実況：決定機阻止！！{keeper}がチームを救いました！！！",
                f"実況：なんという手！！{keeper}、まさにゴッドハンド！！！",
                f"実況：会場がどよめくビッグセーブ！！{keeper}が立ちはだかります！！！",
                f"実況：これは入ったと思いました！！しかし{keeper}が止めています！！！"
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
                f"実況：守護神が止めた！！{attacker_team}、追加点ならず！！！",
                f"実況：{keeper}、冷静でした！！ここはしっかりセーブ！！！",
                f"実況：シュートまで持ち込みましたが、{keeper}が読んでいました！！！",
                f"実況：最後の砦が崩れない！！{keeper}が防ぎました！！！",
                f"実況：これはGKの勝ち！！{keeper}が落ち着いて対応！！！",
                f"実況：チャンスは作ったが決まらない！！{keeper}が立ちはだかります！！！"
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
    home_short = teams[home_team]["short_name"]
    away_short = teams[away_team]["short_name"]
    logs.append(f'<div style="text-align:center; font-size:64px; font-weight:bold; color:#FFD700; margin-bottom:40px;">{home_short} {score_home} - {score_away} {away_short}</div>')
    logs.append('<div style="text-align:center; font-size:42px; font-weight:bold; color:#FFD700; margin-top:30px;">⭐ MAN OF THE MATCH ⭐</div>')
    logs.append(f'<div style="text-align:center; font-size:54px; font-weight:bold; color:white; margin-bottom:30px;">{mom_player}</div>')

    mom_lines = [
        f"実況：今日は完全に{mom_player}が試合を支配しました！！！",
        f"実況：文句なしのMOM！！{mom_player}、圧巻のパフォーマンスです！！！",
        f"実況：攻守に輝いた{mom_player}！！今日の主役はこの男です！！！",
        f"実況：スタジアムを沸かせたのは{mom_player}でした！！！",
        f"実況：まさにゲームチェンジャー！！MOMは{mom_player}です！！！",
        f"実況：この試合の象徴は{mom_player}！！堂々のMOM選出です！！！",
        f"実況：流れを変えたのは{mom_player}！！勝負どころで輝きました！！！",
        f"実況：存在感抜群！！{mom_player}がピッチの中心にいました！！！",
        f"実況：今日のヒーローは{mom_player}！！納得の選出です！！！",
        f"実況：最後まで印象を残した{mom_player}！！MOMにふさわしい活躍でした！！！"
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
