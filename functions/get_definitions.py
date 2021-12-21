import  re
from wiki_crossword.functions.url_searcher import *

# Функция поиска определений
def definition_search(words, dict_titles):
    list_def = []
    list_simplicity = []
    dict_def = dict()
    name=str()
    def_item = False
    for word in words:
        if word in dict_titles.keys() and len(dict_titles[word].split(' ')) <= 3:
            try:
                URL = 'https://ru.wikipedia.org/w/api.php?action=opensearch&search='+url_decoder(dict_titles[word])+'&format=json'
                URL = requests.get(URL).json()[3][0]
            except:
                definition = dict_titles[word]
                continue
        elif word in dict_titles.keys() and len(dict_titles[word].split(' ')) > 3:
            definition = dict_titles[word]
            continue
        else:
            URL = 'https://ru.wikipedia.org/w/api.php?action=opensearch&search='+url_decoder(word.lower())+'&format=json'
            URL = requests.get(URL).json()[3][0]
        page = requests.get(URL).content
        html_tree = html.fromstring(page.decode('UTF-8'))

        category_list = search_category(html_tree, word)[1]

        try:
            if category_list[0] == 'Страницы значений по алфавиту':
                items = html_tree.xpath(".//div[contains(@class,'mw-parser-output')]/ul/li/a")
                current_url = [i.get('href') for i in items][0]
                URL = word_url+current_url[6:]
                page = requests.get(URL).content
                html_tree = html.fromstring(page.decode('UTF-8'))
        except:
            try:
                URL = 'https://ru.wikipedia.org/w/index.php?search='+url_decoder(
                    word
                )+'&title=%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F%3A%D0%9F%D0%BE%D0%B8%D1%81%D0%BA&go=%D0%9F%D0%B5%D1%80%D0%B5%D0%B9%D1%82%D0%B8&ns0=1'
                page = requests.get(URL).content
                html_tree = html.fromstring(page.decode('UTF-8'))
                items = html_tree.xpath(".//div[contains(@class,'mw-search-result-heading')]/a")
                current_url = [i.get('href') for i in items][0]
                URL = word_url+current_url[6:]
            
                page = requests.get(URL).content
                html_tree = html.fromstring(page.decode('UTF-8'))
            except:
                if def_item == False:
                    words.remove(word)
                    continue
                else:
                    definition = dict_titles[word]

        try:
            items_list = html_tree.xpath(".//div[contains(@class,'mw-parser-output')]/p/node()") + [html_tree.xpath(".//div[contains(@class,'mw-parser-output')]/ul/li/node()")[1],]
        except:
            items_list = html_tree.xpath(".//div[contains(@class,'mw-parser-output')]/p/node()")
        if len(items_list)==0 and def_item == False:
            words.remove(word)
            continue
        elif len(items_list)==0 and def_item == True:
            definition = dict_titles[word]
        if def_item == True:
            definition = dict_titles[word]
        else:
            definition = str()
        for item in items_list:
            if isinstance(item, str)==False:
                definition += str(item.text)
            else:
                definition += item
            try:
                if '.\n' in item:
                    break
            except:
                if '\n' in item:
                    break

        definition = definition.replace('\xa0', ' ')
        definition = definition.replace(':\n', '.')
        definition = definition.replace('\n', '.')
        definition = definition.replace('none', '')
        definition = definition.replace('None', '')

        try:
            re_three = r'[A-z]\w+'
            latin = re.findall(re_three, definition)
            for lat in latin:
                try:
                    index_lat = definition.index(lat)
                except:
                    continue
                index_bracket_1 = index_lat + definition[index_lat:].index(')') + 1
                index_bracket_0 = len(definition[index_lat::-1]) - definition[index_lat::-1].index('(') - 1
                definition = definition.replace(definition[index_bracket_0: index_bracket_1],'')
        except:
            pass
      
        # Поиск имен
        re_one = r'[А-Я]. [А-Я]. [А-Я]\w+'
        re_two = r'[А-Я]. [А-Я]\w+'
        try:
            name = re.search(re_one, definition).group()
            if name in definition:
                definition = definition.replace(name, 'n'*len(name))
        except:
            try:
                name = re.search(re_two, definition).group()
                if name in definition:
                    definition = definition.replace(name, 'n'*len(name))
            except:
              definition = definition
        
        if ' или ' in definition and definition.index(' или ') < len(word)+5:
            definition = definition.replace(' или ', ' - ')
    
        if 'это ' in definition.lower() and definition.lower().index('это ') < len(word)+5:
            definition = definition.replace('это ', '- ')
            definition = definition.replace('Это ', '- ')
        
        try:
            if '(' in definition.lower() and definition.lower().index('(') < len(word)*2:
                index_finish_0 = definition.index(')')+1
                definition_new = definition[index_finish_0:]
                if len(definition_new) < 5:
                    definition = definition
                else:
                    definition = definition_new
        except:
            definition = definition
        
        
        try:
            if '(от ' in definition.lower() and definition.lower().index('(от ') < 20:
                index_start_1 = definition.index('(от ')+1
                index_finish_1 = index_start_1 + definition[index_start_1:].index(')')+1
                definition = definition[index_finish_1:]
        except:
            definition = definition
        try:    
            try:
                index_start = definition.index('—')+2
            except:
                index_start = definition.index('-')+2
            index_finish = index_start + definition[index_start:].index('.')+1
            if len(definition[index_start:index_finish]) < 20:
                index_finish = index_finish + definition[index_finish:].index('.')+1

            definition = definition[index_start:index_finish]
        except:
            definition=definition

        
        definition = definition.strip()
        definition = definition.replace('(none)', '')
        definition = definition.replace(' , ', ', ')
        definition = definition.replace('..', '.')
        definition = definition.replace(' ()', '')
        definition = definition.replace('и т.', 'и т.д.')
        definition = definition.replace('(лат.', '')
        definition = definition.strip()
        if definition[-1] != '.':
            definition+='.'
 
    
        for i, symbol in enumerate(definition):
            if symbol == ')' and '(' not in definition:
                definition = definition[i+1:]
                break
            if symbol == '(' and ')' not in definition:
                #definition = definition[i+1:]
                break
        for i, symbol in enumerate(definition):
            if symbol.isalpha() == True:
                definition = definition[i:]
                break

        definition = definition.replace(')', '')
        definition = definition.replace('(', '')
        definition = definition.replace('[', '')
        definition = definition.replace(']', '')
        definition = definition.replace('  ', ' ')
        definition = definition.replace(' ,', ',')

        if word in definition:
            definition.replace(word, '')

        definition = definition[:1].capitalize() + definition[1:]
        definition = definition.replace('n'*len(name), name)



        list_def.append(definition)
        dict_def[word] = definition
    dict_titles.update(dict_def)
    return correct_answers(dict_titles)

