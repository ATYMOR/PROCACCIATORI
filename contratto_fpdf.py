import streamlit as st
from fpdf import FPDF
from datetime import date
import base64

# Función para generar el PDF
def generar_pdf(datos):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Contratto di Procacciamento d’Affari", ln=True, align='C')
    pdf.ln(10)

    for key, value in datos.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

    return pdf.output(dest='S').encode('latin1')

# Interfaz de usuario
st.title("📄 Generatore Contratto PDF")

with st.form("form_contratto"):
    nome = st.text_input("Nome e Cognome")
    sede = st.text_input("Sede")
    via = st.text_input("Via")
    piva = st.text_input("Partita IVA")
    cf = st.text_input("Codice Fiscale")
    prov_gas = st.number_input("Provvigione Gas Metano (€/mc)", format="%.2f")
    prov_luce = st.number_input("Provvigione Luce (€/pod)", format="%.2f")
    data = date.today().strftime("%d/%m/%Y")
    genera = st.form_submit_button("📄 Genera Contratto")

if genera:
    if all([nome, sede, via, piva, cf]):
        dati = {
            "Nome e Cognome": nome,
            "Sede": sede,
            "Via": via,
            "Partita IVA": piva,
            "Codice Fiscale": cf,
            "Provvigione Gas Metano (€/mc)": f"{prov_gas:.2f}",
            "Provvigione Luce (€/pod)": f"{prov_luce:.2f}",
            "Data": data
        }

        pdf_bytes = generar_pdf(dati)
        b64 = base64.b64encode(pdf_bytes).decode()
        href = f'<a href="data:application/pdf;base64,{b64}" download="contratto.pdf">📥 Scarica Contratto PDF</a>'
        st.markdown(href, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Compila tutti i campi obbligatori.")
