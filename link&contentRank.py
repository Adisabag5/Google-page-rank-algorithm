import pathlib, os, re, numpy, string
from pathlib import Path
from Question1 import *



#----------------------------Content-Rank---------------------------------------------------#


def rank_page(file, search_string, mininet):

    total_rank = 0
    words = search_string.split(" ")
    f = open(file, "r")

    #check if the text part of the hyperlinks contain words of the search string

    for link in mininet.links_from_page[file.name]:
        if '||' in link:
            for word in search_string.split():
                if word in link:
                    print (word, link)
                    total_rank += 10

    # check if and how many times the search string apears in the text in hole

    for line in f:
        if search_string.replace(" ", "").lower() in line.replace(" ", "").lower():
            total_rank += 50

    # count the total apearences of each word & check if there are words in the first 3 sentences

    for word in words:
        rows_counter = 0
        count = 0
        f = open(file, "r")
        for line in f:
            if rows_counter == 3:
                count += (line.count(word)) * 3
            else:
                count += line.count(word)
        total_rank += count

    return total_rank


def content_rank(mininet, search_string, extra_params=None):
    content_page_rank = {}

    file_list = mininet.net_pat.glob('*.mnet')

    for file in file_list:
        cuurent_rank = rank_page(file, search_string, mininet)
        content_page_rank.setdefault(file.name, cuurent_rank)

    return content_page_rank

#----------------------------Link-Rank---------------------------------------------------#

def fix_page_rank(content_rank_page, page_rank):
    sum_rank = 0
    extra_sum_rank = 0
    count = 0
    top = int(0.2*len(page_rank))
    top_list = []

    for i in range(top):
        top_list.append(0)

    for key in content_rank_page:
        if content_rank_page[key] == 0:
            sum_rank += page_rank[key]
            page_rank[key] = 0
        else:
            top_list.append(content_rank_page[key])
            extra_sum_rank += 0.2*page_rank[key]
            page_rank[key] *= 0.8
            count += 1

    top_list.sort(reverse=True)
    counter = 0
    for key in page_rank:
        if page_rank[key] != 0:
            page_rank[key] += sum_rank / count
            for i in range(top):
                if top_list[i] == content_rank_page[key] and counter < top:
                    page_rank[key] += extra_sum_rank/top
                    counter += 1
    return page_rank




def link_rank(mininet, beta=0.8, search_string=None, extra_params=None):
    G = mininet.links_to_page
    M = mininet.links_from_page
    i = 0
    page_rank = {}
    temp_rank = {}
    N = len(G)
    r = 1 / N

    for key in G:
        page_rank.setdefault(key, r)
        temp_rank.setdefault(key, r)

    while i <= N:
        for key in page_rank:
            rank = 0
            for x in range(len(G[key])):
                d = G[key][x]
                rank += (page_rank[d] / len(M[d]))
            if rank == 0:
                temp_rank[key] = r
            else:
                temp_rank[key] = beta * rank + (1 - beta) * r

        for key in page_rank:
            page_rank[key] = temp_rank[key]

        i+=1



    if search_string != None:
        content_rank_page = content_rank(mininet, search_string)
        page_rank = fix_page_rank(content_rank_page, page_rank)

    sum = 0
    for key in page_rank:
        sum += page_rank[key]

    print(sum)
    print(page_rank)

    return page_rank





#----------------------------------TEST && INSPECT--------------------------------------------------------#

def print_dict(dict):
    print('')
    print('----------------------------------------------')
    for key in dict:
        print(key , ' -  ' , dict[key])
    print('----------------------------------------------')
    print('')


def count_links(dict):
    counter = 0
    for key in dict:
        for x in dict[key]:
            counter+=1
    print(counter)

def find_max_and_min(dict):
    max = 0
    min = 20
    min_key = ''
    max_key = ''
    for key in dict:
        if dict[key] > max:
            max = dict[key]
            max_key = key
        elif dict[key] != 0 and dict[key] < min:
            min = dict[key]
            min_key = key
    print(max_key, max)
    print(min_key, min)

