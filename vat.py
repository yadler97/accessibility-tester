from bs4 import BeautifulSoup, Comment, Doctype
from urllib.parse import urlparse
import webcolors
import requests
import cssutils
import logging
import sys
cssutils.log.setLevel(logging.FATAL)

stylesheets = []

# set default colors for text, background and buttons that are usually used by the browser
DEFAULT_TEXT_COLOR = "#000000"
DEFAULT_BACKGROUND_COLOR = "#FFFFFF"
DEFAULT_BUTTON_COLOR = "#EFEFEF"

# 3.1.1 H57
# Missing document language
def check_doc_language():
    # check if language attribute exists and is not empty
    lang_attr = soup.find("html").get_attribute_list("lang")[0]
    if not lang_attr == None:
        print("Document language is set")
        return {"category":"doc_language","correct":1,"false":0}
    else:
        print("Document language is missing")
        return {"category":"doc_language","correct":0,"false":1}

# 1.1.1 H37
# Missing alternative text
def check_alt_texts():
    correct = 0
    false = 0
    # get all img elements
    img_elements = soup.find_all("img")
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
def check_input_labels():
    correct = 0
    false = 0
    # get all input and label elements
    input_elements = soup.find_all("input")
    label_elements = soup.find_all("label")
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

# 1.4.3 G18 & G145 (& 148)
# Low contrast
def check_color_contrast():
    correct = 0
    false = 0
    # exclude script, style, title and empty elements as well as doctype and comments
    texts_on_page = extract_texts()
    input_elements = soup.find_all("input")
    elements_with_text = texts_on_page + input_elements
    for text in elements_with_text:
        # exclude invisible texts
        element_visible = get_css_attribute_value(text, "display")
        if not element_visible == "none" and (not text.name == "input" or (text.name == "input" and "type" in text.attrs and not text['type'] == "hidden")):
            text_color = get_text_color(get_css_attribute_value(text, "color"), text)
            background_color = get_background_color(get_background_color_attribute(text), text)

            print(text.name, text_color, background_color)

            # calculate contrast between text color and background color
            contrast = get_contrast_ratio(text_color, background_color)

            # get font size and font weight
            font_size = get_css_attribute_value(text, "font-size")
            font_weight = get_css_attribute_value(text, "font-weight")

            
            if not font_size == None and font_size.__contains__("px") and \
                (int(''.join(filter(str.isdigit, font_size))) >= 18 or ((font_weight == "bold" or font_weight == "bolder" or text.name == "strong") and int(''.join(filter(str.isdigit, font_size))) >= 14)):
                if contrast >= 3:
                    print("Contrast meets minimum requirements")
                    correct += 1
                else:
                    print("Contrast does not meet minimum requirements")
                    false += 1
            else:
                if contrast >= 4.5:
                    print("Contrast meets minimum requirements")
                    correct += 1
                else:
                    print("Contrast does not meet minimum requirements")
                    false += 1

    return {"category":"color_contrast","correct":correct,"false":false}

# 1.1.1 & 2.4.4
# Empty button
def check_buttons():
    correct = 0
    false = 0
    # get all buttons and input elements of the types submit, button and reset
    input_elements = soup.find_all("input", type=["submit", "button", "reset"])
    button_elements = soup.find_all("button")

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

# 2.4.4 G91 & H30
# Empty link
def check_links():
    correct = 0
    false = 0
    # get all a elements
    link_elements = soup.find_all("a")
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
            correct += 1
        else:
            print("Link is empty")
            false += 1

    return {"category":"empty_links","correct":correct,"false":false}

def get_stylesheets():
    # collect styles in style elements
    for styletag in soup.findAll('style'):
        if not styletag.string == None:
            stylesheets.append(cssutils.parseString(styletag.string))

    # collect styles in stylesheets
    for linktag in soup.findAll('link', rel='stylesheet'):
        if linktag['href'].startswith("/") or not linktag['href'].split("/")[0].__contains__(":"):
            if not urlparse(url).path == "/":
                cssreq = requests.get(url.replace(urlparse(url).path, "") + linktag['href'])
            else:
                cssreq = requests.get(url + linktag['href'])
        else:
            cssreq = requests.get(linktag['href'])
        stylesheets.append(cssutils.parseString(cssreq.content))

