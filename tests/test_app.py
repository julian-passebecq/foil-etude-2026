from streamlit.testing.v1 import AppTest


def test_streamlit_app_smoke():
    app = AppTest.from_file("app.py", default_timeout=20).run()
    assert not app.exception
    assert app.title
    assert "Lecture guidée" in app.title[0].value
    assert len(app.tabs) == 5
