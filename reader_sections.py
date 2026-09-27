from __future__ import annotations

import fitz
import pandas as pd
import requests
import streamlit as st

from study_content import (
    EQUATION_GUIDE,
    FIGURE_CROPS,
    METHOD_FACTS,
    PAGE_FIGURES,
    PAGE_GUIDE,
    PAPER_PDF_URL,
    PRIOR_WORK,
)


@st.cache_data(show_spinner=False, ttl=86400)
def _download_source_pdf() -> bytes:
    response = requests.get(PAPER_PDF_URL, timeout=30)
    response.raise_for_status()
    return response.content


@st.cache_data(show_spinner=False)
def _render_source_figure(fig_number: int, dpi: int = 170) -> bytes:
    meta = FIGURE_CROPS[fig_number]
    pdf_bytes = _download_source_pdf()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    page = doc[meta["page"] - 1]

    x0, y0, x1, y1 = meta["box"]
    rect = page.rect
    clip = fitz.Rect(
        rect.x0 + x0 * rect.width,
        rect.y0 + y0 * rect.height,
        rect.x0 + x1 * rect.width,
        rect.y0 + y1 * rect.height,
    )
    zoom = dpi / 72.0
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=clip, alpha=False)
    return pix.tobytes("png")


def render_reader_sidebar() -> tuple[int, int | None]:
    st.sidebar.header("Lecture page par page")
    page_number = st.sidebar.slider(
        "Page de l'étude",
        min_value=1,
        max_value=15,
        value=1,
        step=1,
        key="study_page_slider",
    )
    page = PAGE_GUIDE[page_number - 1]
    figures = PAGE_FIGURES[page_number]
    st.sidebar.caption(f"Article p. {page['article_page']} · {page['title']}")

    selected_figure = None
    if figures:
        figure_position = st.sidebar.slider(
            "Figure de la page",
            min_value=1,
            max_value=len(figures),
            value=1,
            step=1,
            key=f"figure_slider_page_{page_number}",
        )
        selected_figure = figures[figure_position - 1]
        st.sidebar.caption(f"Fig. {selected_figure} · {FIGURE_CROPS[selected_figure]['title']}")
    else:
        st.sidebar.caption("Aucune figure numérotée sur cette page.")

    return page_number, selected_figure


def render_page_reader(page_number: int, selected_figure: int | None) -> None:
    st.subheader("Lecture page par page")
    st.caption(
        "Le curseur de gauche choisit la page du papier. Lorsqu'une page contient plusieurs figures, "
        "le second curseur fait défiler les figures originales de cette page."
    )

    page = PAGE_GUIDE[page_number - 1]

    st.markdown(f"### PDF p. {page_number} · article p. {page['article_page']} — {page['title']}")
    st.write(page["summary"])

    if selected_figure is not None:
        meta = FIGURE_CROPS[selected_figure]
        st.markdown(f"#### Fig. {selected_figure} — {meta['title']}")
        try:
            image_bytes = _render_source_figure(selected_figure)
            st.image(image_bytes, use_container_width=True)
            st.caption(
                f"Figure originale extraite de la page PDF {meta['page']} du papier source. "
                "Le curseur à gauche permet de changer de figure lorsqu'il y en a plusieurs sur la page."
            )
        except Exception as exc:
            st.warning(
                "La figure originale n'a pas pu être chargée depuis la copie publique du papier. "
                f"Le résumé et les repères restent disponibles. Détail technique : {exc}"
            )

    left, right = st.columns([1.15, 0.85])
    with left:
        st.markdown("#### Informations importantes")
        for item in page["important"]:
            st.markdown(f"- {item}")
    with right:
        st.markdown("#### Repères de lecture")
        for fig in page["figures"]:
            st.markdown(f"- **Figure :** {fig}")
        for eq in page["equations_tables"]:
            st.markdown(f"- **Équation / table :** {eq}")

    st.info(f"**Question à garder en tête :** {page['question']}")

    with st.expander("Vue condensée des 15 pages"):
        summary = pd.DataFrame(
            [
                {
                    "PDF": item["pdf_page"],
                    "Article": item["article_page"],
                    "Sujet": item["title"],
                    "À retenir": item["important"][0],
                }
                for item in PAGE_GUIDE
            ]
        )
        st.dataframe(summary, use_container_width=True, hide_index=True)


def render_method_and_equations() -> None:
    st.subheader("Méthode et équations — comprendre ce qui est réellement calculé")
    st.caption("Repères principaux : PDF p. 3-6 · article p. 63-66")

    st.markdown("### Paramètres numériques et cinématiques")
    method_df = pd.DataFrame(METHOD_FACTS, columns=["Élément", "Valeur / description"])
    st.dataframe(method_df, use_container_width=True, hide_index=True)

    st.markdown("### État de l'art cité dans l'introduction")
    prior_df = pd.DataFrame(PRIOR_WORK)
    prior_df.columns = ["Référence", "Résultat rapporté", "Comment le lire"]
    st.dataframe(prior_df, use_container_width=True, hide_index=True)
    st.caption(
        "Ces valeurs viennent d'études citées par Xiao et al. et ne constituent pas un benchmark homogène."
    )

    st.markdown("### Les équations à comprendre")
    for eq in EQUATION_GUIDE:
        with st.expander(f"{eq['name']} — {eq['source']}"):
            if "=" in eq["equation"]:
                st.latex(eq["equation"])
            else:
                st.write(eq["equation"])
            st.write(eq["meaning"])