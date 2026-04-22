import streamlit as st
from datetime import date

st.set_page_config(page_title="Calculator", layout="wide")

STARTKASSE = 300

# =========================
# 🎨 STYLE
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
}

.title {
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 10px;
}

.subtitle {
    font-size: 18px;
    font-weight: 600;
    margin-top: 20px;
}

.highlight {
    font-size: 22px;
    font-weight: bold;
    color: #16a34a;
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
# EINNAHMEN
# =========================
st.markdown('<div class="subtitle">💰 Einnahmen</div>', unsafe_allow_html=True)
col3, col4, col5 = st.columns(3)

bar = col3.number_input("💵 Bar", 0.0)
karte = col4.number_input("💳 Karte", 0.0)
twint = col5.number_input("📱 TWINT", 0.0)

# =========================
# KASSE
# =========================
st.markdown('<div class="subtitle">💵 Kasse</div>', unsafe_allow_html=True)
endkasse = st.number_input("Gezähltes Bargeld (Endkasse)", 0.0)

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
# BUTTONS (WICHTIG)
# =========================
colA, colB = st.columns(2)

with colA:
    if st.button("🔙 Zurück", use_container_width=True, type="secondary"):
        st.switch_page("app.py")

with colB:
    if st.button("➡️ Berechnen", use_container_width=True, type="secondary"):

        total = bar + karte + twint
        barumsatz = endkasse - STARTKASSE
        differenz = barumsatz - bar
        trinkgeld_total = max(differenz, 0)

        st.session_state.result = {
            "name": name,
            "datum": datum,
            "total": total,
            "bar": bar,
            "barumsatz": barumsatz,
            "endkasse": endkasse,
            "differenz": differenz,
            "trinkgeld_total": trinkgeld_total,
            "mitarbeiter": st.session_state.mitarbeiter
        }

        st.session_state.show_result = True

# =========================
# ERGEBNIS (PREVIEW)
# =========================
if st.session_state.show_result:

    data = st.session_state.result

    st.markdown("## 📊 Übersicht")

    c1, c2, c3 = st.columns(3)

    c1.markdown(f"""
    <div class="card">
    💰 Einnahmen<br>
    <div class="highlight">{data['total']:.2f} CHF</div>
    </div>
    """, unsafe_allow_html=True)

    c2.markdown(f"""
    <div class="card">
    📉 Differenz<br>
    <div class="highlight">{data['differenz']:.2f} CHF</div>
    </div>
    """, unsafe_allow_html=True)

    c3.markdown(f"""
    <div class="card">
    💸 Trinkgeld<br>
    <div class="highlight">{data['trinkgeld_total']:.2f} CHF</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 👥 Trinkgeld-Verteilung")

    mitarbeiter = data["mitarbeiter"]
    total_stunden = sum(ma["stunden"] for ma in mitarbeiter)

    if total_stunden > 0:
        for ma in mitarbeiter:
            anteil = ma["stunden"] / total_stunden
            betrag = anteil * data["trinkgeld_total"]

            st.markdown(f"""
            <div class="card">
            <strong>{ma['name']}</strong><br>
            {ma['stunden']} Stunden<br>
            💸 <span class="highlight">{betrag:.2f} CHF</span>
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
            if "history" not in st.session_state:
                st.session_state.history = []

            st.session_state.history.append(data)
            st.session_state.show_result = False
            st.success("Gespeichert!")
            st.switch_page("app.py")