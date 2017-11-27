
import urllib.request

from bs4 import BeautifulSoup

def get_html(url):
    response = urllib.request.urlopen(url)
    return (response.read())


#парсинг Яндекса
def parse_yandex(html):
    soup = BeautifulSoup (html,"lxml")
    div = soup.find("", class_="forecast-briefly__days")

    projects = []

    for div_2 in div.find_all("div"):
        times = div_2.find("a")
        if times:
            #достаю значение дневной температуры
            day_temp = div_2.find("div", class_="temp forecast-briefly__temp forecast-briefly__temp_day")
            day_temp = day_temp.find("span", class_="temp__value")

            #достаю значение ночной температуры
            night_temp = div_2.find("div", class_="temp forecast-briefly__temp forecast-briefly__temp_night")
            night_temp = night_temp.find("span", class_="temp__value")

            projects.append({
                "datetime" : times.time["datetime"][0:10],
                "day_temp" : day_temp.text,
                "night_temp" : night_temp.text
                })
    
    return projects


#Парсинг гисметео
def parse_gismeteo(html):
    soup = BeautifulSoup (html,"lxml")
    div_head = soup.find("div", class_="widget__container") # определил слой со всей информацией
    div_date = div_head.find("div", class_="widget__row") #определил подслой с датами
    div_val = div_head.find_all("div", class_="value") #создал список со значениями

    projects = []

    i = 0

    for div_date_2 in div_date.find_all("div", class_="widget__item"):
        

        div_date_2_text = div_date_2.span.text.lstrip().rstrip() # удаляю пробелы вконце и сначала строки
        div_date_2_text_num = div_date_2_text[0:2].rstrip() # вырезаю число
 
        #для чисел из одной цифры добавляю нолик в начало
        if len(div_date_2_text_num) < 2:
            div_date_2_text_num = "0"+div_date_2_text_num

        year = 2017 # костыли для перехода на следующий год
        if div_date_2_text[-3:] == "янв":
            div_date_2_text_mon = "01"
            if j == '12':
                year = year+1
        elif div_date_2_text[-3:] == "фев":
            div_date_2_text_mon = "02"
        elif div_date_2_text[-3:] == "мар":
            div_date_2_text_mon = "03"
        elif div_date_2_text[-3:] == "апр":
            div_date_2_text_mon = "04"
        elif div_date_2_text[-3:] == "май":
            div_date_2_text_mon = "05"
        elif div_date_2_text[-3:] == "июн":
            div_date_2_text_mon = "06"
        elif div_date_2_text[-3:] == "июл":
            div_date_2_text_mon = "07"
        elif div_date_2_text[-3:] == "авг":
            div_date_2_text_mon = "08"
        elif div_date_2_text[-3:] == "сен":
            div_date_2_text_mon = "09"
        elif div_date_2_text[-3:] == "окт":
            div_date_2_text_mon = "10"
        elif div_date_2_text[-3:] == "ноя":
            div_date_2_text_mon = "11"
        elif div_date_2_text[-3:] == "дек":
            div_date_2_text_mon = "12"
            j = div_date_2_text_mon
           
 
    
        div_val_2 = div_val[i]
        day_temp = div_val_2.find("div", class_="maxt")
        night_temp = div_val_2.find("div", class_="mint")

        i += 1

        projects.append({
            "datetime" : "%s-%s-%s" % (str(year),div_date_2_text_mon,div_date_2_text_num),
            "day_temp" : day_temp.text,
            "night_temp" : night_temp.text
            })          

    return projects
        
def pars_mailru(html):
    soup = BeautifulSoup (html,"lxml")
    div_date_today = soup.find_all ('div', class_= 'information__header__left__date')
    div_temp_today_day = soup.find_all ('div', class_='information__content__temperature')
    div_temp_today_night
    print(div_temp_today)
    

#    print("gismeteo:")
#    print(parse_gismeteo(get_html("https://www.gismeteo.ru/weather-moscow-4368/10-days/")))
#    print("\n \n yandex:")
#    print(parse_yandex (get_html("https://yandex.ru/pogoda/krasnoyarsk")))


# pars_mailru(get_html('http://www.pogoda.mail.ru/prognoz/moskva/'))


