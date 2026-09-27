from study_content import EQUATION_GUIDE, METHOD_FACTS, PAGE_GUIDE, PRIOR_WORK


def test_all_pdf_pages_have_reading_cards():
    assert len(PAGE_GUIDE) == 15
    assert [item["pdf_page"] for item in PAGE_GUIDE] == list(range(1, 16))


def test_every_page_card_is_substantive():
    for item in PAGE_GUIDE:
        assert len(item["summary"]) > 250
        assert len(item["important"]) >= 4
        assert item["figures"]
        assert item["equations_tables"]
        assert len(item["question"]) > 30


def test_method_and_equation_guides_are_populated():
    assert len(METHOD_FACTS) >= 12
    assert len(EQUATION_GUIDE) >= 7
    assert len(PRIOR_WORK) >= 5


def test_key_pages_cover_core_results_and_limitation():
    page9 = PAGE_GUIDE[8]
    page15 = PAGE_GUIDE[14]
    assert "63 %" in page9["summary"]
    assert "50 %" in page9["summary"]
    assert "β=1,5" in page15["summary"]
    assert "prescrits" in page15["summary"]
