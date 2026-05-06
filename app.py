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

    round_num = 1

    while home_wins < 3 and away_wins < 3:

        home_card = home_deck.pop(0)
        away_card = away_deck.pop(0)

        result = judge_card_battle(home_card, away_card)

        battle_logs.append(
            f"{round_num}本目：{home_player} [{home_card['type']}/{home_card['special']}({home_card['power']})] "
            f"vs {away_player} [{away_card['type']}/{away_card['special']}({away_card['power']})]"
        )

        if result == "home":
            home_wins += 1
            winning_card = home_card
            battle_logs.append(f"→ {home_player} がこの攻防を制す！")

        elif result == "away":
            away_wins += 1
            winning_card = away_card
            battle_logs.append(f"→ {away_player} がこの攻防を制す！")

        else:
            battle_logs.append("→ 互角の攻防。ここは決着つかず！")

        round_num += 1

        if len(home_deck) == 0 or len(away_deck) == 0:
            break

    if home_wins > away_wins:
        loser_name = away_player
        battle_logs.append(f"ホットポイント結果：{home_wins}-{away_wins}。{home_player}が攻防を制した。")
        return "home", loser_name, winning_card, battle_logs

    elif away_wins > home_wins:
        loser_name = home_player
        battle_logs.append(f"ホットポイント結果：{away_wins}-{home_wins}。{away_player}が攻防を制した。")
        return "away", loser_name, winning_card, battle_logs

    else:
        battle_logs.append("ホットポイント結果：決着つかず。")
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

teams_by_country = {
    "イングランド": sorted(df["team"].unique().tolist()),
    "イタリア": [],
    "ドイツ": [],
    "スペイン": []
}

def get_teams(country):
    return teams_by_country.get(country, [])

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
        f"{side_label} フィールド選手を7人選択",
        field["name"].tolist(),
        max_selections=7,
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

    used_home_players = []
    used_away_players = []

    for i in range(3):

        minute, context = time_zones[i]

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

        winner, loser_name, winning_card, battle_logs = play_player_match(
            home_player,
            away_player
        )

        logs.append(f"【{minute}】")
        logs.append(context)
        logs.append(f"{home_player} vs {away_player}")

        logs.extend(battle_logs)

        event = winning_card["special"] if winning_card else "save"

        if winner == "home":
            attacker = home_player
            defender = away_player
            attacker_team = home_team
            keeper = away_gk
            side = "home"

        elif winner == "away":
            attacker = away_player
            defender = home_player
            attacker_team = away_team
            keeper = home_gk
            side = "away"

        else:
            logs.append("実況：このホットポイントは決着つかず！")
            continue

if event == "super_goal":

    logs.append('<div class="goal"><span>G</span><span>O</span><span>O</span><span>O</span><span>O</span><span>O</span><span>AL!!</span></div>')
    logs.append('<div class="goal">☄️ SUPER GOAL ☄️</div>')

    points = 1

    super_goal_lines = [
        f"実況：{attacker}のスーパーゴール！！！GKも一歩も動けない！！！",
        f"実況：これは理不尽！！{attacker}、角度のないところから突き刺しました！！！",
        f"実況：スーパーゴール炸裂！！{attacker_team}、会場の空気を一変させました！！！",
        f"実況：{attacker}が魅せた！！まさに試合を切り裂く一撃です！！！",
        f"実況：これは止められない！！{keeper}も見送るしかありません！！！"
    ]

    logs.append(random.choice(super_goal_lines))


elif event == "hat_trick":

    logs.append('<div class="goal"><span>G</span><span>O</span><span>O</span><span>O</span><span>O</span><span>O</span><span>AL!!</span></div>')
    logs.append('<div class="goal">👑 HAT TRICK 👑</div>')

    points = random.choice([2, 3])

    hat_trick_lines = [
        f"実況：{attacker}がハットトリック級の大暴れ！！！会場は完全にお祭り状態！！！",
        f"実況：止まらない{attacker}！！この時間帯の主役は完全にこの男です！！！",
        f"実況：{attacker}、圧巻の連続攻撃！！まさに試合を支配しています！！！",
        f"実況：これはエースの仕事！！{attacker}が一気に流れを持っていきました！！！",
        f"実況：{attacker}が爆発！！相手守備陣、対応しきれません！！！"
    ]

    logs.append(random.choice(hat_trick_lines))


