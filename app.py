import os
import streamlit as st
import google.generativeai as genai
# Pokušaj prvo uzeti ključ iz Streamlit Secrets, a ako ga nema, provjeri sidebar
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    api_key = st.sidebar.tex_input("Unesite vaš Gemini API ključ:", type="password")

# Config stranice
st.set_page_config(page_title="Make it Academic", page_icon="🎓", layout="centered")

# Naslov i opis aplikacije
st.title("🎓 Make it Academic")
st.caption("Transformirajte svakodnevne misli u besprijekoran akademski stil.")

# Unos API ključa u sidebar (ili iz environment varijable)
with st.sidebar:
    st.header("Postavke")
    api_key = st.text_input("Unesite vaš Gemini API ključ:", type="password")
    st.markdown("[Kako dobiti besplatni Gemini API ključ?](https://aistudio.google.com/)")

# Glavno polje za unos teksta
user_input = st.text_area(
    "Unesite vašu rečenicu ili misao:",
    placeholder="Npr. Brza hrana je jeftina pa je svi jedu i debljaju se.",
    height=100
)

# Gumb za transformaciju
if st.button("Make it Academic! 🚀", type="primary"):
    if not api_key:
        st.error("Molimo unesite API ključ u lijevom izborniku kako biste pokrenuli aplikaciju.")
    elif not user_input.strip():
        st.warning("Molimo unesite tekst za transformaciju.")
    else:
        try:
            # Konfiguracija Gemini modela
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')

            # Prompt s preciznim uputama za formatiranje
            prompt = f"""
            Djeluješ ako pozadinski sustav aplikacije 'Make it Academic'.
            Tvoj je zadatak analizirati sljedeći korisnički tekst i preoblikovati ga u visoki akademski registar.

            Korisnički tekst: "{user_input}"

            Odgovori isključivo u sljedećem formatu (koristi Markdown):

            ### 💎 Akademska verzija
            [Ovdje napiši preoblikovanu rečenicu u visokom akademskom stilu]

            ---
            ### 📚 Ključni stručni pojmovi
            * **[Pojam 1]**: [Kratko objašnjenje zašto je upotrijebljen i što znači]
            * **[Pojam 2]**: [Kratko objašnjenje zašto je upotrijebljen i što znači]

            ---
            ### 💡 Savjet za stil
            [Jedna rečenica objašnjenja koja sintaktička ili stilistička izmjena je napravljena (npr. nominalizacija, pasivizacija, uklanjanje kolokvijalizama)]
            """

            with st.spinner("Transformiram tekst u akademski stil..."):
                response = model.generate_content(prompt)
                st.markdown(response.text)

        except Exception as e:
            st.error(f"Došlo je do pogreške prilikom komunikacije s AI modelom: {e}")

# Podnožje
st.divider()
st.caption("© 2026 Make it Academic. Sva prava pridržana.")
