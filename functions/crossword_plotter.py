import matplotlib.pyplot as plt
import numpy as np
from random import randint
import sys
from wiki_crossword.functions.get_definitions import *

class Error(Exception):
    """Base class for other exceptions"""
    pass

class InvalidList(Error):
    """Raised when the input value is too small"""
    pass



# Функция получения рандомного списка слов заданного количества
def random_order(list_words, n_words=None):
    if n_words == None:
      n_words = len(list_words)
    random_list = []
    random_items = []
    while len(random_list) < n_words:
      a = randint(0, len(list_words) - 1)
      if a not in random_list:
        random_list.append(a) 
      else:
        continue
    [random_items.append(list_words[r]) for r in random_list]
    return random_items

# Функция получения списка координат-исключений
def exec_list_new(list_coords):
    list_exc = []
    for x, y in list_coords:
        list_exc.append((x+1,y))
        list_exc.append((x-1,y))
        list_exc.append((x,y+1))
        list_exc.append((x,y-1))
    return list(set(list_exc) - set(list_coords))

# Функция поиска координат с одинаковыми буквами
def find_coords(letter, dict_for_find):
  indexes = []
  for i, value in enumerate(dict_for_find.values()):
    if value == letter:
      indexes.append(i)
  coords = []
  for i in indexes:
    coords.append(list(dict_for_find.keys())[i])
  return coords

# Функция поиска индексов при печати индексов в одной ячейке
def i_search(data_dict, cur_list):
  for key, value in data_dict.items():
    if cur_list[0] == value[0][0]:
      return value[2]
  return None

# Функция поиска списка недоступных для печати координат
def non_free_coords(common_coord):
  non_free_coord = [common_coord, ]
  non_free_coord.append([common_coord[0], common_coord[1]+1])
  non_free_coord.append([common_coord[0], common_coord[1]-1])
  non_free_coord.append([common_coord[0]+1, common_coord[1]])
  non_free_coord.append([common_coord[0]-1, common_coord[1]])
  non_free_coord = [tuple(x) for x in non_free_coord]
  return non_free_coord

# Функция обновления свободных для печати координат
def refresh_free_coords(dict_refresh, coords):
  for k in coords:
    if k in dict_refresh.keys():
      dict_refresh.pop(k)
  return dict_refresh

# Функция обновления свободных для печати координат
def set_letters(list_word, word_except):
  set_letter = set()
  list_except = list_word.copy()
  list_except.remove(word_except)
  for word in list_except:
    for letter in word:
      set_letter.add(letter)
  return len(set(word_except) & set_letter)

# Функция поиска одинаковых букв кроссворда и нового слова
def same_letter(second_coords, word, base_data_dict, first_coord, horisontal = True):
  second_coord = second_coords.copy()
  if second_coord == []:
    return None
  second_coord.remove(first_coord)
  same_coords = list(set(second_coord) & set(base_data_dict.keys()))
  if  len(same_coords) > 0:
      if horisontal == True:
        second_coords.sort(key=sum, reverse=False)
      if horisontal == False:
        second_coords.sort(key=sum, reverse=True)

      touch_list_base = list(base_data_dict.keys())
      touch_list_word = second_coord.copy()
      [touch_list_word.remove(same_coord) for same_coord in same_coords]
      [touch_list_base.remove(same_coord) for same_coord in same_coords]
      touch_list_base.remove(first_coord)

      for touch_coord in touch_list_word:
          if 1.0 in [abs(x[0]-touch_coord[0])+abs(x[1]-touch_coord[1]) for x in touch_list_base]:
            answer= False
            return False

      if all([
              True if word[second_coords.index(same_coord)] == base_data_dict[same_coord] and horisontal == True else False for same_coord in same_coords
              ]) == True:
          answer = True
          return answer


      if all([
              True if word[second_coords.index(same_coord)] == base_data_dict[same_coord] and horisontal == False else False for same_coord in same_coords
              ]) == True:
          answer = True
          return answer

      else:
        return False
  else:
      return False

# Функция поиска всех индексов буквы в слове
def find_index(word, letter):
  index_list = []
  for i, item in enumerate(word):
    if letter == item:
      index_list.append(i)
  return index_list

