# -*- coding: utf-8 -*-
from parsers import *
from builtins import print
import sqlite3


# непонятная хрень,которая вроде как помогает с определителями дальше (хотя и без нее работает)
paramstyle = sqlite3.paramstyle
if paramstyle == 'qmark':
    ph = "?"
    ph1 = "?"
    ph2 = "?"
    ph3 = "?"
    ph4 = "?"
elif paramstyle == 'format':
    ph = "%s"
    ph1 = "%s"
    ph2 = "%s"
    ph3 = "%s"
    ph4 = "%s"
else:
    raise Exception("Unexpected paramstyle: %s" % paramstyle)
# конец непонятной хрени

# Вызов id городов по их именам, если имен нет, то вызываются все
def pars_cities (db_name, *kwargs):

    # инициализация указатедя
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    # конец инициализации

    project = []

    if len(kwargs) > 0:
        for kwarg in kwargs:

            for row in c.execute ("select id from Cities where City_Name_Short  = ?", (str(kwarg),)):
                project.append (row[0])
    else:
        for row in c.execute ("select id from Cities"):
            project.append (row[0])
    
    c.close()
    conn.close()

    return(project)


# функция по id города выдает link сайтов и id сайтов 
def pars_data (db_name, db_city_id):

    # инициализация указатедя
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    # конец инициализации

    project = []

    for row in c.execute ("select Refer, Site_id from Sites_links where Cities_id  = ?", (db_city_id,)):
        project.append (row)

    c.close()
    conn.close()

    return(project)
   
# конец функции


# Функция записи парса в базу данных 
def write_to_db (db_name, pars, db_city_id, db_syte_id):

    # инициализация указатедя
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    # конец инициализации

    # ------ цикл переноса записей из pars в базу
    i=0 #счетчик прогонов для корректной вставки в имя столбца
    for pars_1 in pars:

        varebles = {"ph": str(i)+"_day_day",                    # имя столбца в БД 
                    "ph1": str(i)+"_day_night",                 # имя столбца в БД 
                    "ph2": str(pars_1['datetime']),             # переменная даты из парса
                    "ph3": str(pars_1['day_temp']),             # переменная температуры из парса
                    "ph4": str(pars_1['night_temp']),           # переменная температуры из парса
                    "ph5": int(db_city_id),                     # id города для парса 
                    "ph6": int(db_syte_id),                     # id сайта для парса
                    }         
  
        c.execute("select * from Temps where Date ='%(ph2)s' and City_id = '%(ph5)s' and Site_id = '%(ph6)s'" % varebles) # проверка наличия текущей даты в базе

        if c.fetchone() is None: # если даты нет, то ее нужно создать и внести данные
        
            c.execute ("""insert into 
                          Temps ('Date', City_id, Site_id, '%(ph)s', '%(ph1)s') 
                          values ('%(ph2)s','%(ph5)s','%(ph6)s', '%(ph3)s', '%(ph4)s')""" % varebles)
            conn.commit()

        else: # если дата есть, то данные нужно обновить

            c.execute ("""update Temps
                        set  '%(ph)s'  =  '%(ph3)s',
                             '%(ph1)s'  =  '%(ph4)s' 
                        where Date = '%(ph2)s' and
                              City_id = '%(ph5)s' and 
                              Site_id = '%(ph6)s'""" % varebles)
            conn.commit()

        i += 1


    # закрытие указателя
    c.close()
    conn.close()


# Обновление базы данных
def refresh_bd (db_name, cities):

    #для каждого города из списка
    for db_city_id_ in cities:
        sites = pars_data(db_name, db_city_id_) #забор link и id сайтов

        # для каждого сайта из списка
        for site in sites:
            if site[1] == 1:
                pars_ = parse_yandex(get_html(site[0]))

            elif site[1] == 2:
                pars_ = parse_gismeteo(get_html(site[0]))
    
            write_to_db(db_name_,pars_,db_city_id_, site[1])

db_name_ = 'weather_db.sqlite3' # имя файла с базой
cities_ = pars_cities(db_name_,)

refresh_bd(db_name_, cities_)
