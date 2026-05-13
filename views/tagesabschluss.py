import streamlit as st
import pandas as pd
import json
from datetime import date, datetime

# =========================
# STYLE
# =========================
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}

.card {
    background: #f8fafc;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    margin-bottom: 15px;
    color: #111827;
}

.title {
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 10px;
    color: white;
}

.subtitle {
    font-size: 18px;
    font-weight: 600;
    margin-top: 20px;
    margin-bottom: 8px;
    color: white;
}

.highlight {
    font-size: 22px;
    font-weight: bold;
    color: #16a34a;
}

.card-label {
    font-size: 16px;
    font-weight: 600;
    color: #374151;
    margin-bottom: 8px;
}

.card-subtext {
    font-size: 14px;
    color: #6b7280;
}

.card-name {
    font-size: 18px;
    font-weight: 700;
    color: #111827;
    margin-bottom: 6px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# STATE
# =========================
if "mitarbeiter" not in st.session_state:
    st.session_state.mitarbeiter = []

if "show_result" not in st.session_state:
    st.session_state.show_result = False

if "data_df" not in st.session_state:
    st.session_state.data_df = pd.DataFrame()

# =========================
# HEADER
# =========================
st.markdown('<div class="title">🍸 Tagesabschluss</div>', unsafe_allow_html=True)

# =========================
# BASISDATEN
# =========================
st.markdown('<div class="subtitle">🧾 Basisdaten</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

name = col1.text_input("Name")
datum = col2.date_input("Datum", value=date.today())

# =========================
# KASSENSTOCK
# =========================
st.markdown('<div class="subtitle">💵 Kassenstock</div>', unsafe_allow_html=True)

startkasse = st.number_input(
    "Fixer Kassenstock / Startkasse (CHF)",
    min_value=0.0,
    value=300.0,
    step=10.0,
    help="Standardmässig bleiben 300 CHF in der Kasse. Dieser Betrag wird vom gezählten Bargeld abgezogen."
)

st.info(f"Für diese Abrechnung wird ein Kassenstock von **{startkasse:.2f} CHF** vom gezählten Bargeld abgezogen.")

# =========================
# EINNAHMEN
# =========================
st.markdown('<div class="subtitle">💰 Einnahmen</div>', unsafe_allow_html=True)
col3, col4, col5 = st.columns(3)

bar = col3.number_input("💵 Erwartete Bar-Einnahmen", 0.0)
karte = col4.number_input("💳 Karte", 0.0)
twint = col5.number_input("📱 TWINT", 0.0)

# =========================
# KASSE
# =========================
st.markdown('<div class="subtitle">💵 Endkasse</div>', unsafe_allow_html=True)
endkasse = st.number_input(
    "Gezähltes Bargeld in der Kasse (Endkasse)",
    0.0,
    help="Hier wird der gesamte gezählte Bargeldbetrag am Ende des Tages eingetragen."
)

# =========================
# AUTO TRINKGELD
# =========================
barumsatz_preview = endkasse - startkasse
differenz_preview = barumsatz_preview - bar
trinkgeld_preview = max(differenz_preview, 0)

st.markdown('<div class="subtitle">💸 Trinkgeld</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="card">
    <div class="card-label">Berechnetes Trinkgeld</div>
    <div class="highlight">{trinkgeld_preview:.2f} CHF</div>
    <div class="card-subtext">
        Berechnung: Endkasse - Kassenstock - erwartete Bar-Einnahmen
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# MITARBEITER
# =========================
st.markdown('<div class="subtitle">👥 Mitarbeiter</div>', unsafe_allow_html=True)

if st.button("+ Mitarbeiter hinzufügen"):
    st.session_state.mitarbeiter.append({"name": "", "stunden": 0})

for i, ma in enumerate(st.session_state.mitarbeiter):
    col1, col2 = st.columns(2)
    ma["name"] = col1.text_input(f"Name {i+1}", ma["name"], key=f"name_{i}")
    ma["stunden"] = col2.number_input(
        f"Stunden {i+1}", value=ma["stunden"], key=f"stunden_{i}"
    )

st.markdown("---")

# =========================
# BUTTONS
# =========================
colA, colB = st.columns(2)

with colA:
    if st.button("🔙 Zurück", use_container_width=True, type="secondary"):
        st.switch_page("views/home.py")

with colB:
    if st.button("➡️ Berechnen", use_container_width=True, type="secondary"):

        total = bar + karte + twint
        barumsatz = endkasse - startkasse
        differenz = barumsatz - bar
        trinkgeld_total = max(differenz, 0)

        st.session_state.result = {
            "timestamp": datetime.now(),
            "name": name,
            "datum": datum,
            "startkasse": startkasse,
            "total": total,
            "bar": bar,
            "karte": karte,
            "twint": twint,
            "barumsatz": barumsatz,
            "endkasse": endkasse,
            "differenz": differenz,
            "trinkgeld_total": trinkgeld_total,
            "mitarbeiter": st.session_state.mitarbeiter
        }

        st.session_state.show_result = True

# =========================
# ERGEBNIS
# =========================
if st.session_state.show_result:

    data = st.session_state.result

    st.markdown("## 📊 Übersicht")

    c1, c2, c3 = st.columns(3)

    c1.markdown(f"""
    <div class="card">
        <div class="card-label">💰 Einnahmen gesamt</div>
        <div class="highlight">{data['total']:.2f} CHF</div>
        <div class="card-subtext">Bar + Karte + TWINT</div>
    </div>
    """, unsafe_allow_html=True)

    c2.markdown(f"""
    <div class="card">
        <div class="card-label">📉 Differenz</div>
        <div class="highlight">{data['differenz']:.2f} CHF</div>
        <div class="card-subtext">Endkasse - Kassenstock - erwartete Bar-Einnahmen</div>
    </div>
    """, unsafe_allow_html=True)

    c3.markdown(f"""
    <div class="card">
        <div class="card-label">💸 Trinkgeld total</div>
        <div class="highlight">{data['trinkgeld_total']:.2f} CHF</div>
        <div class="card-subtext">Automatisch aus positiver Differenz berechnet</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 💵 Kassenübersicht")

    st.markdown(f"""
    <div class="card">
        <div class="card-label">Kassenstock</div>
        <div class="highlight">{data['startkasse']:.2f} CHF</div>
        <div class="card-subtext">Dieser Betrag bleibt fix in der Kasse und wurde vom gezählten Bargeld abgezogen.</div>
        <br>
        <div class="card-label">Gezählte Endkasse</div>
        <div class="highlight">{data['endkasse']:.2f} CHF</div>
        <br>
        <div class="card-label">Berechneter Barumsatz</div>
        <div class="highlight">{data['barumsatz']:.2f} CHF</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 👥 Trinkgeld-Verteilung")

    mitarbeiter = data["mitarbeiter"]
    total_stunden = sum(ma["stunden"] for ma in mitarbeiter)

    if total_stunden > 0 and len(mitarbeiter) > 0:
        for ma in mitarbeiter:
            anteil = ma["stunden"] / total_stunden
            betrag = anteil * data["trinkgeld_total"]

            st.markdown(f"""
            <div class="card">
                <div class="card-name">👤 {ma['name'] if ma['name'] else 'Unbenannter Mitarbeiter'}</div>
                <div class="card-subtext">{ma['stunden']} Stunden gearbeitet</div>
                <div class="card-label" style="margin-top:10px;">Ausbezahltes Trinkgeld</div>
                <div class="highlight">💸 {betrag:.2f} CHF</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Keine Stunden → keine Verteilung")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔙 Bearbeiten", use_container_width=True):
            st.session_state.show_result = False

    with col2:
        if st.button("💾 Speichern", use_container_width=True):

            data = st.session_state.result

            mitarbeiter = data["mitarbeiter"]
            total_stunden = sum(ma["stunden"] for ma in mitarbeiter)

            trinkgeld_verteilung = []

            if total_stunden > 0:
                for ma in mitarbeiter:
                    anteil = ma["stunden"] / total_stunden
                    betrag = anteil * data["trinkgeld_total"]

                    trinkgeld_verteilung.append({
                        "name": ma["name"] if ma["name"] else "Unbenannter Mitarbeiter",
                        "stunden": ma["stunden"],
                        "betrag": round(betrag, 2)
                    })

            eintrag = {
                "timestamp": data["timestamp"],
                "name": data["name"],
                "datum": str(data["datum"]),
                "startkasse": data["startkasse"],
                "bar": data["bar"],
                "karte": data["karte"],
                "twint": data["twint"],
                "total": data["total"],
                "endkasse": data["endkasse"],
                "barumsatz": data["barumsatz"],
                "differenz": data["differenz"],
                "trinkgeld_total": data["trinkgeld_total"],
                "trinkgeld_verteilung": json.dumps(trinkgeld_verteilung, ensure_ascii=False)
            }

            neuer_eintrag = pd.DataFrame([eintrag])

            st.session_state["data_df"] = pd.concat(
                [st.session_state["data_df"], neuer_eintrag],
                ignore_index=True
            )

            data_manager = st.session_state["data_manager"]
            data_manager.save_user_data(
                st.session_state["data_df"],
                "data.csv"
            )

            st.session_state.show_result = False
            st.success("Gespeichert!")
            st.switch_page("views/home.py")