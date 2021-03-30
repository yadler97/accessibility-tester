import vat
from bs4 import BeautifulSoup

def test_check_doc_language():
    # missing document language
    test_vat = vat.VAT("http://www.test.com/", 1)
    test_vat.page = BeautifulSoup("<html></html>", "html.parser")
    test_vat.check_doc_language()
    assert test_vat.wrong["doc_language"] == 1
    assert test_vat.correct["doc_language"] == 0

    # empty document language
    test_vat = vat.VAT("http://www.test.com/", 1)
    test_vat.page = BeautifulSoup("<html lang=''></html>", "html.parser")
    test_vat.check_doc_language()
    assert test_vat.wrong["doc_language"] == 1
    assert test_vat.correct["doc_language"] == 0

    # set document language
    test_vat = vat.VAT("http://www.test.com/", 1)
    test_vat.page = BeautifulSoup("<html lang='de'></html>", "html.parser")
    test_vat.check_doc_language()
    assert test_vat.wrong["doc_language"] == 0
    assert test_vat.correct["doc_language"] == 1

def test_check_alt_texts():
    # missing alt attribute
    test_vat = vat.VAT("http://www.test.com/", 1)
    test_vat.page = BeautifulSoup("<html><body><img src=''></body></html>", "html.parser")
    test_vat.check_alt_texts()
    assert test_vat.wrong["alt_texts"] == 1
    assert test_vat.correct["alt_texts"] == 0

    # empty alt attribute
    test_vat = vat.VAT("http://www.test.com/", 1)
    test_vat.page = BeautifulSoup("<html><body><img alt='' src=''></body></html>", "html.parser")
    test_vat.check_alt_texts()
    assert test_vat.wrong["alt_texts"] == 1
    assert test_vat.correct["alt_texts"] == 0

    # set alt attribute
    test_vat = vat.VAT("http://www.test.com/", 1)
    test_vat.page = BeautifulSoup("<html><body><img alt='beautiful image' src=''></body></html>", "html.parser")
    test_vat.check_alt_texts()
    assert test_vat.wrong["alt_texts"] == 0
    assert test_vat.correct["alt_texts"] == 1

def test_get_contrast_ration():
    # highest contrast
    text_color = (0,0,0)
    background_color = (255,255,255)
    assert vat.get_contrast_ratio(text_color, background_color) == 21

    # lowest contrast
    text_color = (0,0,0)
    background_color = (0,0,0)
    assert vat.get_contrast_ratio(text_color, background_color) == 1

    # black text on red background
    text_color = (0,0,0)
    background_color = (255,0,0)
    assert vat.get_contrast_ratio(text_color, background_color) == 5.252