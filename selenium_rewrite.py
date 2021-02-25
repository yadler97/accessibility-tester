from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
import validators
import urllib.parse
import time

class VAT:
    def __init__(self, url):
        options = Options()
        options.headless = True

        self.driver = webdriver.Chrome(options=options)
        self.driver.set_window_size(1120, 550)
        self.driver.get(url)
        self.page = BeautifulSoup(self.driver.page_source, "html.parser")

        #self.link_list = []

        #link_elements = self.page.find_all("a")
        #for link_element in link_elements:
        #    if "href" in link_element.attrs and not link_element['href'] == "":
        #        joined_url = urllib.parse.urljoin(url, link_element['href'])
        #        if joined_url not in self.link_list:
        #            self.link_list.append(joined_url)

        self.link_list = self.driver.find_elements_by_tag_name("a")

    def test_subpages(self):
        for i in range(len(self.link_list)):
            self.driver.execute_script("elements = document.getElementsByTagName('a'); for (var element of elements) {element.setAttribute('target', '')}")
            link = self.driver.find_elements_by_tag_name("a")[i]
            link.click()
            #self.driver.get_screenshot_as_file(str(i) + ".png")
            self.page = BeautifulSoup(self.driver.page_source, "html.parser")
            print("\n" + self.driver.current_url + "\n---------------------")
            self.check_doc_language()
            self.check_alt_texts()
            self.check_input_labels()
            self.check_buttons()
            self.driver.back()

    # 3.1.1 H57
    # Missing document language
    def check_doc_language(self):
        #divs = self.driver.find_elements_by_tag_name("p")
        #for div in divs:
        #    print(div, div.value_of_css_property('background-color'))
        
        # check if language attribute exists and is not empty
        lang_attr = self.page.find("html").get_attribute_list("lang")[0]
        if not lang_attr == None:
            print("Document language is set")
            return {"category":"doc_language","correct":1,"false":0}
        else:
            print("Document language is missing")
            return {"category":"doc_language","correct":0,"false":1}

    # 1.1.1 H37
    # Missing alternative text
    def check_alt_texts(self):
        correct = 0
        false = 0
        # get all img elements
        img_elements = self.page.find_all("img")
        for img_element in img_elements:
            # check if img element has an alternative text that is not empty
            alt_text = img_element.get_attribute_list('alt')[0]
            if not alt_text == None:
                print("Alt text is correct")
                correct += 1
            else:
                print("Alt text is missing")
                false += 1
        
        return {"category":"alt_texts","correct":correct,"false":false}

    # 1.3.1 H44 & ARIA16
    # Missing form label
    def check_input_labels(self):
        correct = 0
        false = 0
        # get all input and label elements
        input_elements = self.page.find_all("input")
        label_elements = self.page.find_all("label")
        for input_element in input_elements:
            # exclude input element of type hidden, submit, reset and button
            if "type" in input_element.attrs and not input_element['type'] == "hidden" and not input_element['type'] == "submit" and not input_element['type'] == "reset" and not input_element['type'] == "button":
                # check if input is of type image and has a alt text that is not empty
                if input_element['type'] == "image" and "alt" in input_element.attrs and not input_element['alt'] == "":
                    print("Input of type image labelled with alt text")
                    correct += 1
                # check if input element uses aria-labelledby
                elif "aria-labelledby" in input_element.attrs and not input_element['aria-labelledby'] == "":
                    print("Input labelled with aria-labelledby attribute")
                    correct += 1
                else:
                    # check if input element has a corresponding label element
                    label_correct = False
                    for label_element in label_elements:
                        # check if "for" attribute of label element is identical to "id" of input element
                        if "for" in label_element.attrs and "id" in input_element.attrs and label_element['for'] == input_element['id']:
                            label_correct = True
                    if label_correct == True:
                        print("Input labelled with label element")
                        correct += 1
                    else:
                        print("Input not labelled at all")
                        false += 1

        return {"category":"input_labels","correct":correct,"false":false}

    # 1.1.1 & 2.4.4
    # Empty button
    def check_buttons(self):
        correct = 0
        false = 0
        # get all buttons and input elements of the types submit, button and reset
        input_elements = self.page.find_all("input", type=["submit", "button", "reset"])
        button_elements = self.page.find_all("button")

        for input_element in input_elements:
            # check if input element has a value attribute that is not empty
            if "value" in input_element.attrs and not input_element['value'] == "":
                print("Button has content")
                correct += 1
            else:
                print("Button is empty")
                false += 1

        for button_element in button_elements:
            # check if the button has content or a title
            texts = button_element.findAll(text=True)
            if not texts == [] or ("title" in button_element.attrs and not button_element["title"] == ""):
                print("Button has content")
                correct += 1
            else:
                print("Button is empty")
                false += 1

        return {"category":"empty_buttons","correct":correct,"false":false}

def main():
    url = sys.argv[1]
    required_degree = float(sys.argv[2])

    if not validators.url(url):
        print("ERROR: Invalid URL")
        exit(1)

    if not 0 <= required_degree <= 1:
        print("ERROR: Accessibility level must be between 0 and 1")
        exit(1)

    vat = VAT(url)

    vat.check_doc_language()
    vat.check_alt_texts()
    vat.check_input_labels()
    vat.check_buttons()

    vat.test_subpages()

    vat.driver.quit()

if __name__ == "__main__":
    main()