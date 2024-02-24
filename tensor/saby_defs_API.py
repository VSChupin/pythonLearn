import requests as req
import datetime as date
import json

# Входные параметры
url_auth = "https://fix-online.sbis.ru/auth/service/"
url_work = "https://fix-online.sbis.ru/service/"
login = ""
password = ""
id_doc_vi = "f473c072-f615-4a0e-9b18-3ee63f83cd6f"


## Описание функций ##
# Авторизация и сохранение sid в файл
def authenticate(login, password):
    now = date.datetime.now()

    # Создаем заголовки запроса
    headers = {
        "Content-Type": "application/json-rpc;charset=utf-8",
        "Accept": "/",
        "User-Agent": "DpLvl",
    }

    # Создаем тело запроса
    auth_body = {
        "jsonrpc": "2.0",
        "method": "СБИС.Аутентифицировать",
        "params": {"Параметр": {"Логин": login, "Пароль": password}},
        "id": 0,
    }

    # Отправляем запрос на аутентификацию
    saby_auth = req.post(url_auth, headers=headers, data=json.dumps(auth_body))

    # Получаем идентификатор сессии
    sabyIdSession = saby_auth.json().get("result")

    # Создаем имя файла с текущим временем и идентификатором сессии
    filename_auth = (
        "id_session_"
        + sabyIdSession
        + "_"
        + now.strftime("%Y-%m-%d_%H-%M-%S")
        + ".json"
    )

    # Сохраняем ответ в файл
    with open(filename_auth, "w") as f:
        f.write(saby_auth.text)

    # Проверяем статус ответа и выводим сообщение
    if saby_auth.status_code == 200:
        print("Ok, session id received. See the id_session.json.")

    # Возвращаем идентификатор сессии
    return sabyIdSession


# Читаем документ и сохраняем в файл
def read_and_save_document(id_doc_vi, sabyIdSession, url_work):
    # Создаем заголовки запроса
    headers = {
        "Content-Type": "application/json-rpc;charset=utf-8",
        "Accept": "*/*",
        "User-Agent": "DpLvl",
        "X-SBISSessionID": sabyIdSession,
    }

    # Создаем тело запроса
    read_doc_body = {
        "jsonrpc": "2.0",
        "method": "СБИС.ПрочитатьДокумент",
        "params": {
            "Документ": {"Идентификатор": id_doc_vi, "ДопПоля": "ДополнительныеПоля"}
        },
        "id": 0,
    }

    # Отправляем запрос на чтение документа
    saby_read_doc = req.post(url_work, headers=headers, data=json.dumps(read_doc_body))

    # Создаем имя файла с текущим временем и идентификатором документа
    now = date.datetime.now()

    filename_doc = (
        "doc_id_"
        + id_doc_vi
        + "_"
        + "id_session_"
        + sabyIdSession
        + "_"
        + now.strftime("%Y-%m-%d_%H-%M-%S")
        + ".json"
    )

    # Сохраняем ответ в файл
    with open(filename_doc, "w") as f:
        f.write(saby_read_doc.text)

    # Проверяем статус ответа и выводим сообщение
    if saby_read_doc.status_code == 200:
        print("Ok, The document is caught. See the doc_.json")


## Вызов функций ##
sabyIdSession = authenticate(login=login, password=password)

read_and_save_document(
    id_doc_vi=id_doc_vi, sabyIdSession=sabyIdSession, url_work=url_work
)
