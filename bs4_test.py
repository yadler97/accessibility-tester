from bs4 import BeautifulSoup
import requests
import cssutils
url = "https://www.telekom.de"
req = requests.get(url)
soup = BeautifulSoup(req.text, "html.parser")
#print(soup.title)

stylesheets = []

def get_stylesheets():
    for styletag in soup.findAll('style'):
        stylesheets.append(cssutils.parseString(styletag.string))

    for linktag in soup.findAll('link', rel='stylesheet'):
        if linktag['href'].startswith("/"):
            cssreq = requests.get(url + linktag['href'])
        else:
            cssreq = requests.get(linktag['href'])
        stylesheets.append(cssutils.parseString(cssreq.content))

# 3.1.1 H57
def check_lang_attribute():
    lang_attribute = soup.find("html").get_attribute_list("lang")[0]
    if not lang_attribute == None:
        print("Lang attribute is correct")
    else:
        print("Lang attribute is missing")

# 1.1.1 H37
def check_alt_texts():
    img_tags = soup.find_all("img")
    for img in img_tags:
        alt_text = img.get_attribute_list('alt')[0]
        if not alt_text == None:
            print("Alt text is correct")
        else:
            print("Alt text is missing")

# 1.3.1 H44
def check_input_label():
    return False

# 1.4.3 G18 & G145 (& 148)
def check_color_contrast():
    return False

get_stylesheets()
#check_lang_attribute()
#check_alt_texts()

#for link in soup.find_all('a'):
#    print(link.get('href'))

#def get_rule(sheet, rule_name):
#    for rule in sheet:
#        if rule.type == rule.STYLE_RULE and rule_name in rule.selectorText:
#            return rule
#
#css = u'''/* a comment with umlaut &auml; */
#     @namespace html "http://www.w3.org/1999/xhtml";
#     @variables { BG: #fff }
#     html|a { color:red; background: var(BG) }'''
#sheet = cssutils.parseString(css)
#
#for rule in sheet:
#    print(get_rule(sheet, "bla").style.color)
#    if rule.type == rule.STYLE_RULE:
#        print(rule.selectorText)