# Функция получения горизонтальных координат слова
def get_coord_horisontal(word, dict_vertical, base_data_dict, none_free_list, none_touch_list):    
    second_coords = []
    list_coords = list(base_data_dict.keys())
    for letter in word:
        if letter in list(dict_vertical.values()):
            coords = find_coords(letter, dict_vertical)
        else:
            continue
        coords = random_order(coords)
        for coord in coords:
            first_dot = coord  
            if first_dot in none_free_list:
                continue
            list_control = list_coords.copy()
            list_control.remove(first_dot)
            
            for index in find_index(word, letter):
                one_side = index
                for i in range(1,one_side+1):
                    second_coords.append((first_dot[0]-i, first_dot[1]))
                other_side = len(word) - index
                for i in range(other_side):
                    second_coords.append((first_dot[0]+i, first_dot[1]))
                
                none_touch_list = exec_list_new(second_coords)
    
    
                none_touch_list.remove((first_dot[0], first_dot[1]-1))
                none_touch_list.remove((first_dot[0], first_dot[1]+1))
    
                
                if True in list(map(lambda x: True if x in list_control else False, none_touch_list)) and same_letter(second_coords, word, base_data_dict, first_dot) == False:
                    second_coords = []
                    continue
                if True in list(map(lambda x: True if x in list_control else False, none_touch_list)) and same_letter(second_coords, word, base_data_dict, first_dot) == True:
                    break
                if True not in list(map(lambda x: True if x in list_control else False, none_touch_list)):
                    break

            if True in list(map(lambda x: True if x in list_control else False, none_touch_list)) and same_letter(second_coords, word, base_data_dict, first_dot) == False:
                second_coords = []
                continue
            if True in list(map(lambda x: True if x in list_control else False, none_touch_list)) and same_letter(second_coords, word, base_data_dict, first_dot) == True:
                break
            if True not in list(map(lambda x: True if x in list_control else False, none_touch_list)):
                break
                
        if True in list(map(lambda x: True if x in list_control else False, none_touch_list)) and same_letter(second_coords, word, base_data_dict, first_dot) == False:
            second_coords = []
            continue
        if True in list(map(lambda x: True if x in list_control else False, none_touch_list)) and same_letter(second_coords, word, base_data_dict, first_dot) == True:
            break
        if True not in list(map(lambda x: True if x in list_control else False, none_touch_list)):
            break
    second_coords.sort(key=sum)
    return second_coords, first_dot

# Функция получения вертикальных координат слова
def get_coord_vertical(word, dict_vertical, base_data_dict, none_free_list, none_touch_list):    
    second_coords = []
    list_coords = list(base_data_dict.keys())
    for letter in word:
        if letter in list(dict_vertical.values()):
            coords = find_coords(letter, dict_vertical)

        else:
            continue
        coords = random_order(coords)
        for coord in coords:
            first_dot = coord
            if first_dot in none_free_list:
                continue
            list_control = list_coords.copy()
            list_control.remove(first_dot)
            
            for index in find_index(word, letter):
                one_side = index
                for i in range(1,one_side+1):
                    second_coords.append((first_dot[0], first_dot[1]+i))
                other_side = len(word) - index
                for i in range(other_side):
                    second_coords.append((first_dot[0], first_dot[1]-i))
            
                none_touch_list = exec_list_new(second_coords)
    
                none_touch_list.remove((first_dot[0]-1, first_dot[1]))
                none_touch_list.remove((first_dot[0]+1, first_dot[1]))
                
                if True in list(map(lambda x: True if x in list_control else False, none_touch_list)) and same_letter(second_coords, word, base_data_dict, first_dot, horisontal = False) == False:
                    second_coords = []
                    continue
                if True in list(map(lambda x: True if x in list_control else False, none_touch_list)) and same_letter(second_coords, word, base_data_dict, first_dot, horisontal = False) == True:
                    break
                if True not in list(map(lambda x: True if x in list_control else False, none_touch_list)):
                    break
            if True in list(map(lambda x: True if x in list_control else False, none_touch_list)) and same_letter(second_coords, word, base_data_dict, first_dot, horisontal = False) == False:
                second_coords = []
                continue
            if True in list(map(lambda x: True if x in list_control else False, none_touch_list)) and same_letter(second_coords, word, base_data_dict, first_dot, horisontal = False) == True:
                break
            if True not in list(map(lambda x: True if x in list_control else False, none_touch_list)):
                break
        if True in list(map(lambda x: True if x in list_control else False, none_touch_list)) and same_letter(second_coords, word, base_data_dict, first_dot, horisontal = False) == False:
            second_coords = []
            continue
        if True in list(map(lambda x: True if x in list_control else False, none_touch_list)) and same_letter(second_coords, word, base_data_dict, first_dot, horisontal = False) == True:
            break
        if True not in list(map(lambda x: True if x in list_control else False, none_touch_list)):
            break
    second_coords.sort(key=sum, reverse=True)
    return second_coords, first_dot

