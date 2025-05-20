import streamlit as st
from datetime import date
from docx import Document
import tempfile
import os
import pypandoc

# ✅ Reemplaza los campos del docx
def compila_docx(dati, nome_file):
    template_path = "contratto_template.docx"  # La plantilla debe estar en el mismo repo
    doc = Document(template_path)

    for par in doc.paragraphs:
        for key, value in dati.items():
            if f"{{{{{key}}}}}" in par.text:
                par.text = par.text.replace(f"{{{{{key}}}}}", str(value))

    output_path = os.path.join(tempfile.gettempdir(), f"{nome_file}.docx")
    doc.save(output_path)
    return output_path

# ✅ Convierte DOCX a PDF usando Pandoc
def converti_docx_a_pdf(docx_path):
    pdf_path = docx_path.replace(".docx", ".pdf")
    try:
        pypandoc.convert_file(docx_path, 'pdf', outputfile=pdf_path)
    except OSError:
        pypandoc.download_pandoc()
        pypandoc.convert_file(docx_path, 'pdf', outputfile=pdf_path)
    return pdf_path

# 🖥️ Interfaz de usuario
st.title("📄 Generatore Contratto Word + PDF – E-LUX")

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
        path_docx = compila_docx(dati, nome_file)
        path_pdf = converti_docx_a_pdf(path_docx)

        st.success("✅ Contratto generato con successo!")

        # Descargar Word
        with open(path_docx, "rb") as f:
            st.download_button(
                label="📥 Scarica Word (.docx)",
                data=f,
                file_name=f"contratto_{nome_file}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

        # Descargar PDF
        with open(path_pdf, "rb") as f:
            st.download_button(
                label="📥 Scarica PDF (.pdf)",
                data=f,
                file_name=f"contratto_{nome_file}.pdf",
                mime="application/pdf"
            )
    else:
        st.warning("⚠️ Compila tutti i campi obbligatori.")
