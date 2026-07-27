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
st.write("Transformirajte ideje u besprijekoran akademski stil u sekundi.")

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
    height=100
)

# Gumb za pokretanje
if st.button("Make it Academic! 🚀", use_container_width=True):
    if not api_key:
        st.error("Molimo unesite API ključ u bočnom izborniku ili ga postavite u Streamlit Secrets.")
    elif not text_input.strip():
        st.warning("Molimo unesite tekst ili kliknite na neki od instant primjera.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")

            system_prompt = f"""
            Djeluj kao vrhunski akademski mentor. 
            Korisnik ti šalje neformalnu misao. Preoblikuj je na hrvatskom jeziku.

            Struktura odgovora:
            **🤖 AI Uvid:** (Kratka analiza teze u 1 rečenici)

            **1. Standardna opcija:**
            (Formalna akademska rečenica)

            **2. Znanstveno-analitička opcija:**
            (Izrazito stručna rečenica s pasivnim oblicima)

            **3. Sažeta teza:**
            (Kratka i direktna rečenica za hipotezu)

            Razina stila: {academic_level}
            Ulazni tekst: '{text_input}'
            """

            with st.spinner("Generiram u sekundi..."):
                # Direktno generiranje bez st.write_stream izbjegava pauze i usporavanja
                response = model.generate_content(system_prompt)
                st.markdown("---")
                st.markdown(response.text)

        except Exception as e:
            st.error(f"Došlo je do pogreške: {e}")

# Podnožje
st.markdown("---")
st.caption("© 2026 Make it Academic. Sva prava pridržana.").")
