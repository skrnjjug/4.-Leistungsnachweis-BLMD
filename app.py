import streamlit as st
from datetime import date

# =========================
# ⚙️ CONFIG
# =========================
st.set_page_config(
    page_title="BarCalc",
    page_icon="🍸",
    layout="wide"
)

STARTKASSE = 300

# =========================
# 🎨 GLOBAL STYLE (HELL)
# =========================
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.card {
    background: #f8fafc;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    margin-bottom: 15px;
    color: #1e293b;
}

.section-title {
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 10px;
    color: #0f172a;
}

.highlight {
    color: #16a34a;
    font-weight: bold;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 🧠 STATE
# =========================
if "page" not in st.session_state:
    st.session_state.page = "home"

if "history" not in st.session_state:
    st.session_state.history = []

if "mitarbeiter" not in st.session_state:
    st.session_state.mitarbeiter = []

# =========================
# 🔁 NAVIGATION
# =========================
def go_to(page):
    st.session_state.page = page


# =========================
# 🏠 HOME
# =========================
def show_home():
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #3b82f6, #6366f1);
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 30px;
    ">
        <h1>🍸 BarCalc</h1>
        <p>Dein smarter Begleiter für den Kassenabschluss</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="card">🔢 Neuer Tagesabschluss</div>', unsafe_allow_html=True)
        if st.button("Starten", use_container_width=True):
            st.session_state.mitarbeiter = []
            go_to("eingabe")

    with col2:
        st.markdown('<div class="card">📊 Verlauf & Übersicht</div>', unsafe_allow_html=True)
        if st.button("Öffnen", use_container_width=True):
            go_to("verlauf")


# =========================
# ✍️ EINGABE
# =========================
def show_input():
    st.markdown("## 🔢 Tagesabschluss")

    st.markdown('<div class="section-title">🧾 Basisdaten</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    name = col1.text_input("Name")
    datum = col2.date_input("Datum", value=date.today())

    st.markdown('<div class="section-title">💰 Einnahmen</div>', unsafe_allow_html=True)
    col3, col4, col5 = st.columns(3)

    bar = col3.number_input("💵 Bar (erfasst)", 0.0)
    karte = col4.number_input("💳 Karte", 0.0)
    twint = col5.number_input("📱 TWINT", 0.0)

    st.markdown('<div class="section-title">💵 Kasse</div>', unsafe_allow_html=True)
    endkasse = st.number_input("Gezähltes Bargeld (Endkasse)", 0.0)

    st.markdown('<div class="section-title">👥 Mitarbeiter</div>', unsafe_allow_html=True)

    if st.button("+ Mitarbeiter hinzufügen"):
        st.session_state.mitarbeiter.append({"name": "", "stunden": 0})

    for i, ma in enumerate(st.session_state.mitarbeiter):
        col1, col2 = st.columns(2)
        ma["name"] = col1.text_input(f"Name {i+1}", ma["name"], key=f"name_{i}")
        ma["stunden"] = col2.number_input(f"Stunden {i+1}", value=ma["stunden"], key=f"stunden_{i}")

    st.markdown("---")

    if st.button("➡️ Berechnen", use_container_width=True):
        total = bar + karte + twint

        barumsatz = endkasse - STARTKASSE
        differenz = barumsatz - bar
        trinkgeld_total = max(differenz, 0)

        st.session_state.temp = {
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

        go_to("ergebnis")


# =========================
# 📊 ERGEBNIS
# =========================
def show_result():
    data = st.session_state.get("temp", {})

    st.markdown("## 📊 Ergebnis")

    col1, col2, col3 = st.columns(3)

    col1.markdown(f"""
    <div class="card">
    💰 Einnahmen<br>
    <span class="highlight">{data.get('total', 0):.2f} CHF</span>
    </div>
    """, unsafe_allow_html=True)

    col2.markdown(f"""
    <div class="card">
    📉 Differenz<br>
    <span class="highlight">{data.get('differenz', 0):.2f} CHF</span>
    </div>
    """, unsafe_allow_html=True)

    col3.markdown(f"""
    <div class="card">
    💸 Trinkgeld<br>
    <span class="highlight">{data.get('trinkgeld_total', 0):.2f} CHF</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
    💵 Startkasse: {STARTKASSE} CHF<br>
    💵 Endkasse: {data.get('endkasse')} CHF<br>
    <span class="highlight">Barumsatz: {data.get('barumsatz'):.2f} CHF</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">👥 Trinkgeld-Verteilung</div>', unsafe_allow_html=True)

    mitarbeiter = data.get("mitarbeiter", [])
    total_stunden = sum(ma["stunden"] for ma in mitarbeiter)

    if total_stunden > 0:
        for ma in mitarbeiter:
            anteil = ma["stunden"] / total_stunden
            betrag = anteil * data.get("trinkgeld_total", 0)

            st.markdown(f"""
            <div class="card">
            <strong>{ma['name']}</strong><br>
            {ma['stunden']} Stunden<br>
            <span class="highlight">💸 {betrag:.2f} CHF</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Keine Stunden erfasst → keine Verteilung möglich")

    col4, col5 = st.columns(2)

    with col4:
        if st.button("🔙 Bearbeiten", use_container_width=True):
            go_to("eingabe")

    with col5:
        if st.button("💾 Speichern", use_container_width=True):
            st.session_state.history.append(data)
            go_to("verlauf")


# =========================
# 📂 VERLAUF
# =========================
def show_history():
    st.markdown("## 📂 Verlauf")

    history = st.session_state.history

    if not history:
        st.info("Noch keine Einträge vorhanden.")

    for i, entry in enumerate(history):
        col1, col2 = st.columns(2)

        col1.markdown(f"""
        <div class="card">
        📅 {entry.get("datum")}<br>
        💰 {entry.get("total")} CHF
        </div>
        """, unsafe_allow_html=True)

        if col2.button("Details", key=f"detail_{i}"):
            st.session_state.selected = entry
            go_to("detail")

    if st.button("🔙 Zurück"):
        go_to("home")


# =========================
# 📄 DETAIL
# =========================
def show_detail():
    st.markdown("## 📄 Detail")

    entry = st.session_state.get("selected", {})

    st.markdown(f"""
    <div class="card">
    📅 {entry.get("datum")}<br>
    💰 {entry.get("total")} CHF<br>
    💸 Trinkgeld: {entry.get("trinkgeld_total")} CHF
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔙 Zurück"):
        go_to("verlauf")


# =========================
# 🔁 ROUTING
# =========================
if st.session_state.page == "home":
    show_home()

elif st.session_state.page == "eingabe":
    show_input()

elif st.session_state.page == "ergebnis":
    show_result()

elif st.session_state.page == "verlauf":
    show_history()

elif st.session_state.page == "detail":
    show_detail()