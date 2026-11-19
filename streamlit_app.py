"""
ELITE ARENA — Streamlit UI
Connect this file to your existing OOP classes.

IMPORTANT:
1) Change the import below to the filename that contains your OOP classes.
2) Keep your OOP classes in a separate Python file.
3) Run: streamlit run streamlit_app.py
"""

import streamlit as st
import pandas as pd
from datetime import datetime

# CHANGE "main" to the name of your Python file (without .py) containing the classes.
# Example: if your classes are in football_project.py, use:
# from football_project import Tournament, Team, HumanPlayer
from main import Tournament, Team, HumanPlayer


# ---------------------------- PAGE CONFIG -----------------------------------
st.set_page_config(
    page_title="Elite Arena | Football League",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------- DESIGN -------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root { --ea-bg: #0b1220; --ea-card: #121d30; --ea-card2: #17243a;
        --ea-line: #26354b; --ea-green: #a3e635; --ea-text: #f3f6fb;
        --ea-muted: #9aa9bf; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: radial-gradient(ellipse at 15% 0%, #182943 0%, #0b1220 46%); color: var(--ea-text); }
.block-container { padding-top: 1.4rem; padding-bottom: 2.4rem; max-width: 1500px; }
[data-testid="stSidebar"] { background: #0d1727; border-right: 1px solid #223149; }
[data-testid="stSidebar"] * { color: #e9eef8; }
.ea-brand { font-size: 1.6rem; font-weight: 800; letter-spacing: .06em; color: #f7fafc; }
.ea-brand span { color: var(--ea-green); }
.ea-kicker { color: var(--ea-green); text-transform: uppercase; letter-spacing: .17em;
             font-size: .72rem; font-weight: 800; margin-bottom: .35rem; }
.ea-title { font-size: 2.2rem; font-weight: 800; letter-spacing: -.04em; margin: 0; color: #f7fafc; }
.ea-subtitle { color: var(--ea-muted); margin-top: .35rem; margin-bottom: 1.2rem; }
.ea-card { background: linear-gradient(145deg, rgba(23,36,58,.96), rgba(16,27,44,.96));
           border: 1px solid #2a3a51; border-radius: 18px; padding: 1.15rem 1.25rem; min-height: 120px; }
.ea-card-label { color: #a6b4c8; font-size: .78rem; font-weight: 600; letter-spacing: .06em; text-transform: uppercase; }
.ea-card-value { color: #f8fafc; font-size: 2rem; font-weight: 800; margin-top: .35rem; }
.ea-card-note { color: #a3e635; font-size: .78rem; margin-top: .25rem; }
.ea-section { font-size: 1.15rem; font-weight: 750; margin: .6rem 0 .8rem; color: #f5f7fb; }
.ea-panel { background: rgba(18,29,48,.78); border: 1px solid #26354b; border-radius: 16px; padding: 1rem 1.1rem; }
.ea-pill { display: inline-block; border-radius: 99px; padding: .22rem .62rem; font-size: .72rem; font-weight: 700;
           background: #243449; color: #dbe6f5; border: 1px solid #3a4c63; }
.ea-pill-green { background: #263a19; border-color: #476a25; color: #c8f68a; }
div[data-testid="stMetric"] { background: #121d30; border: 1px solid #2a3a51; padding: 1rem; border-radius: 16px; }
div[data-testid="stMetricLabel"] { color: #a6b4c8; }
div[data-testid="stMetricValue"] { color: #f8fafc; }
.stButton > button { border-radius: 10px; border: 1px solid #3b4d65; font-weight: 700; }
.stButton > button[kind="primary"] { background: #a3e635; border-color: #a3e635; color: #17210b; }
.stButton > button[kind="primary"]:hover { background: #bef264; border-color: #bef264; color: #17210b; }
div[data-testid="stDataFrame"] { border: 1px solid #26354b; border-radius: 12px; overflow: hidden; }
hr { border-color: #26354b; }
.small-muted { color: #9aa9bf; font-size: .84rem; }
</style>
""", unsafe_allow_html=True)


# ------------------------------ HELPERS -------------------------------------
def safe_attr(obj, attr, default=None):
    return getattr(obj, attr, default)


def team_name(team):
    return str(safe_attr(team, "name", "Unknown team"))


def match_teams(match):
    teams = safe_attr(match, "teams", None)
    if teams and len(teams) >= 2:
        return teams[0], teams[1]
    # Compatibility fallback if your Match class stores teams separately.
    return safe_attr(match, "team1"), safe_attr(match, "team2")


def score_text(match):
    score = safe_attr(match, "score", None)
    if score is None:
        return "—"
    if isinstance(score, (tuple, list)) and len(score) == 2:
        return f"{score[0]}  –  {score[1]}"
    return str(score)


def match_status(match):
    return str(safe_attr(match, "status", "Upcoming"))


def get_matches(tournament):
    return list(safe_attr(tournament, "matches", []) or [])


def get_teams(tournament):
    return list(safe_attr(tournament, "teams", []) or [])


def standings_rows(tournament):
    rows = tournament.get_standings()
    normalized = []

    for index, row in enumerate(rows, start=1):
        team = row.get("team", row.get("name", "Unknown"))

        if isinstance(team, Team):
            team = team.name

        normalized.append({
            "Pos": index,
            "Team": team,
            "P": row.get("played", 0),
            "W": row.get("won", 0),
            "D": row.get("drawn", 0),
            "L": row.get("lost", 0),
            "GF": row.get("goals_for", 0),
            "GA": row.get("goals_against", 0),
            "GD": row.get("goal_difference", 0),
            "PTS": row.get("points", 0),
        })

    return normalized

def count_finished(matches):
    return sum(1 for m in matches if match_status(m).lower() == "finished")


def count_live(matches):
    return sum(1 for m in matches if match_status(m).lower() == "live")


def init_state():
    if "tournament" not in st.session_state:
        # Create a fresh tournament. Edit the name if you like.
        st.session_state.tournament = Tournament("Elite Arena League")
    if "flash" not in st.session_state:
        st.session_state.flash = None


def header(kicker, title, subtitle):
    st.markdown(f"""
    <div class="ea-kicker">{kicker}</div>
    <h1 class="ea-title">{title}</h1>
    <div class="ea-subtitle">{subtitle}</div>
    """, unsafe_allow_html=True)


def stat_card(label, value, note="SEASON OVERVIEW"):
    st.markdown(f"""
    <div class="ea-card">
      <div class="ea-card-label">{label}</div>
      <div class="ea-card-value">{value}</div>
      <div class="ea-card-note">{note}</div>
    </div>
    """, unsafe_allow_html=True)


# ------------------------------ APP STATE -----------------------------------
init_state()
tournament = st.session_state.tournament
teams = get_teams(tournament)
matches = get_matches(tournament)

# ------------------------------- SIDEBAR ------------------------------------
with st.sidebar:
    st.markdown('<div class="ea-brand">ELITE <span>ARENA</span></div>', unsafe_allow_html=True)
    st.caption("FOOTBALL LEAGUE MANAGEMENT")
    st.markdown("---")
    page = st.radio(
        "NAVIGATION",
        ["Dashboard", "Fixtures", "Standings", "Teams & Players", "Manage League"],
        label_visibility="visible",
    )
    st.markdown("---")
    st.markdown("**CURRENT SEASON**")
    st.markdown(f"🏆 {safe_attr(tournament, 'name', 'Elite Arena League')}")
    st.markdown(f"👥 {len(teams)} teams")
    st.markdown(f"⚽ {len(matches)} fixtures")
    st.markdown("---")
    st.caption("ELITE ARENA • OOP EDITION")


if st.session_state.flash:
    kind, message = st.session_state.flash
    if kind == "success":
        st.success(message)
    elif kind == "error":
        st.error(message)
    else:
        st.info(message)
    st.session_state.flash = None


# -------------------------------- DASHBOARD ----------------------------------
if page == "Dashboard":
    header("SEASON CONTROL CENTER", "League Dashboard", "Your tournament at a glance. Fixtures, results and standings in one place.")
    finished = count_finished(matches)
    live = count_live(matches)
    upcoming = len(matches) - finished - live
    cols = st.columns(4, gap="medium")
    metrics = [
        ("REGISTERED TEAMS", len(teams), "Teams in this league"),
        ("TOTAL FIXTURES", len(matches), "Scheduled matchups"),
        ("COMPLETED", finished, "Matches with final scores"),
        ("LIVE NOW", live, "Currently in progress"),
    ]
    for col, (label, value, note) in zip(cols, metrics):
        with col:
            stat_card(label, value, note.upper())

    st.markdown('<div class="ea-section">Matchday overview</div>', unsafe_allow_html=True)
    left, right = st.columns([1.35, 1], gap="large")
    with left:
        st.markdown('<div class="ea-panel">', unsafe_allow_html=True)
        st.markdown("**Recent results**")
        completed = [m for m in matches if match_status(m).lower() == "finished"]
        if completed:
            for m in completed[-5:][::-1]:
                t1, t2 = match_teams(m)
                if t1 is None or t2 is None:
                    continue
                st.markdown(
                    f"**{team_name(t1)}**　`{score_text(m)}`　**{team_name(t2)}**"
                    f"  \n<span class='small-muted'>Match #{safe_attr(m, 'match_id', '?')} · Finished</span>",
                    unsafe_allow_html=True,
                )
                st.markdown("---")
        else:
            st.info("No completed matches yet. Go to Fixtures to start a match and enter its result.")
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown('<div class="ea-panel">', unsafe_allow_html=True)
        st.markdown("**Season progress**")
        progress = (finished / len(matches)) if matches else 0
        st.progress(progress, text=f"{finished} of {len(matches)} fixtures completed")
        st.markdown(f"- **Upcoming:** {upcoming}")
        st.markdown(f"- **Live:** {live}")
        st.markdown(f"- **Finished:** {finished}")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="ea-section">Current standings</div>', unsafe_allow_html=True)
    rows = standings_rows(tournament) if teams else []
    if rows:
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True, height=min(360, 44 + 36 * len(df)))
    else:
        st.info("Register at least two teams and generate the fixture schedule to begin.")


# -------------------------------- FIXTURES -----------------------------------
elif page == "Fixtures":
    header("MATCH CENTER", "Fixtures & Results", "Follow every matchup and update results as your tournament progresses.")
    matches = get_matches(tournament)
    if not matches:
        st.warning("No fixtures yet. Open **Manage League** and generate the schedule after registering at least two teams.")
    else:
        status_filter = st.selectbox("Filter matches", ["All", "Upcoming", "Live", "Finished"])
        shown = [m for m in matches if status_filter == "All" or match_status(m).lower() == status_filter.lower()]
        for match in shown:
            t1, t2 = match_teams(match)
            if t1 is None or t2 is None:
                continue
            mid = safe_attr(match, "match_id", "?")
            status = match_status(match)
            with st.container(border=True):
                top = st.columns([1.2, 2.2, 1.2])
                with top[0]:
                    st.caption(f"MATCH #{mid}")
                    st.markdown(f"**{status.upper()}**")
                with top[1]:
                    st.markdown(
                        f"<div style='text-align:center;font-size:1.13rem;font-weight:750'>"
                        f"{team_name(t1)} &nbsp; <span style='color:#a3e635'>{score_text(match)}</span> &nbsp; {team_name(t2)}"
                        f"</div>",
                        unsafe_allow_html=True,
                    )
                with top[2]:
                    st.markdown("<div style='text-align:right;color:#9aa9bf'>ELITE ARENA</div>", unsafe_allow_html=True)

                if status.lower() == "upcoming":
                    if st.button("▶ Start match", key=f"start_{mid}", type="primary"):
                        try:
                            match.start_match()
                            st.session_state.flash = ("success", f"Match #{mid} is now live.")
                        except Exception as exc:
                            st.session_state.flash = ("error", str(exc))
                        st.rerun()

                elif status.lower() == "live":
                    with st.form(f"finish_{mid}"):
                        st.caption("Enter the final score to finish this match.")
                        c1, c2 = st.columns(2)
                        with c1:
                            score1 = st.number_input(f"{team_name(t1)} goals", min_value=0, max_value=99, step=1, key=f"s1_{mid}")
                        with c2:
                            score2 = st.number_input(f"{team_name(t2)} goals", min_value=0, max_value=99, step=1, key=f"s2_{mid}")
                        submitted = st.form_submit_button("Save final result", type="primary", use_container_width=True)
                        if submitted:
                            try:
                                match.finish_match(int(score1), int(score2))
                                st.session_state.flash = ("success", f"Result saved for match #{mid}. Standings have been recalculated.")
                            except Exception as exc:
                                st.session_state.flash = ("error", f"Could not finish match: {exc}")
                            st.rerun()


# -------------------------------- STANDINGS ----------------------------------
elif page == "Standings":
    header("LEAGUE TABLE", "Official Standings", "The table is calculated from completed match results using your Tournament class.")
    rows = standings_rows(tournament) if get_teams(tournament) else []
    if rows:
        df = pd.DataFrame(rows)
        st.markdown('<div class="ea-panel">', unsafe_allow_html=True)
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            height=min(600, 48 + 38 * len(df)),
            column_config={
                "Pos": st.column_config.NumberColumn("POS", format="%d"),
                "Team": st.column_config.TextColumn("TEAM"),
                "P": st.column_config.NumberColumn("P", help="Played"),
                "W": st.column_config.NumberColumn("W", help="Won"),
                "D": st.column_config.NumberColumn("D", help="Drawn"),
                "L": st.column_config.NumberColumn("L", help="Lost"),
                "GF": st.column_config.NumberColumn("GF", help="Goals for"),
                "GA": st.column_config.NumberColumn("GA", help="Goals against"),
                "GD": st.column_config.NumberColumn("GD", help="Goal difference"),
                "PTS": st.column_config.NumberColumn("PTS", help="Points"),
            },
        )
        st.markdown("</div>", unsafe_allow_html=True)
        st.caption("Ranking is provided by Tournament.get_standings(). The UI does not calculate league points separately.")
    else:
        st.info("Your league table will appear here after teams are registered. Results update the table automatically.")


# ---------------------------- TEAMS & PLAYERS -------------------------------

elif page == "Teams & Players":
    header("SQUAD DIRECTORY", "Teams & Players", "Manage teams and their player rosters.")

    teams = get_teams(tournament)

    if not teams:
        st.info("No teams registered yet. Add teams from Manage League.")
    else:
        options = {
            f"{team_name(t)} · ID {safe_attr(t, 'id', '?')}": t
            for t in teams
        }

        selected_label = st.selectbox("Select a team", list(options.keys()))
        selected_team = options[selected_label]

        st.markdown("### Add a new player")

        with st.form("add_player_form", clear_on_submit=True):
            player_id = st.number_input(
                "Player ID", min_value=1, step=1
            )
            player_name = st.text_input("Player Name")
            player_role = st.selectbox(
                "Player Role",
                ["Goalkeeper", "Defender", "Midfielder", "Forward"]
            )

            submitted = st.form_submit_button(
                "＋ Add Player", type="primary"
            )

            if submitted:
                try:
                    new_player = HumanPlayer(
                        int(player_id),
                        player_name.strip(),
                        player_role
                    )

                    selected_team.add_player(new_player)

                    st.session_state.flash = (
                        "success",
                        f"{player_name} added to {team_name(selected_team)}."
                    )
                except Exception as exc:
                    st.session_state.flash = (
                        "error",
                        f"Could not add player: {exc}"
                    )

                st.rerun()

        players = list(safe_attr(selected_team, "players", []) or [])

        st.markdown("### Squad roster")

        if players:
            player_rows = []

            for p in players:
                player_rows.append({
                    "Player ID": safe_attr(p, "id", "—"),
                    "Name": safe_attr(p, "name", "Unknown"),
                    "Role": safe_attr(p, "role", "—"),
                    "Banned": "Yes" if safe_attr(p, "is_banned", False) else "No",
                })

            st.dataframe(
                pd.DataFrame(player_rows),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("This team has no players registered yet.")


# ------------------------------- MANAGEMENT ---------------------------------
elif page == "Manage League":
    header("LEAGUE ADMINISTRATION", "Manage League", "Register clubs and create the round-robin schedule.")
    st.markdown('<div class="ea-section">Register a team</div>', unsafe_allow_html=True)
    with st.form("register_team_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            team_id = st.text_input("Team ID", placeholder="e.g. RM")
        with c2:
            team_label = st.text_input("Team name", placeholder="e.g. Real Madrid")
        submitted = st.form_submit_button("＋ Register team", type="primary")
        if submitted:
            try:
                new_team = Team(team_id.strip(), team_label.strip())
                tournament.register_team(new_team)
                st.session_state.flash = ("success", f"{team_label.strip()} registered successfully.")
            except Exception as exc:
                st.session_state.flash = ("error", f"Could not register team: {exc}")
            st.rerun()

    st.markdown("---")
    st.markdown('<div class="ea-section">Generate fixture schedule</div>', unsafe_allow_html=True)
    st.write("Creates a single round-robin schedule: every pair of active teams plays once.")
    if st.button("⚽ Generate schedule", type="primary", disabled=len(get_teams(tournament)) < 2):
        try:
            tournament.generate_schedule()
            st.session_state.flash = ("success", f"Schedule generated: {len(get_matches(tournament))} matches.")
        except Exception as exc:
            st.session_state.flash = ("error", f"Could not generate schedule: {exc}")
        st.rerun()

    st.markdown("---")
    st.markdown('<div class="ea-section">Current teams</div>', unsafe_allow_html=True)
    current_teams = get_teams(tournament)
    if current_teams:
        st.dataframe(
            pd.DataFrame([{
                "ID": safe_attr(t, "id", "—"),
                "Team": team_name(t),
                "Players": len(safe_attr(t, "players", []) or []),
                "Status": "Active" if safe_attr(t, "is_active", True) else "Inactive",
            } for t in current_teams]),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.caption("No teams have been registered yet.")

    st.markdown("---")
    st.markdown('<div class="ea-section">Reset demo session</div>', unsafe_allow_html=True)
    st.warning("Reset clears the tournament data held in this running Streamlit session. This does not delete any external database because this version does not use one.")
    if st.button("Reset tournament data"):
        st.session_state.tournament = Tournament("Elite Arena League")
        st.session_state.flash = ("success", "Tournament reset.")
        st.rerun()
