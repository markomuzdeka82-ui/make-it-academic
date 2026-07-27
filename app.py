import streamlit as st
import google.generativeai as genai

# Postavke stranice
st.set_page_config(
    page_title="Make it Academic AI",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 Make it Academic AI")
st.write("Transformirajte ideje u besprijekoran akademski stil u sekundi.")

# Dohvaćanje API ključa
api_key = None
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]

if not api_key:
    api_key = st.sidebar.text_input("Unesite vaš Gemini API ključ:", type="password")

st.sidebar.header("⚙️ Postavke stila")
academic_level = st.sidebar.radio(
    "Razina formalnosti:",
    ["Standardni seminarski rad", "Znanstveni rad / Doktorat", "Kratka i sažeta forma"]
)


# --- OPTIMIZACIJA 1: cachiraj kreiranje modela, ne radi se iznova svaki put ---
@st.cache_resource(show_spinner=False)
def get_model(key: str):
    genai.configure(api_key=key)
    return genai.GenerativeModel("gemini-1.5-flash")


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

text_input = st.text_area(
    "Unesite rečenicu ili odaberite instant primjer iznad:",
    value=st.session_state["user_text"],
    height=100
)

if st.button("Make it Academic! 🚀", use_container_width=True):
    if not api_key:
        st.error("Molimo unesite API ključ u bočnom izborniku ili ga postavite u Streamlit Secrets.")
    elif not text_input.strip():
        st.warning("Molimo unesite tekst ili kliknite na neki od instant primjera.")
    else:
        try:
            model = get_model(api_key)

            prompt = f"""
Djeluj kao vrhunski akademski mentor.
Preoblikuj sljedeću misao na hrvatskom jeziku u akademski stil.
Razina stila: {academic_level}
Ulazni tekst: {text_input}

Struktura odgovora:
**🤖 AI Uvid:** (Kratka analiza teze u 1 rečenici)

**1. Standardna opcija:**
(Formalna akademska rečenica)

**2. Znanstveno-analitička opcija:**
(Izrazito stručna rečenica s pasivnim oblicima)

**3. Sažeta teza:**
(Kratka i direktna rečenica za hipotezu)
"""

            st.markdown("---")

            # --- OPTIMIZACIJA 2: streaming odgovora ---
            # Tekst se prikazuje čim stigne prvi dio, umjesto čekanja
            # da se generira cijeli odgovor. Ovo je najveća promjena
            # za percepciju brzine.
            placeholder = st.empty()
            full_response = ""

            with st.spinner("Generiram akademske opcije..."):
                response_stream = model.generate_content(prompt, stream=True)
                for chunk in response_stream:
                    if chunk.text:
                        full_response += chunk.text
                        placeholder.markdown(full_response + "▌")

            placeholder.markdown(full_response)

        except Exception as e:
            st.error(f"Došlo je do pogreške: {e}")

st.markdown("---")
st.caption("© 2026 Make it Academic. Sva prava pridržana.")
