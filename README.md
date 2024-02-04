## Проект Survey123

Survey123 - веб-приложение на базе Django для проведения опросов и возможностью динамического отображения вопросов в зависимости от ответов пользователя. 
Проект доступен по адресу [https://survey123.hopto.org](https://survey123.hopto.org). Админ-панель по адресу: [https://survey123.hopto.org/admin](https://survey123.hopto.org/admin)

### Автор проекта:

Фуллстек-разработка и дизайн: Ильдар Аюпов, 2024 г., e-mail: ildarbon@gmail.com, Telegramm: @ildarbonn

### Техническое описание проекта:

Основные библиотеки и технологии:
- Бэкенд: Python, Django, PostgreSQL
- Фронтенд: Bootstrap, HTML, CSS
- Деплой: Docker, NGINX, Gunicorn, Continuous Deployment (GitHub Actions)

Реализованы такие вещи, как:
- cоздание и редактирование опросов и вопросов через админку.
- реализация веб-интерфейса, позволяющего пользователям проходить опросы и отвечать на вопросы.
- сохранение ответов пользователей в связке с соответствующими опросами.
- логика, позволяющая определить, какие вопросы показывать или скрывать в зависимости от предыдущих ответов пользователя (т.е. дерево)
- вывод результатов опросов, включая статистику ответов на каждый вопрос, после завершения опроса.
- статистика опросов рассчитывается посредством базовых SQL-запросов без использования ORM и включает следующую информацию:
- - общее кол-во участников опроса (например, 100)
- - На каждый вопрос:
- - - кол-во ответивших и их доля от общего кол-ва участников опроса (например, 95 / 95%)
- - - порядковый номер вопроса по кол-ву ответивших. Если кол-во совпадает, то и номер совпадает (например, для трех вопросов с 95, 95, 75 ответивших получаются соответствующие им номера 1, 1, 2)
- - - кол-во ответивших на каждый из вариантов ответа и их доля от общего кол-ва ответивших на этот вопрос.
- кастомная обработка основных ошибок (404, 500)

### Развернуть проект на локальной машине:

- Установить Docker, Docker Compose:
```
sudo apt update
sudo apt install curl
curl -fSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
sudo apt-get install docker-compose-plugin
```

- Клонировать репозиторий:
```
git clone git@github.com:ildar-aiupov/survey.git
```

- В корне проекта переименовать файл `.env.example` (настройки Джанго и подключения к базе данных) в файл `.env` (команда `mv .env.example .env`). Все настройки рабочие. 

- Находясь в корневой папке проекта, запустить его сборку:
```
sudo docker compose up -d
```

- При сборке проекта для демонстрации его работы сразу автоматически создается база данных с несколькими опросами и рядом вопросов.

- Точки входа в проект:
```
Главная страница проекта: http://localhost:8010/

Админ-панель: http://localhost:8010/admin/
```

- Для остановки контейнеров Docker:
```
sudo docker compose down -v      # с их удалением (также удаляются все хранилища данных проекта)
sudo docker compose stop         # просто остановка без удаления
```