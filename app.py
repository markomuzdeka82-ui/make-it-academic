import streamlit as st
import google.generativeai as genai

# Postavke stranice
st.set_page_config(
    page_title="Make it Academic",
    page_icon="🎓",
    layout="centered"
)

# Naslov i opis
st.title("🎓 Make it Academic")
st.write("Transformirajte svakodnevne misli i neformalne rečenice u besprijekoran akademski stil.")

# Dohvaćanje API ključa (prvo iz Secrets, a ako nema onda iz sidebar-a)
api_key = None
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]

if not api_key:
    api_key = st.sidebar.text_input("Unesite vaš Gemini API ključ:", type="password")

# Postavke u sidebar-u za prilagodbu stila
st.sidebar.header("⚙️ Postavke stila")
academic_level = st.sidebar.selectbox(
    "Odaberite razinu akademskog stila:",
    [
        "Seminarski / Diplomski rad (Standardno)",
        "Znanstveni članak / Doktorat (Napredno)",
        "Kratko i direktno (Sažeto)"
    ]
)

# Glavni ulazni tekst
text_input = st.text_area(
    "Unesite vašu rečenicu ili misao:",
    placeholder="Npr. Digitalizacija škola nije dobra jer djeca stalno gledaju u ekrane...",
    height=120
)

# Gumb za pokretanje
if st.button("Make it Academic! 🚀", use_container_width=True):
    if not api_key:
        st.error("Molimo unesite API ključ u bočnom izborniku ili ga postavite u Streamlit Secrets.")
    elif not text_input.strip():
        st.warning("Molimo unesite tekst koji želite transformirati.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")

            # Prilagodba instrukcija ovisno o odabranoj razini
            if "Znanstveni" in academic_level:
                style_instruction = "Koristi izrazito napredan, znanstveni vokabular, pasivne konstrukcije, stručnu terminologiju te objektivan, distanciran ton."
            elif "Kratko" in academic_level:
                style_instruction = "Preoblikuj u akademski stil, ali neka rečenica bude izrazito sažeta, jasna i izravna bez nepotrebnih riječi."
            else:
                style_instruction = "Koristi standardni akademski stil prikladan za fakultetske i seminarske radove, s formalnim i stručnim rječnikom."

            prompt = f"""
            Preoblikuj sljedeću tvrdnju u akademski stil na hrvatskom jeziku.
            
            Upute za stil: {style_instruction}
            
            Važno: Ponudi TOČNO 2 različite varijacije (Opcija A i Opcija B) koje zadržavaju izvorno značenje.
            
            Formatiraj odgovor točno ovako:
            **Opcija A:** [Prva varijacija]
            
            ---
            
            **Opcija B:** [Druga varijacija]
            
            Izvorni tekst: '{text_input}'
            """

            with st.spinner("Preoblikujem u akademski stil..."):
                response = model.generate_content(prompt)
                
                st.subheader("✨ Akademske verzije:")
                st.markdown(response.text)
                
                # Omogućavanje brzog kopiranja kompletnog rezultata
                st.divider()
                st.caption("💡 Savjet: Odaberite varijaciju koja se najbolje uklapa u kontekst vašeg rada.")

        except Exception as e:
            st.error(f"Došlo je do pogreške prilikom obrade: {e}")

# Podnožje
st.markdown("---")
st.caption("© 2026 Make it Academic. Sva prava pridržana.")
