import vat
from bs4 import BeautifulSoup

def test_check_doc_language():
    # missing document language - should be wrong
    test_vat = vat.VAT("http://www.test.com/", 1)
    test_vat.page = BeautifulSoup("<html></html>", "html.parser")
    test_vat.check_doc_language()
    assert test_vat.wrong["doc_language"] == 1
    assert test_vat.correct["doc_language"] == 0

    # empty document language - should be wrong
    test_vat = vat.VAT("http://www.test.com/", 1)
    test_vat.page = BeautifulSoup("<html lang=''></html>", "html.parser")
    test_vat.check_doc_language()
    assert test_vat.wrong["doc_language"] == 1
    assert test_vat.correct["doc_language"] == 0

    # set document language - should be correct
    test_vat = vat.VAT("http://www.test.com/", 1)
    test_vat.page = BeautifulSoup("<html lang='de'></html>", "html.parser")
    test_vat.check_doc_language()
    assert test_vat.wrong["doc_language"] == 0
    assert test_vat.correct["doc_language"] == 1


def test_check_alt_texts():
    # missing alt attribute - should be wrong
    test_vat = vat.VAT("http://www.test.com/", 1)
    test_vat.page = BeautifulSoup("<html><body><img src=''></body></html>", "html.parser")
    test_vat.check_alt_texts()
    assert test_vat.wrong["alt_texts"] == 1
    assert test_vat.correct["alt_texts"] == 0

    # empty alt attribute - should be wrong
    test_vat = vat.VAT("http://www.test.com/", 1)
    test_vat.page = BeautifulSoup("<html><body><img alt='' src=''></body></html>", "html.parser")
    test_vat.check_alt_texts()
    assert test_vat.wrong["alt_texts"] == 1
    assert test_vat.correct["alt_texts"] == 0

    # set alt attribute - should be correct
    test_vat = vat.VAT("http://www.test.com/", 1)
    test_vat.page = BeautifulSoup("<html><body><img alt='beautiful image' src=''></body></html>", "html.parser")
    test_vat.check_alt_texts()
    assert test_vat.wrong["alt_texts"] == 0
    assert test_vat.correct["alt_texts"] == 1


def test_check_input_labels():
    # input type hidden - should be ignored
    test_vat = vat.VAT("http://www.test.com/", 1)
    test_vat.page = BeautifulSoup("<html><body><input type='hidden'></body></html>", "html.parser")
    test_vat.check_input_labels()
    assert test_vat.wrong["input_labels"] == 0
    assert test_vat.correct["input_labels"] == 0

    # input type image without alt attribute - should be wrong
    test_vat = vat.VAT("http://www.test.com/", 1)
    test_vat.page = BeautifulSoup("<html><body><input type='image'></body></html>", "html.parser")
    test_vat.check_input_labels()
    assert test_vat.wrong["input_labels"] == 1
    assert test_vat.correct["input_labels"] == 0

    # input type image with empty alt attribute - should be wrong
    test_vat = vat.VAT("http://www.test.com/", 1)
    test_vat.page = BeautifulSoup("<html><body><input type='image' alt=''></body></html>", "html.parser")
    test_vat.check_input_labels()
    assert test_vat.wrong["input_labels"] == 1
    assert test_vat.correct["input_labels"] == 0

    # input type image with filled alt attribute - should be correct
    test_vat = vat.VAT("http://www.test.com/", 1)
    test_vat.page = BeautifulSoup("<html><body><input type='image' alt='image as button'></body></html>", "html.parser")
    test_vat.check_input_labels()
    assert test_vat.wrong["input_labels"] == 0
    assert test_vat.correct["input_labels"] == 1

    # input type text without aria-labelledby or label element - should be wrong
    test_vat = vat.VAT("http://www.test.com/", 1)
    test_vat.page = BeautifulSoup("<html><body><input type='text'></body></html>", "html.parser")
    test_vat.check_input_labels()
    assert test_vat.wrong["input_labels"] == 1
    assert test_vat.correct["input_labels"] == 0

    # input type text with empty aria-labelledby attribute - should be wrong
    test_vat = vat.VAT("http://www.test.com/", 1)
    test_vat.page = BeautifulSoup("<html><body><input type='text' aria-labelledby=''></body></html>", "html.parser")
    test_vat.check_input_labels()
    assert test_vat.wrong["input_labels"] == 1
    assert test_vat.correct["input_labels"] == 0

    # input type text with filled aria-labelledby attribute - should be correct
    test_vat = vat.VAT("http://www.test.com/", 1)
    test_vat.page = BeautifulSoup("<html><body><input type='text' aria-labelledby='This is an aria-labelledby attribute'></body></html>", "html.parser")
    test_vat.check_input_labels()
    assert test_vat.wrong["input_labels"] == 0
    assert test_vat.correct["input_labels"] == 1

    # input type text with empty for attribute - should be wrong
    test_vat = vat.VAT("http://www.test.com/", 1)
    test_vat.page = BeautifulSoup("<html><body><input type='text' for=''></body></html>", "html.parser")
    test_vat.check_input_labels()
    assert test_vat.wrong["input_labels"] == 1
    assert test_vat.correct["input_labels"] == 0

    # input type text with filled id attribute but no label - should be wrong
    test_vat = vat.VAT("http://www.test.com/", 1)
    test_vat.page = BeautifulSoup("<html><body><input type='text' id='test-input'></body></html>", "html.parser")
    test_vat.check_input_labels()
    assert test_vat.wrong["input_labels"] == 1
    assert test_vat.correct["input_labels"] == 0

    # input type text with filled id attribute and correct label - should be correct
    test_vat = vat.VAT("http://www.test.com/", 1)
    test_vat.page = BeautifulSoup("<html><body><label for='test-input'>This is an input field</label><input type='text' id='test-input'></body></html>", "html.parser")
    test_vat.check_input_labels()
    assert test_vat.wrong["input_labels"] == 0
    assert test_vat.correct["input_labels"] == 1


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