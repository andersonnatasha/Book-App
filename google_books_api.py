from flask import request, session
import os
import requests
import crud
from random import randint

API_KEY = os.environ['GOOGLEBOOKS_KEY']

def search_a_book():
    """Show results from user's book search."""

    keyword = request.args.get('search', '')

    url = 'https://www.googleapis.com/books/v1/volumes'
    payload = {'q': keyword, 'maxResults': 10, 'apikey': API_KEY}

    res = requests.get(url, params=payload)

    data = res.json()

    search_results = []

    if keyword != '':

        for n in range(len(data['items'])):

            search_result = {}

            base = data['items'][n]['volumeInfo']
            search_result['isbn_13'] = None

            if base.get('industryIdentifiers', None) and (base['industryIdentifiers'][-1]['type'] == 'ISBN_13') and (base.get('imageLinks')):
                search_result['isbn_13'] = base['industryIdentifiers'][-1]['identifier']

            elif base.get('industryIdentifiers', None) and (base['industryIdentifiers'][0]['type'] == 'ISBN_13') and (base.get('imageLinks')):
                search_result['isbn_13'] = base['industryIdentifiers'][0]['identifier']

            if search_result['isbn_13'] != None:

                keys_to_search_for_in_data = ['title', 'subtitle', 'authors', 'publishedDate', 'description', 'categories']

                for key in keys_to_search_for_in_data:
                    if key in base:
                        search_result[key] = base[key]

                    search_result['thumbnail'] = base['imageLinks']['thumbnail']

                search_results.append(search_result)

    if keyword != "":
        search_result_and_keyword = [search_results, keyword]
    else:
        search_result_and_keyword = None

    return search_result_and_keyword


def show_recommended_books():
    """show recommended books."""

    user_id = session['user_id']
    keywords = crud.get_all_interests_for_user(user_id)

    search_results = []
    for keyword in keywords:
        keyword = keyword.interest
        url = 'https://www.googleapis.com/books/v1/volumes'
        keyword = f'subject: {keyword}'
        randint_high = 1000
        payload = {'q': keyword, 'maxResults': 10, 'startIndex': randint(0,randint_high), 'apikey': API_KEY}

        res = requests.get(url, params=payload)

        data = res.json()

        while not data.get('items'):
            randint_high -= 100
            payload = {'q': keyword, 'maxResults': 10, 'startIndex': randint(0,randint_high), 'apikey': API_KEY}
            res = requests.get(url, params=payload)
            data = res.json()

        for n in range(len(data['items'])):

            search_result = {}

            base = data['items'][n]['volumeInfo']
            search_result['isbn_13'] = None

            if base.get('industryIdentifiers', None) and (base['industryIdentifiers'][-1]['type'] == 'ISBN_13') and (base.get('imageLinks')):
                search_result['isbn_13'] = base['industryIdentifiers'][-1]['identifier']

            elif base.get('industryIdentifiers', None) and (base['industryIdentifiers'][0]['type'] == 'ISBN_13') and (base.get('imageLinks')):
                search_result['isbn_13'] = base['industryIdentifiers'][0]['identifier']

            if search_result['isbn_13'] != None:

                keys_to_search_for_in_data = ['title', 'subtitle', 'authors', 'publishedDate', 'description', 'categories']

                for key in keys_to_search_for_in_data:
                    if key in base:
                        search_result[key] = base[key]

                if base.get('imageLinks'):
                    search_result['thumbnail'] = base['imageLinks']['thumbnail']

                search_results.append(search_result)

    return search_results


