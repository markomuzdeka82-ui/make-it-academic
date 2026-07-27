import streamlit as st
import google.generativeai as genai

# Postavke stranice
st.set_page_config(page_title="Make it Academic AI", page_icon="🎓")

# Naslov s Flaticon ikonama (preko HTML-a)
st.markdown("""
    <h1 style='display: flex; align-items: center; gap: 10px;'>
        <img src="https://cdn-icons-png.flaticon.com/512/2997/2997293.png" width="45" height="45">
        Make it Academic AI
    </h1>
""", unsafe_allow_html=True)

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

# Instant primjeri s Flaticon ikonama
st.write("⚡ **Instant primjeri:**")

if "user_text" not in st.session_state:
    st.session_state["user_text"] = ""

col1, col2, col3 = st.columns(3)

# Prikaz gumba s HTML ikonama s Flaticona
with col1:
    st.markdown('<img src="https://cdn-icons-png.flaticon.com/512/644/644458.png" width="20"> <b>Ekrani</b>', unsafe_allow_html=True)
    if st.button("Uredi tekst o ekranima"):
        st.session_state["user_text"] = "Djeca previše gledaju u ekrane i to im uništava koncentraciju u školi."

with col2:
    st.markdown('<img src="https://cdn-icons-png.flaticon.com/512/3448/3448339.png" width="20"> <b>Prijevoz</b>', unsafe_allow_html=True)
    if st.button("Uredi tekst o prijevozu"):
        st.session_state["user_text"] = "Besplatan javni prijevoz smanjuje gužve u gradovima."

with col3:
    st.markdown('<img src="https://cdn-icons-png.flaticon.com/512/2103/2103633.png" width="20"> <b>AI Tehnologija</b>', unsafe_allow_html=True)
    if st.button("Uredi tekst o AI"):
        st.session_state["user_text"] = "AI će zamijeniti puno poslova, ali će otvoriti nove prilike."

st.write("")

# Glavni ulazni tekst
text_input = st.text_area(
    "Unesite rečenicu ili odaberite primjer iznad:",
    value=st.session_state["user_text"],
    height=100
)

# Gumb za pokretanje
if st.button("Make it Academic! 🚀", use_container_width=True):
    if not api_key:
        st.error("Molimo unesite API ključ u bočnom izborniku ili ga postavite u Streamlit Secrets.")
    elif not text_input.strip():
        st.warning("Molimo unesite tekst.")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # Ako gemini-2.5-flash ili gemini-2.0-flash ne rade na tvom ključu, vrati na gemini-1.5-flash
            model = genai.GenerativeModel("gemini-2.5-flash")

            prompt = f"""
            Preoblikuj sljedeću tvrdnju u akademski stil na hrvatskom jeziku (Razina: {academic_level}).
            
            Daj kratak odgovor u ovom formatu:
            
            **Opcija 1 (Standardno):**
            [Napiši preoblikovanu rečenicu]
            
            **Opcija 2 (Znanstveno):**
            [Napiši napredniju rečenicu s pasivnim oblicima]
            
            Tekst: '{text_input}'
            """

            with st.spinner("Generiram u sekundi..."):
                response = model.generate_content(prompt)
                
                if response.text:
                    st.success("✅ Gotovo!")
                    st.markdown(response.text)
                else:
                    st.error("Model nije vratio odgovor. Pokušajte ponovno.")

        except Exception as e:
            # Ako model gemini-2.5-flash baci grešku, pokušavamo s alternativnim nazivom
            st.error(f"Pojavila se greška s API-jem: {e}")

st.markdown("---")
st.caption("© 2026 Make it Academic. Sva prava pridržana.")
