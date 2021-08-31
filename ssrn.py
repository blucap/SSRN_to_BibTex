#!/home/martien/anaconda3/bin/python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#%%
import sys
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen as uReq
import re
from collections import OrderedDict
from dateutil.parser import parse
import calendar


def get_month(m):
    dic = dict(enumerate(calendar.month_abbr))
    m = dic[m]
    return m.lower()


def get_ssrn_entry(url):
    if isinstance(url, int):
        url = str(url)
        url = 'https://papers.ssrn.com/sol3/papers.cfm?abstract_id=' + url
        ssrn_id_int = True

    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    uClient = uReq(req)
    soup = BeautifulSoup(uClient, 'lxml')
    authorsstring = ""
    authorscount = 0
    articledict = OrderedDict({"bib_entry": "",
                               'authors': "",
                                "title": "",
                                "pages": "",
                                'journal': "",
                                'title': "",
                                'publisher': "",
                                "note": "",
                                'year': ""})

    second_author = ""
    first_author = ""

    articledict['journal'] = "{SSRN Electronic Journal}"
    articledict['publisher'] = "{Elsevier BV}"
    articledict['ssrn_no'] = re.search('abstract_id=(.*)', url, re.IGNORECASE).group(1)
    articledict['note'] = '"\\url{https://ssrn.com/abstract=' + articledict['ssrn_no'] + '}"'

    for tag in soup.find_all('meta'):
        if tag.get("name", None) == 'citation_title':
            # print(tag.get("content", None))
            articledict['title'] = "{{" + tag.get("content", None) + "}}"
            raw_title = tag.get("content", None)

        if tag.get("name", None) == 'citation_online_date':
            # print(tag.get("content", None))
            cite_date_str = tag.get("content", None)
            try:
                cite_date = parse(cite_date_str)
            except:
                cite_date = parse("01/01/2099")

        if tag.get("name", None) == 'citation_publication_date':
            # print(tag.get("content", None))
            try_date_str = tag.get("content", None)
            try:
                try_date = parse(try_date_str)
            except:
                try_date = cite_date


            articledict['date_str'] = try_date_str  
            articledict['date'] = try_date  

            articledict['month'] = get_month(articledict['date'].month)
            articledict['year'] = str(articledict['date'].year)

        if tag.get("name", None) == 'citation_author':
            author = tag.get("content", None)
            # print(author)
            if len(author) > 0:
                authorscount += 1
                if authorscount == 1:
                    first_author = author.split(',')[0]
                if authorscount == 2:
                    second_author = author.split(',')[0]
                authorsstring += author + ' and '
    if authorscount == 1:
        bib_entry = first_author + articledict['year']
    elif authorscount == 2:
        bib_entry = first_author + second_author + articledict['year']
    else:
        bib_entry = first_author + 'EtAl' + articledict['year']
    articledict['bib_entry'] = "@article{" + bib_entry
    authorsstring = re.sub(r' and $', r"", authorsstring)
    articledict['authors'] = "{" + authorsstring + "}"

    pp = "0"
    # print('\n', pp)
    pages = re.search('Number of pages:\s+(\d+)', soup.get_text(strip=True), re.IGNORECASE)
    if pages != None and pp == "0":
        pp = pages.group(1)
        articledict['pages'] = "pages = {1--" + str(pp) + "}"
        articledict['pagescount'] = int(pp)

    pages = re.search('pp.\s+(\d+-\d+)', soup.get_text(strip=True), re.IGNORECASE)
    if pages != None and pp == "0":
        pp = pages.group(1)
        articledict['pagescount'] = int(pp.split('-')[1]) - int(pp.split('-')[0])
        articledict['pages'] = "pages = {" + str(pp) + "}"

    pages = re.search('(\d+) Pages', soup.get_text(strip=False), re.IGNORECASE)
    if pages != None and pp == "0":
        pp = pages.group(1)
        articledict['pages'] = "pages = {1--" + str(pp) + "}"
        articledict['pagescount'] = int(pp)
    dic = {}
    print('\n')
    print(f'{raw_title}')
    print('\n')
    authors_prefix = 'Author\'s names:\n' if authorscount > 1  else 'Author\'s name:'
    print(authors_prefix)
    for link in soup.find_all('a', href=True):
        dlink = link.get('title')
        #print(dlink)
        if dlink == "View other papers by this author":
            #print(link.get('href'))
            ssrn_id = re.search('per_id=(\d+)', link.get('href'), re.IGNORECASE)
            if (ssrn_id) and (not link.get_text().startswith("See all articles")):
                ssrn_id = int(ssrn_id.group(1))
                if ssrn_id not in dic:
                    dic[ssrn_id] = link.get_text()
                    print(f'{dic[ssrn_id]} ({ssrn_id})')

    print('\nBibtex:\n')
    print(f'{articledict["bib_entry"]},')
    print(f'author = {articledict["authors"]},')
    print(f'title = {articledict["title"]},')
    if pp != "0":
        print(f'{articledict["pages"]},')
    print(f'publisher = {articledict["publisher"]},')
    print(f'note = {articledict["note"]},')
    print(f'month = {articledict["month"]},')
    print(f'year = {articledict["year"]}')
    print('}')
    print('\n')
    print(url)
    print('\n')

    return articledict, soup.prettify(), dic


def main(argv):
    if len(argv) > 1:
        if isinstance(argv, str):
            if argv.startswith('https://'):
                get_ssrn_entry(argv)
            elif argv.startswith('--help'):
                print("\nUsage:\nssrn 3846655\nssrn https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3846655\n")
            else:
                print(f":{argv}.")
                try:
                    argv = int(argv.strip())
                    print(f"+{str(argv)}.")
                    get_ssrn_entry(argv)
                except:
                    print("Check your inputs, give it some time, or use the URL instead.")


if __name__ == "__main__":
    if len(sys.argv)>1:
        main(sys.argv[1])
    else:
        print("Please add the SSRN # or url string")



#%%
'''
test, soup, dic = get_ssrn_entry('https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3846655')

test, soup, dic = get_ssrn_entry(3846655)
test, soup, dic = get_ssrn_entry(2828073)
test, soup, dic = get_ssrn_entry(3197365)
test, soup, dic = get_ssrn_entry(2576277)
test, soup, dic = get_ssrn_entry(252653)
"

'''