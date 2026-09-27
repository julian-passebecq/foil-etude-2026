from pathlib import Path

from streamlit.testing.v1 import AppTest


def _page_slider(app):
    for slider in app.sidebar.slider:
        if slider.label == "Page de l'étude":
            return slider
    raise AssertionError("Page slider not found")


def test_streamlit_app_smoke():
    app_path = Path(__file__).resolve().parents[1] / "app.py"
    app = AppTest.from_file(app_path, default_timeout=20).run()
    assert not app.exception
    assert app.title
    assert "Étude des foils oscillants" in app.title[0].value
    assert len(app.tabs) == 7


def test_single_figure_pages_do_not_create_invalid_slider():
    app_path = Path(__file__).resolve().parents[1] / "app.py"
    app = AppTest.from_file(app_path, default_timeout=20).run()

    for page in (2, 5, 11, 14):
        app = _page_slider(app).set_value(page).run()
        assert not app.exception
        assert not any(slider.label == "Figure de la page" for slider in app.sidebar.slider)


def test_multi_figure_page_keeps_figure_slider():
    app_path = Path(__file__).resolve().parents[1] / "app.py"
    app = AppTest.from_file(app_path, default_timeout=20).run()
    app = _page_slider(app).set_value(3).run()
    assert not app.exception
    figure_sliders = [slider for slider in app.sidebar.slider if slider.label == "Figure de la page"]
    assert len(figure_sliders) == 1
    assert figure_sliders[0].min == 1
    assert figure_sliders[0].max == 2
