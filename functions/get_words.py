import sys
import numpy as np
import requests
from lxml import html
from random import randint
import time
from wiki_crossword.functions.url_searcher import *

# Функция поиска слов

def find_words(request_word, count_of_words=5, coef=0.7):

  try:
    URL = 'https://ru.wikipedia.org/w/api.php?action=opensearch&profile=engine_autoselect&format=json&search='+url_decoder(request_word)
    word_new = requests.get(URL).json()[1][0]
    return request_to_search(word_new, count_of_words, coef)
  except:
    URL = 'https://ru.wikipedia.org/wiki/' + url_decoder(request_word)
    page = requests.get(URL).content
    html_tree = html.fromstring(page.decode('UTF-8'))
    category_list = search_category(html_tree, request_word)[1]
  try:
    URL = 'https://ru.wikipedia.org/wiki/%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D0%B8?from='+url_decoder(request_word)
    page = requests.get(URL).content
    html_tree = html.fromstring(page.decode('UTF-8'))
    items = html_tree.xpath(".//div[contains(@class,'mw-spcontent')]/ul/li/a")
    category = [i.text for i in items][0]
    if distance(category, request_word) < 2 or len(set(request_word.lower())&set(category.lower()))==len(set(request_word.lower())):
        attention = '\rВыполняется поиск слов на тему '+'"'+category+'".'
        sys.stdout.write(attention)
        return request_to_search(category, count_of_words, coef)
    
    if 'Страницы значений' in category_list[0]:
      URL = 'https://ru.wikipedia.org/wiki/'+url_decoder(request_word)
      page = requests.get(URL).content
      html_tree = html.fromstring(page.decode('UTF-8'))
      items = html_tree.xpath(".//div[contains(@class,'mw-parser-output')]/ul/li/b/a")
      if len(items) < 1:
        items = html_tree.xpath(".//div[contains(@class,'mw-parser-output')]/ul/li/a")
      request_word = [i.get('title') for i in items][0]
      URL = 'https://ru.wikipedia.org/wiki/' + url_decoder(request_word)
      page = requests.get(URL).content
      html_tree = html.fromstring(page.decode('UTF-8'))
      category_list = search_category(html_tree, request_word)[1]
      attention = '\rВыполняется поиск слов на тему '+'"'+category_list[0]+'".'
      sys.stdout.write(attention)
      return request_to_search(request_word, count_of_words, coef)
  except:
    if request_word in category_list:
        attention = '\rВыполняется поиск слов на тему '+'"'+request_word+'".'
        sys.stdout.write(attention)
        return request_to_search(request_word, count_of_words, coef)
    else:
        try:
          URL = 'https://ru.wikipedia.org/w/api.php?action=opensearch&search='+url_decoder(request_word)+'&format=xmlfm&limit=10&profile=engine_autoselect'
          page = requests.get(URL).content
          html_tree = html.fromstring(page.decode('UTF-8'))
          new_request = html_tree.xpath(".//div[contains(@class,'mw-highlight mw-highlight-lang-xml mw-content-ltr')]/pre/text()")[10]
          
          attention = '\rВыполняется поиск слов на тему '+'"'+new_request+'".'
          sys.stdout.write(attention)
          return request_to_search(new_request, count_of_words, coef)
        
        except:
          new_request = search_unknown_category(request_word)
        try:
          URL = 'https://ru.wikipedia.org/wiki/' + url_decoder(new_request)
          page = requests.get(URL).content
          html_tree = html.fromstring(page.decode('UTF-8'))
          category_list = search_category(html_tree, request_word)[1]
          category_list = range_category(category_list, request_word)
          attention = '\rВыполняется поиск слов на тему '+'"'+category_list[0]+'".'
          sys.stdout.write(attention)
          return request_to_search(category_list[0], count_of_words, coef)
        except:
          attention = '\rВыполняется поиск слов на тему '+'"'+new_request+'".'
          sys.stdout.write(attention)
          return request_to_search(new_request, count_of_words, coef)
  else:
    attention = '\rВыполняется поиск слов на тему '+'"'+category_list[0]+'".'
    sys.stdout.write(attention)
    return request_to_search(category_list[0], count_of_words, coef)

# Функция корректировки запроса и нахождения слов
def request_to_search(request_word, count_of_words, coef):
    count_of_words += int(count_of_words*coef)
    URL = 'https://ru.wikipedia.org/wiki/' + url_decoder(request_word)
    page = requests.get(URL).content
    html_tree = html.fromstring(page.decode('UTF-8'))
    
    # Cлова основной страницы
    words_page = parse_items(request_word)

    # Названия и ссылки категорий основной страницы
    urls_category_page, words_category_page = search_category(html_tree, request_word)

    words_category_page = range_category(words_category_page, request_word)

    # Слова и ссылки подкатегорий
    URL = 'https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:' + url_decoder(words_category_page[0])
    page = requests.get(URL).content
    html_tree = html.fromstring(page.decode('UTF-8'))
    words_under_category, urls_under_category = get_words_urls(html_tree, request_word)

    if len(urls_under_category) < 1:
        URL = 'https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:' + url_decoder(request_word)
        page = requests.get(URL).content
        html_tree = html.fromstring(page.decode('UTF-8'))
        words_under_category, urls_under_category = get_words_urls(html_tree, request_word)

    urls = urls_under_category + urls_category_page


    words = list(set(words_under_category + words_page))

    if len(words) < count_of_words:
        words = searsh_words(urls, count_of_words, html_tree, words, request_word)
    
    a_list = association_list(request_word)

    w_list = list(set(words))

    a_list = [i.lower() for i in a_list]
    w_list = [i.lower() for i in w_list]

    final_list = list(set(a_list)&set(w_list))

    #w_list.sort(key=len)

    for item in w_list:
        
        if len(final_list) < count_of_words and item not in final_list:
            final_list.append(item)
    return random_list(final_list, len(final_list))

