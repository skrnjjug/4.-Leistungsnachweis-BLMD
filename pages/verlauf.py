import streamlit as st

st.set_page_config(page_title="Verlauf", layout="wide")

st.title("📊 Verlauf")

# Daten holen
history = st.session_state.get("history", [])

if not history:
    st.info("Noch keine Einträge vorhanden.")
else:
    for entry in reversed(history):

        with st.container():
            st.markdown("---")

            st.write(f"📅 Datum: {entry['datum']}")

            # ✅ FIX: String → float
            total = float(entry["total"])
            trinkgeld = float(entry["trinkgeld_total"])

            st.write(f"💰 Einnahmen: {total:.2f} CHF")
            st.write(f"💸 Trinkgeld: {trinkgeld:.2f} CHF")

# Abstand
st.markdown("---")

# Zurück Button unten
if st.button("🔙 Zurück zur Startseite", use_container_width=True):
    st.switch_page("app.py")