# Функция построения слов по горизонтали
def plot_word_horiz(word, coordinates, ax, item, color_words):
    x = coordinates[0][0]-0.5
    y = coordinates[0][1]-0.5
    ax.plot(x+0.2,y+0.8,marker='$'+str(item+1)+'$', markersize=10, c='black')
    w_line = np.linspace(y, y+1, 10)
    h_line = np.linspace(x, x+len(word), 10)
    ax.plot(h_line,np.linspace(y,y,10), color='black')
    ax.plot(h_line,np.linspace(y+1,y+1,10), color='black')
    for i, letter in enumerate(word):
        ax.plot(np.linspace(x+i,x+i,10),w_line, color='black')
        ax.scatter(coordinates[0][0]+i,coordinates[0][1],marker='$'+letter+'$', s=150, color=color_words)
    i+=1
    ax.plot(np.linspace(x+i,x+i,10),w_line, color='black')

# Функция построения слов по вертикали
def plot_word_vert(word, coordinates, ax, item, color_words):
    x = coordinates[0][0] - 0.5
    y = coordinates[0][1] + 0.5
    ax.plot(x+0.2,y-0.2,marker='$'+str(item+1)+'$', markersize=10, c='black')
    w_line = np.linspace(y, y-len(word), 10)
    h_line = np.linspace(x, x+1, 10)
    ax.plot(np.linspace(x,x,10), w_line, color='black')
    ax.plot(np.linspace(x+1,x+1,10), w_line, color='black')
    for i, letter in enumerate(word):
        ax.plot(h_line,np.linspace(y-i,y-i,10), color='black')
        ax.scatter(coordinates[i][0],coordinates[i][1], marker='$'+letter+'$', s=150, color=color_words)
    i+=1
    ax.plot(h_line,np.linspace(y-i,y-i,10), color='black')
    
# Функция добавления координат в список
def list_coord_append(base_list, new_list):
    for i, item in enumerate(new_list):
        base_list.append(str(item[0])+','+str(item[1]))
    return base_list

