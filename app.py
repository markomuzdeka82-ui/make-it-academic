import streamlit as st
import google.generativeai as genai

# Postavke stranice
st.set_page_config(
    page_title="Make it Academic AI",
    page_icon="🎓",
    layout="centered"
)

# Naslov i opis
st.title("🎓 Make it Academic AI")
st.write("Transformirajte ideje u besprijekoran akademski stil uz AI asistenciju u stvarnom vremenu.")

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

# Instant odgovori / Predlošci
st.write("⚡ **Instant primjeri (kliknite za brzi unos):**")
col1, col2, col3 = st.columns(3)

if "user_text" not in st.session_state:
    st.session_state["user_text"] = ""

if col1.button("📱 Ekran & Djeca"):
    st.session_state["user_text"] = "Djeca previše gledaju u ekrane i to im uništava koncentraciju u školi."
if col2.button("🚌 Javni prijevoz"):
    st.session_state["user_text"] = "Besplatan javni prijevoz smanjuje gužve u gradovima i loš je za zagađenje."
if col3.button("🤖 Umjetna inteligencija"):
    st.session_state["user_text"] = "AI će zamijeniti puno poslova, ali će otvoriti nove prilike u tehnologiji."

# Glavni ulazni tekst
text_input = st.text_area(
    "Unesite rečenicu ili odaberite instant primjer iznad:",
    value=st.session_state["user_text"],
    height=100,
    key="main_input"
)

# Funkcija za generiranje i streaming
def process_text(prompt_text):
    if not api_key:
        st.error("Molimo unesite API ključ u bočnom izborniku ili ga postavite u Streamlit Secrets.")
        return

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        system_prompt = f"""
        Djeluj kao vrhunski akademski mentor i AI stručnjak za pisanje radova na hrvatskom jeziku.
        Korisnik ti šalje neformalnu misao ili tvrdnju.
        
        Tvoj zadatak je odgovoriti u sljedećoj strukturi:
        1. **Kratki AI uvid (Kao asistencijski komentar):** Analiziraj u jednoj do dvije rečenice što je ključni problem/teza u izjavi.
        2. **Višestruke akademske opcije:**
           - **Opcija 1 (Standardna):** Formalna akademska formulacija.
           - **Opcija 2 (Znanstveno-analitička):** Izrazito stručna formulacija s pasivom i uzročno-posljedičnim konstrukcijama.
           - **Opcija 3 (Sažeta teza):** Izravna, fokusirana rečenica idealna za hipotezu ili zaključak.
        3. **Preporučeni stručni pojmovi:** Popis 3-4 ključna akademska pojma/vokabulara korištena u odgovoru.

        Odabrana razina stila: {academic_level}
        Ulazni tekst: '{prompt_text}'
        """

        with st.spinner("AI analizira i preoblikuje tekst..."):
            response = model.generate_content(system_prompt, stream=True)
            st.markdown("### 🤖 AI Odgovor i Preporuke")
            st.write_stream(chunk.text for chunk in response)

    except Exception as e:
        st.error(f"Došlo je do pogreške: {e}")

# Gumb za pokretanje
if st.button("Make it Academic! 🚀", use_container_width=True):
    if text_input.strip():
        process_text(text_input)
    else:
        st.warning("Molimo unesite tekst ili kliknite na neki od instant primjera.")

# Podnožje
st.markdown("---")
st.caption("© 2026 Make it Academic. Sva prava pridržana.")
