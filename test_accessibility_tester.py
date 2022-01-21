from http.server import BaseHTTPRequestHandler, HTTPServer
import multiprocessing
import sys

from bs4 import BeautifulSoup

import accessibility_tester


HOST_NAME = "localhost"
SERVER_PORT = 45459

def test_check_doc_language():
    # missing document language - should be wrong
    test_accessibility_tester = accessibility_tester.AccessibilityTester("test URL")
    test_accessibility_tester.page = BeautifulSoup("<html></html>", "html.parser")
    test_accessibility_tester.check_doc_language()
    assert test_accessibility_tester.wrong["doc_language"] == 1
    assert test_accessibility_tester.correct["doc_language"] == 0

    # empty document language - should be wrong
    test_accessibility_tester = accessibility_tester.AccessibilityTester("test URL")
    test_accessibility_tester.page = BeautifulSoup("<html lang=''></html>", "html.parser")
    test_accessibility_tester.check_doc_language()
    assert test_accessibility_tester.wrong["doc_language"] == 1
    assert test_accessibility_tester.correct["doc_language"] == 0

    # set document language - should be correct
    test_accessibility_tester = accessibility_tester.AccessibilityTester("test URL")
    test_accessibility_tester.page = BeautifulSoup("<html lang='de'></html>", "html.parser")
    test_accessibility_tester.check_doc_language()
    assert test_accessibility_tester.wrong["doc_language"] == 0
    assert test_accessibility_tester.correct["doc_language"] == 1


def test_check_alt_texts():
    # missing alt attribute - should be wrong
    test_accessibility_tester = accessibility_tester.AccessibilityTester("test URL")
    test_accessibility_tester.page = BeautifulSoup("<html><body><img src=''></body></html>", "html.parser")
    test_accessibility_tester.check_alt_texts()
    assert test_accessibility_tester.wrong["alt_texts"] == 1
    assert test_accessibility_tester.correct["alt_texts"] == 0

    # empty alt attribute - should be wrong
    test_accessibility_tester = accessibility_tester.AccessibilityTester("test URL")
    test_accessibility_tester.page = BeautifulSoup("<html><body><img alt='' src=''></body></html>", "html.parser")
    test_accessibility_tester.check_alt_texts()
    assert test_accessibility_tester.wrong["alt_texts"] == 1
    assert test_accessibility_tester.correct["alt_texts"] == 0

    # set alt attribute - should be correct
    test_accessibility_tester = accessibility_tester.AccessibilityTester("test URL")
    test_accessibility_tester.page = BeautifulSoup("<html><body><img alt='beautiful image' src=''></body></html>", "html.parser")
    test_accessibility_tester.check_alt_texts()
    assert test_accessibility_tester.wrong["alt_texts"] == 0
    assert test_accessibility_tester.correct["alt_texts"] == 1


