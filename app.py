from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="Lecture guidée — Xiao et al. (2012)",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .block-container {padding-top: 2rem; padding-bottom: 3rem; max-width: 1500px;}
    [data-testid="stMetricValue"] {font-size: 2rem;}
    .small-note {font-size: 0.92rem; color: #5c6470;}
    .study-ref {padding: 0.85rem 1rem; border: 1px solid #e5e7eb; border-radius: 0.65rem; background: #fafafa;}
    </style>
    """,
    unsafe_allow_html=True,
)


# Valeurs reprises directement des tableaux de Xiao et al. (2012).
SCENARIOS = pd.DataFrame(
    [
        {"h0/c": 0.5, "alpha0": 10, "Cop_beta1": 0.14, "power_best_ratio": 1.40, "power_worst_ratio": 0.833, "eta_best_ratio": 1.25, "eta_best_beta": 1.25, "eta_worst_ratio": 0.74, "st_best_ratio": 1.17, "st_worst_ratio": 0.57},
        {"h0/c": 0.5, "alpha0": 20, "Cop_beta1": 0.28, "power_best_ratio": 1.43, "power_worst_ratio": 0.82, "eta_best_ratio": 1.50, "eta_best_beta": 1.50, "eta_worst_ratio": 0.66, "st_best_ratio": 1.17, "st_worst_ratio": 0.66},
        {"h0/c": 1.0, "alpha0": 10, "Cop_beta1": 0.36, "power_best_ratio": 1.63, "power_worst_ratio": 0.71, "eta_best_ratio": 1.50, "eta_best_beta": 1.50, "eta_worst_ratio": 0.656, "st_best_ratio": 1.28, "st_worst_ratio": 0.43},
        {"h0/c": 1.0, "alpha0": 20, "Cop_beta1": 0.73, "power_best_ratio": 1.347, "power_worst_ratio": 0.54, "eta_best_ratio": 1.25, "eta_best_beta": 1.25, "eta_worst_ratio": 0.52, "st_best_ratio": 1.347, "st_worst_ratio": 0.57},
    ]
)

POWER_DECOMP = pd.DataFrame(
    {
        "beta": [1.0, 1.5, 2.0, 4.0],
        "Cop": [0.36, 0.62, 0.563, -0.842],
        "Cp1_lift": [0.55, 0.96, 1.13, 1.23],
        "Cp2_moment": [-0.181, -0.34, -0.564, -2.07],
    }
)

PAGE_MAP = pd.DataFrame(
    [
        ("Question et contexte", "1-2", "61-62", "Résumé, Fig. 1", "Pourquoi tester une trajectoire de tangage non sinusoïdale ?"),
        ("Méthode numérique", "3-4", "63-64", "Eq. 1-8, Fig. 2-5", "Navier-Stokes, Re=10⁴, profil β, angle d'attaque effectif."),
        ("Mesures de performance", "5-6", "65-66", "Eq. 9-16, Tab. 1-3, Fig. 6-7", "Puissance, rendement, optimum de β et St critique."),
        ("Décomposition énergétique", "7-8", "67-68", "Fig. 8-9, Tab. 4", "Pourquoi portance et moment contribuent différemment."),
        ("Vortex et pression", "9-14", "69-74", "Fig. 10-15", "LEV, pression de paroi, lien avec C_L et C_M."),
        ("Conclusion / limite", "14-15", "74-75", "Section 4", "Optimum autour de β≈1,5 dans le domaine étudié ; mouvement imposé."),
    ],
    columns=["Section", "Pages PDF", "Pages article", "Repères", "À chercher"],
)

GLOSSARY = {
    "β (bêta)": "Paramètre qui transforme le tangage d'une sinusoïde (β=1) vers une forme de plus en plus trapézoïdale / carrée.",
    "St": "Nombre de Strouhal. Dans l'étude : St = fA/U∞, avec A la course balayée du foil.",
    "h₀/c": "Amplitude de pilonnement rapportée à la corde du profil.",
    "α₀": "Angle d'attaque nominal utilisé pour paramétrer les cas calculés.",
    "θ₀": "Amplitude maximale de tangage.",
    "C̄op": "Coefficient de puissance moyen extrait sur un cycle.",
    "ηT": "Rendement total défini avec la puissance disponible sur la surface balayée A=2h₀.",
    "Cp1": "Contribution à la puissance liée à C_L × dh/dt (portance × vitesse de pilonnement).",
    "Cp2": "Contribution à la puissance liée à C_M × dθ/dt (moment × vitesse angulaire de tangage).",
    "Stc": "Strouhal critique au-delà duquel la puissance moyenne commence à décroître.",
    "LEV": "Leading-edge vortex : vortex de bord d'attaque suivi dans les Fig. 10-12.",
}


@dataclass(frozen=True)
class KinematicState:
    phase: np.ndarray
    h_norm: np.ndarray
    theta_norm: np.ndarray
    theta_deg: np.ndarray
    alpha_eff_deg: np.ndarray
    theta0_deg: float


def pitching_profile(phase: np.ndarray, beta: float) -> np.ndarray:
    """Équation (5), écrite sur la phase normalisée t/T dans [0,1]."""
    phase = np.asarray(phase, dtype=float)
    b = float(beta)
    a1 = (1.0 - 1.0 / b) / 4.0
    a2 = (1.0 + 1.0 / b) / 4.0
    a3 = (3.0 - 1.0 / b) / 4.0
    a4 = (3.0 + 1.0 / b) / 4.0

    theta = np.empty_like(phase)
    m1 = phase <= a1
    m2 = (phase > a1) & (phase <= a2)
    m3 = (phase > a2) & (phase <= a3)
    m4 = (phase > a3) & (phase <= a4)
    m5 = phase > a4

    theta[m1] = 1.0
    theta[m2] = np.sin(2.0 * np.pi * b * phase[m2] + np.pi * (1.0 - b / 2.0))
    theta[m3] = -1.0
    theta[m4] = np.sin(2.0 * np.pi * b * phase[m4] + np.pi * (2.0 - 3.0 * b / 2.0))
    theta[m5] = 1.0
    return theta


def kinematics(beta: float, st_value: float, alpha0_deg: float) -> KinematicState:
    phase = np.linspace(0.0, 1.0, 1001)
    h_norm = np.sin(2.0 * np.pi * phase)
    theta_norm = pitching_profile(phase, beta)

    # Eq. (8): alpha0 = -atan(omega*h0/Uinf) + theta0.
    # Avec St=f*(2h0)/Uinf, omega*h0/Uinf = pi*St.
    theta0_deg = alpha0_deg + math.degrees(math.atan(math.pi * st_value))
    theta_deg = theta0_deg * theta_norm

    plunge_induced_deg = np.degrees(np.arctan(math.pi * st_value * np.cos(2.0 * np.pi * phase)))
    alpha_eff_deg = theta_deg - plunge_induced_deg
    return KinematicState(phase, h_norm, theta_norm, theta_deg, alpha_eff_deg, theta0_deg)


def pct(ratio: float) -> str:
    value = (ratio - 1.0) * 100.0
    return f"{value:+.0f} %"


def scenario_row(h_ratio: float, alpha0_deg: int) -> pd.Series:
    row = SCENARIOS[(SCENARIOS["h0/c"] == h_ratio) & (SCENARIOS["alpha0"] == alpha0_deg)]
    return row.iloc[0]


def page_badge(pdf_page: str, article_page: str) -> str:
    return f"PDF p. {pdf_page} · article p. {article_page}"


st.title("Lecture guidée de l'étude sur les foils oscillants")
st.markdown(
    "**Q. Xiao, W. Liao, S. Yang, Y. Peng — Renewable Energy 37 (2012) 61-75.**  "
    "Compagnon de lecture en français : cinématique, résultats, mécanisme et limites."
)

with st.sidebar:
    st.header("Paramètres de lecture")
    beta = st.slider("β — forme du tangage", 1.0, 4.0, 1.5, 0.05)
    st_value = st.slider("St — nombre de Strouhal", 0.05, 0.50, 0.35, 0.01)
    alpha0 = st.selectbox("α₀ — angle nominal", [10, 20], index=0, format_func=lambda x: f"{x}°")
    h_ratio = st.selectbox("h₀/c — amplitude", [0.5, 1.0], index=1)
    st.caption(
        "L'article calcule β = 1, 1,25, 1,5, 2 et 4. Entre ces valeurs, l'app ne fait qu'illustrer "
        "l'équation cinématique (5), pas prédire la performance."
    )
    st.divider()
    st.markdown("**Repère rapide**")
    st.markdown("- Fig. 2-3 : mouvement et αeff\n- Fig. 5-7 : puissance / rendement\n- Fig. 8-9 : mécanisme Cp1 / Cp2\n- Fig. 10-15 : vortex / pression")

state = kinematics(beta, st_value, alpha0)
row = scenario_row(h_ratio, alpha0)


tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["1. Lecture express", "2. Trajectoire", "3. Performances", "4. Mécanisme", "5. Carte & limites"]
)

with tab1:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Gain max de C̄op", "+63 %", help="Meilleur cas rapporté vs β=1 : β=1,5, h₀/c=1, α₀=10°.")
    c2.metric("Gain max de rendement", "+50 %", help="Maximum rapporté vs β=1 dans les cas testés.")
    c3.metric("Zone optimale", "β ≈ 1,25-1,5")
    c4.metric("Régime numérique", "Re = 10⁴")

    st.subheader("Ce que l'étude cherche à montrer")
    st.write(
        "Les auteurs remplacent le **tangage sinusoïdal** d'un foil NACA0012 par un tangage "
        "**trapézoïdal**, contrôlé par β, tout en gardant le pilonnement sinusoïdal. L'objectif est de voir si "
        "la forme temporelle du mouvement permet d'extraire davantage d'énergie."
    )

    a, b = st.columns([1.15, 1.0])
    with a:
        st.markdown("#### Résultat central")
        st.success(
            "Un β légèrement supérieur à 1 peut augmenter nettement puissance et rendement. "
            "Dans les cas étudiés, l'optimum se situe typiquement vers β=1,25 ou 1,5. "
            "Un β trop élevé (β=4) devient au contraire pénalisant."
        )
        st.markdown(
            "**Pourquoi ?** Le gain lié à la portance (*Cp1*) augmente, mais les transitions de tangage "
            "trop brusques font exploser la pénalité de moment (*Cp2*)."
        )
    with b:
        st.markdown("#### Le point à ne pas perdre")
        st.info(
            "Ce papier démontre un **mécanisme hydrodynamique numérique** sur un foil oscillant avec mouvement imposé. "
            "Il ne valide pas à lui seul une machine réelle, un rendement système complet ou un LCOE."
        )

    st.subheader("Parcours conseillé pour Francis")
    st.dataframe(PAGE_MAP, use_container_width=True, hide_index=True)

    st.markdown(
        '<div class="study-ref"><b>Référence</b><br>How motion trajectory affects energy extraction performance of a biomimic energy generator with an oscillating foil? — DOI 10.1016/j.renene.2011.05.029</div>',
        unsafe_allow_html=True,
    )

with tab2:
    st.subheader("Comprendre β avant de lire les courbes")
    st.caption(page_badge("3-5", "63-65") + " — Eq. (4), (5), (7), (8), Fig. 2-3")

    k1, k2, k3 = st.columns(3)
    k1.metric("β choisi", f"{beta:.2f}")
    k2.metric("θ₀ calculé", f"{state.theta0_deg:.1f}°", help="Issu de l'équation (8) pour le St et α₀ sélectionnés.")
    k3.metric("|αeff| max (cinématique)", f"{np.max(np.abs(state.alpha_eff_deg)):.1f}°")

    fig_motion = go.Figure()
    fig_motion.add_trace(go.Scatter(x=state.phase, y=state.h_norm, mode="lines", name="h/h₀ — pilonnement"))
    fig_motion.add_trace(go.Scatter(x=state.phase, y=state.theta_norm, mode="lines", name="θ/θ₀ — tangage"))
    fig_motion.update_layout(
        title="Un cycle de mouvement — forme normalisée",
        xaxis_title="t/T",
        yaxis_title="amplitude normalisée",
        yaxis_range=[-1.25, 1.25],
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        height=430,
    )
    st.plotly_chart(fig_motion, use_container_width=True)

    fig_alpha = px.line(
        pd.DataFrame({"t/T": state.phase, "αeff (°)": state.alpha_eff_deg}),
        x="t/T",
        y="αeff (°)",
        title="Angle d'attaque effectif αeff sur le cycle",
    )
    fig_alpha.add_hline(y=0, line_dash="dot")
    fig_alpha.update_layout(template="plotly_white", height=390)
    st.plotly_chart(fig_alpha, use_container_width=True)

    if beta <= 1.6:
        st.info(
            "Lecture : β modéré allonge les plateaux de tangage sans rendre les inversions excessivement brutales. "
            "C'est précisément la zone où l'étude observe les meilleurs compromis."
        )
    elif beta >= 3.0:
        st.warning(
            "Lecture : avec β élevé, les plateaux sont longs mais les inversions deviennent très rapides. "
            "Le papier montre que la pénalité de moment peut alors dominer."
        )

    with st.expander("Équations utilisées dans ce widget"):
        st.latex(r"h(t)=h_0\sin(\omega t)")
        st.write("Le profil de θ(t) est la forme par morceaux de l'équation (5), pilotée par β.")
        st.latex(r"\alpha_{eff}(t)=-\arctan\left(\frac{\dot h(t)}{U_\infty}\right)+\theta(t)")
        st.latex(r"\alpha_0=-\arctan\left(\frac{\omega h_0}{U_\infty}\right)+\theta_0")
        st.caption(
            "Avec St=f(2h₀)/U∞, on a ωh₀/U∞ = π·St. Le widget reproduit la cinématique, pas le solveur CFD."
        )

with tab3:
    st.subheader("Ce que les résultats chiffrés permettent d'affirmer")
    st.caption(page_badge("4-9", "64-69") + " — Fig. 5-7, Tab. 1-3")

    baseline = SCENARIOS.copy()
    baseline["Scénario"] = baseline.apply(lambda r: f"h₀/c={r['h0/c']:.1f}, α₀={int(r['alpha0'])}°", axis=1)
    fig_base = px.bar(
        baseline,
        x="Scénario",
        y="Cop_beta1",
        text="Cop_beta1",
        title="Maximum de C̄op avec tangage sinusoïdal (β=1) — valeurs exactes de la Table 1",
        labels={"Cop_beta1": "C̄op max"},
    )
    fig_base.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    fig_base.update_layout(template="plotly_white", height=420, yaxis_range=[0, 0.82])
    st.plotly_chart(fig_base, use_container_width=True)

    st.markdown(f"#### Scénario sélectionné : h₀/c={h_ratio:.1f}, α₀={alpha0}°")
    p1, p2, p3, p4 = st.columns(4)
    p1.metric("Référence β=1", f"C̄op max {row['Cop_beta1']:.2f}")
    p2.metric("Meilleur ratio de puissance", f"×{row['power_best_ratio']:.3g}", pct(row["power_best_ratio"]))
    p3.metric("Meilleur ratio de rendement", f"×{row['eta_best_ratio']:.3g}", pct(row["eta_best_ratio"]))
    p4.metric("Extension max de Stc", f"×{row['st_best_ratio']:.3g}", pct(row["st_best_ratio"]))

    compare_df = pd.DataFrame(
        {
            "Indicateur": ["C̄op — meilleur", "ηT — meilleur", "Stc — meilleur", "C̄op — β=4", "ηT — β=4", "Stc — β=4"],
            "Ratio vs β=1": [
                row["power_best_ratio"],
                row["eta_best_ratio"],
                row["st_best_ratio"],
                row["power_worst_ratio"],
                row["eta_worst_ratio"],
                row["st_worst_ratio"],
            ],
        }
    )
    fig_ratio = px.bar(
        compare_df,
        x="Indicateur",
        y="Ratio vs β=1",
        text="Ratio vs β=1",
        title="Tables 2-3 — gain maximal et dégradation à β=4",
    )
    fig_ratio.add_hline(y=1.0, line_dash="dash", annotation_text="référence β=1")
    fig_ratio.update_traces(texttemplate="×%{text:.3g}", textposition="outside")
    fig_ratio.update_layout(template="plotly_white", height=430)
    st.plotly_chart(fig_ratio, use_container_width=True)

    st.warning(
        "β=4 n'est pas une amélioration 'plus forte'. Dans les cas testés, il peut faire tomber le maximum de puissance "
        "jusqu'à 54 % de la référence β=1, le rendement jusqu'à 52 %, et Stc jusqu'à 43 %."
    )

    with st.expander("Voir les Tables 1-3 reconstituées"):
        exact_table = SCENARIOS.copy()
        exact_table["gain C̄op max"] = exact_table["power_best_ratio"].map(pct)
        exact_table["perte C̄op β=4"] = exact_table["power_worst_ratio"].map(pct)
        exact_table["gain η max"] = exact_table["eta_best_ratio"].map(pct)
        exact_table["perte η β=4"] = exact_table["eta_worst_ratio"].map(pct)
        exact_table["gain Stc max"] = exact_table["st_best_ratio"].map(pct)
        exact_table["perte Stc β=4"] = exact_table["st_worst_ratio"].map(pct)
        st.dataframe(
            exact_table[
                [
                    "h0/c",
                    "alpha0",
                    "Cop_beta1",
                    "gain C̄op max",
                    "perte C̄op β=4",
                    "gain η max",
                    "perte η β=4",
                    "gain Stc max",
                    "perte Stc β=4",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )
        st.caption(
            "Pour la puissance maximale, le meilleur cas de la Table 2 est donné à β=1,5. "
            "Pour Stc, le maximum est donné à β=1,25."
        )

with tab4:
    st.subheader("Le mécanisme : Cp1 aide, Cp2 peut annuler le gain")
    st.caption(page_badge("7-14", "67-74") + " — Fig. 8-15, Tab. 4")

    mech_long = POWER_DECOMP.melt(id_vars="beta", var_name="Contribution", value_name="Valeur")
    mech_long["Contribution"] = mech_long["Contribution"].map(
        {"Cop": "C̄op total", "Cp1_lift": "C̄p1 — portance", "Cp2_moment": "C̄p2 — moment"}
    )
    fig_mech = px.bar(
        mech_long,
        x="beta",
        y="Valeur",
        color="Contribution",
        barmode="group",
        title="Table 4 — décomposition moyenne à St=0,35 et α₀=10°",
        labels={"beta": "β"},
    )
    fig_mech.add_hline(y=0, line_dash="dot")
    fig_mech.update_layout(
        template="plotly_white",
        height=460,
        xaxis=dict(tickmode="array", tickvals=[1, 1.5, 2, 4]),
    )
    st.plotly_chart(fig_mech, use_container_width=True)

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown("**1 — Portance (Cp1)**")
        st.write(
            "Le produit C_L × dh/dt est positif pendant une grande partie du cycle. "
            "Quand β augmente, cette contribution positive tend à s'étendre."
        )
    with m2:
        st.markdown("**2 — Moment (Cp2)**")
        st.write(
            "C_M et dθ/dt sont généralement de signes opposés pendant les inversions : Cp2 est donc négatif."
        )
    with m3:
        st.markdown("**3 — Compromis**")
        st.write(
            "À β≈1,5, Cp1 progresse plus vite que la pénalité Cp2. À β=4, les inversions très rapides rendent "
            "Cp2 dominant et C̄op devient négatif dans la Table 4."
        )

    st.markdown("#### Ce que montrent les champs d'écoulement")
    flow = pd.DataFrame(
        [
            ("t = 0", "Début de formation du vortex de bord d'attaque (LEV).", "Fig. 10-12, PDF p. 9-11"),
            ("t = T/8", "Le LEV grandit et modifie la pression près du bord d'attaque.", "Fig. 13-15, PDF p. 12-14"),
            ("t = T/4", "LEV le plus intense parmi les instantanés décrits ; minimum de pression marqué.", "Fig. 10-15"),
            ("t = 3T/8", "Le vortex se déplace le long du profil ; la distribution de pression évolue.", "Fig. 13-15"),
            ("t = T/2", "Fin du demi-cycle ; l'autre moitié est inverse-symétrique dans ce modèle.", "PDF p. 13, texte §3.3.2"),
        ],
        columns=["Instant", "Lecture physique", "Repère"],
    )
    st.dataframe(flow, use_container_width=True, hide_index=True)

    st.info(
        "Le papier ne dit pas simplement 'plus de vortex = plus d'énergie'. Il relie surtout la pression de surface "
        "aux signes de C_L, C_M, dh/dt et dθ/dt, donc au bilan Cp1 + Cp2."
    )

with tab5:
    st.subheader("Carte de l'article et limites de portée")
    st.dataframe(PAGE_MAP, use_container_width=True, hide_index=True)

    left, right = st.columns(2)
    with left:
        st.markdown("#### Ce que l'étude établit dans son domaine")
        st.markdown(
            "- Un tangage non sinusoïdal peut améliorer C̄op et ηT.\n"
            "- L'optimum dépend de β, St, α₀ et h₀/c.\n"
            "- Les cas testés placent l'optimum typique autour de β=1,25-1,5.\n"
            "- Le mécanisme peut être compris par le bilan Cp1 (portance) + Cp2 (moment).\n"
            "- Un profil trop abrupt dégrade fortement la performance."
        )
    with right:
        st.markdown("#### Ce qu'il ne faut pas extrapoler sans autre preuve")
        st.markdown(
            "- Le mouvement de tangage et de pilonnement est **imposé**.\n"
            "- La réponse dynamique complète de la machine aux charges instationnaires n'est pas couplée.\n"
            "- Le calcul est 2D sur NACA0012, à **Re=10⁴** et en régime laminaire.\n"
            "- L'étude ne traite pas le LCOE, la fatigue, la disponibilité, le contrôle industriel ou le rendement électrique complet.\n"
            "- Ce n'est donc pas une validation directe d'une architecture Foil'O particulière."
        )

    st.markdown("#### Glossaire de lecture")
    for term, definition in GLOSSARY.items():
        with st.expander(term):
            st.write(definition)

    st.markdown("#### Repères figures / tables")
    refs = pd.DataFrame(
        [
            ("Fig. 2-3", "PDF p. 3", "Profils de h(t), θ(t), αeff(t) selon β"),
            ("Fig. 5", "PDF p. 4", "C̄op en fonction de St"),
            ("Tab. 1 + Fig. 6", "PDF p. 5", "Référence β=1 et rendement ηT"),
            ("Fig. 7 + Tab. 2-3", "PDF p. 6", "Optimum de β et extension de Stc"),
            ("Fig. 8 + Tab. 4", "PDF p. 7", "Décomposition C̄op = C̄p1 + C̄p2"),
            ("Fig. 9", "PDF p. 8", "Signes de C_L, dh/dt, C_M, dθ/dt"),
            ("Fig. 10-12", "PDF p. 9-11", "Vorticité pour β=1, 1,5, 4"),
            ("Fig. 13-15", "PDF p. 12-14", "Pression de paroi pour β=1, 1,5, 4"),
            ("Conclusion", "PDF p. 14-15", "Optimum et limite du mouvement imposé"),
        ],
        columns=["Repère", "Où", "Pourquoi le regarder"],
    )
    st.dataframe(refs, use_container_width=True, hide_index=True)

st.divider()
st.caption(
    "Application de lecture — valeurs tabulaires reprises de Xiao et al. (2012). "
    "Les graphiques cinématiques sont recalculés à partir des équations de l'article ; "
    "aucune courbe CFD de performance n'est interpolée."
)
