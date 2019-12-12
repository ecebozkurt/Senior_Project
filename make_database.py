import requests
from bs4 import BeautifulSoup
import re
import unidecode


# TODO Description
def clean_html_text(http_response):
    soup = BeautifulSoup(http_response.text, 'html.parser')
    # get rid of Javascript and CSS elements
    [script.extract() for script in soup(['script', 'style'])]
    text = soup.get_text()
    # get rid of special accents for easier search
    normal = unidecode.unidecode(text)
    return normal


# TODO Description
def get_data(url, type_list):
    http_response = requests.get(url)
    list_str = clean_html_text(http_response)
    head, sep, list_str = list_str.partition("Most Popular " + type_list)
    head, sep, list_str = list_str.partition("Most Popular " + type_list)
    list_str, sep, tail = list_str.partition("ArkivMusic")

    # get rid of the values inside parantheses
    list_str = list_str.replace("\t", '')
    list_str = re.sub(r'\(.+\)', '', list_str)
    list_str = list_str.strip()
    return list_str


# TODO Description
def separate_last_name(list_str):
    # get their last names for easier search
    list_str_last = re.sub(r',.+\n', '', list_str)
    return list_str, list_str_last


# TODO Description
def make_list(string):
    str_list = string.split("\n")
    new_str_list = []
    for item in str_list:
        item = item.strip()
        if item != ' ' and item != '':
            new_str_list.append(item)
    return new_str_list


# TODO Description
def switch_last_first(name_list):
    fl = [" ".join(n.split(", ")[::-1]) for n in name_list]
    return fl


# TODO Description
def get_strings():
    conductor_str = get_data("https://www.arkivmusic.com/classical/NameList?featured=1&role_wanted=3", "Conductors")
    label_str = get_data("https://www.arkivmusic.com/classical/MusicList?featured=1&role_wanted=6", "Labels")
    performer_str = get_data("https://www.arkivmusic.com/classical/NameList?featured=1&role_wanted=2", "Performers")
    ensemble_str = get_data("https://www.arkivmusic.com/classical/NameList?featured=1&role_wanted=4", "Ensembles")

    performer_str += conductor_str
    performer_str, performer_str_last = separate_last_name(performer_str)

    performer_list = switch_last_first(make_list(performer_str))
    performer_last_list = make_list(performer_str_last)

    label_list = make_list(label_str)
    ensemble_list = make_list(ensemble_str)

    return performer_list, performer_last_list, label_list, ensemble_list







