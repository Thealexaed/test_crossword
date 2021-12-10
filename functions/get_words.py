import sys
import numpy as np
import requests
from lxml import html
from random import randint
import time
from wiki_crossword.functions.url_searcher import *
import string
from IPython.display import clear_output
import matplotlib.pyplot as plt
from wiki_crossword.functions.get_definitions import *


from wiki_crossword.functions.crossword_plotter import *
import pymorphy2
morph = pymorphy2.MorphAnalyzer()
from IPython import display
import matplotlib

def print_fact(text):
    clear_output()
    fig, ax = plt.subplots()
    ax.axis('off')
    ax.text(0, 1, text, fontsize=20)
    plt.show()

def get_category_item(title):
    except_list = 'алфави статьи вики'
    raw_category_item = get_raw_category(title)
    raw_category_item = ' '.join(raw_category_item)
    raw_category_item = raw_category_item.lower()
    raw_category_item = raw_category_item.split(' ')
    raw_category_item = list(set([item[:-2] if len(item) > 5 else item.lower()[:-1] if len(item) > 4 else item.lower() for item in raw_category_item]))
    [raw_category_item.remove(item) if len(item) < 3 else None for item in raw_category_item]
    [raw_category_item.remove(item) if item in except_list else None for item in raw_category_item]
    return raw_category_item

def get_unknown_category(request_word): 
    URL = 'https://ru.wikipedia.org/w/index.php?search='+url_decoder(request_word).replace('_','+')+'&title=%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:%D0%9F%D0%BE%D0%B8%D1%81%D0%BA&profile=advanced&fulltext=1&ns14=1'
    page = requests.get(URL).content
    html_tree = html.fromstring(page.decode('UTF-8'))
    items = html_tree.xpath(".//div[contains(@class,'mw-search-result-heading')]/a")
    category = [i.get('title') for i in items][0]
    return category

def get_facts(request_word):
    pre_words = ['Кстати, а Вы знали?...\n\n   ',
                 'Пока ищу слова, стоит узнать, что...\n\n   ',
                 'Возможно, это подкачает Вашу эрудицию...\n\n   ',
                 'Оказывается, что...\n\n   ',
                 'Интересно, а Вы знали, что...\n\n   ',
                 'Спорим, Вы не знали про то, что...\n\n   ',
                 'Взгляните на интересный факт...\n\n   ',
                 'Нашёл факт по Вашей теме...\n\n   ']
    facts = []
    URL = 'https://ru.wikipedia.org/wiki/'+url_decoder(request_word)
    page = requests.get(URL).content
    html_tree = html.fromstring(page.decode('UTF-8'))
    items = html_tree.findall(".//p")
    texts = [i.text for i in items]
    for text in texts:
        try:
            if '. ' in text and len(text.split('. ')[0]) > 100:
                text = text.replace('\xa0—', '')
                text = text.replace('\xa0', '')
                text = cutter_text(text)
                facts.append(text.split('. ')[0]+'.')
        except:
            continue

    #try:
        #clear = '(Факт о ' + ' '.join([morph.parse(w)[0].inflect({'loct'}).word if i < 2 else w for i, w in enumerate(request_word.split(' '))]) + ')'
    #except:
        #clear = '(Факт о "' + request_word + '")'
    clear = '(Факт на тему "' + request_word + '")'
    for i, fact in enumerate(facts):
        pre_words[randint(0,len(pre_words)-1)]
        fact = '    ' + pre_words[randint(0,len(pre_words)-1)] + ' ' + fact
        length = max([len(i) for i in fact.split('\n')])
        facts[i] = fact + "\n" + "_" * length + '\n' + ' ' * ((length - len(clear)) * 2) + clear

    return facts

