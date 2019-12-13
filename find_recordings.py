import make_database
import scrape
import os


def make_dict(performers):
    return dict.fromkeys(performers, 0)


def count_performers(data_arr, performers, piece, performer_freq):
    for item in data_arr:
        # if the piece is in that particular paragraph, then look for performers mentioned
        if scrape.look_for_piece(item, piece):
            for performer in performers:
                if performer in item:
                    performer_freq[performer] += 1

    return performer_freq


def make_ranking(dictionary):
    dictionary = {k: v for k, v in dictionary.items() if v != 0}
    sorted_arr = sorted(dictionary, key=dictionary.get, reverse=True)
    return sorted_arr


def find_main(piece):
    performer_list, performer_last_list, label_list, ensemble_list = make_database.get_strings()

    dir_name = piece.replace(' ', "_")
    # scrape data, add it inside directory as text files
    scrape.scrape_main(piece)

    os.chdir(dir_name)
    performer_freq = make_dict(performer_list)
    # open each file into a string and start processing
    for filename in os.listdir(os.getcwd()):
        with open(filename, 'r') as file:
            data = file.read()
            # split each file into paragraphs
            data_split = data.split("\n\n")
            performer_freq = count_performers(
                data_split, performer_list, piece, performer_freq)

    sorted = make_ranking(performer_freq)
    # move back up to the parent directory
    os.chdir("..")
    return sorted
