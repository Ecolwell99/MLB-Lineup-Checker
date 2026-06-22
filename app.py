import streamlit as st
import pandas as pd
import xml.etree.ElementTree as ET

st.set_page_config(
    page_title="MLB Lineup Checker",
    layout="wide"
)

st.title("MLB Lineup Checker")


def parse_lineup_xml(xml_text):
    players = []

    root = ET.fromstring(xml_text.strip())

    for player in root.findall("player"):
        players.append({
            "player_id": str(player.attrib.get("id", "")).strip(),
            "name": player.attrib.get("name", ""),
            "team": player.attrib.get("team", ""),
            "substitute": player.attrib.get("substitute") == "true",
        })

    return players


def parse_roster_files(files):
    roster_ids = set()
    file_summaries = []

    for file in files:
        try:
            df = pd.read_csv(
                file,
                sep=None,
                engine="python",
                header=None,
                dtype=str,
                keep_default_na=False
            )

            for col in df.columns:
                values = df[col].fillna("").astype(str).str.strip()

                for value in values:
                    if value.isdigit() and 6 <= len(value) <= 8:
                        roster_ids.add(value)

            team = ""

            if len(df.columns) > 0:
                possible_team_col = df.columns[-1]

                teams = (
                    df[possible_team_col]
                    .astype(str)
                    .str.strip()
                    .replace("", pd.NA)
                    .dropna()
                    .unique()
                )

                if len(teams) == 1:
                    team = teams[0]
                elif len(teams) > 1:
                    team = ", ".join(teams[:3])

            file_summaries.append({
                "File": file.name,
                "Team": team,
                "Rows": len(df),
            })

        except Exception as e:
            file_summaries.append({
                "File": file.name,
                "Team": "",
                "Rows": 0,
            })

            st.error(f"Failed to read {file.name}: {e}")

    return roster_ids, file_summaries


xml_input = st.text_area(
    "Paste Lineup XML",
    height=300
)

uploaded_files = st.file_uploader(
    "Drop roster CSV files here",
    type=["csv", "txt"],
    accept_multiple_files=True
)

if st.button("Check Lineup"):

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

        missing_players = []

        for player in lineup_players:
            if player["player_id"] not in roster_ids:
                missing_players.append(player)

        st.subheader("Results")

        if len(missing_players) == 0:
            st.success(f"All {len(lineup_players)} lineup players found.")
        else:
            st.error(f"{len(missing_players)} players missing.")
            st.dataframe(
                pd.DataFrame(missing_players),
                use_container_width=True,
                hide_index=True
            )

    except Exception as e:
        st.error(f"Error: {e}")
