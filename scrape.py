import requests
from bs4 import BeautifulSoup
import unidecode
import os


# TODO Description
def construct_url(piece):
    user_keywords = "best recording " + piece
    user_keywords = user_keywords.replace(" ", "+")
    return "https://www.google.com/search?q=" + user_keywords


# TODO Description
def http_requests(url):
    # get rid of any special characters that might appear in the link
    http_response = requests.get(url)
    if http_response.status_code == 200:
        return http_response
    else:
        return "Try a different URL"


# TODO Description
def parse_google_search(http_response):
    soup = BeautifulSoup(http_response.text, 'html.parser')

    # parse the html code that the http request returns by first finding all a tags
    a_tags = soup.findAll('a')

    # put all of the actual URL results in an array
    search_results = []
    for value in a_tags:
        url_string = value.get("href")
        if "url" in url_string:
            # get rid of the first 7 characters of the string and get rid of any unnecessary search queries after "&"
            url_string_clean = url_string[7:]
            index = url_string_clean.index("&")
            url_string_clean = url_string_clean[:index]

            # make sure the search result does not include a youtube link or a google sign up/sign in
            if "youtube" not in url_string_clean and "google" not in url_string_clean and \
                    "amazon" not in url_string_clean and "prestomusic" not in url_string_clean:
                search_results.append(url_string_clean)

    return search_results


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
def gramophone_clean(text):
    # for Deutsche Gramophon Remove everything after the Follow us text.
    text, sep, tail = text.partition('Follow us')
    head, sep, text = text.partition('No 1')
    text = text.replace("\n \n", "\n\n")
    return sep + text


# TODO Description
def talk_classical_clean(text):
    strip_arr = ["View Profile", "View Forum Posts", "View Blog Entries", "Reply With Quote", "Senior Member",
                 "Junior Member", "Banned", "Visit Homepage"]
    # start after the first forum entry
    head, sep, text = text.partition("#1")
    text, sep, tail = text.partition("Jump to page:")

    for item in strip_arr:
        text = text.replace(item, "")

    text_arr = text.split("Join Date")
    new_text_arr = []
    for item in text_arr:
        item = item.replace('\n', '').replace('\t', ' ').replace('\r', ' ').strip()
        items = item.split("Likes (Received)")
        [new_text_arr.append(i) for i in items]

    # also split by if the string has a date in it.
    wo_date_arr = []
    for item in new_text_arr:
        if "Dec" in item:
            item_parts = item.split("Dec")
            wo_date_arr.append(item_parts[0])
        elif "Jan" in item:
            item_parts = item.split("Jan")
            wo_date_arr.append(item_parts[0])
        elif "Feb" in item:
            item_parts = item.split("Feb")
            wo_date_arr.append(item_parts[0])
        elif "Mar" in item:
            item_parts = item.split("Mar")
            wo_date_arr.append(item_parts[0])
        elif "Apr" in item:
            item_parts = item.split("Apr")
            wo_date_arr.append(item_parts[0])
        elif "May" in item:
            item_parts = item.split("May")
            wo_date_arr.append(item_parts[0])
        elif "Jun" in item:
            item_parts = item.split("Jun")
            wo_date_arr.append(item_parts[0])
        elif "Jul" in item:
            item_parts = item.split("Jul")
            wo_date_arr.append(item_parts[0])
        elif "Aug" in item:
            item_parts = item.split("Aug")
            wo_date_arr.append(item_parts[0])
        elif "Sep" in item:
            item_parts = item.split("Sep")
            wo_date_arr.append(item_parts[0])
        elif "Oct" in item:
            item_parts = item.split("Oct")
            wo_date_arr.append(item_parts[0])
        elif "Nov" in item:
            item_parts = item.split("Nov")
            wo_date_arr.append(item_parts[0])

    final_arr = []
    [final_arr.append(item) for item in wo_date_arr if "Likes (Given)" not in item]

    # after we are done with getting rid of the unnecessary values, join the text delimited by \ns
    text = "\n".join(final_arr)
    return text


