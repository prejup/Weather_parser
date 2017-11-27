from parsers import *
from BD_connect import *

db_name_ = 'weather_db.sqlite3' # имя файла с базой

cities_ = pars_cities(db_name_,) #определение списка городов

refresh_bd(db_name_, cities_) # обновление базы
