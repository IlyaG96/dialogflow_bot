# Бот DialogFlow для ВК и Telegram

Учебный проект курсов веб-разработчиков [dvmn](https://dvmn.org).  
[Ссылка на группу ВК с подключенным ботом](https://vk.com/club209738895).  
Бот в телеграм: @dialogflow_test_devman_bot .  

## Установка
Вам понадобится установленный Python 3.8+ и git.

Склонируйте репозиторий:
```bash
git clone git@github.com:IlyaG96/dialogflow_bot.git
```

Создайте в этой папке виртуальное окружение:
```bash
cd dialogflow_bot
python3 -m venv env
```

Активируйте виртуальное окружение и установите зависимости:
```bash
source env/bin/activate
pip install -r requirements.txt
```

## Настройка перед использованием

### Переменные окружения

Перед использованием вам необходимо заполнить .env.example файл или иным образом передать переменные среды:
* TELEGRAM_TOKEN - токен бота Telegram. Можно получить у [@BotFather](https://t.me/BotFather).
* GOOGLE_APPLICATION_CREDENTIALS - путь до json файла с ключами. Только путь. Саму переменную в проекте никуда запихивать не надо. Это магия.
* VK_TOKEN - токен группы ВК (в меню работа с API)
* PROJECT_ID - project_id из GOOGLE_APPLICATION_CREDENTIALS
* DEBUG_CHAT_ID - chat_id для сообщений о багах. (скорее всего, ваш chat_id)


<details>
<summary>Для получения GOOGLE_APPLICATION_CREDENTIALS:</summary>

Для получения GOOGLE_APPLICATION_CREDENTIALS:
- [Создайте профиль в Google Cloud](https://cloud.google.com/dialogflow/docs/quick/setup)
- [Создайте агента](https://cloud.google.com/dialogflow/es/docs/quick/build-agent)
- [Создайте json с ключами и скопируйте его себе на компьютер](https://cloud.google.com/docs/authentication/getting-started)
</details>

## Использование


### Обучить агента фразам

Для того, чтобы обучить своего агента тестовым фразам, связанным с трудоустройством, запустите скрипт `create_intent.py`:
```bash
$ python create_intent -p 'full/path/to/file.json'
```
Обязательный аргумент json_path - полный путь до файла с тренировочными фразами.  
Вы можете подробно изучить структуру файла `training_phrases.json` и внести туда изменения.

### ВК-бот
Для старта вк-бота, запустите скрипт:
```bash
$ python vk_bot
```
<img src="https://github.com/IlyaG96/dialogflow_bot/blob/main/gif-examples/vk-1.gif" width="50%" height="50%">

### Телеграм-бот

Для старта телеграм-бота, запустите скрипт:
```bash
$ python tg_bot
```
<img src="https://github.com/IlyaG96/dialogflow_bot/blob/main/gif-examples/tg.gif" width="50%" height="50%">


### config.py и dialogflow.py 

Используются для работы с переменными окружения и для работы с агентом google соответственно.
