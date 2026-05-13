import streamlit as st
import pandas as pd
import json

st.markdown("## 📊 Verlauf")
st.caption("Hier siehst du alle gespeicherten Tagesabschlüsse.")

# =========================
# DATEN LADEN
# =========================
if "data_df" not in st.session_state:
    data_manager = st.session_state["data_manager"]
    st.session_state["data_df"] = data_manager.load_user_data(
        "data.csv",
        initial_value=pd.DataFrame(),
        parse_dates=["timestamp"]
    )

data_df = st.session_state["data_df"]

# =========================
# STYLE
# =========================
st.markdown("""
<style>
.detail-card {
    background: #f8fafc;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    margin-bottom: 15px;
    color: #111827;
}

.detail-title {
    font-size: 20px;
    font-weight: 700;
    color: #111827;
    margin-bottom: 10px;
}

.detail-label {
    font-weight: 600;
    color: #374151;
}

.detail-highlight {
    font-size: 20px;
    font-weight: bold;
    color: #16a34a;
}
</style>
""", unsafe_allow_html=True)

# =========================
# INHALT
# =========================
if data_df.empty:
    st.info("Noch keine gespeicherten Einträge vorhanden.")

else:
    data_df = data_df.copy()

    if "datum" in data_df.columns:
        data_df["datum"] = data_df["datum"].astype(str)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Einträge", len(data_df))

    with col2:
        if "total" in data_df.columns:
            st.metric("Gesamteinnahmen", f"{data_df['total'].sum():.2f} CHF")

    with col3:
        if "trinkgeld_total" in data_df.columns:
            st.metric("Gesamtes Trinkgeld", f"{data_df['trinkgeld_total'].sum():.2f} CHF")

    st.markdown("---")
    st.markdown("### Gespeicherte Tagesabschlüsse")

    spalten = [
        col for col in [
            "datum",
            "name",
            "startkasse",
            "bar",
            "karte",
            "twint",
            "total",
            "differenz",
            "trinkgeld_total"
        ]
        if col in data_df.columns
    ]

    st.dataframe(
        data_df[spalten],
        use_container_width=True
    )

    st.markdown("---")
    st.markdown("### Detailansicht")

    optionen = []

    for index, row in data_df.iterrows():
        datum = row.get("datum", "ohne Datum")
        name = row.get("name", "ohne Name")
        total = row.get("total", 0)
        optionen.append(f"{index} | {datum} | {name} | {float(total):.2f} CHF")

    auswahl = st.selectbox(
        "Wähle einen Eintrag aus:",
        optionen
    )

    selected_index = int(auswahl.split(" | ")[0])
    eintrag = data_df.loc[selected_index]

    st.markdown(f"""
    <div class="detail-card">
        <div class="detail-title">Details zum Tagesabschluss</div>
        <p><span class="detail-label">Datum:</span> {eintrag.get("datum", "-")}</p>
        <p><span class="detail-label">Name:</span> {eintrag.get("name", "-")}</p>
        <p><span class="detail-label">Kassenstock:</span> {float(eintrag.get("startkasse", 0)):.2f} CHF</p>
        <p><span class="detail-label">Bar:</span> {float(eintrag.get("bar", 0)):.2f} CHF</p>
        <p><span class="detail-label">Karte:</span> {float(eintrag.get("karte", 0)):.2f} CHF</p>
        <p><span class="detail-label">TWINT:</span> {float(eintrag.get("twint", 0)):.2f} CHF</p>
        <p><span class="detail-label">Total:</span> {float(eintrag.get("total", 0)):.2f} CHF</p>
        <p><span class="detail-label">Endkasse:</span> {float(eintrag.get("endkasse", 0)):.2f} CHF</p>
        <p><span class="detail-label">Barumsatz:</span> {float(eintrag.get("barumsatz", 0)):.2f} CHF</p>
        <p><span class="detail-label">Differenz:</span> {float(eintrag.get("differenz", 0)):.2f} CHF</p>
        <p><span class="detail-label">Trinkgeld:</span> {float(eintrag.get("trinkgeld_total", 0)):.2f} CHF</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 👥 Trinkgeld-Verteilung")

    if "trinkgeld_verteilung" in eintrag and pd.notna(eintrag["trinkgeld_verteilung"]):
        try:
            verteilung = json.loads(eintrag["trinkgeld_verteilung"])

            if len(verteilung) > 0:
                for person in verteilung:
                    st.markdown(f"""
                    <div class="detail-card">
                        <p><span class="detail-label">Mitarbeiter:</span> {person.get("name", "-")}</p>
                        <p><span class="detail-label">Stunden:</span> {person.get("stunden", 0)}</p>
                        <p><span class="detail-label">Trinkgeld-Anteil:</span></p>
                        <div class="detail-highlight">{float(person.get("betrag", 0)):.2f} CHF</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Für diesen Eintrag wurde keine Trinkgeld-Verteilung gespeichert.")

        except Exception:
            st.warning("Trinkgeld-Verteilung konnte nicht gelesen werden.")
    else:
        st.info("Keine Trinkgeld-Verteilung für diesen Eintrag vorhanden.")

    st.markdown("---")
    st.markdown("### 🗑️ Abschluss löschen")

    st.warning("Achtung: Wenn du diesen Abschluss löschst, wird er dauerhaft aus dem Verlauf entfernt.")

    delete_confirm = st.checkbox(
        "Ich möchte diesen Abschluss wirklich löschen.",
        key=f"delete_confirm_{selected_index}"
    )

    if st.button("🗑️ Ausgewählten Abschluss löschen", use_container_width=True, type="primary"):
        if delete_confirm:
            data_df = data_df.drop(index=selected_index).reset_index(drop=True)

            st.session_state["data_df"] = data_df

            data_manager = st.session_state["data_manager"]
            data_manager.save_user_data(
                st.session_state["data_df"],
                "data.csv"
            )

            st.success("Abschluss wurde gelöscht.")
            st.rerun()
        else:
            st.error("Bitte bestätige zuerst, dass du diesen Abschluss löschen möchtest.")

st.markdown("---")

if st.button("🔙 Zurück zur Startseite", use_container_width=True):
    st.switch_page("views/home.py")