# Функция фильтрации найденных слов
def append_list(list_words):
    new_list_words = []
    for word in list_words:
        if ' ' in word or '-' in word or ':' in word:
            continue
        if False in list(map(lambda x: True if x in alphabet else False, word)) and 'А' not in word:
            continue
        if len(word) < 3 or len(re.findall(r'[А-Я]', word)) > 2:
            continue
        else:
            new_list_words.append(word) 
    return list(set(new_list_words))

# Функция поиска слов
def searsh_words(urls, n, current_tree, words, request_word):
    url_list = []
    time_1 = time.mktime(time.gmtime())
    while len(words) < n: 
        if time.mktime(time.gmtime()) - time_1 > 30:
            break
        for url_under_category in urls: 
            URL = 'https://ru.wikipedia.org/' + url_under_category
            #print(URL)
            page = requests.get(URL).content
            html_tree = html.fromstring(page.decode('UTF-8'))
            words += get_words_urls(html_tree, request_word)[0]
            url_list += get_words_urls(html_tree, request_word)[1]
            words = list(set(words))
            #print(words)
            if len(words) > n:
                break
        urls = list(set(url_list))
        if 15 > time.mktime(time.gmtime()) - time_1 > 8:
            urls = search_category(current_tree)[0]
        if 25 > time.mktime(time.gmtime()) - time_1 > 20:
            urls = search_category(html_tree)[0]
    return words

# Функция для получения списка в рандомном порядке
def random_list(words_list, count_word):
    list_random = []
    while len(list_random) < count_word:
        random_index = np.random.randint(0, len(words_list), 1)[0]
        random_word = words_list[random_index]
        if random_word not in list_random:
            list_random.append(random_word)
            words_list.remove(random_word)
    return list_random

def search_unknown_category(request):
    min_dists = []
    categories = []
    dict_category = dict()
    words = request.split(' ')
    words = [w.strip() for w in words]
    list_categories = []
    for word in words:
        p = morph.parse(word)[0]
        word = p.normal_form
        if p.tag.POS == 'NOUN' and p.tag.case != 'nomn':
            i = 1
            word[:-i]
        elif p.tag.POS == 'ADJF':
            i = 2
            word[:-i]
        else:
            word = word
        URL = 'https://ru.wikipedia.org/wiki/%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D0%B8?from='+url_decoder(word)
        page = requests.get(URL).content
        html_tree = html.fromstring(page.decode('UTF-8'))
        items = html_tree.xpath(".//div[contains(@class,'mw-spcontent')]/ul/li/a")
        categories += [i.text for i in items]
        
    URL = 'https://ru.wikipedia.org/w/index.php?title=%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:%D0%9F%D0%BE%D0%B8%D1%81%D0%BA&limit=10&offset=0&profile=default&search='+url_decoder(request)
    page = requests.get(URL).content
    html_tree = html.fromstring(page.decode('UTF-8'))
    items = html_tree.xpath(".//div[contains(@class,'mw-search-result-heading')]/a")
    categories += [i.get('title') for i in items]

    for category in categories:
        min_dists.append(min([distance(' '.join(words).lower(), category.lower()), distance(' '.join(words[::-1]).lower(), category.lower())]))
    
    for i, dist in enumerate(min_dists):
        if dist not in dict_category.keys():
            dict_category[dist] = [categories[i],]
        else:
            category_list = dict_category[dist].copy()
            category_list.append(categories[i])
            dict_category[dist] = category_list
    count = 0
    i = 0
    while count < 2:
        try:
            list_categories += dict_category[min(dict_category.keys())+i]
            count += 1
            i += 1
        except:
            i += 1
    set_lens = [len(set(near_category.lower())& set(request.lower())) for near_category in list_categories]
    return list_categories[set_lens.index(max(set_lens))]

def distance(a, b):
    n, m = len(a), len(b)
    if n > m:
        # убедимся что n <= m, чтобы использовать минимум памяти O(min(n, m))
        a, b = b, a
        n, m = m, n
    current_row = range(n + 1)  # 0 ряд - просто восходящая последовательность (одни вставки)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)
    return current_row[n]


def get_content_text(word):

    URL = 'https://ru.wikipedia.org/wiki/' + url_decoder(word)
    page = requests.get(URL).content
    html_tree = html.fromstring(page.decode('UTF-8'))
    text_items = html_tree.xpath(".//div[contains(@class,'mw-parser-output')]/*")
    try:
        URL = 'https://ru.wikipedia.org/w/api.php?action=parse&prop=categories&format=json&page=' + url_decoder(word)
        page = requests.get(URL).json()['parse']['categories']
        category_items = [i['*'] for i in page]
    except:
        category_items = []
    items = text_items + category_items
    new_item = str()
    for item in items:
        try:
            new_item += item.text
        except:
            continue
    return new_item

def parse_items(word_request):
    URL = 'https://ru.wikipedia.org/w/api.php?action=parse&prop=links&format=json&page=' + url_decoder(word_request)
    page = requests.get(URL).json()['parse']['links']
    words_page = [i['*'] for i in page]

    page_words_list = []

    for i, word in enumerate(words_page):

        if len(append_list([word,])) > 0 and word_request.lower()[:-2] in get_content_text(word) and 'государство' not in get_content_text(word):
            page_words_list.append(word)
    return page_words_list
