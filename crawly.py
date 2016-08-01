##################### HEAD #######################

import requests
from lxml import html

import sys
import csv
from operator import attrgetter

################### FUNCTIONS ####################


# This function prompts the keyord and returns it with - as encoding
def prompt(character):

    keyword = raw_input("Enter search query >>> ")
    keyword = keywords.strip().replace(" ", character) 

    return keyword


# This function fetches the website and returns an html object
def load_page(url):

    try:
        if "http://" not in url: url = "http://"+ url
        response = requests.get(url)
    except:
        print "[ERROR] Connection error."
        quit()

    try:
        response = html.fromstring(response.text)
    except:
        print "[ERROR] Parsing error."
        quit()

    return response


# This function prints listings
def pretty_print(objects, arguments):

    print "-" * 80

    for j in arguments:
        for i, listing in enumerate(data):
            i += 1
            print "[{:2}]".format(i), getattr(objects, j)
        print "-" * 80


# This function exports listings as csv file:
def export_csv(filename, objects, fields):

    if ".csv" not in filename: filename = filename + ".csv"
    row_headers = fields.keys()

    try :
        file = open(filename, "a")
        writer = csv.writer(file)
    except :
        file = open(filename, "w")
        write = csv.writer(file)
        writer.writerow(row_headers)

    for obj in objects:
        row = [attrgetter(fields[header])(obj) for header in row_headers]
        for count, column in enumerate(row):
            if callable(column):
                row[count] = column()
            if type(column) is unicode:
                row[count] = column.encode('utf8')
        writer.writerow(row)

#    for i, object in enumerate(objects):
#        for j in arguments:
#            i += 1
#            row = [str(i), getattr(data, j), listing.price, listing.date, listing.link]
#            row = [_.encode('utf-8') for _ in row]
#            writer.writerow(row)

    print "[Info] Wrote to {}".format(filename)


# This function exports listings as csv file:
def pprint(filename, objects, fields):

    write = csv.writer(sys.stdout)
    writer.writerow(row_headers)

    for obj in objects:
        row = [attrgetter(fields[header])(obj) for header in row_headers]
        for count, column in enumerate(row):
            if callable(column):
                row[count] = column()
            if type(column) is unicode:
                row[count] = column.encode('utf8')
        writer.writerow(row)