def test_check_input_labels():
    # input type hidden - should be ignored
    test_accessibility_tester = accessibility_tester.AccessibilityTester("test URL")
    test_accessibility_tester.page = BeautifulSoup("<html><body><input type='hidden'></body></html>", "html.parser")
    test_accessibility_tester.check_input_labels()
    assert test_accessibility_tester.wrong["input_labels"] == 0
    assert test_accessibility_tester.correct["input_labels"] == 0

    # input type image without alt attribute - should be wrong
    test_accessibility_tester = accessibility_tester.AccessibilityTester("test URL")
    test_accessibility_tester.page = BeautifulSoup("<html><body><input type='image'></body></html>", "html.parser")
    test_accessibility_tester.check_input_labels()
    assert test_accessibility_tester.wrong["input_labels"] == 1
    assert test_accessibility_tester.correct["input_labels"] == 0

    # input type image with empty alt attribute - should be wrong
    test_accessibility_tester = accessibility_tester.AccessibilityTester("test URL")
    test_accessibility_tester.page = BeautifulSoup("<html><body><input type='image' alt=''></body></html>", "html.parser")
    test_accessibility_tester.check_input_labels()
    assert test_accessibility_tester.wrong["input_labels"] == 1
    assert test_accessibility_tester.correct["input_labels"] == 0

    # input type image with filled alt attribute - should be correct
    test_accessibility_tester = accessibility_tester.AccessibilityTester("test URL")
    test_accessibility_tester.page = BeautifulSoup("<html><body><input type='image' alt='image as button'></body></html>", "html.parser")
    test_accessibility_tester.check_input_labels()
    assert test_accessibility_tester.wrong["input_labels"] == 0
    assert test_accessibility_tester.correct["input_labels"] == 1

    # input type text without aria-labelledby or label element - should be wrong
    test_accessibility_tester = accessibility_tester.AccessibilityTester("test URL")
    test_accessibility_tester.page = BeautifulSoup("<html><body><input type='text'></body></html>", "html.parser")
    test_accessibility_tester.check_input_labels()
    assert test_accessibility_tester.wrong["input_labels"] == 1
    assert test_accessibility_tester.correct["input_labels"] == 0

    # input type text with empty aria-labelledby attribute - should be wrong
    test_accessibility_tester = accessibility_tester.AccessibilityTester("test URL")
    test_accessibility_tester.page = BeautifulSoup("<html><body><input type='text' aria-labelledby=''></body></html>", "html.parser")
    test_accessibility_tester.check_input_labels()
    assert test_accessibility_tester.wrong["input_labels"] == 1
    assert test_accessibility_tester.correct["input_labels"] == 0

    # input type text with filled aria-labelledby attribute - should be correct
    test_accessibility_tester = accessibility_tester.AccessibilityTester("test URL")
    test_accessibility_tester.page = BeautifulSoup("<html><body><input type='text' aria-labelledby='This is an aria-labelledby attribute'></body></html>", "html.parser")
    test_accessibility_tester.check_input_labels()
    assert test_accessibility_tester.wrong["input_labels"] == 0
    assert test_accessibility_tester.correct["input_labels"] == 1

    # input type text with empty for attribute - should be wrong
    test_accessibility_tester = accessibility_tester.AccessibilityTester("test URL")
    test_accessibility_tester.page = BeautifulSoup("<html><body><input type='text' for=''></body></html>", "html.parser")
    test_accessibility_tester.check_input_labels()
    assert test_accessibility_tester.wrong["input_labels"] == 1
    assert test_accessibility_tester.correct["input_labels"] == 0

    # input type text with filled id attribute but no label - should be wrong
    test_accessibility_tester = accessibility_tester.AccessibilityTester("test URL")
    test_accessibility_tester.page = BeautifulSoup("<html><body><input type='text' id='test-input'></body></html>", "html.parser")
    test_accessibility_tester.check_input_labels()
    assert test_accessibility_tester.wrong["input_labels"] == 1
    assert test_accessibility_tester.correct["input_labels"] == 0

    # input type text with filled id attribute and correct label - should be correct
    test_accessibility_tester = accessibility_tester.AccessibilityTester("test URL")
    test_accessibility_tester.page = BeautifulSoup("<html><body><label for='test-input'>This is an input field</label><input type='text' id='test-input'></body></html>", "html.parser")
    test_accessibility_tester.check_input_labels()
    assert test_accessibility_tester.wrong["input_labels"] == 0
    assert test_accessibility_tester.correct["input_labels"] == 1


