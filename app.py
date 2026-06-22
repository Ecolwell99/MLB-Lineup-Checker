```python
import streamlit as st
import pandas as pd
import xml.etree.ElementTree as ET

st.set_page_config(
    page_title="MLB Lineup Checker",
    layout="wide"
)

st.title("⚾ MLB Lineup Checker")

# -----------------------------
# XML PARSER
# -----------------------------
def parse_lineup_xml(xml_text):
    """
    Returns:
        lineup_players = [
            {
                "player_id": "1473708",
                "name": "Turang, Brice",
                "team": "1",
                "substitute": False
            }
        ]
    """

    players = []

    root = ET.fromstring(xml_text)

    for player in root.findall("player"):
        players.append(
            {
                "player_id": player.attrib.get("id"),
                "name": player.attrib.get("name"),
                "team": player.attrib.get("team"),
                "substitute": player.attrib.get("substitute") == "true",
            }
        )

    return players


# -----------------------------
# CSV PARSER
# -----------------------------
def parse_roster_files(files):
    """
    Pulls all player IDs from uploaded roster exports.
    Assumes player_id appears somewhere in the row.

    Adjust column selection later once exact schema is known.
    """

    roster_ids = set()

    for file in files:

        try:
            df = pd.read_csv(
                file,
                sep=None,
                engine="python",
                header=None
            )

            # Search every column for numeric IDs
            for col in df.columns:

                values = (
                    df[col]
                    .astype(str)
                    .str.strip()
                )

                for value in values:

                    if value.isdigit():

                        # MLB player IDs tend to be 6-8 digits
                        if 6 <= len(value) <= 8:
                            roster_ids.add(value)

        except Exception as e:
            st.error(f"Failed to read {file.name}: {e}")

    return roster_ids


# -----------------------------
# UI
# -----------------------------
xml_input = st.text_area(
    "Paste Lineup XML",
    height=300
)

uploaded_files = st.file_uploader(
    "Drop roster CSV files here",
    type=["csv", "txt"],
    accept_multiple_files=True
)

# -----------------------------
# CHECK BUTTON
# -----------------------------
if st.button("Check Lineup"):

    if not xml_input:
        st.warning("Paste lineup XML first.")
        st.stop()

    if not uploaded_files:
        st.warning("Upload roster CSV files.")
        st.stop()

    try:

        lineup_players = parse_lineup_xml(xml_input)
        roster_ids = parse_roster_files(uploaded_files)

        missing_players = []

        for player in lineup_players:

            player_id = player["player_id"]

            if player_id not in roster_ids:

                missing_players.append(player)

        st.subheader("Results")

        if len(missing_players) == 0:

            st.success(
                f"All {len(lineup_players)} lineup players found."
            )

        else:

            st.error(
                f"{len(missing_players)} players missing."
            )

            missing_df = pd.DataFrame(missing_players)

            st.dataframe(
                missing_df,
                use_container_width=True
            )

    except Exception as e:

        st.error(f"Error: {e}")
```