def get_rules(css_list):
    rules = []
    for sheet in stylesheets:
        for rule in sheet:
            if rule.type == rule.STYLE_RULE:
                for single_rule in rule.selectorText.split(","):
                    starting_rule = True
                    iterable_css_list = css_list[:]
                    iterable_single_rule = single_rule.split(" ")
                    is_correct_full = True
                    for single_rule_part in reversed(iterable_single_rule):
                        is_correct = False
                        for css_list_rule in iterable_css_list:
                            if single_rule_part in ["." + class_name for class_name in css_list_rule[1]] or single_rule_part == css_list_rule[0] or single_rule_part == "#" + css_list_rule[2] or single_rule_part in [css_list_rule[0] + "." + class_name for class_name in css_list_rule[1]] or single_rule_part == "*":
                                is_correct = True
                                starting_rule = False
                                del iterable_css_list[0]
                                break
                            elif starting_rule:
                                break
                            if not len(iterable_single_rule) == 0:
                                del iterable_single_rule[0]
                        if not is_correct:
                            is_correct_full = False
                            break
                    if is_correct_full:
                        rule_to_be_added = rule
                        rule_to_be_added.selectorText = single_rule
                        rules.append(rule_to_be_added)

    rules.sort(reverse=True, key=get_specificity)
    return rules

def get_specificity(rule):
    # get the CSS specificity of a certain rule
    specificity = rule.selectorList[0].specificity
    return specificity[0] * 1000 + specificity[1] * 100 + specificity[2] * 10 + specificity[3]

def extract_texts():
    soup2 = soup

    # remove script, style and title elements
    for invisible_element in soup2(["script", "style", "title"]):
        invisible_element.extract()

    # remove comments
    comments = soup2.findAll(text=lambda text:isinstance(text, Comment))
    for comment in comments:
        comment.extract()

    # remove doctype
    doctype = soup2.find(text=lambda text:isinstance(text, Doctype))
    if not doctype == None:
        doctype.extract()

    # get all elements with text
    texts = []
    texts_on_page = soup2.findAll(text=True)
    for text in texts_on_page:
        if not text.strip() == "" and not text == "\n":
            texts.append(text.parent)

    return texts

def get_text_color(text_color, text):
    # cover special cases like initial and inherit
    if text_color == "initial":
        return convert_color(DEFAULT_TEXT_COLOR)
    elif text_color == "inherit" or text_color == "transparent" or text_color == None:
        return convert_color(get_text_color(get_text_color_attribute(text.parent), text.parent))
    elif not text_color == None:
        return convert_color(text_color)
    else:
        return convert_color(DEFAULT_TEXT_COLOR)

def get_background_color(background_color, text):
    # cover special cases like initial and inherit
    if background_color == "initial":
        return convert_color(DEFAULT_BACKGROUND_COLOR)
    elif background_color == "inherit" or background_color == "transparent" or background_color == None:
        return convert_color(get_background_color(get_background_color_attribute(text.parent), text.parent))
    elif not background_color == None:
        return convert_color(background_color)
    else:
        return convert_color(DEFAULT_BACKGROUND_COLOR)

def convert_color(color):
    # check the current format of the color value and convert it if in wrong format
    if type(color) is tuple:
        return color
    if str(color).startswith("rgba"):
        color = eval(color[4:])
        return (color[0], color[1], color[2])
    if str(color).startswith("#"):
        return webcolors.hex_to_rgb(color)
    if str(color).startswith("IntegerRGB"):
        return color
    else:
        return webcolors.name_to_rgb(color, spec='css3')

def get_css_attribute_value(text, attribute):
    # inline styles have the highest specificity
    if "style" in text.attrs:
        sheet = cssutils.parseStyle(text['style'])
        if not sheet[attribute] == "":
            return sheet[attribute]

    # get path of element in DOM tree
    class_list = get_css_class_list(text)

    # get style rules applying for this path
    rules = get_rules(class_list)

    # get attribute value for rule with the highest specificity
    for rule in rules:
        if not rule.style[attribute] == "":
            return rule.style[attribute]
    
    return None

def get_background_color_attribute(text):
    # traverse tree until element with wanted attribute is found
    background_color = get_css_attribute_value(text, "background-color")
    if background_color == None:
        background_color = get_css_attribute_value(text, "background")
    if background_color == None and not text.name == "html" and not text.name == "input":
        background_color = get_background_color_attribute(text.parent)
    elif background_color == None and "type" in text.attrs and text["type"] == "submit" and text["type"] == "button" and text["type"] == "reset":
        return DEFAULT_BUTTON_COLOR
    elif background_color == None:
        return DEFAULT_BACKGROUND_COLOR
    if background_color.startswith("url"):
        background_color = get_background_color_attribute(text.parent)
    return background_color