def test_check_buttons():
    # input type text - should be ignored
    test_accessibility_tester = accessibility_tester.AccessibilityTester("test URL")
    test_accessibility_tester.page = BeautifulSoup("<html><body><input type='text'></body></html>", "html.parser")
    test_accessibility_tester.check_buttons()
    assert test_accessibility_tester.wrong["empty_buttons"] == 0
    assert test_accessibility_tester.correct["empty_buttons"] == 0

    # input type submit without value attribute - should be wrong
    test_accessibility_tester = accessibility_tester.AccessibilityTester("test URL")
    test_accessibility_tester.page = BeautifulSoup("<html><body><input type='submit'></body></html>", "html.parser")
    test_accessibility_tester.check_buttons()
    assert test_accessibility_tester.wrong["empty_buttons"] == 1
    assert test_accessibility_tester.correct["empty_buttons"] == 0

    # input type submit with empty value attribute - should be wrong
    test_accessibility_tester = accessibility_tester.AccessibilityTester("test URL")
    test_accessibility_tester.page = BeautifulSoup("<html><body><input type='submit' value=''></body></html>", "html.parser")
    test_accessibility_tester.check_buttons()
    assert test_accessibility_tester.wrong["empty_buttons"] == 1
    assert test_accessibility_tester.correct["empty_buttons"] == 0

    # input type submit with filled value attribute - should be correct
    test_accessibility_tester = accessibility_tester.AccessibilityTester("test URL")
    test_accessibility_tester.page = BeautifulSoup("<html><body><input type='submit' value='Submit'></body></html>", "html.parser")
    test_accessibility_tester.check_buttons()
    assert test_accessibility_tester.wrong["empty_buttons"] == 0
    assert test_accessibility_tester.correct["empty_buttons"] == 1

    # button element without text or title attribute - should be wrong
    test_accessibility_tester = accessibility_tester.AccessibilityTester("test URL")
    test_accessibility_tester.page = BeautifulSoup("<html><body><button></button></body></html>", "html.parser")
    test_accessibility_tester.check_buttons()
    assert test_accessibility_tester.wrong["empty_buttons"] == 1
    assert test_accessibility_tester.correct["empty_buttons"] == 0

    # button element with an empty other element - should be wrong
    test_accessibility_tester = accessibility_tester.AccessibilityTester("test URL")
    test_accessibility_tester.page = BeautifulSoup("<html><body><button><p></p></button></body></html>", "html.parser")
    test_accessibility_tester.check_buttons()
    assert test_accessibility_tester.wrong["empty_buttons"] == 1
    assert test_accessibility_tester.correct["empty_buttons"] == 0

    # button element with text - should be correct
    test_accessibility_tester = accessibility_tester.AccessibilityTester("test URL")
    test_accessibility_tester.page = BeautifulSoup("<html><body><button>Click here!</button></body></html>", "html.parser")
    test_accessibility_tester.check_buttons()
    assert test_accessibility_tester.wrong["empty_buttons"] == 0
    assert test_accessibility_tester.correct["empty_buttons"] == 1

    # button element with text inside another element - should be correct
    test_accessibility_tester = accessibility_tester.AccessibilityTester("test URL")
    test_accessibility_tester.page = BeautifulSoup("<html><body><button><p>Click here!</p></button></body></html>", "html.parser")
    test_accessibility_tester.check_buttons()
    assert test_accessibility_tester.wrong["empty_buttons"] == 0
    assert test_accessibility_tester.correct["empty_buttons"] == 1

    # button element with empty title attribute - should be wrong
    test_accessibility_tester = accessibility_tester.AccessibilityTester("test URL")
    test_accessibility_tester.page = BeautifulSoup("<html><body><button title=''></button></body></html>", "html.parser")
    test_accessibility_tester.check_buttons()
    assert test_accessibility_tester.wrong["empty_buttons"] == 1
    assert test_accessibility_tester.correct["empty_buttons"] == 0

    # button element with filled title attribute - should be correct
    test_accessibility_tester = accessibility_tester.AccessibilityTester("test URL")
    test_accessibility_tester.page = BeautifulSoup("<html><body><button title='Click here!'></button></body></html>", "html.parser")
    test_accessibility_tester.check_buttons()
    assert test_accessibility_tester.wrong["empty_buttons"] == 0
    assert test_accessibility_tester.correct["empty_buttons"] == 1


