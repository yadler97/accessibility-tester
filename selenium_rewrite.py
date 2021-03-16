from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import sys
import validators
import urllib.parse
import time
import os

class VAT:
    def __init__(self, url, required_degree):
        options = Options()
        options.headless = True

        self.url = url
        self.required_degree = required_degree
        self.driver = webdriver.Chrome(options=options)
        self.driver.set_window_size(1980, 1080)
        self.driver.get(url)
        self.page = BeautifulSoup(self.driver.page_source, "html.parser")
        self.correct = {"doc_language":0, "alt_texts":0, "input_labels":0, "empty_buttons":0, "empty_links":0}
        self.wrong = {"doc_language":0, "alt_texts":0, "input_labels":0, "empty_buttons":0, "empty_links":0}

        #self.link_list = []

        #link_elements = self.page.find_all("a")
        #for link_element in link_elements:
        #    if "href" in link_element.attrs and not link_element['href'] == "":
        #        joined_url = urllib.parse.urljoin(url, link_element['href'])
        #        if joined_url not in self.link_list:
        #            self.link_list.append(joined_url)

        self.visited_links = []

    def test_subpages(self):
        self.page = BeautifulSoup(self.driver.page_source, "html.parser")
        print("\n" + self.driver.current_url + "\n---------------------")
        self.check_doc_language()
        self.check_alt_texts()
        self.check_input_labels()
        self.check_buttons()
        self.check_links()

        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.driver.get_screenshot_as_file(dir_path + "/screenshots/" + str(time.time()) + ".png")

        self.visited_links.append(self.driver.current_url)

        link_list = self.driver.find_elements_by_tag_name("a")
        for i in range(len(link_list)):
            self.driver.execute_script("elements = document.getElementsByTagName('a'); for (var element of elements) {element.setAttribute('target', '')}")
            link = self.driver.find_elements_by_tag_name("a")[i]
            if not link.is_displayed() or link.get_attribute("href") == "" or link.get_attribute("href") == None or str(urllib.parse.urljoin(self.url, link.get_attribute("href"))) == self.driver.current_url:
                continue
            self.driver.execute_script("arguments[0].style.height = '10px'; arguments[0].style.width = '10px';", link)
            link.click()
            if self.driver.current_url in self.visited_links or not self.url in self.driver.current_url:
                self.driver.back()
                continue

            self.test_subpages()

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
            self.correct["doc_language"] += 1
        else:
            print("Document language is missing")
            self.wrong["doc_language"] += 1

    # 1.1.1 H37
    # Missing alternative text
    def check_alt_texts(self):
        # get all img elements
        img_elements = self.page.find_all("img")
        for img_element in img_elements:
            # check if img element has an alternative text that is not empty
            alt_text = img_element.get_attribute_list('alt')[0]
            if not alt_text == None:
                print("Alt text is correct")
                self.correct["alt_texts"] += 1
            else:
                print("Alt text is missing")
                self.wrong["alt_texts"] += 1

    # 1.3.1 H44 & ARIA16
    # Missing form label
    def check_input_labels(self):
        # get all input and label elements
        input_elements = self.page.find_all("input")
        label_elements = self.page.find_all("label")
        for input_element in input_elements:
            # exclude input element of type hidden, submit, reset and button
            if "type" in input_element.attrs and not input_element['type'] == "hidden" and not input_element['type'] == "submit" and not input_element['type'] == "reset" and not input_element['type'] == "button":
                # check if input is of type image and has a alt text that is not empty
                if input_element['type'] == "image" and "alt" in input_element.attrs and not input_element['alt'] == "":
                    print("Input of type image labelled with alt text")
                    self.correct["input_labels"] += 1
                # check if input element uses aria-labelledby
                elif "aria-labelledby" in input_element.attrs and not input_element['aria-labelledby'] == "":
                    print("Input labelled with aria-labelledby attribute")
                    self.correct["input_labels"] += 1
                else:
                    # check if input element has a corresponding label element
                    label_correct = False
                    for label_element in label_elements:
                        # check if "for" attribute of label element is identical to "id" of input element
                        if "for" in label_element.attrs and "id" in input_element.attrs and label_element['for'] == input_element['id']:
                            label_correct = True
                    if label_correct == True:
                        print("Input labelled with label element")
                        self.correct["input_labels"] += 1
                    else:
                        print("Input not labelled at all")
                        self.wrong["input_labels"] += 1

    # 1.1.1 & 2.4.4
    # Empty button
    def check_buttons(self):
        # get all buttons and input elements of the types submit, button and reset
        input_elements = self.page.find_all("input", type=["submit", "button", "reset"])
        button_elements = self.page.find_all("button")

        for input_element in input_elements:
            # check if input element has a value attribute that is not empty
            if "value" in input_element.attrs and not input_element['value'] == "":
                print("Button has content")
                self.correct["empty_buttons"] += 1
            else:
                print("Button is empty")
                self.wrong["empty_buttons"] += 1

        for button_element in button_elements:
            # check if the button has content or a title
            texts = button_element.findAll(text=True)
            if not texts == [] or ("title" in button_element.attrs and not button_element["title"] == ""):
                print("Button has content")
                self.correct["empty_buttons"] += 1
            else:
                print("Button is empty")
                self.wrong["empty_buttons"] += 1

    # 2.4.4 G91 & H30
    # Empty link
    def check_links(self):
        # get all a elements
        link_elements = self.page.find_all("a")
        for link_element in link_elements:
            # check if link has content
            texts_in_link_element = link_element.findAll(text=True)
            img_elements = link_element.findChildren("img" , recursive=False)
            all_alt_texts_set = True
            for img_element in img_elements:
                alt_text = img_element.get_attribute_list('alt')[0]
                if alt_text == None:
                    all_alt_texts_set = False
            if not texts_in_link_element == [] or (not img_elements == [] and all_alt_texts_set):
                print("Link has content")
                self.correct["empty_links"] += 1
            else:
                print("Link is empty")
                self.wrong["empty_links"] += 1

    def calculate_result(self):
        # calculate correct and false implementations
        correct = sum(self.correct.values())
        false = sum(self.wrong.values())
        print("\nResult")
        print("---------------------")
        print("Correct:", correct)
        for category in self.correct:
            print(" ", category + ":", self.correct[category])
        print("Errors:", false)
        for category in self.wrong:
            print(" ", category + ":", self.wrong[category])
        print("Ratio (correct to total):", round(correct/(correct+false), 2), "\n")

        # check if ratio correct/total reaches wanted minimum value
        if correct/(correct+false) >= self.required_degree:
            print("Accessibility test successful - can deploy")
        else:
            sys.tracebacklimit = 0
            raise Exception("Too many accessibility errors - try fix them!")

def main():
    url = sys.argv[1]
    required_degree = float(sys.argv[2])

    if not validators.url(url):
        raise Exception("Invalid URL")

    if not 0 <= required_degree <= 1:
        raise Exception("Accessibility level must be between 0 and 1")

    vat = VAT(url, required_degree)

    vat.test_subpages()

    vat.driver.quit()

    vat.calculate_result()

if __name__ == "__main__":
    main()