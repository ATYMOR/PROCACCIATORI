import streamlit as st
from datetime import date
from docx import Document
import tempfile
import os

# 📄 Función para reemplazar los campos en el documento Word
def compila_docx(template_path, dati, nome_file):
    doc = Document(template_path)
    for par in doc.paragraphs:
        for key, value in dati.items():
            if f"{{{{{key}}}}}" in par.text:
                par.text = par.text.replace(f"{{{{{key}}}}}", str(value))

    # Guardar documento final en directorio temporal
    output_path = os.path.join(tempfile.gettempdir(), f"{nome_file}.docx")
    doc.save(output_path)
    return output_path

# 🖥️ Interfaz Streamlit
st.title("📄 Generatore Contratto Word da Template")

# Cargar plantilla
template_path = "/mnt/data/contratto_template.docx"

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
        path_finale = compila_docx(template_path, dati, nome_file)

        with open(path_finale, "rb") as f:
            st.download_button(
                label="📥 Scarica Contratto Word (.docx)",
                data=f,
                file_name=f"contratto_{nome_file}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
    else:
        st.warning("⚠️ Compila tutti i campi obbligatori.")
