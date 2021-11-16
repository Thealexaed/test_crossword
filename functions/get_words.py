import requests
from lxml import html
from random import randint
import time
from test_crossword.functions.url_searcher import *

# Функция поиска слов

def find_words(request_word, count_of_words=5, coef=0.7):
  URL = 'https://ru.wikipedia.org/wiki/' + url_decoder(request_word)
  page = requests.get(URL).content
  html_tree = html.fromstring(page.decode('UTF-8'))
  category_urls = search_category(html_tree)[0]
  category_list = search_category(html_tree)[1]
  category_list = range_category(category_list, request_word)

  #if category_list[0] == 'Страницы значений по алфавиту':
  if 'Страницы значений' in category_list[0]:
    try:
      items = html_tree.xpath(".//div[contains(@class,'mw-parser-output')]/ul/li/b/a")
      request_word = [i.get('title') for i in items][0]
    except:
      items = html_tree.xpath(".//div[contains(@class,'mw-parser-output')]/ul/li/a")
      request_word = [i.get('title') for i in items][0]
    URL = 'https://ru.wikipedia.org/wiki/' + url_decoder(request_word)
    page = requests.get(URL).content
    html_tree = html.fromstring(page.decode('UTF-8'))
    category_urls = search_category(html_tree)[0]
    category_list = search_category(html_tree)[1]
    category_list = range_category(category_list, request_word)
    return request_to_search(category_list[0], count_of_words, coef)
  if request_word in category_list:
    return request_to_search(request_word, count_of_words, coef)
  else:
    return request_to_search(category_list[0], count_of_words, coef)

# Функция корректировки запроса и нахождения слов
def request_to_search(request_word, count_of_words, coef):
    count_of_words += int(count_of_words*coef)
    URL = 'https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:' + url_decoder(request_word)
    page = requests.get(URL).content
    html_tree = html.fromstring(page.decode('UTF-8'))
    # Слова и ссылки основной страницы
    words, urls = get_words_urls(html_tree)
    if len(words) < count_of_words:
        words += searsh_words(urls, count_of_words, html_tree)
    a_list = association_list(request_word)
    w_list = list(set(words))

    a_list = [i.lower() for i in a_list]
    w_list = [i.lower() for i in w_list]
    w_list.sort(key=len)
    final_list = final_list = list(set(a_list)&set(w_list))
    for item in w_list:
        if len(final_list) < count_of_words and item not in final_list:
            final_list.append(item)
    return final_list

# Функция фильтрации найденных слов
def append_list(list_words):
    new_list_words = []
    for word in list_words:
        if ' ' in word or '-' in word or ':' in word:
            #print(1, word)
            continue
        if False in list(map(lambda x: True if x in alphabet else False, word)) and 'А' not in word:
            #print(2, word)
            continue
        if len(word) < 3 or len(re.findall(r'[А-Я]', word)) > 2:
            #print(3, word)
            continue
        else:
            new_list_words.append(word) 
    return list(set(new_list_words))

# Функция поиска слов
def searsh_words(urls, n, current_tree):
  words_list = []
  url_list = []
  time_1 = time.mktime(time.gmtime())
  while len(words_list) < n: 
    if time.mktime(time.gmtime()) - time_1 > 30:
      break
    for url_under_category in urls: 
      URL = 'https://ru.wikipedia.org/' + url_under_category
      page = requests.get(URL).content
      html_tree = html.fromstring(page.decode('UTF-8'))
      words_list += get_words_urls(html_tree)[0]
      url_list += get_words_urls(html_tree)[1]
      words_list = list(set(words_list))
      if len(words_list) > n:
        break
    urls = list(set(url_list))
    if 10 > time.mktime(time.gmtime()) - time_1 > 4:
      urls = search_category(current_tree)[0]
    if 20 > time.mktime(time.gmtime()) - time_1 > 16:
      urls = search_category(html_tree)[0]
  return words_list

# Функция для получения списка в рандомном порядке
def random_list(count_word, words_list):
    list_random = []
    for _ in range(count_word):
        random_index = np.random.randint(0, len(words_list), 1)[0]
        random_word = words_list[random_index]
        if random_word not in list_random:
            list_random.append(random_word)
    return list_random