# TODO Description
def nyt_clean(text):
    strip_arr = ["Share This Page", "Continue reading the main story", "Advertisement", "Credit", "Associated Press",
                 "Photo" "Opt out or contact us anytime"]
    head, sep, text = text.partition("Continue reading the main story")

    # get rid of subscription popup
    head, sep, tail = text.partition("Newsletter")
    head2, sep, tail2 = tail.partition("Opt out or contact us anytime")
    text = head + tail2

    for item in strip_arr:
        text = text.replace(item, "")

    # get rid of the parts that are not the main article
    head, sep, tail = text.partition("Subscribe")
    text = head
    text = text.strip()
    return text


# TODO Description
def wfmt_clean(text):
    head, sep, text = text.partition("Share this Post")
    text, sep, tail = text.partition("Related Posts")
    text = text.strip()
    return text


# TODO Description
def quora_clean(text):
    text_arr = text.split("views")
    final_arr = []
    [final_arr.append(item) for item in text_arr if "Related Questions" not in item and "Upvoters" not in item]
    text = "\n\n".join(final_arr)
    return text


# TODO Description
def classicfm_clean(text):
    head, sep, text = text.partition("More Composers")
    text, sep, tail = text.partition("News")
    text = text.strip()
    return text


# TODO Description
def spectator_clean(text):
    head, sep, text = text.partition("Whatsapp")
    text, sep, tail = text.partition("See also")
    text = text.strip()
    return text


# TODO Description
def classical_music_clean(text):
    head, sep, text = text.partition("Rating:")
    text, sep, tail = text.partition("Article Type")
    text = text.strip()
    return text


# TODO Description
def look_for_piece(text, piece):
    piece_separate = piece.split(" ")
    for item in piece_separate:
        if item in text.lower():
            continue
        else:
            return False
    return True


# TODO Description
def write_to_file(piece, results):
    file_name = piece.replace(' ', "_") + ".txt"
    f = open(file_name, "a")
    # in case there is already data in the file, we want to get rid of it before overwriting the most recent data
    f.truncate(0)
    f.write(results)
    f.close()


# TODO Description
def make_directory(piece):
    dir_name = piece.replace(' ', "_")
    try:
        os.mkdir(dir_name)
        os.chdir(dir_name)
    except FileExistsError:
        os.chdir(dir_name)
        return


# TODO Add Description
def scrape_main(piece_name):
    # construct the google search url
    google_search_url = construct_url(piece_name)
    response = http_requests(google_search_url)
    # parse the google search results and return a list of urls in the order in which they are displayed
    url_results = parse_google_search(response)
    # for each google search result get the response, and clean the text
    count = 1
    # make a directory for all of the files that will have data pulled from the web
    make_directory(piece_name)

    for url_result in url_results:
        search_response = http_requests(url_result)
        if type(search_response) != str:
            clean_text = clean_html_text(search_response)

            if "gramophone" in url_result:
                clean_text = gramophone_clean(clean_text)
            elif "talkclassical" in url_result:
                clean_text = talk_classical_clean(clean_text)
            elif "nytimes" in url_result:
                clean_text = nyt_clean(clean_text)
            elif "wfmt" in url_result:
                clean_text = wfmt_clean(clean_text)
            elif "quora" in url_result:
                clean_text = quora_clean(clean_text)
            elif "classicfm" in url_result:
                clean_text = classicfm_clean(clean_text)
            elif "spectator" in url_result:
                clean_text = spectator_clean(clean_text)
            elif "classical-music" in url_result:
                clean_text = classical_music_clean(clean_text)
            else:
                continue

            # if the article actually includes the piece that the user is searching for
            if look_for_piece(clean_text, piece_name):
                write_to_file(piece_name + "_" + str(count), str(clean_text))
                count += 1

    # move back up to the parent directory
    os.chdir('..')