def test_check_links():
    # link element without text - should be wrong
    test_accessibility_tester = accessibility_tester.AccessibilityTester("test URL")
    test_accessibility_tester.page = BeautifulSoup("<html><body><a href='/'></a></body></html>", "html.parser")
    test_accessibility_tester.check_links()
    assert test_accessibility_tester.wrong["empty_links"] == 1
    assert test_accessibility_tester.correct["empty_links"] == 0

    # link element with text - should be correct
    test_accessibility_tester = accessibility_tester.AccessibilityTester("test URL")
    test_accessibility_tester.page = BeautifulSoup("<html><body><a href='/'>Click here</a></body></html>", "html.parser")
    test_accessibility_tester.check_links()
    assert test_accessibility_tester.wrong["empty_links"] == 0
    assert test_accessibility_tester.correct["empty_links"] == 1

    # link element with image element without alt attribute - should be wrong
    test_accessibility_tester = accessibility_tester.AccessibilityTester("test URL")
    test_accessibility_tester.page = BeautifulSoup("<html><body><a href='/'><img src=''></a></body></html>", "html.parser")
    test_accessibility_tester.check_links()
    assert test_accessibility_tester.wrong["empty_links"] == 1
    assert test_accessibility_tester.correct["empty_links"] == 0

    # link element with image element with empty alt attribute - should be wrong
    test_accessibility_tester = accessibility_tester.AccessibilityTester("test URL")
    test_accessibility_tester.page = BeautifulSoup("<html><body><a href='/'><img alt='' src=''></a></body></html>", "html.parser")
    test_accessibility_tester.check_links()
    assert test_accessibility_tester.wrong["empty_links"] == 1
    assert test_accessibility_tester.correct["empty_links"] == 0

    # link element with image element with filled alt attribute - should be correct
    test_accessibility_tester = accessibility_tester.AccessibilityTester("test URL")
    test_accessibility_tester.page = BeautifulSoup("<html><body><a href='/'><img alt='beautiful image' src=''></a></body></html>", "html.parser")
    test_accessibility_tester.check_links()
    assert test_accessibility_tester.wrong["empty_links"] == 0
    assert test_accessibility_tester.correct["empty_links"] == 1


def test_check_color_contrast():
    # Test is not working on Windows, so it will be skipped if sys.platform equals win32
    if sys.platform != 'win32':
        web_server = HTTPServer((HOST_NAME, SERVER_PORT), ColorContrastTestServer)
        proc = multiprocessing.Process(target=start_server, args=(web_server,))
        proc.start()

        # standard text and standard background - should be correct
        test_accessibility_tester = accessibility_tester.AccessibilityTester("http://localhost:%s/color-contrast-test-case-1" % SERVER_PORT)
        test_accessibility_tester.start_driver()
        test_accessibility_tester.check_color_contrast()
        assert test_accessibility_tester.wrong["color_contrast"] == 0
        assert test_accessibility_tester.correct["color_contrast"] == 1

        # black text and red background - should be correct
        test_accessibility_tester = accessibility_tester.AccessibilityTester("http://localhost:%s/color-contrast-test-case-2" % SERVER_PORT)
        test_accessibility_tester.start_driver()
        test_accessibility_tester.check_color_contrast()
        assert test_accessibility_tester.wrong["color_contrast"] == 0
        assert test_accessibility_tester.correct["color_contrast"] == 1

        # black text on grey background - should be wrong
        test_accessibility_tester = accessibility_tester.AccessibilityTester("http://localhost:%s/color-contrast-test-case-3" % SERVER_PORT)
        test_accessibility_tester.start_driver()
        test_accessibility_tester.check_color_contrast()
        assert test_accessibility_tester.wrong["color_contrast"] == 1
        assert test_accessibility_tester.correct["color_contrast"] == 0

        # black text with font-size 18px on grey background - should be correct
        test_accessibility_tester = accessibility_tester.AccessibilityTester("http://localhost:%s/color-contrast-test-case-4" % SERVER_PORT)
        test_accessibility_tester.start_driver()
        test_accessibility_tester.check_color_contrast()
        assert test_accessibility_tester.wrong["color_contrast"] == 0
        assert test_accessibility_tester.correct["color_contrast"] == 1

        # black bold text with font-size 14px on grey background - should be correct
        test_accessibility_tester = accessibility_tester.AccessibilityTester("http://localhost:%s/color-contrast-test-case-5" % SERVER_PORT)
        test_accessibility_tester.start_driver()
        test_accessibility_tester.check_color_contrast()
        assert test_accessibility_tester.wrong["color_contrast"] == 0
        assert test_accessibility_tester.correct["color_contrast"] == 1

        # black strong text with font-size 14px on grey background - should be correct
        test_accessibility_tester = accessibility_tester.AccessibilityTester("http://localhost:%s/color-contrast-test-case-6" % SERVER_PORT)
        test_accessibility_tester.start_driver()
        test_accessibility_tester.check_color_contrast()
        assert test_accessibility_tester.wrong["color_contrast"] == 0
        assert test_accessibility_tester.correct["color_contrast"] == 1

        # black text with font-size 14px on grey background - should be wrong
        test_accessibility_tester = accessibility_tester.AccessibilityTester("http://localhost:%s/color-contrast-test-case-7" % SERVER_PORT)
        test_accessibility_tester.start_driver()
        test_accessibility_tester.check_color_contrast()
        assert test_accessibility_tester.wrong["color_contrast"] == 1
        assert test_accessibility_tester.correct["color_contrast"] == 0

        # rgb and rgba color values - should be correct
        test_accessibility_tester = accessibility_tester.AccessibilityTester("http://localhost:%s/color-contrast-test-case-8" % SERVER_PORT)
        test_accessibility_tester.start_driver()
        test_accessibility_tester.check_color_contrast()
        assert test_accessibility_tester.wrong["color_contrast"] == 0
        assert test_accessibility_tester.correct["color_contrast"] == 1

        web_server.server_close()
        proc.terminate()
        proc.join()
    else:
        print("sys.platform equals win32 - skipping test")


