import webbrowser
from sklearn.feature_extraction.text import CountVectorizer     #pip install scikit-learn
from sklearn.linear_model import LogisticRegression
import datetime
import words
import requests
from bs4 import BeautifulSoup as bs
import random
import urllib
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config
from numpy import all
import wikipedia
from pytube import YouTube


TRIGGERS = {'гоша', 'гош', 'герундий', 'гарик', 'горик', 'гошка',  'гошечка', 'горошек'}

def yotube_dowold(data):
    list1 = ['скачай', 'качай видео', 'загрузи', 'загрузи']
    return 2

def wiki(data):
    list1 = ['найди', 'на', 'википедия','вики', 'педия','википедии', 'педии', 'найти']
    try:
        for i in list1:
            if i in data:
                data = data.replace(i, '')
                data = data.strip()
        wikipedia.set_lang('ru')
        otvet = wikipedia.summary(data, sentences=4)
        page = wikipedia.page(data)
        URL = page.url
        return otvet + '\n\n' + URL
    except:
        return ("Извините данная функция не доработана, можете повторить")


def homi(data):
    try:
        url = 'https://vk.com/away.php?utf=1&to=https%3A%2F%2Fyandex.ru%2Fvideo%2Ftouch%2Fsearch%2F%3Ftext%3D%25D0%25B6%25D0%25B5%25D1%2581%25D1%2582%25D0%25BA%25D0%25BE%25D0%25B5%2520%25D0%25B3%25D0%25B5%25D0%25B9%2520%25D0%25BF%25D0%25BE%25D1%2580%25D0%25BD%25D0%25BE%26filmId%3D13580388513346902939'
        webbrowser.open(url)
        return 'Врубаю жесткое гей порно с немцами'
    except IOError:
        return "Газинур сказал что нужно проверить подключение к интернету"


def youtube(data):
    try:
        webbrowser.open('https://www.youtube.com')
        return 'Сейчас открою ютуб'
    except IOError:
        return ("Проверьте подключение к интернету")


def vk(data):
    try:
        webbrowser.open('https://www.vk.com')
        return 'Сейчас открою вконтакте'
    except IOError:
        return ("Проверьте подключение к интернету")


def instagram(data):
    try:
        webbrowser.open('https://www.instagram.com')
        return 'Сейчас открою инстаграмм'
    except IOError:
        return ("Проверьте подключение к интернету")


def whats_app(data):
    whats = ['У меня всё хрошо', 'У меня всё как обычно',
             'Мне бывает часто скучно, вам стоит почаще со мной разговаривать',
             'Чего стоит спросить \"Как дела?\", людям правда искрене интересно? Но я все волишь робот 🤖 и не умею чувствовать 😞',
             '7 из 10', 'Настроение улучшается когда вы со мной разговариваете']
    return random.choice(whats)


def hi(data):
    return random.choice(['пиривет', 'Привет я Гоша, голосовой асистент соданый как проект по информатике, приятно познакомится', 'доброго времени суток', 'хаааааааааай', 'привет привет'])


def search(data):
    try:
        for i in ['погугли','поищи','найди']:
            if i in data:
                zapros = data.replace(i, '')
                zapros = zapros.strip()
                webbrowser.open(f'https://www.google.com/search?q={zapros}')
                return 'Сейчас найду'
    except IOError:
        return ("Проверьте подключение к интернету")


def wether(data):
    try:
        owm = OWM('2a5fe42188a26d52849a753f80442562')
        config_dict = get_default_config()
        config_dict['language'] = 'ru'
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place('Ufa,RU')
        weather = observation.weather
        temp = weather.temperature('celsius')
        temp = temp['temp']
        wind = observation.weather.wind()
        wind = (wind['speed'])
        humidity = observation.weather.humidity
        weather_status = weather.detailed_status
        return ('Температура ' + str(temp) + '° цельсия ' + weather_status + '\nСкорость ветра ' + str(wind) + ' метров в секунду  \nВлажность ' + str(humidity) + '%')
    except IOError:
        return ("Проверьте подключение к интернету")

def anekdot(data):
    try:
        URL = 'https://www.anekdot.ru/last/good/'
        r = requests.get(URL)
        soap = bs(r.text, 'html.parser')
        anekdot = soap.find_all('div', class_='text')
        clear_anekdot = [c.text for c in anekdot]
        return (random.choice(clear_anekdot))
    except IOError:
        list2 = ['Настя упала и разбила подбородок. Но ничего страшного, у нее есть второй!',
                 'Штирлиц и Мюллер ездили по очереди на танке. Очередь редела, но не расходилась...',
                 'Штирлиц стрелял вслепую. Слепая испугалась и побежала скачками, но качки быстро отстали.',
                 'Штирлиц вытащил из сейфа записку Мюллера. Мюллеру было очень больно и он сильно ругался.',
                 'Штирлицу попала в голову пуля. "Разрывная," - раскинул мозгами Штирлиц.',
                 'Жил-был царь. И было у него косоглазие. Пошёл он однажды куда глаза глядят и порвался.',
                 'Курица приняла Ислам', 'Маленькую Лизу, глухую на одно ухо, мама ласково называла Моно Лиза.',
                 'Олег попал в жуткую аварию и чудом выжил. "Чудес не бывает", — подумал Олег и залез обратно в горящую машину.',
                 'Черепашки-ниндзя нападали вчетвером на одного, потому что у них тренер был крыса.',
                 'Девушка, которая по ошибке вытащила из сумочки электрошокер, со словами "Алло", вырубила себя на трое суток.']
        return random.choice(list2)


def time_tooday(data):
    now = datetime.datetime.now()
    return ("Сейчас " + str(now.hour) + ":" + str(now.minute))


def recognize(data, data_set):

    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(data_set.keys()))

    clf = LogisticRegression()
    clf.fit(vectors, list(data_set.values()))

    del data_set

    trg = words.TRIGGERS.intersection(data.split())
    if trg:
        data.replace(list(trg)[0], '')
    if data in words.ex:
        return 1
    else:
        text_vector = vectorizer.transform([data]).toarray()[0]
        if all(text_vector == text_vector[0]):
            return None
        else:
            func_name = clf.predict([text_vector])[0]
            return globals()[func_name](data)


