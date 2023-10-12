#!/usr/bin/python3
import os
import sys
import contextlib

#ver 3
#рекурсивный проход по каталогам в поисках файлов
#поиск в каждом файле строки на русском языке в нескольких кодировках
#utf-8(Linux), koi8-r(Linux), cp866(DOS), cp1251(Windows)
#файл должен быть целиком в одной кодировке(формат - текстовый)

#поиск в каждом файле строки (подстроки) в указаной кодировке
def search_string_mcode_file(file_name, encoding_s, stroka_s):
  result_dict = dict()#словарь для найденных номеров строк и самих строк в которых найдена подстрока

  #счетчик номера строки в файле
  number_string = 0

  #искомая строка
  #перевод в нижний регистр
  stroka_search = stroka_s.lower()

  #открытие  файла в нужной кодировке,
  #далее построчное чтение файла (без загрузки всего его в память)  
  with open(file_name, 'r', encoding=encoding_s, errors='ignore') as f1:
    for read_string in f1:

      number_string += 1#после прочтения строки из файла увеличиваем счетчик на 1

      #перевод в нижний регистр
      #далее, поиск подстроки в строке в нижнем регистре
      #и печать строки из файла в первоначальном виде
      read_string1 = read_string.lower()
      if read_string1.find(stroka_search) != -1:#если подстрока найдена в строке...

        read_string = read_string.replace('\n','')#удаляем перевод строки в конце строки
        result_dict[number_string]=read_string#добавляем в словарь:  ключ - номер строки в файле, в которой надена подстрока, значение - строка вкотолрой найдена подстрока
        #result_dict['file encoding']=encoding_s#добавляем название кодировки поиска
        result_dict[0]=encoding_s#добавляем название кодировки поиска
  return result_dict#возвращаем словарь с результатами поиска в файле
#===



#функция, которая проходит по каталогам
def stroll_file_dir(dir):
  result_search = dict()
  fff_name = ''
  #подавляем вывод ошибок OSError (много запутанных взаимных ссылок на файлы)
  #подавляем исключение без try...except
  with contextlib.suppress(OSError):
    #заходим в каждый подкаталог текущего каталога
    for name in os.listdir(dir):
      path = os.path.join(dir, name)
      #если это файл то пишем его название и текущий каталог
      if os.path.isfile(path):

        #print("Каталог:", dir, "файл:", name)
        fff_name = dir+"/"+name
        #print("Файл:",dir+"/"+name)
        print("Файл:", fff_name )

        #поиск строки в файле, 4 кодировки c map
        #fff_string = 'приве'
        fff_string = find_string_m#принимаем строку поиска от пользователя

        #для запуска map создаем 3 списка одинокового размера (по 4)
        fff_name_lst = [fff_name, fff_name, fff_name, fff_name]
        fff_code_lst = ['utf-8', 'koi8-r', 'cp866', 'cp1251']        
        fff_string_lst = [fff_string, fff_string, fff_string, fff_string]
        
        #print(fff_name_lst, fff_code_lst, fff_string_lst)

        #список с результатами поиска строки в файле (список из 4 словарей)
        #каждый словарь - результаты поиска по одной кодировке
        result_search_lst =list(map(search_string_mcode_file, fff_name_lst, fff_code_lst, fff_string_lst ))
        #print(result_search_lst)
        
        #печать только удачных результатов поиска
        #если в списке пустой элемент-словарь, то не печатаем его
        #проходим по списку, где элементы словари
        for i in range(len(result_search_lst)):
          if len(result_search_lst[i]) != 0:
                        
            print('Результаты поиска :')
            print('Что искали :', fff_string)
            print('Что нашли :')
            #если словарь непустой, то создаем строку из его ключей и значений и печатаем ее
            print('[Номер строки] : [Строка, в которой найдено]')
            s_result = ''
            for i_dict in result_search_lst[i]:#проходим по всем ключам (кроме 0-го) каждого словаря
              if i_dict != 0:
                s_result += str(i_dict) + ' : ' + result_search_lst[i][i_dict] + '\n'
            
              if  i_dict == 0:#этому ключу словаря(его значению) присвоено название кодировки файла
                s_result2 = result_search_lst[i][i_dict]
            print(s_result)
            print('Кодировка:', s_result2)
            print('====================\n')
            #печать всех результатов поиска (и пустых, т е файлов в которых не найдено)


      #если это каталог, то запускаем(ся) фунцию рекурсивно
      else:
        stroll_file_dir(path)
#===

#получение параметров командной строки
#и проверка на корректность
def get_check_parameters_cli():

  result_param = ['','']#список возвращаемых параметров [каталог, строка]

  arguments = sys.argv[:]
  #print(type(arguments))

  #проверка количества параметров командной строки
  #если меньше 2 заданых - выходим
  if len(arguments) < 3:

    print('Не указаны параметры поиска: каталог поиска(dir) и строка(string)')
    print('Пример использования:\n')
    print(arguments[0], 'dir=/home/user99/test string="приве"')
    sys.exit()


  else:
    #print(arguments)
    #получаем значения параметра dir
    #даже если dir и string в командной строке поменяли местами (1 и 2)
    if arguments[1].find('dir=') != -1:
      arguments[1] = arguments[1].replace('dir=', '')
      result_param[0] = arguments[1]


    if arguments[2].find('dir=') != -1:
      arguments[2] = arguments[2].replace('dir=', '')
      result_param[0] = arguments[2]



    #получаем значения параметра string
    #даже если dir и string в командной строке поменяли местами (1 и 2)
    if arguments[1].find('string=') != -1:
      arguments[1] = arguments[1].replace('string=', '')
      result_param[1] = arguments[1]


    if arguments[2].find('string=') != -1:
      arguments[2] = arguments[2].replace('string=', '')
      result_param[1] = arguments[2]


    #если каталог поиска не найден или строка поиска пустая - выходим
    if (not os.path.exists(result_param[0])) or (not os.path.isdir(result_param[0])):
      print('Каталог поиска не найден !\n')
      sys.exit()

    if result_param[1] == '':
      print('Строка поиска не указана !\n')
      sys.exit()

  #возвращаем список с параметрами для поиска, если они правильные
  return result_param

#===

#Основная программа

#Получение верных параметров поиска
find_parameter = get_check_parameters_cli()
print(find_parameter)

#Задаем искомую строку
find_string_m = find_parameter[1]

#Задаем с какого каталога начинать рекурсивный поиск по файлам
find_dir = find_parameter[0]


#Запуск рекурсивного поиска
stroll_file_dir(find_dir)