def test_calculate_result(capsys):
    # case nothing found
    test_accessibility_tester = accessibility_tester.AccessibilityTester("test URL")
    test_accessibility_tester.calculate_result()
    assert capsys.readouterr().out == "Nothing found\n"

    # case successful test
    test_accessibility_tester = accessibility_tester.AccessibilityTester("test URL")
    test_accessibility_tester.correct = {"doc_language":1, "alt_texts":0, "input_labels":1, "empty_buttons":0, "empty_links":1, "color_contrast":0}
    test_accessibility_tester.wrong = {"doc_language":0, "alt_texts":1, "input_labels":0, "empty_buttons":1, "empty_links":0, "color_contrast":1}
    test_accessibility_tester.calculate_result()
    assert capsys.readouterr().out == "\nResult\n---------------------\nCorrect: 3\n  doc_language: 1\n  alt_texts: 0\n  input_labels: 1\n  empty_buttons: 0\n  empty_links: 1\n  color_contrast: 0\nErrors: 3\n  doc_language: 0\n  alt_texts: 1\n  input_labels: 0\n  empty_buttons: 1\n  empty_links: 0\n  color_contrast: 1\nRatio (correct to total): 0.5 \n\nAccessibility test successful - can deploy\n"


def test_get_contrast_ratio():
    # highest contrast
    text_color = (0,0,0)
    background_color = (255,255,255)
    assert accessibility_tester.get_contrast_ratio(text_color, background_color) == 21

    # lowest contrast
    text_color = (0,0,0)
    background_color = (0,0,0)
    assert accessibility_tester.get_contrast_ratio(text_color, background_color) == 1

    # black text on red background
    text_color = (0,0,0)
    background_color = (255,0,0)
    assert accessibility_tester.get_contrast_ratio(text_color, background_color) == 5.252


class ColorContrastTestServer(BaseHTTPRequestHandler):
    def do_get(self):
        if self.path == "/color-contrast-test-case-1":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><body><div><p>Some Text</p></div></body></html>", "utf-8"))

        if self.path == "/color-contrast-test-case-2":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><body><div style='background-color: red'><p style='color: black'>Some Text</p></div></body></html>", "utf-8"))

        if self.path == "/color-contrast-test-case-3":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><body><div style='background-color: #666666'><p style='color: #000000'>Some Text</p></div></body></html>", "utf-8"))

        if self.path == "/color-contrast-test-case-4":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><body><div style='background-color: #666666'><p style='color: #000000; font-size: 18px'>Some Text</p></div></body></html>", "utf-8"))

        if self.path == "/color-contrast-test-case-5":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><body><div style='background-color: #666666'><p style='color: #000000; font-size: 14px; font-weight: bold'>Some Text</p></div></body></html>", "utf-8"))

        if self.path == "/color-contrast-test-case-6":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><body><div style='background-color: #666666'><p style='color: #000000; font-size: 14px'><strong>Some Text</strong></p></div></body></html>", "utf-8"))

        if self.path == "/color-contrast-test-case-7":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><body><div style='background-color: #666666'><p style='color: #000000; font-size: 14px'>Some Text</p></div></body></html>", "utf-8"))

        if self.path == "/color-contrast-test-case-8":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><body><div style='background-color: rgb(40, 40, 40)'><p style='color: rgba(240, 240, 240, 0); font-size: 14px'>Some Text</p></div></body></html>", "utf-8"))

def start_server(web_server):
    print("Server started http://%s:%s" % (HOST_NAME, SERVER_PORT))
    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass
