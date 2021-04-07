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


def test_check_buttons():
    # input type text - should be ignored
    test_vat = vat.VAT("http://www.test.com/", 1)
    test_vat.page = BeautifulSoup("<html><body><input type='text'></body></html>", "html.parser")
    test_vat.check_buttons()
    assert test_vat.wrong["empty_buttons"] == 0
    assert test_vat.correct["empty_buttons"] == 0

    # input type submit without value attribute - should be wrong
    test_vat = vat.VAT("http://www.test.com/", 1)
    test_vat.page = BeautifulSoup("<html><body><input type='submit'></body></html>", "html.parser")
    test_vat.check_buttons()
    assert test_vat.wrong["empty_buttons"] == 1
    assert test_vat.correct["empty_buttons"] == 0

    # input type submit with empty value attribute - should be wrong
    test_vat = vat.VAT("http://www.test.com/", 1)
    test_vat.page = BeautifulSoup("<html><body><input type='submit' value=''></body></html>", "html.parser")
    test_vat.check_buttons()
    assert test_vat.wrong["empty_buttons"] == 1
    assert test_vat.correct["empty_buttons"] == 0

    # input type submit with filled value attribute - should be correct
    test_vat = vat.VAT("http://www.test.com/", 1)
    test_vat.page = BeautifulSoup("<html><body><input type='submit' value='Submit'></body></html>", "html.parser")
    test_vat.check_buttons()
    assert test_vat.wrong["empty_buttons"] == 0
    assert test_vat.correct["empty_buttons"] == 1

    # button element without text or title attribute - should be wrong
    test_vat = vat.VAT("http://www.test.com/", 1)
    test_vat.page = BeautifulSoup("<html><body><button></button></body></html>", "html.parser")
    test_vat.check_buttons()
    assert test_vat.wrong["empty_buttons"] == 1
    assert test_vat.correct["empty_buttons"] == 0

    # button element with an empty other element - should be wrong
    test_vat = vat.VAT("http://www.test.com/", 1)
    test_vat.page = BeautifulSoup("<html><body><button><p></p></button></body></html>", "html.parser")
    test_vat.check_buttons()
    assert test_vat.wrong["empty_buttons"] == 1
    assert test_vat.correct["empty_buttons"] == 0

    # button element with text - should be correct
    test_vat = vat.VAT("http://www.test.com/", 1)
    test_vat.page = BeautifulSoup("<html><body><button>Click here!</button></body></html>", "html.parser")
    test_vat.check_buttons()
    assert test_vat.wrong["empty_buttons"] == 0
    assert test_vat.correct["empty_buttons"] == 1

    # button element with text inside another element - should be correct
    test_vat = vat.VAT("http://www.test.com/", 1)
    test_vat.page = BeautifulSoup("<html><body><button><p>Click here!</p></button></body></html>", "html.parser")
    test_vat.check_buttons()
    assert test_vat.wrong["empty_buttons"] == 0
    assert test_vat.correct["empty_buttons"] == 1

    # button element with empty title attribute - should be wrong
    test_vat = vat.VAT("http://www.test.com/", 1)
    test_vat.page = BeautifulSoup("<html><body><button title=''></button></body></html>", "html.parser")
    test_vat.check_buttons()
    assert test_vat.wrong["empty_buttons"] == 1
    assert test_vat.correct["empty_buttons"] == 0

    # button element with filled title attribute - should be correct
    test_vat = vat.VAT("http://www.test.com/", 1)
    test_vat.page = BeautifulSoup("<html><body><button title='Click here!'></button></body></html>", "html.parser")
    test_vat.check_buttons()
    assert test_vat.wrong["empty_buttons"] == 0
    assert test_vat.correct["empty_buttons"] == 1


def test_check_links():
    # link element without text - should be wrong
    test_vat = vat.VAT("http://www.test.com/", 1)
    test_vat.page = BeautifulSoup("<html><body><a href='/'></a></body></html>", "html.parser")
    test_vat.check_links()
    assert test_vat.wrong["empty_links"] == 1
    assert test_vat.correct["empty_links"] == 0

    # link element with text - should be correct
    test_vat = vat.VAT("http://www.test.com/", 1)
    test_vat.page = BeautifulSoup("<html><body><a href='/'>Click here</a></body></html>", "html.parser")
    test_vat.check_links()
    assert test_vat.wrong["empty_links"] == 0
    assert test_vat.correct["empty_links"] == 1

    # link element with image element without alt attribute - should be wrong
    test_vat = vat.VAT("http://www.test.com/", 1)
    test_vat.page = BeautifulSoup("<html><body><a href='/'><img src=''></a></body></html>", "html.parser")
    test_vat.check_links()
    assert test_vat.wrong["empty_links"] == 1
    assert test_vat.correct["empty_links"] == 0

    # link element with image element with empty alt attribute - should be wrong
    test_vat = vat.VAT("http://www.test.com/", 1)
    test_vat.page = BeautifulSoup("<html><body><a href='/'><img alt='' src=''></a></body></html>", "html.parser")
    test_vat.check_links()
    assert test_vat.wrong["empty_links"] == 1
    assert test_vat.correct["empty_links"] == 0

    # link element with image element with filled alt attribute - should be correct
    test_vat = vat.VAT("http://www.test.com/", 1)
    test_vat.page = BeautifulSoup("<html><body><a href='/'><img alt='beautiful image' src=''></a></body></html>", "html.parser")
    test_vat.check_links()
    assert test_vat.wrong["empty_links"] == 0
    assert test_vat.correct["empty_links"] == 1


def test_get_contrast_ratio():
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