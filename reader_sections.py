from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from figure_content import figures_for_page
from study_content import EQUATION_GUIDE, METHOD_FACTS, PAGE_GUIDE, PRIOR_WORK

ROOT = Path(__file__).resolve().parent


def render_reader_sidebar() -> tuple[int, int]:
    st.sidebar.header("Lecture page par page")
    page_number = st.sidebar.slider(
        "Page du PDF",
        min_value=1,
        max_value=len(PAGE_GUIDE),
        value=1,
        step=1,
        help="Fait avancer l'étude page par page, de l'abstract à la conclusion.",
    )

    figures = figures_for_page(page_number)
    if len(figures) > 1:
        figure_index = st.sidebar.slider(
            "Figure de cette page",
            min_value=1,
            max_value=len(figures),
            value=1,
            step=1,
            help="Change la figure source affichée pour la page sélectionnée.",
        )
        selected = figures[figure_index - 1]
        st.sidebar.caption(f"Fig. {selected['figure']} — {selected['title']}")
    elif len(figures) == 1:
        figure_index = 1
        st.sidebar.caption(f"Figure : Fig. {figures[0]['figure']} — {figures[0]['title']}")
    else:
        figure_index = 0
        st.sidebar.caption("Aucune figure imprimée sur cette page.")

    st.sidebar.caption(
        "Les images sont des extraits directs du PDF source. "
        "Le slider ne fabrique ni n'interpole de résultat CFD."
    )
    return page_number, figure_index


def render_page_reader(page_number: int, figure_index: int) -> None:
    page = PAGE_GUIDE[page_number - 1]
    figures = figures_for_page(page_number)

    st.subheader(f"PDF p. {page['pdf_page']} · article p. {page['article_page']} — {page['title']}")

    text_col, visual_col = st.columns([0.95, 1.25], gap="large")

    with text_col:
        st.markdown("### Résumé de la page")
        st.write(page["summary"])

        st.markdown("### Informations importantes")
        for item in page["important"]:
            st.markdown(f"- {item}")

        st.info(f"**Question de lecture :** {page['question']}")

    with visual_col:
        st.markdown("### Figure source")
        if figures and figure_index > 0:
            selected = figures[figure_index - 1]
            asset_path = ROOT / selected["asset"]
            if asset_path.exists():
                st.image(
                    str(asset_path),
                    caption=selected["caption"],
                    use_container_width=True,
                )
                st.markdown(f"**À regarder :** {selected['focus']}")
            else:
                st.error(f"Asset manquant : {selected['asset']}")
        else:
            st.info(
                "Cette page ne contient pas de figure numérotée dans l'article. "
                "Le contenu utile est donc présenté dans le résumé et les repères ci-dessous."
            )

        st.markdown("### Repères exacts")
        for fig in page["figures"]:
            st.markdown(f"- **Figure :** {fig}")
        for eq in page["equations_tables"]:
            st.markdown(f"- **Équation / table :** {eq}")

    st.divider()
    st.markdown("### Carte rapide des 15 pages")
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
