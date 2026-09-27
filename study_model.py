from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import pandas as pd


# Source: Xiao et al. (2012), Table 1, PDF p. 5 / article p. 65.
# Ratios: Tables 2-3, PDF p. 6 / article p. 66.
SCENARIOS = pd.DataFrame(
    [
        {
            "h0/c": 0.5,
            "alpha0": 10,
            "Cop_beta1": 0.14,
            "power_best_ratio": 1.40,
            "power_best_beta": 1.50,
            "power_worst_ratio": 0.833,
            "power_worst_beta": 4.00,
            "eta_best_ratio": 1.25,
            "eta_best_beta": 1.25,
            "eta_worst_ratio": 0.74,
            "eta_worst_beta": 4.00,
            "st_best_ratio": 1.17,
            "st_best_beta": 1.25,
            "st_worst_ratio": 0.57,
            "st_worst_beta": 4.00,
        },
        {
            "h0/c": 0.5,
            "alpha0": 20,
            "Cop_beta1": 0.28,
            "power_best_ratio": 1.43,
            "power_best_beta": 1.50,
            "power_worst_ratio": 0.82,
            "power_worst_beta": 4.00,
            "eta_best_ratio": 1.50,
            "eta_best_beta": 1.50,
            "eta_worst_ratio": 0.66,
            "eta_worst_beta": 4.00,
            "st_best_ratio": 1.17,
            "st_best_beta": 1.25,
            "st_worst_ratio": 0.66,
            "st_worst_beta": 4.00,
        },
        {
            "h0/c": 1.0,
            "alpha0": 10,
            "Cop_beta1": 0.36,
            "power_best_ratio": 1.63,
            "power_best_beta": 1.50,
            "power_worst_ratio": 0.71,
            "power_worst_beta": 4.00,
            "eta_best_ratio": 1.50,
            "eta_best_beta": 1.50,
            "eta_worst_ratio": 0.656,
            "eta_worst_beta": 4.00,
            "st_best_ratio": 1.28,
            "st_best_beta": 1.25,
            "st_worst_ratio": 0.43,
            "st_worst_beta": 4.00,
        },
        {
            "h0/c": 1.0,
            "alpha0": 20,
            "Cop_beta1": 0.73,
            "power_best_ratio": 1.347,
            "power_best_beta": 1.50,
            "power_worst_ratio": 0.54,
            "power_worst_beta": 4.00,
            "eta_best_ratio": 1.25,
            "eta_best_beta": 1.25,
            "eta_worst_ratio": 0.52,
            "eta_worst_beta": 4.00,
            "st_best_ratio": 1.347,
            "st_best_beta": 1.25,
            "st_worst_ratio": 0.57,
            "st_worst_beta": 4.00,
        },
    ]
)

# Source: Xiao et al. (2012), Table 4, PDF p. 7 / article p. 67.
# The printed table is rounded, hence Cop can differ slightly from Cp1 + Cp2.
POWER_DECOMP = pd.DataFrame(
    {
        "beta": [1.0, 1.5, 2.0, 4.0],
        "Cop": [0.36, 0.62, 0.563, -0.842],
        "Cp1_lift": [0.55, 0.96, 1.13, 1.23],
        "Cp2_moment": [-0.181, -0.34, -0.564, -2.07],
    }
)


@dataclass(frozen=True)
class KinematicState:
    phase: np.ndarray
    h_norm: np.ndarray
    theta_norm: np.ndarray
    theta_deg: np.ndarray
    alpha_eff_deg: np.ndarray
    theta0_deg: float


def pitching_profile(phase: np.ndarray, beta: float) -> np.ndarray:
    """Equation (5) of Xiao et al. (2012), on normalized phase t/T in [0, 1]."""
    phase = np.asarray(phase, dtype=float)
    b = float(beta)
    if b < 1.0:
        raise ValueError("beta must be >= 1")

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
    """Rebuild the kinematic curves from equations (4), (5), (7) and (8)."""
    if st_value <= 0:
        raise ValueError("St must be positive")

    phase = np.linspace(0.0, 1.0, 1001)
    h_norm = np.sin(2.0 * np.pi * phase)
    theta_norm = pitching_profile(phase, beta)

    # Eq. (8): alpha0 = -atan(omega*h0/Uinf) + theta0.
    # With St=f*(2h0)/Uinf, omega*h0/Uinf = pi*St.
    theta0_deg = alpha0_deg + math.degrees(math.atan(math.pi * st_value))
    theta_deg = theta0_deg * theta_norm

    plunge_induced_deg = np.degrees(np.arctan(math.pi * st_value * np.cos(2.0 * np.pi * phase)))
    alpha_eff_deg = theta_deg - plunge_induced_deg
    return KinematicState(phase, h_norm, theta_norm, theta_deg, alpha_eff_deg, theta0_deg)


def pct(ratio: float) -> str:
    return f"{(ratio - 1.0) * 100.0:+.0f} %"


def scenario_row(h_ratio: float, alpha0_deg: int) -> pd.Series:
    rows = SCENARIOS[(SCENARIOS["h0/c"] == h_ratio) & (SCENARIOS["alpha0"] == alpha0_deg)]
    if len(rows) != 1:
        raise KeyError(f"No unique scenario for h0/c={h_ratio}, alpha0={alpha0_deg}")
    return rows.iloc[0]


def table4_rounding_error() -> pd.Series:
    """Difference between printed Cop and the sum of the two printed rounded components."""
    return POWER_DECOMP["Cop"] - (POWER_DECOMP["Cp1_lift"] + POWER_DECOMP["Cp2_moment"])