def find_words(request_word, count_of_words=5, coef=0.3):
    user_request = request_word
    try:
        try:
            URL = 'https://ru.wikipedia.org/wiki/' + url_decoder(request_word)
            page = requests.get(URL).content
            html_tree = html.fromstring(page.decode('UTF-8'))
            category_urls = search_category(html_tree, request_word)[0]
            category_list = search_category(html_tree, request_word)[1]
            category_list = range_category(category_list, request_word)
            if 'Страницы значений' in category_list[0]:
              try:
                items = html_tree.xpath(".//div[contains(@class,'mw-parser-output')]/ul/li/b/a")
                new_title = [i.get('title') for i in items][0]
                print(new_title)
                return request_to_search(new_title, count_of_words, coef, user_request)

              except:
                items = html_tree.xpath(".//div[contains(@class,'mw-parser-output')]/ul/li/a")
                new_title = [i.get('title') for i in items][0]
                print(new_title)
                return request_to_search(new_title, count_of_words, coef, user_request)
            else:
                # Поиск страницы
                URL = 'https://ru.wikipedia.org/w/index.php?search='+url_decoder(request_word).replace('_','+')+'&title=%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:%D0%9F%D0%BE%D0%B8%D1%81%D0%BA&profile=advanced&fulltext=1&ns0=1&searchToken=8i9o18hyjykfrnyfsle42py32'
                page = requests.get(URL).content
                html_tree = html.fromstring(page.decode('UTF-8'))
                items = html_tree.xpath(".//div[contains(@class,'mw-search-result-heading')]/a")
                new_title = [i.get('title') for i in items][0]
                return request_to_search(new_title, count_of_words, coef, user_request)

        except:
            # Поиск страницы
            URL = 'https://ru.wikipedia.org/w/index.php?search='+url_decoder(request_word).replace('_','+')+'&title=%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:%D0%9F%D0%BE%D0%B8%D1%81%D0%BA&profile=advanced&fulltext=1&ns0=1&searchToken=8i9o18hyjykfrnyfsle42py32'
            page = requests.get(URL).content
            html_tree = html.fromstring(page.decode('UTF-8'))
            items = html_tree.xpath(".//div[contains(@class,'mw-search-result-heading')]/a")
            new_title = [i.get('title') for i in items][0]
            return request_to_search(new_title, count_of_words, coef, user_request)
        # Поиск категории
    except:
        URL = 'https://ru.wikipedia.org/w/index.php?search='+url_decoder(request_word).replace('_','+')+'&title=%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:%D0%9F%D0%BE%D0%B8%D1%81%D0%BA&profile=advanced&fulltext=1&ns14=1'
        page = requests.get(URL).content
        html_tree = html.fromstring(page.decode('UTF-8'))
        items = html_tree.xpath(".//div[contains(@class,'mw-search-result-heading')]/a")
        category = [i.get('title') for i in items][0]
        return request_to_search(category, count_of_words, coef, user_request)