# Функция сортировки определений
def sort_definitions(definotions):
  dict_defs = dict()
  for definition in definotions:
    index = definition.index(')')
    dict_defs[int(definition[:index])] = definition[index:]
  list_sort = list(dict_defs.keys())
  list_sort.sort()
  new_definitions = [str(key) + dict_defs[key] for key in list_sort]
  return new_definitions

def cutter_text(text, width=60):
    i = 0
    try:
        while [max(len(x) for x in text.split('\n'))][0] > width+15:
            index_reset = text.split('\n')[i][width:].index(' ')+width + len(text) - len(text.split('\n')[i])
            text = text[:index_reset]+text[index_reset:index_reset+1].replace(' ', '\n')+'\t\t\t\t'+text[index_reset+1:]
            i += 1
    except:
        return None
    return text

# Функция предобработки определений
def create_definition(data_dict, dict_def):
  definitions = []
  orientation_list = [data_dict[x][1] for x in data_dict.keys()]
  for w in data_dict.keys():
    i = 0
    defs_new = cutter_text(dict_def[w])

    definitions.append(defs_new)

  horizontal_def = []
  vertical_def = []
  for i, [key, value] in enumerate(data_dict.items()):
    index = value[2]
    orientation = value[1]
    if orientation == 'По горизонтали':
      horizontal_def.append(str(index+1) + ') ' + definitions[i])
    else:
      vertical_def.append(str(index+1) + ') ' + definitions[i])
  horizontal_def = sort_definitions(horizontal_def)
  horizontal_def = ['По горизонтали:', ] + horizontal_def
  vertical_def = sort_definitions(vertical_def)
  vertical_def = ['По вертикали:', ] + vertical_def
  definitions = horizontal_def + vertical_def
  return definitions

def get_answers(data_dict):
    horisontal_answers = ''
    vertical_answers = ''
    for k,v in data_dict.items():
        if v[1] == 'По горизонтали':
            horisontal_answers += (str(v[2]+1)+') '+k.capitalize()) + ', '
        else:
            vertical_answers += (str(v[2]+1)+') '+k.capitalize()) + ', '
    horisontal_answers = cutter_text(horisontal_answers[:-2]+'.', 50)
    vertical_answers = cutter_text(vertical_answers[:-2]+'.', 50)
    answers = 'Ответы:\nПо горизонтали\n\t\t\t\t' + horisontal_answers + '\n' + 'По вертикали\n\t\t\t\t' + vertical_answers
    return answers



def correct_answers(dict_words):
    dict_for_iterations = dict_words.copy()
    for item in dict_for_iterations.keys():
        if len(item.split(' ')) == 1:
            continue
        else:
            new_item = format_word(item, target_words = dict_words[item], raw_category_item = '', user_words = '')
            if item != new_item:
                dict_words[new_item] = dict_words[item]
                dict_words.pop(item)
                
            curt_item = [
            new_item.lower()[:-2] if len(new_item) > 5 else new_item.lower()[:-1] if len(new_item) >= 4 else new_item.lower() for item in [new_item,]
                        ][0]
            definitions = dict_words[new_item].split(' ')
            if curt_item in dict_words[new_item] and len(definitions) > 0:
                for definition in definitions:
                    if curt_item not in definition.lower() and len(definition) > 50:
                        dict_words[new_item] = definition
                        continue
    return dict_words



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
