### Система сбора информации

#### SERVER

необходимо виртуальное окружение
(подробнее по ссылке [how to install virtual env](https://gist.github.com/Geoyi/d9fab4f609e9f75941946be45000632b))

установить окружение 
```shell script
virtualenv venv
```

активация окружения
```shell script
source venv/bin/activate
```

установка зависимостей
```shell script
pip install requirements.txt
```

добавим в переменную окружения приложение
```shell script
export FLASK_APP=das_se/app.py
```

запуск сервера на порту 5000
```shell script
flask run
```

Можно добавить в переменную окружния порт и при запуск сервер возьмет указанный порт 
```shell script
export FLASK_RUN_PORT=8001
```

или при запуске явно указать порт
```shell script
flask run -p 8001
```

#### CLIENT
работа с клиентом 

запустит клиент
```shell script
sh das_client/send_cpu.sh start
```

запустит клиент, клиент будет отправлять запросы по указаному адресу
```shell script
sh das_client/send_cpu.sh start 127.0.0.1:8002
```

остановка клиента
```shell script
sh das_client/send_cpu.sh stop
```

перезапуск клиента
```shell script
sh das_client/send_cpu.sh restart
```

