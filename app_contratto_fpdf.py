import streamlit as st
from fpdf import FPDF
from datetime import date
import base64

# 📄 Funzione per generare il PDF
def genera_pdf(dati):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, "Contratto di Procacciamento d’Affari", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)

    lines = [
        f"Il sottoscritto {dati['NOME']} con sede in {dati['SEDE']},",
        f"via {dati['VIA']}, P.IVA {dati['PIVA']}, C.F. {dati['CF']},",
        "assume l’incarico di procacciatore d’affari per conto della società E-LUX Srl.",
        "",
        f"Provvigione Gas Metano: {dati['PROV_GAS']} €/mc",
        f"Provvigione Luce: {dati['PROV_LUCE']} €/pod",
        "",
        f"Data di sottoscrizione: {dati['DATA']}",
        "",
        "Firma del Procacciatore:",
        "",
        "____________________________"
    ]

    for line in lines:
        pdf.cell(200, 10, line, ln=True)

    return pdf.output(dest='S').encode('latin1')

# 🖥️ Interfaccia utente
st.title("📄 Generatore Contratto PDF (FPDF)")

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
            "NOME": nome,
            "SEDE": sede,
            "VIA": via,
            "PIVA": piva,
            "CF": cf,
            "PROV_GAS": f"{prov_gas:.2f}",
            "PROV_LUCE": f"{prov_luce:.2f}",
            "DATA": data
        }

        pdf_bytes = genera_pdf(dati)
        b64 = base64.b64encode(pdf_bytes).decode()
        href = f'<a href="data:application/pdf;base64,{b64}" download="contratto_{nome.replace(" ", "_")}.pdf">📥 Scarica Contratto PDF</a>'
        st.markdown(href, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Compila tutti i campi obbligatori.")
