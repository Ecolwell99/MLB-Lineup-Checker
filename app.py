import streamlit as st
import pandas as pd
import xml.etree.ElementTree as ET

st.set_page_config(
    page_title="MLB Lineup Checker",
    layout="wide"
)

TEAM_URLS = {
    "Arizona Diamondbacks": "https://sbdeco.prod.simplebet-infra.com/admin/mlb/mlbplayer/?current_team__id__exact=459d7455-e83c-4de3-b761-2936e1c296e8&q=",
    "Atlanta Braves": "https://sbdeco.prod.simplebet-infra.com/admin/mlb/mlbplayer/?current_team__id__exact=45d728b7-b8c8-41be-b017-18ff1db84ef8&q=",
    "Baltimore Orioles": "https://sbdeco.prod.simplebet-infra.com/admin/mlb/mlbplayer/?current_team__id__exact=c478d13d-e017-45eb-a858-e1f12fd081bb&q=",
    "Boston Red Sox": "https://sbdeco.prod.simplebet-infra.com/admin/mlb/mlbplayer/?current_team__id__exact=e9d976a0-3520-4c54-9093-e169bce68286&q=",
    "Chicago Cubs": "https://sbdeco.prod.simplebet-infra.com/admin/mlb/mlbplayer/?current_team__id__exact=b0604af0-28b5-4240-82c5-266c56acb0eb&q=",
    "Chicago White Sox": "https://sbdeco.prod.simplebet-infra.com/admin/mlb/mlbplayer/?current_team__id__exact=34ef96af-312b-4e79-8133-c3815a217985&q=",
    "Cincinnati Reds": "https://sbdeco.prod.simplebet-infra.com/admin/mlb/mlbplayer/?current_team__id__exact=1b92f24f-a706-429d-95f0-6f1efad911ad&q=",
    "Cleveland Guardians": "https://sbdeco.prod.simplebet-infra.com/admin/mlb/mlbplayer/?current_team__id__exact=c23e595c-9807-47de-a73e-df65bf4d7047&q=",
    "Colorado Rockies": "https://sbdeco.prod.simplebet-infra.com/admin/mlb/mlbplayer/?current_team__id__exact=530dbc84-c57d-498b-8fd6-683edfbc0f30&q=",
    "Detroit Tigers": "https://sbdeco.prod.simplebet-infra.com/admin/mlb/mlbplayer/?current_team__id__exact=c1208c99-10bb-4a6d-a818-5a2170379e58&q=",
    "Houston Astros": "https://sbdeco.prod.simplebet-infra.com/admin/mlb/mlbplayer/?current_team__id__exact=b4ced502-5d26-4e81-88fd-822fd9963f06&q=",
    "Kansas City Royals": "https://sbdeco.prod.simplebet-infra.com/admin/mlb/mlbplayer/?current_team__id__exact=b6a28ffd-70ea-41e2-a200-c08dc561ca3d&q=",
    "Los Angeles Angels": "https://sbdeco.prod.simplebet-infra.com/admin/mlb/mlbplayer/?current_team__id__exact=102b30df-f9b0-4227-8e42-d4db466affa6&q=",
    "Los Angeles Dodgers": "https://sbdeco.prod.simplebet-infra.com/admin/mlb/mlbplayer/?current_team__id__exact=80592147-e6e6-41a6-86ec-ea3422f39c1f&q=",
    "Miami Marlins": "https://sbdeco.prod.simplebet-infra.com/admin/mlb/mlbplayer/?current_team__id__exact=a066812f-90c8-48ec-8543-a5c0d2fc6c93&q=",
    "Milwaukee Brewers": "https://sbdeco.prod.simplebet-infra.com/admin/mlb/mlbplayer/?current_team__id__exact=6557b9d7-c25c-4583-9a5a-cac7cd5f2154&q=",
    "Minnesota Twins": "https://sbdeco.prod.simplebet-infra.com/admin/mlb/mlbplayer/?current_team__id__exact=675c161f-7e9a-485c-b075-79f67af54e7b&q=",
    "New York Mets": "https://sbdeco.prod.simplebet-infra.com/admin/mlb/mlbplayer/?current_team__id__exact=443f3ca9-d8af-4e0d-8116-73c68d7dc60d&q=",
    "New York Yankees": "https://sbdeco.prod.simplebet-infra.com/admin/mlb/mlbplayer/?current_team__id__exact=416af0eb-dd90-4a3f-9a1e-b8bb684b3471&q=",
    "Athletics": "https://sbdeco.prod.simplebet-infra.com/admin/mlb/mlbplayer/?current_team__id__exact=91d275c1-686a-40fd-aad6-bd7c5e7fa679&q=",
    "Philadelphia Phillies": "https://sbdeco.prod.simplebet-infra.com/admin/mlb/mlbplayer/?current_team__id__exact=71c795b7-178f-44ff-9fd7-821c7fcd0f28&q=",
    "Pittsburgh Pirates": "https://sbdeco.prod.simplebet-infra.com/admin/mlb/mlbplayer/?current_team__id__exact=e9a8a330-fa1d-4298-9a84-28e24bfe6f6a&q=",
    "San Diego Padres": "https://sbdeco.prod.simplebet-infra.com/admin/mlb/mlbplayer/?current_team__id__exact=a41ef939-abc7-4103-98b0-e8db0a560152&q=",
    "San Francisco Giants": "https://sbdeco.prod.simplebet-infra.com/admin/mlb/mlbplayer/?current_team__id__exact=24b936b4-e4fa-4359-a7a1-edc5fd802792&q=",
    "Seattle Mariners": "https://sbdeco.prod.simplebet-infra.com/admin/mlb/mlbplayer/?current_team__id__exact=720d8d83-d7ad-480c-adf2-e86890f9fb26&q=",
    "St. Louis Cardinals": "https://sbdeco.prod.simplebet-infra.com/admin/mlb/mlbplayer/?current_team__id__exact=c0bd4c17-72b9-464b-a071-bc34597ca87d&q=",
    "Tampa Bay Rays": "https://sbdeco.prod.simplebet-infra.com/admin/mlb/mlbplayer/?current_team__id__exact=583b1bea-be21-4f30-9060-add216cdde64&q=",
    "Texas Rangers": "https://sbdeco.prod.simplebet-infra.com/admin/mlb/mlbplayer/?current_team__id__exact=619faa0a-2dc6-46c9-923c-e04cc57275cb&q=",
    "Toronto Blue Jays": "https://sbdeco.prod.simplebet-infra.com/admin/mlb/mlbplayer/?current_team__id__exact=256cb5f6-c25f-4838-aaca-052c28bf12db&q=",
    "Washington Nationals": "https://sbdeco.prod.simplebet-infra.com/admin/mlb/mlbplayer/?current_team__id__exact=d5699a17-9f13-4ec4-8dca-600fc88b26d2&q=",
}


