import streamlit as st
from datetime import date
from docx import Document
import os
import tempfile
from docx2pdf import convert

# Reemplazo de variables en el documento
def compila_contratto(doc, dati):
    for par in doc.paragraphs:
        for key, value in dati.items():
            if f"{{{{{key}}}}}" in par.text:
                par.text = par.text.replace(f"{{{{{key}}}}}", str(value))
    return doc

# Guardar Word temporal
def salva_docx(doc, filename):
    temp_dir = tempfile.gettempdir()
    path_docx = os.path.join(temp_dir, filename + ".docx")
    doc.save(path_docx)
    return path_docx

# Convertir Word a PDF
def converti_pdf(path_docx):
    path_pdf = path_docx.replace(".docx", ".pdf")
    convert(path_docx, path_pdf)
    return path_pdf

# Interfaz
st.title("📄 Generatore Contratto E-LUX (Word + PDF)")

# Subida de plantilla
template_file = st.file_uploader("📎 Carica il modello del contratto (.docx)", type="docx")

# Formulario de datos
with st.form("form_contratto"):
    st.subheader("🔧 Dati da compilare")
    nome = st.text_input("Nome e Cognome")
    sede = st.text_input("Sede")
    via = st.text_input("Via")
    piva = st.text_input("Partita IVA")
    cf = st.text_input("Codice Fiscale")
    prov_gas = st.number_input("Provvigione Gas Metano (€/mc)", format="%.2f")
    prov_luce = st.number_input("Provvigione Luce (€/pod)", format="%.2f")
    data = date.today().strftime("%d/%m/%Y")

    submit = st.form_submit_button("📄 Genera Contratto")

# Lógica de generación
if submit:
    if not template_file:
        st.error("⚠️ Carica prima un file modello .docx.")
    elif not all([nome, sede, via, piva, cf]):
        st.error("⚠️ Compila tutti i campi richiesti.")
    else:
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

        doc = Document(template_file)
        doc = compila_contratto(doc, dati)

        filename = f"contratto_{nome.replace(' ', '_')}"
        path_docx = salva_docx(doc, filename)
        path_pdf = converti_pdf(path_docx)

        st.success("✅ Contratto generato con successo!")

        # Botones de descarga
        with open(path_docx, "rb") as f:
            st.download_button("📥 Scarica Word (.docx)", data=f, file_name=filename + ".docx")

        with open(path_pdf, "rb") as f:
            st.download_button("📥 Scarica PDF (.pdf)", data=f, file_name=filename + ".pdf")

        # Limpieza
        os.remove(path_docx)
        os.remove(path_pdf)
