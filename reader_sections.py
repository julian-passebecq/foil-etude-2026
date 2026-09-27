from __future__ import annotations

import pandas as pd
import streamlit as st

from study_content import EQUATION_GUIDE, METHOD_FACTS, PAGE_GUIDE, PRIOR_WORK


def render_page_reader() -> None:
    st.subheader("Lecture page par page")
    st.caption(
        "Chaque fiche reprend uniquement les informations soutenues par le PDF source, "
        "avec les repères de page, figures, tableaux et équations."
    )

    options = [
        f"PDF p. {item['pdf_page']} · article p. {item['article_page']} — {item['title']}"
        for item in PAGE_GUIDE
    ]
    selected = st.selectbox("Choisir une page", options, index=0)
    page = PAGE_GUIDE[options.index(selected)]

    st.markdown(f"### {page['title']}")
    st.caption(f"PDF p. {page['pdf_page']} · article p. {page['article_page']}")
    st.write(page["summary"])

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

    st.divider()
    st.markdown("### Vue condensée des 15 pages")
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
