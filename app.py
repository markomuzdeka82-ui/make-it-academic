import streamlit as st
from google import genai

# Postavke stranice
st.set_page_config(page_title="Make it Academic AI", page_icon="🎓", layout="centered")

# Naslov s Flaticon ikonama
st.markdown("""
    <h1 style='display: flex; align-items: center; gap: 12px;'>
        <img src="https://cdn-icons-png.flaticon.com/512/2997/2997293.png" width="45" height="45">
        Make it Academic AI
    </h1>
""", unsafe_allow_html=True)

st.write("Vaš osobni AI asistent za pretvaranje svakodnevnih misli u besprijekoran akademski stil.")

# Dohvaćanje API ključa
api_key = None
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]

if not api_key:
    api_key = st.sidebar.text_input("Unesite vaš Gemini API ključ:", type="password")

# Postavke u sidebar-u
st.sidebar.header("⚙️ Postavke stila")
academic_level = st.sidebar.radio(
    "Razina formalnosti:",
    ["Standardni seminarski rad", "Znanstveni rad / Doktorat", "Kratka i sažeta forma"]
)

# Instant primjeri s Flaticon ikonama
st.write("⚡ **Brzi primjeri (kliknite za unos):**")

if "user_text" not in st.session_state:
    st.session_state["user_text"] = ""

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<img src="https://cdn-icons-png.flaticon.com/512/644/644458.png" width="18"> <b>Ekrani</b>', unsafe_allow_html=True)
    if st.button("Uredi tekst o ekranima"):
        st.session_state["user_text"] = "Djeca previše gledaju u ekrane i to im uništava koncentraciju u školi."

with col2:
    st.markdown('<img src="https://cdn-icons-png.flaticon.com/512/3448/3448339.png" width="18"> <b>Prijevoz</b>', unsafe_allow_html=True)
    if st.button("Uredi tekst o prijevozu"):
        st.session_state["user_text"] = "Besplatan javni prijevoz smanje gužve u gradovima."

with col3:
    st.markdown('<img src="https://cdn-icons-png.flaticon.com/512/2103/2103633.png" width="18"> <b>AI Tehnologija</b>', unsafe_allow_html=True)
    if st.button("Uredi tekst o AI"):
        st.session_state["user_text"] = "AI će zamijeniti puno poslova, ali će otvoriti nove prilike."

st.write("")

# Glavni ulazni tekst
text_input = st.text_area(
    "Unesite rečenicu ili misao:",
    value=st.session_state["user_text"],
    height=100,
    placeholder="Upišite svoju rečenicu ovdje..."
)

# Gumb za pokretanje
if st.button("Make it Academic! 🚀", use_container_width=True):
    if not api_key:
        st.error("Molimo unesite API ključ u bočnom izborniku ili ga postavite u Streamlit Secrets.")
    elif not text_input.strip():
        st.warning("Molimo unesite tekst ili odaberite neki od primjera.")
    else:
        try:
            # Pokretanje novog klijenta
            client = genai.Client(api_key=api_key)

            prompt = f"""
            Djeluj kao pristupačan, pametan i stručan AI asistent.
            Korisnik ti šalje neformalnu rečenicu, a ti mu odgovaraš izravno i odmah na hrvatskom jeziku.

            Formatiraj odgovor točno ovako:

            Bok! Evo kako možemo tvoju misao pretvoriti u akademski stil:

            💬 **Kratki AI uvid:**
            (Napiši 1-2 rečenice analize teze)

            🎓 **Preporučene akademske opcije:**

            * **Opcija A (Standardni akademski stil):**
            "(Umetni formalnu rečenicu)"

            * **Opcija B (Napredni znanstveni stil):**
            "(Umetni rečenicu s pasivnim oblicima)"

            💡 **Ključni stručni pojmovi:**
            (Navedi 3-4 stručna pojma)

            Odabrana razina stila: {academic_level}
            Uneseni tekst korisnika: '{text_input}'
            """

            response_container = st.empty()
            full_text = ""

            # Poziv s novim SDK-om koji munjevito ispisuje slovo po slovo
            response = client.models.generate_content_stream(
                model="gemini-2.5-flash",
                contents=prompt,
            )

            for chunk in response:
                if chunk.text:
                    full_text += chunk.text
                    response_container.markdown(full_text)

        except Exception as e:
            st.error(f"Pojavila se greška: {e}")

st.markdown("---")
st.caption("© 2026 Make it Academic. Sva prava pridržana.")
