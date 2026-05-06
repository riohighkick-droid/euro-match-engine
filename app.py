
import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="EURO MATCH ENGINE - TACTICAL SIX", layout="wide")

st.markdown("""
<style>
.stApp {
    background: #030303;
    color: #f8fafc;
}

.big-title {
    text-align: center;
    font-size: 76px;
    font-weight: 900;
    letter-spacing: 5px;
    color: #ffffff;
    margin-top: 20px;
    margin-bottom: 0px;
}

.sub-title {
    text-align: center;
    font-size: 26px;
    color: #facc15;
    letter-spacing: 4px;
    margin-bottom: 35px;
}

.card {
    background: #111827;
    border: 1px solid #374151;
    border-radius: 18px;
    padding: 24px;
    margin-bottom: 24px;
}

.team-title {
    font-size: 30px;
    font-weight: 900;
    color: #facc15;
    margin-bottom: 15px;
}

.score {
    text-align: center;
    font-size: 56px;
    font-weight: 900;
    color: #facc15;
    margin-bottom: 20px;
}

.result {
    text-align: center;
    font-size: 34px;
    font-weight: 900;
    color: white;
    margin-bottom: 30px;
}

.live {
    background: #020617;
    border-left: 5px solid #facc15;
    padding: 14px 18px;
    margin: 10px 0;
    border-radius: 8px;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">EURO MATCH ENGINE</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">TACTICAL SIX</div>', unsafe_allow_html=True)

df = pd.read_csv("players.csv", encoding="utf-8-sig")
df.columns = df.columns.str.strip().str.replace(" ", "_")

# 今はteam列から全部取得。国列がない間はイングランドに全部入れる
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
    st.markdown(f'<div class="team-title">{side_icon} {side_label}</div>', unsafe_allow_html=True)

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

special_events = ["normal_goal", "save", "super_goal", "god_hand", "hat_trick"]

def play_demo_match():
    score_home = 0
    score_away = 0
    logs = []

    for i in range(3):
        minute, context = time_zones[i]

        home_player = random.choice(home_starters)
        away_player = random.choice(away_starters)

        home_wins = random.choice([True, False])
        event = random.choice(special_events)

        logs.append(f"【{minute}】")
        logs.append(context)
        logs.append(f"{home_player} vs {away_player}")

        if home_wins:
            attacker = home_player
            defender = away_player
            attacker_team = home_team
            keeper = away_gk
            side = "home"
        else:
            attacker = away_player
            defender = home_player
            attacker_team = away_team
            keeper = home_gk
            side = "away"

        set_score = random.choice(["3-0", "3-1", "3-2"])
        logs.append(f"ホットポイント結果：{set_score}。{attacker}が攻防を制した。")
        logs.append(f"次戦出場停止：{defender}")

        if event == "super_goal":
            logs.append(f"実況：出たーーー！！{attacker}のスーパーゴール！！")
            logs.append("実況：GKのポジション、相手のカード、すべてを置き去りにする理不尽な一撃！！")
            points = 1

        elif event == "god_hand":
            logs.append(f"実況：止めたーーー！！{keeper}、まさにゴッドハンド！！")
            logs.append("実況：これは失点を覚悟した場面、しかし最後の砦が奇跡的に立ちはだかりました！！")
            points = 0

        elif event == "hat_trick":
            points = random.choice([2, 3])
            logs.append(f"実況：{attacker}、ここでハットトリック級の決定力！！")
            logs.append(f"実況：一撃で{points}点級の価値を持つビッグプレー！！試合の流れが大きく動きます！！")

        elif event == "normal_goal":
            logs.append(f"実況：{attacker}がGK戦を冷静に制した！")
            logs.append(f"実況：{attacker_team}、貴重なゴールを奪います！！")
            points = 1

        else:
            logs.append(f"実況：{attacker}が抜け出したが、{keeper}が冷静に対応！")
            logs.append("実況：ここはノーゴール。まだ試合は分かりません。")
            points = 0

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
            st.markdown(f'<div class="result">{home_team} WIN</div>', unsafe_allow_html=True)
        elif away_score > home_score:
            st.markdown(f'<div class="result">{away_team} WIN</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="result">DRAW</div>', unsafe_allow_html=True)

        st.subheader("🎙️ MATCH LIVE")

        for line in logs:
            st.markdown(f'<div class="live">{line}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