elif event == "doppel_back":

    logs.append('<div class="goal"><span>G</span><span>O</span><span>O</span><span>O</span><span>O</span><span>O</span><span>AL!!</span></div>')
    logs.append('<div class="goal">🔥 DOPPEL BACK!! 🔥</div>')

    points = 2

    doppel_back_lines = [
        f"実況：決まったぁぁぁ！！！ドッペルバック炸裂！！一気に2点を奪う！！！",
        f"実況：これはデカい！！{attacker}のドッペルバックで試合が大きく動きます！！！",
        f"実況：まさかの2点級プレー！！{attacker_team}、ここで一気に突き放す！！！",
        f"実況：ドッペルバック発動！！この一撃はあまりにも重い！！！",
        f"実況：{attacker}が勝負を決めにきた！！ドッペルバックで流れを完全掌握！！！"
    ]

    logs.append(random.choice(doppel_back_lines))


elif event == "normal_goal" or event == "normal":

    logs.append('<div class="goal"><span>G</span><span>O</span><span>O</span><span>O</span><span>O</span><span>O</span><span>AL!!</span></div>')
    logs.append('<div class="goal">⚽ GOAL ⚽</div>')

    points = 1

    normal_goal_lines = [
        f"実況：{attacker}がGK戦を冷静に制した！！{attacker_team}に貴重なゴール！！！",
        f"実況：決めた！！{attacker}、落ち着いて流し込みました！！！",
        f"実況：{attacker}が最後はきっちり仕留めた！！{keeper}届きません！！！",
        f"実況：ゴール！！{attacker_team}、このチャンスを逃しませんでした！！！",
        f"実況：{attacker}が決め切った！！この一撃は大きい！！！"
    ]

    logs.append(random.choice(normal_goal_lines))


elif event == "god_hand":

    logs.append('<div class="goal">🧤 GOD HAND 🧤</div>')

    points = 0

    god_hand_lines = [
        f"実況：止めたぁぁぁ！！！{keeper}、まさにゴッドハンド！！！",
        f"実況：これは神セーブ！！{keeper}が失点濃厚の場面を救いました！！！",
        f"実況：{keeper}が立ちはだかる！！信じられない反応です！！！",
        f"実況：ゴッドハンド炸裂！！{attacker}の決定機を完全に封じました！！！",
        f"実況：{keeper}、ここでビッグセーブ！！流れを渡しません！！！"
    ]

    logs.append(random.choice(god_hand_lines))


else:

    logs.append('<div class="goal">🧤 GREAT SAVE 🧤</div>')

    points = 0

    save_lines = [
        f"実況：{keeper}がしっかり防いだ！ここはノーゴール！！",
        f"実況：{attacker}が抜け出したが、{keeper}が冷静に対応しました！！",
        f"実況：これは決めきれない！！{keeper}が落ち着いて処理！！！",
        f"実況：{keeper}、正面でキャッチ！！このチャンスは得点ならず！！！",
        f"実況：守護神が止めた！！{attacker_team}、追加点ならず！！！"
    ]

    logs.append(random.choice(save_lines))
if side == "home":
    score_home += points
else:
    score_away += points
logs.append(f"現在スコア：{home_team} {score_home} - {score_away} {away_team}")

    return score_home, score_away, logs

st.markdown('<div class="card">', unsafe_allow_html=True)

if st.button("⚽ MATCH START", use_container_width=True):
    if home_team is None or away_team is None:
        st.error("両チームを選択してください。")
    elif home_team == away_team:
        st.error("同じチーム同士は選べません。")
    elif len(home_starters) != 7 or len(away_starters) != 7:
        st.error("両チームともフィールド選手を7人選んでください。")
    else:
        home_score, away_score, logs = play_demo_match()

        st.markdown(
            f'<div class="score">{home_team} {home_score} - {away_score} {away_team}</div>',
            unsafe_allow_html=True
        )

        if home_score > away_score:
            st.markdown(f'<div class="result">FULL TIME</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result">{home_team} {home_score} - {away_score} {away_team}</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="live">実況：試合終了！！最後に歓喜を爆発させたのは{home_team}！！激しいホットポイントを制し、堂々の勝利です！！</div>',
                unsafe_allow_html=True
            )

        elif away_score > home_score:
            st.markdown(f'<div class="result">FULL TIME</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result">{home_team} {home_score} - {away_score} {away_team}</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="live">実況：試合終了！！敵地で勝ち切ったのは{away_team}！！終盤まで続いた激闘を制し、勝利を持ち帰ります！！</div>',
                unsafe_allow_html=True
            )

        else:
            st.markdown(f'<div class="result">FULL TIME</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result">{home_team} {home_score} - {away_score} {away_team}</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="live">実況：ここで試合終了！！両者一歩も譲らず、決着はつきません！！まさに紙一重のドローです！！</div>',
                unsafe_allow_html=True
            )

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
