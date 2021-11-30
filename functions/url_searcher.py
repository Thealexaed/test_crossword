# Определение URL-адресов
import requests
from lxml import html
from urllib.parse import parse_qs
from urllib.parse import urlencode
import openpyxl
import pymorphy2
import  re
morph = pymorphy2.MorphAnalyzer()

alphabet = 'АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя'

category_url = 'https://ru.wikipedia.org/wiki/%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D0%B8?from='
word_url = 'https://ru.wikipedia.org/wiki/'
assotioation_url = [
  'https://wordassociations.net/ru/%D0%B0%D1%81%D1%81%D0%BE%D1%86%D0%B8%D0%B0%D1%86%D0%B8%D0%B8-%D0%BA-%D1%81%D0%BB%D0%BE%D0%B2%D1%83/',
   '?button=%D0%9D%D0%B0%D0%B9%D1%82%D0%B8'
   ]

# Функция кодирования символов из кирилицы в формат URL
def url_decoder(word):
    url_word = urlencode({'str':word}).split('=')[1].replace('+', '_')
    return url_word

# Функция декодирования символов из формата URL в кирилицу
def url_encoder(url):
    word = parse_qs('str=' + url, encoding='utf-8')['str'][0]
    return word

# Нахождение ассоциативных слов
def association_list(word):
    URL = assotioation_url[0] + word+assotioation_url[1]
    page = requests.get(URL).content
    html_tree = html.fromstring(page.decode('UTF-8'))
    items = html_tree.xpath(".//div[contains(@class,'section NOUN-SECTION')]/ul/li/a")
    return [i.text for i in items]

# Сортировка категорий
def range_category(category_list, request_word):
    category_list_new = []
    for category in category_list:
        if request_word[:-2] in category:
            category_list_new.append(category)
    category_list = list(set(category_list) - set(category_list_new))
    category_list.sort(key=len)
    for category in category_list:
        if 'по алфавиту' in category:
            latest_category = category
            continue
        category_list_new.append(category)   
    try:
        category_list_new.append(latest_category)  
    except:
        return category_list_new
    return category_list_new

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

# Нахождение URL-адресов и названий категорий и подкатегорий
def get_words_urls(current_tree):
  current_words = []
  # Названия категорий запроса
  category_list = current_tree.xpath(".//div[contains(@class,'CategoryTreeItem')]/a")
  category_words = [i.text for i in category_list]
  category_words = [
      morph.parse(word)[0].normal_form if morph.
      parse(word)[0].tag.number == 'plur' and morph.
      parse(word)[0].tag.case == 'nomn' else word for word in category_words
  ]
  urls_list = list(map(lambda x: x.get('href'), category_list))
  # Названия подкатегорий
  under_category_list = current_tree.xpath(
      ".//div[contains(@class,'mw-category-group')]/ul/li/a"
      ) + current_tree.xpath(
          ".//div[contains(@class,'mw-content-ltr')]/ul/li/a"
          )
  under_category_words = list(map(lambda x: x.get('title'), under_category_list))
  current_words = category_words + under_category_words 
  return append_list(current_words), urls_list

# Получение URL-адресов и названий категорий и подкатегорий
def search_category(current_tree):
  search_category_list = current_tree.xpath(".//div[contains(@class,'mw-normal-catlinks')]/ul/li/a")
  category_urls_list = list(map(lambda x: x.get('href'), search_category_list))
  category_text_list = list(map(lambda x: x.text, search_category_list))
  return category_urls_list, category_text_list
