[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3101/)

# Visual Accessibility Tester

A Python script to test a web page for six testing criteria regarding visual accessibility. The criteria are based on a report from WebAIM and are implemented by following the Web Content Accessibility Guidelines 2.1 (WCAG 2.1).

## Testing Criteria

1. Low contrast text
2. Missing alternative texts for images
3. Empty links
4. Missing form input labels
5. Empty buttons
6. Missing document language

## How to run

First, you need ChromeDriver:

    https://chromedriver.chromium.org/ (Make sure that the selected ChromeDriver version matches your current Chrome version)

The path to your chromedriver.exe must be in your PATH.

\
Then, install all dependencies with pip:

    pip install -r requirements.txt
\
A test for a specific web page can then be executed with the following command:

    python vat.py <url> <required accessibility level>

The required accessibility level is a value between 0 and 1. It is compared with the actual accessibility level that is achieved in the test, which is calculated by dividing the successful checks through the total number of executed checks. If the achieved accessibility level is equal to or higher than the required accessibility level, the program will return an exit code of 0, otherwise an exit code of 1 will be returned.
