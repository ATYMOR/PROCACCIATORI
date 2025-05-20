import streamlit as st
import tempfile
import os
import subprocess
from datetime import date

# Template LaTeX
latex_template = r"""
\documentclass[11pt]{article}
\usepackage[margin=2.5cm]{geometry}
\usepackage[utf8]{inputenc}
\usepackage{lmodern}
\usepackage{datetime}
\renewcommand{\familydefault}{\sfdefault}

\begin{document}

\section*{Contratto di Procacciamento d’Affari}

Tra la società \textbf{E-LUX Srl} e il Procacciatore:

\vspace{0.5cm}

\textbf{Nome:} {{NOME}} \\
\textbf{Sede:} {{SEDE}} \\
\textbf{Via:} {{VIA}} \\
\textbf{Partita IVA:} {{PIVA}} \\
\textbf{Codice Fiscale:} {{CF}} \\

\vspace{0.5cm}

Si concordano le seguenti provvigioni: \\
- Gas Metano: \textbf{{PROV_GAS}} €/mc \\
- Energia Elettrica: \textbf{{PROV_LUCE}} €/pod

\vspace{0.5cm}

Data di sottoscrizione: \textbf{{DATA}} \\
\\[2cm]

\begin{tabular}{p{7cm}p{7cm}}
\textbf{E-LUX Srl} & \textbf{Il Procacciatore} \\
\rule{7cm}{0.4pt} & \rule{7cm}{0.4pt}
\end{tabular}

\end{document}
"""

# Funzione per generare il LaTeX compilato
def genera_pdf(dati, filename_base):
    tex_content = latex_template
    for k, v in dati.items():
        tex_content = tex_content.replace(f"{{{{{k}}}}}", str(v))

    temp_dir = tempfile.mkdtemp()
    tex_path = os.path.join(temp_dir, f"{filename_base}.tex")
    with open(tex_path, "w") as f:
        f.write(tex_content)

    # Compilazione con pdflatex
    subprocess.run(
        ["pdflatex", "-output-directory", temp_dir, tex_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True
    )

    pdf_path = os.path.join(temp_dir, f"{filename_base}.pdf")
    return pdf_path

# UI Streamlit
st.title("📄 Generatore Contratto PDF (compilato con pdflatex)")

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

        filename = f"contratto_{nome.replace(' ', '_')}"
        try:
            pdf_path = genera_pdf(dati, filename)
            with open(pdf_path, "rb") as f:
                st.download_button(
                    "📥 Scarica Contratto PDF",
                    data=f,
                    file_name=filename + ".pdf",
                    mime="application/pdf"
                )
        except subprocess.CalledProcessError:
            st.error("Errore durante la compilazione del PDF con pdflatex.")
    else:
        st.warning("⚠️ Compila tutti i campi obbligatori.")