def get_text_color_attribute(text):
    # traverse tree until element with wanted attribute is found
    text_color = get_css_attribute_value(text, "color")
    if text_color == None and not text.name == "html" and not text.name == "input":
        text_color = get_text_color_attribute(text.parent)
    elif text_color == None and "type" in text.attrs and text["type"] == "submit" and text["type"] == "button" and text["type"] == "reset":
        return DEFAULT_TEXT_COLOR
    elif text_color == None:
        return DEFAULT_TEXT_COLOR
    return text_color

def get_contrast_ratio(text_color, background_color):
    # preparing the RGB values
    r_1 = convert_rgb_8bit_value(text_color[0])
    g_1 = convert_rgb_8bit_value(text_color[1])
    b_1 = convert_rgb_8bit_value(text_color[2])
    r_2 = convert_rgb_8bit_value(background_color[0])
    g_2 = convert_rgb_8bit_value(background_color[1])
    b_2 = convert_rgb_8bit_value(background_color[2])

    # calculating the relative luminance
    l_1 = 0.2126 * r_1 + 0.7152 * g_1 + 0.0722 * b_1
    l_2 = 0.2126 * r_2 + 0.7152 * g_2 + 0.0722 * b_2

    # check if l_1 or l_2 is lighter
    if l_1 > l_2:
        # calculating contrast ration when l_1 is the relative luminance of the lighter colour
        contrast_ratio = (l_1 + 0.05) / (l_2 + 0.05)
    else:
        # calculating contrast ration when l_2 is the relative luminance of the lighter colour
        contrast_ratio = (l_2 + 0.05) / (l_1 + 0.05)

    return contrast_ratio

def convert_rgb_8bit_value(single_rgb_8bit_value):
    # dividing the 8-bit value through 255
    srgb = single_rgb_8bit_value / 255

    # check if the srgb value is lower than or equal to 0.03928
    if srgb <= 0.03928:
        return srgb / 12.92
    else:
        return ((srgb + 0.055) / 1.055) ** 2.4

def get_css_class_list(navigate_text):
    class_list = []
    # get DOM tree as list in list (element tag, class name, id)
    while (not navigate_text.name == "html"):
        if "class" in navigate_text.attrs and "id" in navigate_text.attrs:
            class_list.append([navigate_text.name, navigate_text['class'], navigate_text['id']])
        elif "class" in navigate_text.attrs:
            class_list.append([navigate_text.name, navigate_text['class'], ""])
        elif "id" in navigate_text.attrs:
            class_list.append([navigate_text.name, [], navigate_text['id']])
        else:
            class_list.append([navigate_text.name, [], ""])
        navigate_text = navigate_text.parent
    
    return class_list


try:
    url = sys.argv[1]
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    # check if given accessibility level has correct format
    if not 0 <= float(sys.argv[2]) <= 1:
        print("ERROR: Accessibility level must be between 0 and 1")
        exit(1)
except requests.exceptions.MissingSchema:
    # exit when URL is invalid
    print("ERROR: Invalid URL")
    exit(1)

def main():
    get_stylesheets()

    # execute the six tests
    result_color_contrast = check_color_contrast()
    result_input_labels = check_input_labels()
    result_doc_language = check_doc_language()
    result_alt_texts = check_alt_texts()
    result_empty_links = check_links()
    result_empty_buttons = check_buttons()

    result = {
        "categories":[
            result_color_contrast,
            result_input_labels,
            result_doc_language,
            result_alt_texts,
            result_empty_links,
            result_empty_buttons
        ]
    }

    # calculate correct and false implementations
    correct = sum(category['correct'] for category in result["categories"])
    false = sum(category['false'] for category in result["categories"])
    print("---------------------")
    print("Correct:", correct)
    for category in result["categories"]:
        print(" ", category['category'] + ":", category['correct'])
    print("Errors:", false)
    for category in result["categories"]:
        print(" ", category['category'] + ":", category['false'])
    print("Ratio (correct to total):", correct/(correct+false))

    # check if ratio correct/total reaches wanted minimum value
    if correct/(correct+false) >= float(sys.argv[2]):
        print("Accessibility test successful - can deploy")
    else:
        print("Too many accessibility errors - try fix them!")
        exit(1)

if __name__ == "__main__":
    main()