# Функция корректировки запроса и нахождения слов
def request_to_search(request_word, count_of_words, coef, user_request):
    count_of_words += int(count_of_words*coef)
    URL = 'https://ru.wikipedia.org/wiki/' + url_decoder(request_word)
    page = requests.get(URL).content
    html_tree = html.fromstring(page.decode('UTF-8'))
    words_page = []
    words_page_two = []
    words_search = []
    search_page = False
    new_request_word = str()
    dict_titles = dict()
    # Если запрос не имеет общих слов с названием найденной страницы/категории
    # То сначала производится поиск слов по найденной странице
    if len(set(set(request_word.split(' ')) & set(user_request.split(' ')))) == 0 and\
       len(set(user_request)) / len(set(user_request) & set(request_word)) < 0.7:
        sys.stdout.write('\rКажется, запрос немного непростой. Дайте минуточку...')
        words_page, dict_titles = parse_items(request_word, count_of_words, user_request)
        if len(words_page) < 2:
            try:
                new_request_word = get_unknown_category(user_request)
            except:
                new_request_word = search_unknown_category(user_request)
            sys.stdout.write('\rПопробую поискать на странице ' + new_request_word)
            words_page, dict_titles = parse_items(new_request_word, count_of_words, user_request)
        search_page = True

    if len(words_page) >= count_of_words:
        return words_page, dict_titles

    if len(new_request_word) > 1:
        request_word = new_request_word
        URL = 'https://ru.wikipedia.org/wiki/' + url_decoder(request_word)
        page = requests.get(URL).content
        html_tree = html.fromstring(page.decode('UTF-8'))

    # Названия и ссылки категорий основной страницы
    urls_category_page, words_category_page = search_category(html_tree, request_word)

    words_category_page = range_category(words_category_page, request_word)


    # Слова и ссылки подкатегорий
    URL = 'https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:' + url_decoder(words_category_page[0])
    page = requests.get(URL).content
    html_tree = html.fromstring(page.decode('UTF-8'))
    words, urls_under_category = get_words_urls(html_tree, request_word)

    if len(urls_under_category) < 1:
        URL = 'https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:' + url_decoder(request_word)
        page = requests.get(URL).content
        html_tree = html.fromstring(page.decode('UTF-8'))
        words, urls_under_category = get_words_urls(html_tree, request_word)
    

    urls = urls_under_category + urls_category_page

    if len(words) < count_of_words and search_page == False:
        count_of_words_for_search = count_of_words - len(words)
        # Cлова основной страницы
        sys.stdout.write('\r Ищу слова на странице википедии...')
        words_page_two, dict_titles = parse_items(request_word, count_of_words_for_search, user_request)
    
    words = [i.lower() for i in words]
    words = list(set(words + words_page + words_page_two))

    if len(words) < count_of_words:
        sys.stdout.write('\r Кажется найденных слов недостаточно... Подключаю специальные алгоритмы для поиска!')
        words_search = searsh_words(urls, count_of_words, html_tree, words, request_word)

    final_list = list(set([i.lower() for i in words]))
    
    a_list = association_list(request_word)
    
    words_search = list(set(words_search))

    a_list = [i.lower() for i in a_list]
    words_search = [i.lower() for i in words_search]


    search_list = list(set(a_list)|set(words_search))

    for item in search_list:
        if len(final_list) < count_of_words and item not in final_list:
            final_list.append(item)
    sys.stdout.write('\r Слова найдены!')   
    return random_list(final_list, len(final_list)), dict_titles

def get_title(word_request):
    abc = string.ascii_letters
    URL = 'https://ru.wikipedia.org/w/api.php?action=opensearch&search='+url_decoder(word_request)+'&format=json'
    new_url = requests.get(URL).json()[3][0]
    page = requests.get(new_url).content
    html_tree = html.fromstring(page.decode('UTF-8'))
    items = html_tree.xpath(".//h1[contains(@class,'firstHeading')]")[0]
    word = items.text

    try:
        if len(word.split(' ')) > len(word_request.split(' ')):
            word = word_request
    except:
        return None

    if any([i in abc for i in word]) == True:
        word = word_request
    if any([i in abc for i in word]) == True:
        return None
    return word


