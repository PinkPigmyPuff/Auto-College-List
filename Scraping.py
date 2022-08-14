# imports
import requests
import pandas as pd
import csv
from bs4 import BeautifulSoup
from random import randint
from time import sleep

setName = 'Mega1.2'
# the pages we want to scrape
pages = [
    # STEM (7)
    'liberal-arts-colleges-to-consider-that-offer-great-sciences/317/',
    'the-top-20-wired-colleges/743/',
    'consortium-for-innovative-environments-in-learning/239/',
    'great-colleges-to-study-astronomy/111/',
    '10-radically-innovative-engineering-science-programs/154/',
    'great-colleges-for-the-future-engineer/153/',
    'the-experts-choice-great-engineering-and-liberal-arts/158/',
    'the-experts-choice-unexpectedly-strong-science-programs/226/',

    # Liberal Arts (1)
    'colleges-with-great-english-creative-writing-and-literature-programs/166/',

    # Values + Extracirriculars (2)
    'the-experts-choice-colleges-for-the-leader-or-soon-to-be-leader/408/',
    'colleges-with-a-winning-tradition-in-speech-and-debate/461/',

    # Value (4)
    'the-experts-choice-colleges-that-are-great-values/343/',
    'the-experts-choice-colleges-with-great-reputations-that-are-not-incredibly-selective/680/',
    'where-money-is-given-to-students-without-financial-need/354/',
    'best-student-faculty-ratios/920/',

    # Education (3)
    'colleges-for-the-scholar/426/',
    'high-intensity-colleges/425/',
    'colleges-for-the-independent-learner/424/',

    # Worldliness (4)
    'the-experts-choice-terrific-study-abroad-programs/319/',
    '75-best-colleges-for-food-in-america-for-2018/2320/',
    'which-colleges-are-havens-for-hipsters/1664/',
    'colleges-with-all-types-of-student-diversity/446/',

    # 'Goodness (5)
    'green-colleges-and-universities/253/',
    'colleges-for-the-person-who-cares-about-the-world/437/',
    'the-10-best-colleges-with-an-environmental-focus/443/',
    'the-north-american-alliance-for-green-education/254/',
    'making-a-difference-colleges/433/',

    # Places (4)
    'four-year-colleges-and-universities-in-california/2832/',
    'excellent-colleges-in-or-near-new-york-city/721/',
    'four-year-colleges-and-universities-in-colorado/2835/',
    'the-experts-choice-most-beautiful-campuses/701/',

    # Not working
    # 'colleges-with-excellent-programs-in-computer-science-including-animation-and-game-design/133/' #not working, link
    # 'colleges-with-innovative-academic-programs/238/', # not working, no link. V DIFF FORMAT
    ]

# my weighting of how importand every list is to me
values = [
    #STEM: total = 40
    6, 6, 6, 6, 6, 6, 6, 6,
    # Liberal Arts: total = 5
    5,
    # Values + Extracirriculals: total = 10
    5, 5,
    # Value: total = 40
    10, 10, 10, 10,
    # Education: total = 15
    5, 5, 5,
    # Wordliness: total = 20
    5, 5, 5, 5,
    # Goodness: total = 20
    4, 4, 4, 4, 4,
    # Places: total = 25
    5, 7.5, 5, 7.5

]
tags = [
    #STEM:
    'libSTEM', 'wired', 'innov', 'astron', 'innovEng', 'eng', 'lib+emgomeer', 'science',
    # Liberal Arts:
    'english',
    # Values + Extracirriculals:
    'leader', 'debate',
    # Value:
    'value', 'notTooSelective', 'FAFO', 'ratiod',
    # Education:
    'scholar', 'high-intens', 'independent',
    # Wordliness:
    'abroad', 'food', 'hip', 'diversity',
    # Goodness:
    'green', 'careWorld', 'envFocus', 'NAGreen', 'impact',
    # Places:
    'cali', 'NYC', 'CO', 'beut'
]
# NW = english, cs, campus
# Amherst = scholar, english, libSTEM, MA, campus, innovative
# the two output lists, with the name of colleges and their weighting
megalist = []
occurences = []
references = []

# characters to remove from text, in order to avoid discrepancies
remove = ['.', ':', '%', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']


# whenever we scrape a new college, add it to megalist (if new) or increase its weight
def addToList(college):
    if college not in megalist:
        # new college goes to THE END of our MEGALIST
        megalist.append(college)
        # the VALUE at the CURRENT PAGE (index - 1) is added to THE END of OCCURENCES
        occurences.append(values[page]) # -1?
        # the STRING at the CURRENT PAGE (index - 1) is added IN AN EMPTY ARRAY to THE END of REFERENCES
        references.append([tags[page]])
    else:
        # find the first time this college pops up in the MEGALIST (index -1)
        firstOccurence = megalist.index(college)
        print(firstOccurence)
        # the VALUE at the FIRST OCCURING TIME is increased by the VALUE of the current page (index -1)
        occurences[firstOccurence] += values[page] #-1?
        # the LIST at the FIRST ACCURING TIME is appended by the current tag (index -1)
        references[firstOccurence].append(tags[page])

# remove any of the characters in the 'remove' list
def removeChar(word):
    listWord = list(word)
    final = []
    for char in listWord:
        if(char not in remove):
            final.append(char)
    if(final[0] == ' '):
        final.pop(0)
    return ''.join(final)


for page in range(0, len(pages)):
# for page in range(0, 3):
    # turn the current page into a url, and then download the HTML file
    url = "https://www.collegexpress.com/lists/list/" + pages[page]
    print(url)
    print(page)
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')

    # find all colleges
    colleges = soup.find_all(class_='name')
    for college in colleges:
        # clean up the characters, and then add it to our list
        desiredCollege = removeChar(college.get_text())
        print(desiredCollege)
        addToList(desiredCollege)


print(megalist)
print(occurences)
print(references)

# create a pandas dict to store our colleges and wieghts in a graph
d = {"Colleges": megalist, "Occurrences": occurences, "References": references}
df = pd.DataFrame.from_dict(d)
print(df)

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter(setName + '.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name=setName, index = False)

# Close the Pandas Excel writer and output the Excel file.
writer.save()