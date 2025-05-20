import streamlit as st
from fpdf import FPDF
from datetime import date
import base64
from io import BytesIO

# 🧾 Funzione per generare PDF e restituirlo in memoria
def genera_pdf(dati):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, "Contratto di Procacciamento d’Affari", ln=True, align='C')
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
        linea_sicura = linea.encode('latin-1', 'replace').decode('latin-1')
        pdf.cell(200, 10, linea_sicura, ln=True)

    # Genera PDF in memoria (BytesIO)
    buffer = BytesIO()
    pdf.output(buffer)
    pdf_bytes = buffer.getvalue()
    return pdf_bytes

# 🖥️ Interfaccia Streamlit
st.title("📄 Generatore Contratto PDF – FPDF")

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

        pdf = genera_pdf(dati)
        st.success("✅ Contratto generato con successo!")

        st.download_button(
            label="📥 Scarica Contratto PDF",
            data=pdf,
            file_name=f"contratto_{nome.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("⚠️ Compila tutti i campi obbligatori.")
