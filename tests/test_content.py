from study_content import EQUATION_GUIDE, FIGURE_CROPS, METHOD_FACTS, PAGE_FIGURES, PAGE_GUIDE, PRIOR_WORK


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


def test_figure_slider_map_covers_all_paper_figures():
    assert sorted(FIGURE_CROPS) == list(range(1, 16))
    assert PAGE_FIGURES == {
        1: [],
        2: [1],
        3: [2, 3],
        4: [4, 5],
        5: [6],
        6: [7],
        7: [8],
        8: [9],
        9: [10],
        10: [11],
        11: [12],
        12: [13],
        13: [14],
        14: [15],
        15: [],
    }


def test_figure_crop_boxes_are_normalized():
    for meta in FIGURE_CROPS.values():
        x0, y0, x1, y1 = meta["box"]
        assert 0 <= x0 < x1 <= 1
        assert 0 <= y0 < y1 <= 1

def test_page_11_distinguishes_referenced_and_printed_figures():
    page11 = PAGE_GUIDE[10]
    assert any("Fig. 9" in item and "publiée p. 68" in item for item in page11["figures"])
    assert any("Fig. 12" in item and "imprimée sur cette page" in item for item in page11["figures"])
