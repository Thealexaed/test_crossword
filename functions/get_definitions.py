import  re
from test_crossword.functions.url_searcher import *

# Функция поиска определений
def definition_search(words):
    list_def = []
    list_simplicity = []
    dict_def = dict()
    name=str()
    for word in words:
        URL = word_url+url_decoder(word.lower())    
        page = requests.get(URL).content
        html_tree = html.fromstring(page.decode('UTF-8'))

        category_list = search_category(html_tree)[1]

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
                words.remove(word)
                continue

        try:
            items_list = html_tree.xpath(".//div[contains(@class,'mw-parser-output')]/p/node()") + [html_tree.xpath(".//div[contains(@class,'mw-parser-output')]/ul/li/node()")[1],]
        except:
            items_list = html_tree.xpath(".//div[contains(@class,'mw-parser-output')]/p/node()")
        if len(items_list)==0:
            words.remove(word)
            continue
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
            if '(' in definition.lower() and definition.lower().index('(') < len(word)*2+20:
                index_finish_0 = definition.index(')')+1
                definition_new = definition[index_finish_0:]
                if len(definition_new) < 5:
                    definition = definition
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
    return dict_def

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

# Функция предобработки определений
def create_definition(data_dict, dict_def):
  definitions = []
  orientation_list = [data_dict[x][1] for x in data_dict.keys()]
  for w in data_dict.keys():
    i = 0
    defs_new = dict_def[w]
    while [max(len(x) for x in defs_new.split('\n'))][0] > 100:
      index_reset = defs_new.split('\n')[i][81:].index(' ')+81 + len(defs_new) - len(defs_new.split('\n')[i])
      defs_new = defs_new[:index_reset]+defs_new[index_reset:index_reset+1].replace(' ', '\n')+defs_new[index_reset+1:]
      i += 1
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
