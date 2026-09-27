from pathlib import Path

from streamlit.testing.v1 import AppTest


def test_streamlit_app_smoke():
    app_path = Path(__file__).resolve().parents[1] / "app.py"
    app = AppTest.from_file(app_path, default_timeout=20).run()
    assert not app.exception
    assert app.title
    assert "Étude des foils oscillants" in app.title[0].value
    assert len(app.tabs) == 7
