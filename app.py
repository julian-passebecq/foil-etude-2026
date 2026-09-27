from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from study_model import POWER_DECOMP, SCENARIOS, kinematics, pct, scenario_row, table4_rounding_error


st.set_page_config(
    page_title="Lecture guidée — Xiao et al. (2012)",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .block-container {padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1480px;}
    [data-testid="stMetricValue"] {font-size: 1.8rem;}
    .study-ref {padding: .85rem 1rem; border: 1px solid #dfe5e8; border-radius: .65rem; background: #f8fafb;}
    .reader-note {padding: .8rem 1rem; border-left: 4px solid #18313e; background: #f5f8f9; border-radius: .25rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

PAGE_MAP = pd.DataFrame(
    [
        ("Question et contexte", "1-2", "61-62", "Résumé, Fig. 1", "Pourquoi modifier la trajectoire de tangage ?"),
        ("Méthode numérique", "3-4", "63-64", "Eq. 1-8, Fig. 2-5", "Re=10⁴, NACA0012, β, angle d'attaque effectif."),
        ("Puissance et rendement", "5-6", "65-66", "Eq. 9-16, Tab. 1-3, Fig. 6-7", "Où se trouve l'optimum et comment Stc évolue ?"),
        ("Mécanisme énergétique", "7-8", "67-68", "Fig. 8-9, Tab. 4", "Pourquoi Cp1 aide et Cp2 pénalise ?"),
        ("Vortex et pression", "9-14", "69-74", "Fig. 10-15", "Comment les charges de surface évoluent ?"),
        ("Conclusion et limite", "14-15", "74-75", "Section 4", "Ce que le papier établit — et ce qu'il n'établit pas."),
    ],
    columns=["Section", "Pages PDF", "Pages article", "Repères", "Question de lecture"],
)

GLOSSARY = {
    "β (bêta)": "Paramètre qui transforme le tangage d'une sinusoïde (β=1) vers un profil de plus en plus trapézoïdal.",
    "St": "Nombre de Strouhal : St=fA/U∞, avec A la course balayée du foil.",
    "h₀/c": "Amplitude de pilonnement rapportée à la corde du profil.",
    "α₀": "Angle d'attaque nominal utilisé pour paramétrer les cas calculés.",
    "θ₀": "Amplitude maximale de tangage.",
    "C̄op": "Coefficient de puissance moyen extrait sur un cycle.",
    "ηT": "Rendement total, normalisé par la puissance disponible sur la surface balayée A=2h₀.",
    "Cp1": "Contribution de puissance associée à C_L × dh/dt.",
    "Cp2": "Contribution de puissance associée à C_M × dθ/dt.",
    "Stc": "Strouhal critique après lequel la puissance moyenne décroît.",
    "LEV": "Leading-edge vortex : vortex de bord d'attaque observé dans les Fig. 10-12.",
}


def page_badge(pdf_page: str, article_page: str) -> str:
    return f"PDF p. {pdf_page} · article p. {article_page}"


def beta_text(value: float) -> str:
    return f"β={value:g}".replace(".", ",")


st.title("Étude des foils oscillants — guide de lecture")
st.markdown(
    "**Q. Xiao, W. Liao, S. Yang, Y. Peng — Renewable Energy 37 (2012) 61-75.**  "
    "Une lecture française centrée sur les résultats, les équations utiles et leurs limites."
)

with st.sidebar:
    st.header("Explorer la cinématique")
    beta = st.slider("β — forme du tangage", 1.0, 4.0, 1.5, 0.05)
    st_value = st.slider("St — nombre de Strouhal", 0.05, 0.50, 0.35, 0.01)
    alpha0 = st.selectbox("α₀ — angle nominal", [10, 20], format_func=lambda x: f"{x}°")
    h_ratio = st.selectbox("h₀/c — amplitude", [0.5, 1.0], index=1)
    st.caption(
        "β continu sert uniquement à recalculer les équations cinématiques. Les résultats CFD du papier existent "
        "pour β = 1, 1,25, 1,5, 2 et 4 et ne sont pas interpolés ici."
    )
    st.divider()
    st.markdown("**Repères dans le PDF**")
    st.markdown("- p. 3 : mouvement / αeff\n- p. 4-6 : puissance / rendement\n- p. 7-8 : Cp1 / Cp2\n- p. 9-14 : vortex / pression")

state = kinematics(beta, st_value, alpha0)
row = scenario_row(h_ratio, alpha0)


tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["1 · Essentiel", "2 · Trajectoire", "3 · Performances", "4 · Pourquoi ?", "5 · Carte & limites"]
)

with tab1:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Gain max C̄op", "+63 %", help="Table 2 : cas h₀/c=1, α₀=10°, β=1,5 vs β=1.")
    c2.metric("Gain max ηT", "+50 %", help="Table 2 : meilleur gain de rendement parmi les cas testés.")
    c3.metric("Optimum observé", "β ≈ 1,25-1,5")
    c4.metric("Cadre numérique", "Re = 10⁴")

    st.markdown(
        '<div class="reader-note"><b>En une phrase.</b> Modifier légèrement la forme temporelle du tangage peut améliorer fortement la récupération d\'énergie, mais des inversions trop abruptes finissent par coûter plus qu\'elles ne rapportent.</div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.05, 0.95])
    with left:
        st.subheader("La logique du papier")
        st.markdown(
            "1. Le **pilonnement reste sinusoïdal**.\n"
            "2. Le **tangage** passe d'une sinusoïde (β=1) vers une forme plus trapézoïdale.\n"
            "3. Les auteurs calculent la puissance et le rendement pour plusieurs St, α₀ et h₀/c.\n"
            "4. Ils expliquent ensuite le résultat par **Cp1 (portance)** et **Cp2 (moment)**."
        )
    with right:
        st.subheader("À garder en tête")
        st.info(
            "Le papier traite un foil NACA0012 en calcul 2D, à Re=10⁴, avec mouvement imposé. "
            "C'est une preuve de mécanisme hydrodynamique, pas une validation complète d'une machine réelle."
        )

    st.subheader("Parcours conseillé")
    st.dataframe(PAGE_MAP, use_container_width=True, hide_index=True)

    st.markdown(
        '<div class="study-ref"><b>Source</b><br>How motion trajectory affects energy extraction performance of a biomimic energy generator with an oscillating foil? · DOI 10.1016/j.renene.2011.05.029</div>',
        unsafe_allow_html=True,
    )

with tab2:
    st.subheader("Voir ce que β change réellement")
    st.caption(page_badge("3-5", "63-65") + " — Eq. (4), (5), (7), (8), Fig. 2-3")

    k1, k2, k3 = st.columns(3)
    k1.metric("β", f"{beta:.2f}")
    k2.metric("θ₀ issu de l'Eq. (8)", f"{state.theta0_deg:.1f}°")
    k3.metric("|αeff| max", f"{np.max(np.abs(state.alpha_eff_deg)):.1f}°")

    motion = go.Figure()
    motion.add_trace(go.Scatter(x=state.phase, y=state.h_norm, mode="lines", name="h/h₀ — pilonnement"))
    motion.add_trace(go.Scatter(x=state.phase, y=state.theta_norm, mode="lines", name="θ/θ₀ — tangage"))
    motion.update_layout(
        title="Un cycle — mouvements normalisés",
        xaxis_title="t/T",
        yaxis_title="amplitude normalisée",
        yaxis_range=[-1.25, 1.25],
        template="plotly_white",
        height=410,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )
    st.plotly_chart(motion, use_container_width=True)

    alpha_fig = px.line(
        pd.DataFrame({"t/T": state.phase, "αeff (°)": state.alpha_eff_deg}),
        x="t/T",
        y="αeff (°)",
        title="Angle d'attaque effectif αeff",
    )
    alpha_fig.add_hline(y=0, line_dash="dot")
    alpha_fig.update_layout(template="plotly_white", height=370)
    st.plotly_chart(alpha_fig, use_container_width=True)

    if beta <= 1.6:
        st.success(
            "Lecture : dans cette zone, le plateau de tangage s'allonge sans rendre les inversions extrêmes. "
            "C'est la zone où le papier trouve ses meilleurs compromis."
        )
    elif beta >= 3.0:
        st.warning(
            "Lecture : le tangage devient très carré. Les inversions rapides augmentent fortement |dθ/dt|, "
            "ce qui amplifie la pénalité de moment décrite plus loin."
        )
    else:
        st.info("Lecture : la trajectoire est déjà nettement aplatie ; l'étude montre que l'amélioration n'est plus monotone avec β.")

    with st.expander("Équations derrière le widget"):
        st.latex(r"h(t)=h_0\sin(\omega t)")
        st.write("θ(t) suit la définition par morceaux de l'équation (5), contrôlée par β.")
        st.latex(r"\alpha_{eff}(t)=-\arctan\left(\frac{\dot h(t)}{U_\infty}\right)+\theta(t)")
        st.latex(r"\alpha_0=-\arctan\left(\frac{\omega h_0}{U_\infty}\right)+\theta_0")
        st.caption("Ici, ωh₀/U∞ = π·St. Le calcul reproduit la cinématique publiée, pas le solveur CFD.")

with tab3:
    st.subheader("Comparer les performances sans inventer de CFD")
    st.caption(page_badge("4-9", "64-69") + " — Fig. 5-7 et Tables 1-3")

    baseline = SCENARIOS.copy()
    baseline["Scénario"] = baseline.apply(lambda r: f"h₀/c={r['h0/c']:.1f}, α₀={int(r['alpha0'])}°", axis=1)
    base_fig = px.bar(
        baseline,
        x="Scénario",
        y="Cop_beta1",
        text="Cop_beta1",
        labels={"Cop_beta1": "C̄op max"},
        title="Table 1 — maximum de C̄op pour le tangage sinusoïdal β=1",
    )
    base_fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    base_fig.update_layout(template="plotly_white", height=390, yaxis_range=[0, 0.82])
    st.plotly_chart(base_fig, use_container_width=True)

    st.markdown(f"#### Cas sélectionné : h₀/c={h_ratio:.1f}, α₀={alpha0}°")
    p1, p2, p3, p4 = st.columns(4)
    p1.metric("Référence β=1", f"C̄op={row['Cop_beta1']:.2f}")
    p2.metric(f"Puissance max ({beta_text(row['power_best_beta'])})", f"×{row['power_best_ratio']:.3g}", pct(row["power_best_ratio"]))
    p3.metric(f"Rendement max ({beta_text(row['eta_best_beta'])})", f"×{row['eta_best_ratio']:.3g}", pct(row["eta_best_ratio"]))
    p4.metric(f"Stc max ({beta_text(row['st_best_beta'])})", f"×{row['st_best_ratio']:.3g}", pct(row["st_best_ratio"]))

    st.markdown(
        f"**Lecture directe :** pour ce cas, la Table 2 rapporte un meilleur maximum de puissance de "
        f"**{pct(row['power_best_ratio'])}** à {beta_text(row['power_best_beta'])}, et un meilleur rendement de "
        f"**{pct(row['eta_best_ratio'])}** à {beta_text(row['eta_best_beta'])}. La Table 3 étend Stc de "
        f"**{pct(row['st_best_ratio'])}** à {beta_text(row['st_best_beta'])}."
    )

    ratios = pd.DataFrame(
        {
            "Indicateur": ["C̄op — meilleur", "ηT — meilleur", "Stc — meilleur", "C̄op — β=4", "ηT — β=4", "Stc — β=4"],
            "Ratio vs β=1": [
                row["power_best_ratio"], row["eta_best_ratio"], row["st_best_ratio"],
                row["power_worst_ratio"], row["eta_worst_ratio"], row["st_worst_ratio"],
            ],
        }
    )
    ratio_fig = px.bar(ratios, x="Indicateur", y="Ratio vs β=1", text="Ratio vs β=1", title="Tables 2-3 — amélioration optimale vs β=4")
    ratio_fig.add_hline(y=1.0, line_dash="dash", annotation_text="β=1")
    ratio_fig.update_traces(texttemplate="×%{text:.3g}", textposition="outside")
    ratio_fig.update_layout(template="plotly_white", height=420)
    st.plotly_chart(ratio_fig, use_container_width=True)

    st.warning(
        "Le message important n'est pas « augmenter β ». À β=4, les quatre scénarios publiés se dégradent par rapport à β=1."
    )

    with st.expander("Voir les valeurs exactes des Tables 1-3"):
        exact = SCENARIOS.copy()
        exact["gain C̄op max"] = exact["power_best_ratio"].map(pct)
        exact["gain η max"] = exact["eta_best_ratio"].map(pct)
        exact["gain Stc max"] = exact["st_best_ratio"].map(pct)
        exact["C̄op à β=4"] = exact["power_worst_ratio"].map(pct)
        exact["η à β=4"] = exact["eta_worst_ratio"].map(pct)
        exact["Stc à β=4"] = exact["st_worst_ratio"].map(pct)
        st.dataframe(
            exact[["h0/c", "alpha0", "Cop_beta1", "gain C̄op max", "gain η max", "gain Stc max", "C̄op à β=4", "η à β=4", "Stc à β=4"]],
            use_container_width=True,
            hide_index=True,
        )

with tab4:
    st.subheader("Pourquoi l'optimum existe")
    st.caption(page_badge("7-14", "67-74") + " — Fig. 8-15 et Table 4")

    long = POWER_DECOMP.melt(id_vars="beta", var_name="Contribution", value_name="Valeur")
    long["Contribution"] = long["Contribution"].map({"Cop": "C̄op total", "Cp1_lift": "C̄p1 — portance", "Cp2_moment": "C̄p2 — moment"})
    mech = px.bar(
        long,
        x="beta",
        y="Valeur",
        color="Contribution",
        barmode="group",
        title="Table 4 — bilan moyen à St=0,35 et α₀=10°",
        labels={"beta": "β"},
    )
    mech.add_hline(y=0, line_dash="dot")
    mech.update_layout(template="plotly_white", height=440, xaxis=dict(tickmode="array", tickvals=[1, 1.5, 2, 4]))
    st.plotly_chart(mech, use_container_width=True)

    a, b, c = st.columns(3)
    with a:
        st.markdown("**Cp1 — portance**")
        st.write("C_L et dh/dt ont le même signe pendant une grande partie du cycle : leur produit apporte généralement de la puissance.")
    with b:
        st.markdown("**Cp2 — moment**")
        st.write("C_M et dθ/dt sont généralement de signes opposés pendant les inversions : leur produit pénalise le bilan.")
    with c:
        st.markdown("**Le compromis**")
        st.write("β modéré étend les zones favorables de Cp1. β trop élevé rend les inversions si rapides que la pénalité Cp2 domine.")

    max_rounding = table4_rounding_error().abs().max()
    st.caption(
        f"Contrôle : la Table 4 est imprimée avec des valeurs arrondies ; l'écart maximal entre C̄op imprimé et C̄p1+C̄p2 imprimés est {max_rounding:.3f}."
    )

    st.markdown("#### Lire les figures de vortex et de pression")
    flow = pd.DataFrame(
        [
            ("t=0", "Le LEV commence à se former près du bord d'attaque.", "Fig. 10-12 · PDF p. 9-11"),
            ("t=T/8", "Le vortex grandit et la distribution de pression se structure.", "Fig. 13-15 · PDF p. 12-14"),
            ("t=T/4", "Le LEV est le plus intense parmi les instantanés décrits ; minimum de pression marqué.", "Fig. 10-15"),
            ("t=3T/8", "Le vortex migre le long du profil ; les charges de surface évoluent.", "Fig. 13-15"),
            ("t=T/2", "Fin du demi-cycle ; l'autre moitié est inverse-symétrique dans le modèle.", "§3.3.2 · PDF p. 13"),
        ],
        columns=["Instant", "Ce qu'il faut regarder", "Repère"],
    )
    st.dataframe(flow, use_container_width=True, hide_index=True)
    st.info("Le papier relie les vortex à la pression de surface, puis la pression aux forces et moments. Il ne réduit pas le résultat à « plus de vortex = mieux ». ")

with tab5:
    st.subheader("Carte de lecture et limites")
    st.dataframe(PAGE_MAP, use_container_width=True, hide_index=True)

    left, right = st.columns(2)
    with left:
        st.markdown("#### Ce que le papier soutient")
        st.markdown(
            "- Le profil temporel de tangage modifie fortement la récupération d'énergie.\n"
            "- L'optimum dépend de β, St, α₀ et h₀/c.\n"
            "- Dans les cas testés, β≈1,25-1,5 est la zone la plus favorable.\n"
            "- Le bilan Cp1/Cp2 explique pourquoi un β excessif devient défavorable."
        )
    with right:
        st.markdown("#### Ce que le papier ne valide pas")
        st.markdown(
            "- Réponse dynamique libre et couplée de la machine.\n"
            "- Performance 3D à grand Reynolds d'une machine industrielle.\n"
            "- Fatigue, disponibilité, commande, conversion électrique ou LCOE.\n"
            "- Validation directe d'une architecture Foil'O particulière."
        )

    st.markdown("#### Glossaire")
    for term, definition in GLOSSARY.items():
        with st.expander(term):
            st.write(definition)

    st.markdown("#### Où regarder dans le PDF")
    refs = pd.DataFrame(
        [
            ("Fig. 2-3", "PDF p. 3", "h(t), θ(t), αeff(t)"),
            ("Fig. 5", "PDF p. 4", "C̄op vs St"),
            ("Tab. 1 + Fig. 6", "PDF p. 5", "Référence β=1 et ηT"),
            ("Fig. 7 + Tab. 2-3", "PDF p. 6", "Optimum de β et Stc"),
            ("Fig. 8 + Tab. 4", "PDF p. 7", "C̄op = C̄p1 + C̄p2"),
            ("Fig. 9", "PDF p. 8", "Signes de C_L, dh/dt, C_M, dθ/dt"),
            ("Fig. 10-12", "PDF p. 9-11", "Vorticité pour β=1, 1,5, 4"),
            ("Fig. 13-15", "PDF p. 12-14", "Pression de paroi"),
            ("Conclusion", "PDF p. 14-15", "Résultat et limite du mouvement imposé"),
        ],
        columns=["Repère", "Où", "À observer"],
    )
    st.dataframe(refs, use_container_width=True, hide_index=True)

st.divider()
st.caption(
    "Données numériques : Tables 1-4 de Xiao et al. (2012). Courbes interactives de trajectoire : recalcul des équations publiées. "
    "Aucune courbe CFD de performance n'est interpolée."
)
