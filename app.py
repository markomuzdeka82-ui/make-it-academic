import streamlit as st
import google.generativeai as genai

# Postavke stranice
st.set_page_config(page_title="Make it Academic AI", page_icon="🎓")

st.title("🎓 Make it Academic AI")
st.write("Transformirajte ideje u besprijekoran akademski stil.")

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

# Instant primjeri
st.write("⚡ **Instant primjeri:**")
col1, col2, col3 = st.columns(3)

if "user_text" not in st.session_state:
    st.session_state["user_text"] = ""

if col1.button("📱 Ekran & Djeca"):
    st.session_state["user_text"] = "Djeca previše gledaju u ekrane i to im uništava koncentraciju u školi."
if col2.button("🚌 Javni prijevoz"):
    st.session_state["user_text"] = "Besplatan javni prijevoz smanjuje gužve u gradovima."
if col3.button("🤖 Umjetna inteligencija"):
    st.session_state["user_text"] = "AI će zamijeniti puno poslova, ali će otvoriti nove prilike."

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
            
            # Koristimo standardni stabilni model
            model = genai.GenerativeModel("gemini-1.5-flash")

            prompt = f"""
            Preoblikuj sljedeću tvrdnju u akademski stil na hrvatskom jeziku (Razina: {academic_level}).
            
            Daj kratak odgovor u ovom formatu:
            
            **Opcija 1 (Standardno):**
            [Napiši preoblikovanu rečenicu]
            
            **Opcija 2 (Znanstveno):**
            [Napiši napredniju rečenicu s pasivnim oblicima]
            
            Tekst: '{text_input}'
            """

            with st.spinner("Generiram akademski tekst..."):
                response = model.generate_content(prompt)
                
                if response.text:
                    st.success("✅ Gotovo!")
                    st.markdown(response.text)
                else:
                    st.error("Model nije vratio odgovor. Pokušajte ponovno.")

        except Exception as e:
            st.error(f"Pojavila se greška s API ključem ili servisom: {e}")

st.markdown("---")
st.caption("© 2026 Make it Academic. Sva prava pridržana.")