def parse_items(word_request, count_of_words, user_word_request):
    
    facts = get_facts(word_request)
    time_1 = time.mktime(time.gmtime())
    delta = 10
    
    URL = 'https://ru.wikipedia.org/wiki/' + url_decoder(word_request)
    page = requests.get(URL).content
    html_tree = html.fromstring(page.decode('UTF-8'))
    items = html_tree.findall(".//a")
    words_page = filter_items(items)
    page_words_list = []
    common_categories = []
    new_target_words = []
    control_page_words_list = []
    common_words = []
    dict_items = dict()
    word_for_facts = ''
    if len(user_word_request.split(' ')) > 1:
        target_words = user_word_request.split(' ')
        target_words = [
        item.lower()[:-2] if len(item) > 5 else item.lower()[:-1] if len(item) >= 4 else item.lower() for item in target_words
                        ]
        user_words = target_words
        
        for word in target_words:
            if word not in word_request.lower():
                new_target_words.append(word)
        if len(new_target_words) > 0:
            target_words = new_target_words
        for title in words_page:
            if time.mktime(time.gmtime()) - time_1 > 8 * count_of_words + 10:
                break
            if word_for_facts != '':
                facts += get_facts(word_for_facts)
            else:
                facts = facts
            if time.mktime(time.gmtime()) - time_1 > delta and len(facts) > 1:
                fact = facts[randint(0, len(facts)-1)]
                if len(fact) > 10:
                    print_fact(fact)
                #sys.stdout.write('\r' + facts[randint(0, len(facts)-1)])
                delta += 30
            try:
                raw_category_item = ' '.join(get_raw_category(title))
                raw_category_item = raw_category_item.lower()
            except:
                continue

            word = get_title(title)
            word = format_word(word, raw_category_item, user_words, target_words)

                
            if word == '---':
                continue
            if (any([i in raw_category_item for i in target_words]) or\
                any([i in raw_category_item for i in get_category_item(word_request)])) and\
                word.lower() not in control_page_words_list:

                control_page_words_list.append(word.lower())
                page_words_list.append(word)
                [common_categories.append(i) for i in get_raw_category(title)]
                [common_words.append(i) for i in raw_category_item.split(' ')]
                dict_items.update({word.lower():title.lower()})
                word_for_facts = title
                if len(page_words_list) >= count_of_words:
                    break
                else:
                    continue
            
            if (all([i in get_content_text(title) for i in target_words]) or\
               any([i in raw_category_item for i in get_category_item(word_request)])) and\
                word.lower() not in control_page_words_list:
                
                control_page_words_list.append(word.lower())
                page_words_list.append(word)
                [common_categories.append(i) for i in get_raw_category(title)]
                [common_words.append(i) for i in raw_category_item.split(' ')]
                dict_items.update({word.lower():title.lower()})
                word_for_facts = title
                if len(page_words_list) >= count_of_words:
                    break
            

    else:
        target_word = [
        item.lower()[:-2] if len(item) > 5 else item.lower()[:-1] if len(item) >= 4 else item.lower() for item in [user_word_request,]
                        ]
        target_word = target_word[0]
        user_word = target_word
        
        for title in words_page:
            if time.mktime(time.gmtime()) - time_1 > 8 * count_of_words + 10:
                break
            if word_for_facts != '':
                facts += get_facts(word_for_facts)
            else:
                facts = facts
            if time.mktime(time.gmtime()) - time_1 > delta and len(facts) > 1:
                fact = facts[randint(0, len(facts)-1)]
                if len(fact) > 10:
                    print_fact(fact)
                #sys.stdout.write('\r' + facts[randint(0, len(facts)-1)])
                delta += 30
            try:
                raw_category_item = ' '.join(get_raw_category(title))
                raw_category_item = raw_category_item.lower()
            except:
                continue
            word = get_title(title)
            word = format_word(word, raw_category_item, user_word, target_word)

            if word == '---':
                continue

            if (target_word in raw_category_item or\
                target_word in get_content_text(title)) and\
                word.lower() not in control_page_words_list:
                control_page_words_list.append(word.lower())
                page_words_list.append(word)
                [common_categories.append(i) for i in get_raw_category(title)]
                [common_words.append(i) for i in raw_category_item.split(' ')]
                dict_items.update({word.lower():title.lower()})
                word_for_facts = title

            if len(page_words_list) == count_of_words:
                break
    
    return page_words_list, dict_items, #sort_count_category(common_categories, 3), sort_count_category(common_words, 15)

def get_raw_category(word_request):
    #URL = 'https://ru.wikipedia.org/w/api.php?action=parse&prop=categories&format=json&page=' + url_decoder(word_request)
    #try:
    #    page = requests.get(URL).json()['parse']['categories']
    #except:
    URL = 'https://ru.wikipedia.org/w/api.php?action=opensearch&search='+url_decoder(word_request)+'&format=json'
    new_url = requests.get(URL).json()[3][0]
    page = requests.get(new_url).content
    html_tree = html.fromstring(page.decode('UTF-8'))
    items = html_tree.xpath(".//div[contains(@class,'mw-normal-catlinks')]/ul/li/a")
    page = [i.text for i in items]
    category_list = []
    for i in page:
        if 'Вики' not in i and 'Страницы' not in i:
            category_list.append(i)
    category_list = [i.lower() for i in category_list]
    category_list = [i.replace('_', ' ') for i in category_list]
    return category_list

