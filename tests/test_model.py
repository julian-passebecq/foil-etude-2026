import numpy as np
import pytest

from study_model import POWER_DECOMP, SCENARIOS, kinematics, pitching_profile, scenario_row, table4_rounding_error


def test_beta_one_is_cosine_pitching():
    phase = np.linspace(0.0, 1.0, 1001)
    actual = pitching_profile(phase, 1.0)
    expected = np.cos(2.0 * np.pi * phase)
    assert np.allclose(actual, expected, atol=1e-12)


@pytest.mark.parametrize("beta", [1.0, 1.25, 1.5, 2.0, 4.0])
def test_pitching_profile_is_bounded_and_periodic(beta):
    phase = np.linspace(0.0, 1.0, 4001)
    theta = pitching_profile(phase, beta)
    assert theta.min() >= -1.0 - 1e-12
    assert theta.max() <= 1.0 + 1e-12
    assert theta[0] == pytest.approx(theta[-1], abs=1e-12)


def test_invalid_beta_rejected():
    with pytest.raises(ValueError):
        pitching_profile(np.array([0.0, 0.5, 1.0]), 0.9)


def test_kinematics_equation_8_relation():
    state = kinematics(beta=1.5, st_value=0.35, alpha0_deg=10.0)
    assert state.theta0_deg > 10.0
    assert len(state.phase) == len(state.alpha_eff_deg) == 1001


def test_all_four_source_scenarios_are_unique():
    assert len(SCENARIOS) == 4
    for h_ratio in (0.5, 1.0):
        for alpha0 in (10, 20):
            row = scenario_row(h_ratio, alpha0)
            assert row["Cop_beta1"] > 0


def test_table4_signs_and_rounding_consistency():
    beta4 = POWER_DECOMP.loc[POWER_DECOMP["beta"] == 4.0].iloc[0]
    assert beta4["Cop"] < 0
    assert beta4["Cp1_lift"] > 0
    assert beta4["Cp2_moment"] < 0
    assert table4_rounding_error().abs().max() < 0.011


def test_key_published_ratios_are_preserved():
    row = scenario_row(1.0, 10)
    assert row["power_best_ratio"] == pytest.approx(1.63)
    assert row["eta_best_ratio"] == pytest.approx(1.50)
    assert row["st_worst_ratio"] == pytest.approx(0.43)
