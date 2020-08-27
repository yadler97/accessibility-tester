import requests
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super(MyHTMLParser, self).__init__()
        self.lang_attribute = ""
        self.img_alt_missing = 0
        self.img_alt_empty = 0
        self.img_alt_correct = 0

    def handle_starttag(self, tag, attrs):
        if tag == "html":
            if 'lang' in dict(attrs):
                if not dict(attrs)['lang'] == "":
                    self.lang_attribute = "exists"
                else:
                    self.lang_attribute = "is empty"
            else:
                self.lang_attribute = "is missing"

        if tag == "img":
            #print("Encountered a start tag:", tag, "included attrs", attrs)
            if 'alt' in dict(attrs):
                if not dict(attrs)['alt'] == "":
                    self.img_alt_correct += 1
                else:
                    self.img_alt_empty += 1
            else:
                self.img_alt_missing += 1

    #def handle_endtag(self, tag):
        #print("Encountered an end tag :", tag)

    #def handle_data(self, data):
        #print("Encountered some data  :", data)

page_content = requests.get("https://www.telekom.de/").content
parser = MyHTMLParser()
parser.feed(str(page_content))
print("Result")
print("------------------------------------")
print("* Lang Attribute")
print(parser.lang_attribute)
print("* Alt Tags")
print("Correct Alt Tags:", parser.img_alt_correct)
print("Empty Alt Tags:  ", parser.img_alt_empty)
print("Missing Alt Tags:", parser.img_alt_missing)

def convert_rgb_8bit_value(single_rgb_8bit_value):
    srgb = single_rgb_8bit_value / 255
    if srgb <= 0.03928:
        return srgb / 12.92
    else:
        return ((srgb + 0.055) / 1.055) ** 2.4

def check_contrast(r_1_8bit, g_1_8bit, b_1_8bit, r_2_8bit, g_2_8bit, b_2_8bit):
    r_1 = convert_rgb_8bit_value(r_1_8bit)
    g_1 = convert_rgb_8bit_value(g_1_8bit)
    b_1 = convert_rgb_8bit_value(b_1_8bit)
    r_2 = convert_rgb_8bit_value(r_2_8bit)
    g_2 = convert_rgb_8bit_value(g_2_8bit)
    b_2 = convert_rgb_8bit_value(b_2_8bit)

    l_1 = 0.2126 * r_1 + 0.7152 * g_1 + 0.0722 * b_1
    l_2 = 0.2126 * r_2 + 0.7152 * g_2 + 0.0722 * b_2

    contrast_ratio = (l_1 + 0.05) / (l_2 + 0.05)

    return contrast_ratio