def format_word(title, raw_category_item, user_words, target_words):

    try:
        words = title.split(' ')
    except:
        return '---'

    if '(значения)' in words:
        words.remove('(значения)')
    
    # Возвращение аббривеатур
    for word in words:
        if all([letter.isupper() == True for letter in word]) == True:
            return word

    # Пропуск запросов с предлогами
    if any([morph.parse(item)[0].tag.POS == 'PREP' for item in words]) == True:
        return '---'

    # Пропуск праздников
    if 'праздник' in raw_category_item:
        return '---'

    if len(words) == 1 and '-' in words[0]:
        return words[0].split('-')[0]
        
    # Проверка имён
    if 'родившиеся' in raw_category_item:
        if ',' in title:
            return words[0][:-1]
        if ')' in title:
            return words[0]
        else:
            return words[-1]

    if len(words) == 2:

        if morph.parse(words[0])[0].tag.POS == 'ADJF' and any([i in words[0].lower() for i in user_words + target_words]) == True:
            return words[1]

        if morph.parse(words[1])[0].tag.POS == 'ADJF' and any([i in words[1].lower() for i in user_words + target_words]) == True:
            return words[0]

        if morph.parse(words[0])[0].tag.number == 'sing' and morph.parse(words[0])[0].tag.POS == 'ADJF':
            return words[0]

        if morph.parse(words[1])[0].tag.number == 'sing' and morph.parse(words[1])[0].tag.POS == 'ADJF':
            return words[0]

    if len(words) == 3:
        for item in words:
            p = morph.parse(item)[0]
            if p.tag.POS == 'NOUN':
                return item
    else:
        word = words[0]
        return word
    
    
def filter_items(items):
    filter_list = []
    page_words = [i.get('title') if isinstance(i.text, str) == True and isinstance(i.get('title'), str) == True else 0 for i in items]
    #page_words = items
    for raw_word in page_words:
        if raw_word == 0:
            continue
        if any([i.isdigit() == True for i in raw_word]):
            continue
        if any([len(item) == 1 for item in raw_word.split(' ')]) == True:
            continue
        if len(raw_word) < 2 or len(raw_word.split(' ')) > 3:
            continue
        if any([morph.parse(item)[0].tag.POS == 'PREP' for item in raw_word.split(' ')]) == True:
            continue
        if any(i in raw_word.lower() for i in ['редактировать', 'отсутствует', 'википедия', 'портал', ':', '-', '.', 'значения']) == True:
            continue
        filter_list.append(raw_word)
    filter_list = list(set(filter_list))
    filter_list = [i.split(' ') for i in filter_list]
    filter_list.sort(key=len)
    filter_list = [' '.join(i) for i in filter_list]
    #filter_list.sort(key=len)
    return filter_list

def sort_count_category(common_categories, n):
    for category in common_categories:
        if any([i in category for i in ['статьи',]])==True:
            common_categories.remove(category)
    
        
    count_categories = [common_categories.count(i) for i in common_categories]
    count_categories.sort(reverse=True)
    count_category_list = []
    for count in count_categories:
        for category in common_categories:
            if common_categories.count(category) == count and category not in count_category_list and len(count_category_list) < n:
                count_category_list.append(category)
    return list(set(count_category_list))


def get_content_text(word):
    URL = 'https://ru.wikipedia.org/wiki/' + url_decoder(word)
    page = requests.get(URL).content
    html_tree = html.fromstring(page.decode('UTF-8'))
    items = html_tree.findall(".//a")
    content_list = [i.text if isinstance(i.text, str) == True else ' ' for i in items]
    content_text = ' '.join(content_list)[:200]

    text_items = html_tree.xpath(".//p")
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
    return content_text + new_item[:400]


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

