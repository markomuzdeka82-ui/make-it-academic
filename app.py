import streamlit as st
import google.generativeai as genai

# Postavke stranice
st.set_page_config(page_title="Make it Academic", page_icon="🎓")

st.title("🎓 Make it Academic")
st.write("Transformirajte svakodnevne misli u besprijekoran akademski stil.")

# Provjera API ključa
api_key = None

if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]

if not api_key:
    api_key = st.sidebar.text_input("Unesite vaš Gemini API ključ:", type="password")

# Glavno sučelje
text_input = st.text_area("Unesite vašu rečenicu ili misao:", placeholder="Npr. Besplatan javni prijevoz šteti društvu")

if st.button("Make it Academic! 🚀"):
    if not api_key:
        st.error("Molimo unesite API ključ u bočnom izborniku ili ga postavite u Streamlit Secrets.")
    elif not text_input.strip():
        st.warning("Molimo unesite tekst koji želite transformirati.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            prompt = f"Preoblikuj sljedeću tvrdnju u formalni, akademski stil na hrvatskom jeziku. Zadrži izvorno značenje, ali koristi stručniji i akademski vokabular:\n\n'{text_input}'"
            
            # Prikazujemo natpis dok čeka
            st.success("**Akademska verzija:**")
            
            # Generiramo tekst u stvarnom vremenu (stream=True)
            response = model.generate_content(prompt, stream=True)
            
            # st.write_stream ispisuje riječ po riječ čim stignu od Googlea
            st.write_stream(chunk.text for chunk in response)
            
        except Exception as e:
            st.error(f"Došlo je do pogreške: {e}")

st.markdown("---")
st.caption("© 2026 Make it Academic. Sva prava pridržana.")
