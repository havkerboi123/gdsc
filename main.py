import streamlit as st
import pandas as pd

# List of teams
teams = [
    "Programista", "Wrong Faculty", "Dynamic Mind's"
]

# Initialize session state for dynamic dropdown and scores
if "remaining_teams" not in st.session_state:
    st.session_state["remaining_teams"] = teams.copy()

if "scores" not in st.session_state:
    st.session_state["scores"] = []

# Initialize session state for user authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Hardcoded user credentials
users = {
    "mah": "mah123",
    "kib": "kib123"
}

# Function for user login
def login():
    username = st.text_input("Username", key="username")
    password = st.text_input("Password", type="password", key="password")

    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state["authenticated"] = True
            st.success("Login successful!")
        else:
            st.error("Invalid credentials, please try again.")

# Login page
if not st.session_state["authenticated"]:
    login()
else:
    # Apply custom CSS for layout, background, and logos
    st.markdown(
        """
        <style>
        body {
            background-color: white;  /* Change background to white */
            color: black;  /* Change text color to black for visibility */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Streamlit app layout
    st.title("Hackathon Point Scorer")

    # Dropdown to select a team
    selected_team = st.selectbox(
        "Select a team to score:",
        st.session_state["remaining_teams"],
        help="Choose a team to evaluate."
    )

    # Input placeholders for four evaluation scores
    st.subheader(f"Scoring for: {selected_team}")
    score1 = st.number_input(
        "Score 1 (Innovation + Social Impact):", min_value=0, max_value=5, step=1, key="score1"
    )
    score2 = st.number_input(
        "Score 2 (Business Viability):", min_value=0, max_value=5, step=1, key="score2"
    )
    score3 = st.number_input(
        "Score 3 (Theme):", min_value=0, max_value=5, step=1, key="score3"
    )
    score4 = st.number_input(
        "Score 4 (Prototype Functionality):", min_value=0, max_value=5, step=1, key="score4"
    )

    # Submit button to finalize scoring
    if st.button("Submit Score"):
        if score1 < 0 or score1 > 5 or score2 < 0 or score2 > 5 or score3 < 0 or score3 > 5 or score4 < 0 or score4 > 5:
            st.error("Scores must be between 0 and 5 for all categories.")
        else:
            if selected_team:
                total_score = score1 + score2 + score3 + score4
                st.session_state["scores"].append({
                    "Team Name": selected_team,
                    "Innovation + Social Impact": score1,
                    "Business Viability": score2,
                    "Theme": score3,
                    "Prototype Functionality": score4,
                    "Total Score": total_score
                })
                # Remove the team from the remaining teams list
                st.session_state["remaining_teams"].remove(selected_team)
                
                # Reset score placeholders
                st.experimental_rerun()
                
                st.success(f"Score for {selected_team} submitted successfully! Total Score: {total_score}")
            else:
                st.warning("Please select a team.")

    # Display scores of all teams
    if st.session_state["scores"]:
        st.subheader("Team Scores")
        scores_df = pd.DataFrame(st.session_state["scores"])
        st.write(scores_df)

        # CSV download
        csv = scores_df.to_csv(index=False)
        st.download_button(
            label="Download Results as CSV",
            data=csv,
            file_name="hackathon_scores.csv",
            mime="text/csv"
        )