st.title("MLB Lineup Checker")


def parse_lineup_xml(xml_text):
    players = []
    root = ET.fromstring(xml_text.strip())

    for player in root.findall("player"):
        players.append({
            "player_id": str(player.attrib.get("id", "")).strip(),
            "name": player.attrib.get("name", ""),
            "team": player.attrib.get("team", ""),
        })

    return players


def parse_roster_files(files):
    roster_ids = set()
    file_summaries = []
    team_number_map = {}

    for file in files:
        try:
            df = pd.read_csv(
                file,
                sep=None,
                engine="python",
                dtype=str,
                keep_default_na=False
            )

            for col in df.columns:
                values = df[col].astype(str).str.strip()

                for value in values:
                    if value.isdigit() and 6 <= len(value) <= 8:
                        roster_ids.add(value)

            team = ""

            if "current_team_name" in df.columns:
                teams = (
                    df["current_team_name"]
                    .astype(str)
                    .str.strip()
                    .replace("", pd.NA)
                    .dropna()
                    .unique()
                )

                if len(teams) > 0:
                    team = teams[0]

            file_summaries.append({
                "File": file.name,
                "Team": team,
                "Rows": len(df)
            })

        except Exception as e:
            st.error(f"Failed to read {file.name}: {e}")

            file_summaries.append({
                "File": file.name,
                "Team": "Error",
                "Rows": 0
            })

    return roster_ids, file_summaries


st.subheader("Roster Downloads")

team_cols = st.columns(3)
team_options = sorted(TEAM_URLS.keys())

for i, team in enumerate(team_options):
    with team_cols[i % 3]:
        st.markdown(f"[{team}]({TEAM_URLS[team]})")

st.divider()

xml_input = st.text_area(
    "Paste Lineup XML",
    height=300
)

uploaded_files = st.file_uploader(
    "Drop roster CSV files here",
    type=["csv", "txt"],
    accept_multiple_files=True
)

if st.button("Check Lineup", use_container_width=True):

    if not xml_input.strip():
        st.warning("Paste lineup XML first.")
        st.stop()

    if not uploaded_files:
        st.warning("Upload roster CSV files.")
        st.stop()

    try:
        lineup_players = parse_lineup_xml(xml_input)
        roster_ids, file_summaries = parse_roster_files(uploaded_files)

        st.subheader("Upload Summary")

        st.dataframe(
            pd.DataFrame(file_summaries),
            use_container_width=True,
            hide_index=True
        )

        team_name_map = {
            "1": "Team 1",
            "2": "Team 2",
        }

        uploaded_team_names = [
            row["Team"]
            for row in file_summaries
            if row.get("Team") and row.get("Team") != "Error"
        ]

        if len(uploaded_team_names) >= 2:
            team_name_map = {
                "1": uploaded_team_names[0],
                "2": uploaded_team_names[1],
            }

        missing_players = []

        for player in lineup_players:
            if player["player_id"] not in roster_ids:
                missing_players.append({
                    "Player ID": player["player_id"],
                    "Name": player["name"],
                    "Team": team_name_map.get(player["team"], player["team"]),
                })

        st.subheader("Results")

        if len(missing_players) == 0:
            st.success("All lineup players found.")
        else:
            st.error(f"{len(missing_players)} players missing.")

            st.dataframe(
                pd.DataFrame(missing_players),
                use_container_width=True,
                hide_index=True
            )

    except Exception as e:
        st.error(f"Error: {e}")