# Функция печати кроссворда
def print_words(words, n_words=None, definitions=dict(), random_sort=True, answers=True, plot=True, request_word=str()):
    if n_words == None:
      n_words = len(words)
    if n_words > len(words):
      sys.stdout.write(f'\rОбщее число найденных слов - {len(words)}. Задано при построении - {n_words}!')
      return None
    number_of_try = 0
    if answers==True:
        color_words='black'
    else:
        color_words='white'
    if np.array([1 if set_letters(words, i) > 0 else 0 for i in words]).sum() != len(words):
        sys.stdout.write('\rНевозможно составить кроссворд!')
        return None
    while True:
        number_of_try += 1
        try:
            if number_of_try > 200:
                raise InvalidList('Слишком много итераций, попробуйте изменить слова или сократить список слов')
        except:
            print('\nСлишком много итераций, попробуйте изменить слова или сократить список слов')
            return None
        try:
            if random_sort == True:
                order_list = random_order(words, n_words)
            else:
                order_list = words[:n_words]
            base_data_dict = dict()
            data_dict = dict()  # все слова со всеми координатами и ориентацией
            data_dict_vertical = dict()  # координаты и буквы всех вертикалей
            data_dict_horizontal = dict()  # координаты и буквы всех горизонталей
            none_free_list = list()    # координаты в которых никак не может быть вторых слов
            none_touch_list = list()   # координаты котрые находятся в касании всех слов
        
            list_coords = []
            corrector_index = 0
            first_word = order_list[0]
            len_word = len(first_word)
            x, y = len_word//2, len_word//2
            fig, ax = plt.subplots(2,1, gridspec_kw={'height_ratios': [1000, 1]})
            ax[0].set_axis_off()
            ax[1].set_axis_off()
            first_coordinates = [[x_0+0.5+x,y+0.5] for x_0 in range(len_word)]
            plt.subplots_adjust(hspace=0.01)

            for i,word in enumerate(order_list):
                if i == 0:
                    true_i = i
                    orientation = 'По горизонтали'
                    plot_word_horiz(word, first_coordinates, ax[0], true_i, color_words)
                    list_coords = list_coord_append(list_coords, first_coordinates)
                    first_coordinates = [tuple(x) for x in first_coordinates]
        
                    # Заполнение горизонтальных координат
                    data_dict_horizontal.update(dict(zip([tuple(x) for x in first_coordinates], word)))
                    
                    # Заполнение общего словаря, слово, координаты, ориентация
                    data_dict[word] = [first_coordinates, orientation, true_i]
                    
                    # Заполнение общего словаря со всеми буквами
                    base_data_dict.update(dict(zip(first_coordinates, word)))
                    none_touch_list += exec_list_new(first_coordinates)
        
            
                    first_word = word
                    continue
                if i == 1:
                    orientation = 'По вертикали'
                    cur_list, base_coord = get_coord_vertical(word, data_dict_horizontal, base_data_dict, none_free_list, none_touch_list)

                    true_i = i_search(data_dict, cur_list)
                    if true_i != None:
                      corrector_index += 1
                    else:
                      true_i = i

                    plot_word_vert(word, cur_list, ax[0], true_i, color_words)
                    list_coords = list_coord_append(list_coords, cur_list)
                    cur_list = [tuple(x) for x in cur_list]

                    data_dict_vertical.update(dict(zip(cur_list, word)))
                    data_dict[word] = [cur_list, orientation, true_i]
                    base_data_dict.update(dict(zip(cur_list, word)))
                    none_touch_list += exec_list_new(cur_list)
                    none_free_list += non_free_coords(base_coord)
        
                    data_dict_horizontal = refresh_free_coords(data_dict_horizontal, none_free_list)
                    data_dict_vertical = refresh_free_coords(data_dict_vertical, none_free_list)
        
                    first_word = word
                    continue
                if i % 2 == 0:
                    try:
                        orientation = 'По горизонтали'
                        cur_list, base_coord = get_coord_horisontal(word, data_dict_vertical, base_data_dict, none_free_list, none_touch_list)

                        true_i = i_search(data_dict, cur_list)
                        if true_i != None:  
                          corrector_index += 1
                        else:
                          true_i = i
                          true_i -= corrector_index

                        plot_word_horiz(word, cur_list, ax[0], true_i, color_words)
                        list_coords = list_coord_append(list_coords, cur_list)
                        cur_list = [tuple(x) for x in cur_list]

                        data_dict_horizontal.update(dict(zip(cur_list, word)))
                        data_dict[word] = [cur_list, orientation, true_i]
                        base_data_dict.update(dict(zip(cur_list, word)))
        
                        none_touch_list += exec_list_new(cur_list)
                        none_free_list += non_free_coords(base_coord)

                        data_dict_horizontal = refresh_free_coords(data_dict_horizontal, none_free_list)
                        data_dict_vertical = refresh_free_coords(data_dict_vertical, none_free_list)
        
                        first_word = word
                    except:
                        orientation = 'По вертикали'
                        cur_list, base_coord = get_coord_vertical(word, data_dict_horizontal, base_data_dict, none_free_list, none_touch_list)
    
                        true_i = i_search(data_dict, cur_list)
                        if true_i != None:  
                          corrector_index += 1
                        else:
                          true_i = i
                          true_i -= corrector_index

                        plot_word_vert(word, cur_list, ax[0], true_i, color_words)
                        list_coords = list_coord_append(list_coords, cur_list)
                        cur_list = [tuple(x) for x in cur_list]
        
                        data_dict_vertical.update(dict(zip(cur_list, word)))
                        data_dict[word] = [cur_list, orientation, true_i]
                        base_data_dict.update(dict(zip(cur_list, word)))
        
                        none_touch_list += exec_list_new(cur_list)
                        none_free_list += non_free_coords(base_coord)
        
                    
        
                        data_dict_vertical = refresh_free_coords(data_dict_vertical, none_free_list)
                        data_dict_horizontal = refresh_free_coords(data_dict_horizontal, none_free_list)
        
                        first_word = word
                        
                if i % 2 == 1:
                    try:
                        orientation = 'По вертикали'
                        cur_list, base_coord = get_coord_vertical(word, data_dict_horizontal, base_data_dict, none_free_list, none_touch_list)
    
                        true_i = i_search(data_dict, cur_list)
                        if true_i != None:  
                          corrector_index += 1
                        else:
                          true_i = i
                          true_i -= corrector_index

                        plot_word_vert(word, cur_list, ax[0], true_i, color_words)
                        list_coords = list_coord_append(list_coords, cur_list)
                        cur_list = [tuple(x) for x in cur_list]
        
                        data_dict_vertical.update(dict(zip(cur_list, word)))
                        data_dict[word] = [cur_list, orientation, true_i]
                        base_data_dict.update(dict(zip(cur_list, word)))
        
                        none_touch_list += exec_list_new(cur_list)
                        none_free_list += non_free_coords(base_coord)
        
                    
        
                        data_dict_vertical = refresh_free_coords(data_dict_vertical, none_free_list)
                        data_dict_horizontal = refresh_free_coords(data_dict_horizontal, none_free_list)
        
                        first_word = word
                    except:
                        orientation = 'По горизонтали'
                        cur_list, base_coord = get_coord_horisontal(word, data_dict_vertical, base_data_dict, none_free_list, none_touch_list)

                        true_i = i_search(data_dict, cur_list)
                        if true_i != None:  
                          corrector_index += 1
                        else:
                          true_i = i
                          true_i -= corrector_index

                        plot_word_horiz(word, cur_list, ax[0], true_i, color_words)
                        list_coords = list_coord_append(list_coords, cur_list)
                        cur_list = [tuple(x) for x in cur_list]

                        data_dict_horizontal.update(dict(zip(cur_list, word)))
                        data_dict[word] = [cur_list, orientation, true_i]
                        base_data_dict.update(dict(zip(cur_list, word)))
        
                        none_touch_list += exec_list_new(cur_list)
                        none_free_list += non_free_coords(base_coord)

                        data_dict_horizontal = refresh_free_coords(data_dict_horizontal, none_free_list)
                        data_dict_vertical = refresh_free_coords(data_dict_vertical, none_free_list)
        
                        first_word = word

            if plot == True:
                
                x_s = [float(i.split(',')[0]) for i in list_coords]
                y_s = [float(i.split(',')[1]) for i in list_coords]

                x_min = min(x_s)
                y_min = min(y_s)

                x_max = max(x_s)
                y_max = max(y_s)

                width = int(x_max - x_min)
                height = int(y_max - y_min)

                definitions = create_definition(data_dict, definitions)
                new_def = ['\n'+x+'\n\n' if x=='По горизонтали:' or x=='По вертикали:'  else x+'\n' for x in definitions]
                new_def = ''.join(new_def)
                y_min -= new_def.count('\n')
                x_min -= 1
            
        except: 
            text = '\r'+'Попытка построения '+str(number_of_try)
            sys.stdout.write(text)
            plt.close()
            continue
        else:
            if plot == True:
                if request_word == 'Своя тема':
                    theme = 'Кроссворд на свою тему'
                else:
                    theme = 'Кроссворд на тему\n"'+request_word+'"'
                ax[0].text((x_max - abs(x_min))/2+3, y_max+2, theme, ha='center', rotation=0, wrap=True, fontsize=25)
                ax[1].text(0,
                           0,
                           new_def,
                           ha='left',
                           rotation=0,
                           wrap=True,
                           fontsize=20,
                           fontstyle='italic',
                           verticalalignment='top')
                fig.set_figwidth(width)
                fig.set_figheight(height)
                text = '\r'+'Поздравляем! Кроссворд составлен!'
                sys.stdout.write(text)
                plt.show()
            else:
                plt.close()
            break
