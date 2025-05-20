import streamlit as st
from fpdf import FPDF
from datetime import date
import os
import tempfile

def latin1_safe(text):
    return text.encode("latin-1", "replace").decode("latin-1")

# ✅ Genera PDF y lo guarda temporalmente como archivo
def genera_pdf(dati, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, latin1_safe("Contratto di Procacciamento d’Affari"), ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)

    righe = [
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

    for linea in righe:
        pdf.cell(200, 10, latin1_safe(linea), ln=True)

    temp_path = os.path.join(tempfile.gettempdir(), f"{filename}.pdf")
    pdf.output(temp_path)
    return temp_path

# Interfaccia Streamlit
st.title("📄 Generatore Contratto PDF – E-LUX (finale stabile)")

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

        nome_file = nome.replace(" ", "_")
        path_pdf = genera_pdf(dati, nome_file)

        with open(path_pdf, "rb") as f:
            st.download_button(
                label="📥 Scarica Contratto PDF",
                data=f,
                file_name=f"contratto_{nome_file}.pdf",
                mime="application/pdf"
            )
    else:
        st.warning("⚠️ Compila tutti i campi obbligatori.")
