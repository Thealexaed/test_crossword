# Функция получения входных данных и построения кроссворда
import sys
from wiki_crossword.functions.get_words import find_words
from wiki_crossword.functions.get_definitions import definition_search
from wiki_crossword.functions.crossword_plotter import print_words

def get_crossword(request_word, count_of_words, print_answers, difficult):
  difficult_dict = {
    'Легко':1,
    'Средне':0.8,
    'Сложно':0.4,
    'Очень сложно':0.0,
  }
  difficult = difficult_dict[difficult]
  try:
    if request_word == '':
      print('Введите слово!')
    else:
      try:
        final_def(request_word, count_of_words, print_answers, difficult)
      except:
        sys.stdout.write('\rСлова не найдены! Уточните запрос!')
  except KeyboardInterrupt:
    sys.stdout.write('\rПроцесс остановлен!')
    pass


# Функция составления кроссворда
def final_def(word, count_of_words, print_answers, difficult):
    text = '\rИщу слова...'
    sys.stdout.write(text)
    if ',' in word:
      words = word.split(',')
      words = [word.strip() for word in words]
      request_word = 'Своя тема'
    else:
      words = find_words(word, count_of_words)
      request_word = word
    words = [i.lower() for i in words]
    if word.lower() not in words and ' ' not in word:
      words.append(word.lower())
    
    text = '\rИщу определения к словам...'
    sys.stdout.write(text)
    definitions = definition_search(words)
    words = list(definitions.keys())

    text = '\rИдет построение сканворда...'
    sys.stdout.write(text)

    print_words(words,
                n_words = count_of_words,
                random_sort=True,
                answers=print_answers,
                definitions=definitions,
                request_word=request_word, difficult=difficult)
