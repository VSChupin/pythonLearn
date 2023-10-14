import win32com.client
import json
import uuid
import random


"""Шаг 1. Подключение к СБИС3.Плагин"""


ole = win32com.client.Dispatch("Tensor.SbisPluginClientCOM")  # Получаем COM объект

# При получении COM объекта плагин генерирует событие типа 'Event' c eventName=connected,
# поэтому если среди полученных ответов от ReadAllObject() есть событие стаким eventName, то вам удалось подключиться
# к плагину, иначе стоит сделать таймаут 100 - 500мс и повторить вызов ReadAllObject().Пример цикла.

while True:
    events = json.loads(ole.ReadAllObject())  # получаем события от плагина и преобразуем в массив json объектов
    # в цикле проходим по каждому событию и ищем нужное с eventName=connected
    for event in events:
        if event['type'] == 'Event' and event['data']['eventName'] == 'connected':
            print("Подключение к Плагину выполнено")
            # если нужное событие пришло выходим из цикла
            break
    else:       
    # если ожидаемое событие не найдено, то делаем таймаут в 300мс
        ole.Sleep(300)
        continue            
    break
# После подключения к плагину вы можете подключаться к ExtSdk2 и звать методы данного модуля


"""Шаг 2. Подключение к ExtSDK2"""


# Получаем uuid модуля ExtSdk2 через ole.GetModule. Если uuid получен, значит подключение к ExtSdk2 успешно и можно совершать запросы в модуль.
guid_module = ole.GetModule("ExtSdk2")  # Получаем uuid модуля ExtSdk2
print("Подключение к ExtSDK2 выполнено, uuid: ", guid_module)


"""Шаг 3. Аутентификация по логину и паролю"""


query_id = str(uuid.uuid4())  # генерируем идентификатор запроса (UUID) по которому будем ожидать ответ
module_method = "ExtSdk2.AuthByPassword"  # метод, который хотим позвать
parameters_module_method = json.dumps({"Login": "мчд_физик_инсайд2", "Password": "мчд_физик_инсайд2123"},
                                      ensure_ascii=True)  # формируем параметры метода ExtSdk2.AuthByPassword
host = "test-online.sbis.ru"  # хост, на который хотим пойти online.sbis.ru.

# Вызов метода аутентификации без авторизаии, чтобы получить идентификатор сессии
ole.CallMethodWithoutAuth(query_id, guid_module, module_method, parameters_module_method, host)

# Ожидаем ответ через ReadAllObject в цикле по query_id
session_id = ""  # Переменная для сохранения идентификатора сессии для вызов методов ExtSdk2 с пройденной аутентификацией
while True:
    events = json.loads(ole.ReadAllObject())  # получаем события от плагина и преобразуем в массив json объектов
    # в цикле проходим по каждому событию и ищем нужное с ожидаемым query_id
    for event in events:
        if event['type'] == 'Message' and event['queryID'] == query_id:
            # если нужное событие пришло, то записываем идентификатор сессии в переменную
            session_id = event['data']['Result']
            break
    else:
        # если ожидаемое событие не найдено, то делаем таймаут в 300мс
        ole.Sleep(300)
        continue
    break
print("Получен идентификатор сессии: ", session_id)


"""Функция, зовущая метод ExtSDK2.WriteDocument"""


def write_document():
    document_id = "d8e74588-f9e9-4a50-a4f8-82753ab" + str(random.randint(10000, 99999)) #генерирую рандомный ИД документа
    query_id = str(uuid.uuid4())  # генерируем идентификатор запроса (UUID) по которому будем ожидать ответ
    module_method = "ExtSdk2.WriteDocument"  # метод, который хотим позвать
    parameters_module_method = json.dumps(
        {
        "Document": {
            "Вложение": [
                {
                "Идентификатор": "8b8d54e2-44ae-4de3-8433-f4a7c86c2c5e",
                "Файл": {
                    "ДвоичныеДанные": "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0id2luZG93cy0xMjUxIiA/Pgo81ODp6yDC5fDxz/Du4z0i0cHo0TMiIMLl8PHU7vDsPSI1LjAxIiDI5NTg6es9Ik9OX05TQ0hGRE9QUFJfMkJFMjRlNjJkMmYyYmE1NDk0MmJmZTQ5MDI1YzU1M2NjNjJfMkJFOGYzMTc4ZTdhZThjNDE2NzkwMTc1ZTk1ZTlhZWQ1MjRfMjAyMjAxMjRfMzlDRkM1RjEtREE2RC00Mjg1LUE2OUQtMTg3RURFMjY4RDBGIj4KCiAgPNHi0/fE7urO4e7wIMjkzvLv8D0iMkJFOGYzMTc4ZTdhZThjNDE2NzkwMTc1ZTk1ZTlhZWQ1MjQiIMjkz+7rPSIyQkUyNGU2MmQyZjJiYTU0OTQyYmZlNDkwMjVjNTUzY2M2MiI+CiAgICA80eLO3cTO8u/wIMjNzd7LPSI3NjA1MDE2MDMwIiDI5N3Ezj0iMkJFIiDN4OjszvDjPSLOzs4gJnF1b3Q7yu7s7+Dt6P8gJnF1b3Q70uXt5+7wJnF1b3Q7Ii8+CiAgPC/R4tP3xO7qzuHu8D4KCiAgPMTu6vPs5e3yIMLw5ezI7fTP8D0iMTEuNDQuNDEiIMTg8uDI7fTP8D0iMjQuMDEuMjAyMiIgys3EPSIxMTE1MTMxIiDN4OjsxO7qzu/wPSLR9+XyLfTg6vLz8OAg6CDk7urz7OXt8iDu4SDu8uPw8+fq5SDy7uLg8O7iICji++/u6+3l7ejoIPDg4e7yKSwg7+Xw5eTg9+Ug6Ozz+eXx8uLl7e379SDv8ODiICjk7urz7OXt8iDu4SDu6uDn4O3o6CDz8evz4ykiIM3g6Ozd6u7t0fPh0e7x8j0izs7OICZxdW90O83u4vvpIO7y7/Dg4ujy5ev8JnF1b3Q7IiDP7tTg6vLVxj0ixO7q8+zl7fIg7uEg7vLj8PPn6uUg8u7i4PDu4iAo4vvv7uvt5e3o6CDw4OHu8iksIO/l8OXk4PflIOjs8/nl8fLi5e3t+/Ug7/Dg4iAo5O7q8+zl7fIg7uEg7urg5+Dt6Ogg8/Hr8+MpIiDU8+3q9uj/PSLR19TEzs8iPgogICAgPNHi0ffU4OryIMTg8uDR99Q9IjI0LjAxLjIwMjIiIMru5M7Kwj0iNjQzIiDN7uzl8NH31D0iNDE0ODk0MjYxODk0NTMxIj4KICAgICAgPMjx7/DR99QgxOX0xODy4Mjx7/DR99Q9Ii0iIMTl9M3u7Mjx7/DR99Q9Ii0iLz4KICAgICAgPNHiz/Du5D4KICAgICAgICA8yOTR4j4KICAgICAgICAgIDzR4t7L0/cgyM3N3ss9IjY3MzIwMjA1OTkiIMrPzz0iNjczMjAxMDAxIiDN4OjszvDjPSLPyiAmcXVvdDvL4OLg+CZxdW90Oywgzs7OIi8+CiAgICAgICAgPC/I5NHiPgogICAgICAgIDzA5PDl8T4KICAgICAgICAgIDzA5PDQ1CDD7vDu5D0i4y4gyu7x8vDu7OAiIMTu7D0iMTEiIMjt5OXq8T0iMTU2MDA1IiDK7uTQ5ePo7u09IjQ0IiDT6+j24D0i8+suIMvl8e3g/yIvPgogICAgICAgIDwvwOTw5fE+CiAgICAgICAgPMru7fLg6vIg3evP7vfy4D0iYXYub3Jsb3ZAdGVuc29yLnJ1Ii8+CiAgICAgIDwv0eLP8O7kPgogICAgICA8w/Dz587yPgogICAgICAgIDzO7cblPu7tIOblPC/O7cblPgogICAgICA8L8Pw8+fO8j4KICAgICAgPMPw8+fP7uvz9z4KICAgICAgICA8yOTR4j4KICAgICAgICAgIDzR4t7L0/cgyM3N3ss9IjI2MDAzMDMzODUiIMrPzz0iMjYwMDAxMDAxIiDN4OjszvDjPSLOzs4gJnF1b3Q7ze7i++kgz+7r8/fg8uXr/CZxdW90OyIvPgogICAgICAgIDwvyOTR4j4KICAgICAgICA8wOTw5fE+CiAgICAgICAgICA8wOTw0NQgw+7w7uQ9IuMuIMDh5PPr6O3uIiDI7eTl6vE9IjEyNTQ4NyIgyu7k0OXj6O7tPSI1NiIg0ODp7u09IvAt7SDA4eTz6+jt8ero6SIvPgogICAgICAgIDwvwOTw5fE+CiAgICAgIDwvw/Dz58/u6/P3PgogICAgICA80eLP7urz7z4KICAgICAgICA8yOTR4j4KICAgICAgICAgIDzR4t7L0/cgyM3N3ss9IjI2MDAzMDMzODUiIMrPzz0iMjYwMDAxMDAxIiDN4OjszvDjPSLOzs4gJnF1b3Q7ze7i++kgz+7r8/fg8uXr/CZxdW90OyIvPgogICAgICAgIDwvyOTR4j4KICAgICAgICA8wOTw5fE+CiAgICAgICAgICA8wOTw0NQgw+7w7uQ9IuMuIMDh5PPr6O3uIiDI7eTl6vE9IjEyNTQ4NyIgyu7k0OXj6O7tPSI1NiIg0ODp7u09IvAt7SDA4eTz6+jt8ero6SIvPgogICAgICAgIDwvwOTw5fE+CiAgICAgIDwv0eLP7urz7z4KICAgICAgPMTu6s/u5PLizvLj8CDE4PLgxO7qzvLj8D0iMjQuMDEuMjAyMiIgzeDo7MTu6s7y4/A9IsTu6vPs5e3yIO7hIO7y4/Dz5+rlIPLu4uDw7uIgKOL77+7r7eXt6Ogg8ODh7vIpLCDv5fDl5OD35SDo7PP55fHy4uXt7fv1IO/w4OIgKOTu6vPs5e3yIO7hIO7q4Ofg7ejoIPPx6/PjKSIgze7sxO7qzvLj8D0iNDE0ODk0MjYxODk0NTMxIi8+CiAgICAgIDzI7fTP7uvU1cYxPgogICAgICAgIDzS5erx8sjt9CDH7eD35e09IvDl4Ovo5+D26P8g8SDTz8QiIMjk5e3y6PQ9Is/w6Ozl9+Dt6OUiLz4KICAgICAgICA80uXq8fLI7fQgx+3g9+XtPSLw5eDr6Ofg9uj/IPEg08/EIiDI5OXt8uj0PSLI7fTP5fDl5NLg4esiLz4KICAgICAgICA80uXq8fLI7fQgx+3g9+XtPSIyNC4wMS4yMDIyIDExOjQ0OjQxIiDI5OXt8uj0PSLE4PLgw+XtIi8+CiAgICAgICAgPNLl6vHyyO30IMft4Pfl7T0iNDE0ODk0MjYxODk0NTMxIiDI5OXt8uj0PSLN4Orr4OTt4P/N7uzl8CIvPgogICAgICAgIDzS5erx8sjt9CDH7eD35e09IjI0LjAxLjIwMjIiIMjk5e3y6PQ9Is3g6uvg5O3g/8Tg8uAiLz4KICAgICAgICA80uXq8fLI7fQgx+3g9+XtPSIyNC4wMS4yMDIyIiDI5OXt8uj0PSLO8uPw8+fq4MTg8uAiLz4KICAgICAgICA80uXq8fLI7fQgx+3g9+XtPSIyMCIgyOTl7fLo9D0i0fLg4urgzcTRIi8+CiAgICAgICAgPNLl6vHyyO30IMft4Pfl7T0i8+suIMvl8e3g/ywg5C4gMTEiIMjk5e3y6PQ9ItHq6+DkzeDo7OXt7uLg7ejlIi8+CiAgICAgICAgPNLl6vHyyO30IMft4Pfl7T0iaHR0cHM6Ly9maXgtb25saW5lLnNiaXMucnUvb3BlbmRvYy5odG1sP2d1aWQ9MmRiNTY1NDEtZjQ2NC00YTM3LWFhZWMtMGZlNjhjOTgzYWVlJmFtcDtmMz0xMjkmYW1wO2ZpbGU9OTg3NjdlNmMtOGI1ZC00Yzg1LThiN2ItYTJkNDFhNDg1NTJjJmFtcDt2ZXI9MSZhbXA7ZGF0ZT0yMDIyMDEyNDExNDQ0MCZhbXA7YWNjb3VudD0zMTI3NDkyIiDI5OXt8uj0PSLE7urz7OXt8i7R8fvr6uDN4MLr7ubl7ejlIi8+CiAgICAgICAgPNLl6vHyyO30IMft4Pfl7T0iMjQxNTNlNjEtYTMzZC00YWZhLTk2MmQtYTMwMThiM2EzOGY1IiDI5OXt8uj0PSLM18QiLz4KICAgICAgPC/I7fTP7uvU1cYxPgogICAgPC/R4tH31ODq8j4KICAgIDzS4OHr0ffU4OryPgogICAgICA80eLl5NLu4iDK7uvS7uI9IjExIiDN4Ojs0u7iPSLS7uLg8CC5N2I4MTQ5NDctZjg0Yi00OWJmLThhZTYtYjRkNGI4MWNjY2YyXyhAIyQlXn4uLC8pIiDN4OvR8j0iMjAlIiDN7uzR8vA9IjEiIM7Kxchf0u7iPSI3OTYiINHy0u7iweXnzcTRPSIxNTUuODMiINHy0u7i0/fN4Os9IjE4Ny4wMCIg1uXt4NLu4j0iMTQuMTciPgogICAgICAgIDzA6vbo5z4KICAgICAgICAgIDzB5efA6vbo5z7h5ecg4Or26OfgPC/B5efA6vbo5z4KICAgICAgICA8L8Dq9ujnPgogICAgICAgIDzR8+zN4Os+CiAgICAgICAgICA80fPszeDrPjMxLjE3PC/R8+zN4Os+CiAgICAgICAgPC/R8+zN4Os+CiAgICAgICAgPMTu79Hi5eTS7uIgyu7k0u7iPSIwMzM5MjE4NS05YzcxLTMyNzYtYTg2OC0zYTQ4ZjhkZTlmZjIiIM3g6OzF5Mjn7D0i+PIiIM/w0u7i0ODhPSIxIi8+CiAgICAgICAgPMjt9M/u69TVxjIgx+3g9+XtPSLx8vDg7eAg3ev84fDz8ej/IiDI5OXt8uj0PSLP8Ojs5ffg7ejlIi8+CiAgICAgICAgPMjt9M/u69TVxjIgx+3g9+XtPSIwMzM5MjE4NS05YzcxLTMyNzYtYTg2OC0zYTQ4ZjhkZTlmZjIiIMjk5e3y6PQ9ItjKIi8+CiAgICAgICAgPMjt9M/u69TVxjIgx+3g9+XtPSIwMzM5MjE4NS05YzcxLTMyNzYtYTg2OC0zYTQ4ZjhkZTlmZjIiIMjk5e3y6PQ9Isru5CIvPgogICAgICAgIDzI7fTP7uvU1cYyIMft4Pfl7T0iMDMzOTIxODUtOWM3MS0zMjc2LWE4NjgtM2E0OGY4ZGU5ZmYyIiDI5OXt8uj0PSLI5CIvPgogICAgICAgIDzI7fTP7uvU1cYyIMft4Pfl7T0iMDMzOTIxODUtOWM3MS0zMjc2LWE4NjgtM2E0OGY4ZGU5ZmYyIiDI5OXt8uj0PSLK7uTP7vHy4OL56OrgIi8+CiAgICAgICAgPMjt9M/u69TVxjIgx+3g9+XtPSLS7uLg8CC5N2I4MTQ5NDctZjg0Yi00OWJmLThhZTYtYjRkNGI4MWNjY2YyXyhAIyQlXn4uLC8pIiDI5OXt8uj0PSLN4Ofi4O3o5c/u8fLg4vno6uAiLz4KICAgICAgICA8yO30z+7r1NXGMiDH7eD35e09IiZxdW90O1R5cGUmcXVvdDs6JnF1b3Q70u7i4PAmcXVvdDssJnF1b3Q7Q2F0ZWdvcnkmcXVvdDs6JnF1b3Q70u7i4PD7JnF1b3Q7IiDI5OXt8uj0PSLP7uv/ze7s5e3q6+Dy8/D7Ii8+CiAgICAgIDwv0eLl5NLu4j4KICAgICAgPMLx5ePuzu/rINHy0u7iweXnzcTRwvHl4+49IjE1NS44MyIg0fLS7uLT983g68Lx5ePuPSIxODcuMDAiPgogICAgICAgIDzR8+zN4OvC8eXj7j4KICAgICAgICAgIDzR8+zN4Os+MzEuMTc8L9Hz7M3g6z4KICAgICAgICA8L9Hz7M3g68Lx5ePuPgogICAgICAgIDzK7uvN5fLy7sLxPjExPC/K7uvN5fLy7sLxPgogICAgICA8L8Lx5ePuzu/rPgogICAgPC/S4OHr0ffU4OryPgogICAgPNHiz/Du5M/l8D4KICAgICAgPNHiz+XwIMTg8uDP5fA9IjI0LjAxLjIwMjIiINHu5M7v5fA9ItLu4uDw+yDv5fDl5ODt+yI+CiAgICAgICAgPM7x7c/l8CDN4OjszvHtPSLB5ecg5O7q8+zl7fLgLe7x7e7i4O3o/yIvPgogICAgICA8L9Hiz+XwPgogICAgPC/R4s/w7uTP5fA+CiAgICA8z+7k7+jx4O3yIM7h68/u6+09IjUiINHy4PLz8T0iMSIgzvHtz+7r7T0ixO7r5u3u8fLt++Ug7uH/5+Dt7e7x8ugiPgogICAgICA83ssgyM3N3ss9IjY3MzIwMjA1OTkiIM3g6OzO8OM9Is7B2cXR0sLOINEgzsPQwM3I18XNzc7JIM7SwsXS0dLCxc3NztHS3N4gJnF1b3Q7z9DOyMfCzsTR0sLFzc3A3yDKzszPwM3I3yAmcXVvdDvLwMLA2CZxdW90OzEyMyIgxO7r5u09IiI+CiAgICAgICAgPNTIziDU4Ozo6+j/PSLB5ev88ero6SIgyOz/PSLA6+Xq8eDt5PAiIM7y9+Xx8uLuPSLN6Oru6+Dl4uj3Ii8+CiAgICAgIDwv3ss+CiAgICA8L8/u5O/o8eDt8j4KICA8L8Tu6vPs5e3yPgoKPC/U4OnrPgo=",
                    "Имя": "ON_NSCHFDOPPR_2BE24e62d2f2ba54942bfe49025c553cc62_2BE8f3178e7ae8c416790175e95e9aed524_20220124_39CFC5F1-DA6D-4285-A69D-187EDE268D0F.xml"
                },
                    "Подпись": [
                        {
                        "Файл": {
                        "Имя": "ON_NSCHFDOPPR_2BE24e62d2f2ba54942bfe49025c553cc62_2BE8f3178e7ae8c416790175e95e9aed524_20220124_39CFC5F1-DA6D-4285-A69D-187EDE268D0F.xml.sgn",
                        "ДвоичныеДанные": "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"
                                }
                        }
                            ]
                }
            ],
            "ДопПоля":"ЭтапВернутьВсеСертификаты",
            "Дата": "27.09.2023",
            "Номер": "OLA27092023",
            "Идентификатор": document_id,
            "Контрагент": {
                "СвЮЛ": {
                "ИНН": "2600303385",
                "КПП": "260001001",
                "Название": "Новый получатель"
                }
            },
            "НашаОрганизация": {
                "СвЮЛ": {
                "ИНН": "6732020599",
                "КПП": "673201001"
                }
            },
            "Примечание": "Тест ExtSDK2 Степанова",
            "Тип": "ДокОтгрИсх"
        }
        }
        )
    # формируем параметры метода ExtSdk2.WriteDocument.

    # Вызов метода ExtSdk2.WriteDocument
    ole.CallMethod(query_id, guid_module, module_method, parameters_module_method, session_id)

    # Ожидаем ответ через ReadAllObject в цикле по query_id
    result = {}  # Переменная для сохранения результата ExtSdk2.WriteDocument
    result_checked = False

    while not result_checked:

        events = json.loads(ole.ReadAllObject())  # получить события от плагина и преобразовать в массив json объектов

        # в цикле пройти по каждому событию и найти нужное с ожидаемым query_id
        for event in events:
            if event['type'] == 'Event':
                # если нужное событие пришло, то записать результат в нужную переменную
                print('Запрос ExtSDK2.WriteDocument ушел, смотри логи Плагина')
                response_writedocument = event['data']['data']['Result']      
                result_checked = True
                break
            
        # если ожидаемое событие не найдено, то сделать таймаут в 300мс
        ole.Sleep(300)
    return response_writedocument
    
    
"""Функция, зовущая метод ExtSDK2.ExecuteAction"""


def execute_action(response_writedocument):   
    query_id = str(uuid.uuid4())  # генерируем идентификатор запроса (UUID) по которому будем ожидать ответ
    module_method = "ExtSdk2.ExecuteAction"  # метод, который хотим позвать
    parameters_module_method = json.dumps(
                {
                "Document": {
                    "Идентификатор": response_writedocument['Идентификатор'],
                        "Этап": {
                        "Вложение": [
                            {
                                "Идентификатор": response_writedocument['Вложение'][0]['Идентификатор'],
                                "Подпись": [
                                    {
                                        "Файл": {
                                            "Имя": "ON_NSCHFDOPPR_6732020599673201001_7186455910827245482_20230926_6D90A234-E1C1-42AE-9899-DD7DEAB3E181.xml.sgn",
                                            "ДвоичныеДанные": "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"
                                                },
                                    }
                                ]
                            }
                        ],
                        "Действие": [
                            {
                                "Комментарий": "",
                                "Название": "Отправить",
                                "Сертификат": {
                                    "Отпечаток": "FEC6BAE4A3069DF3E80049EFD1D1AD2364F51E14"
                                }
                            }
                        ],
                        "Название": "Отправка"
                        }
                            }
                }
        )
    
    # Вызов метода ExtSdk2.ExecuteAction
    ole.CallMethod(query_id, guid_module, module_method, parameters_module_method, session_id)

    # Ожидаем ответ через ReadAllObject в цикле по query_id
    result = {}  # Переменная для сохранения результата ExtSdk2.CallSabyApi
    result_checked = False
    while not result_checked:

        events = json.loads(ole.ReadAllObject())  # получить события от плагина и преобразовать в массив json объектов

        # в цикле пройти по каждому событию и найти нужное с ожидаемым query_id
        for event in events:
            if event['type'] == 'Message':
                # если нужное событие пришло, то записать результат в нужную переменную
                print('Запрос ExtSDK2.ExecuteAction ушел, смотри логи Плагина')
                response_executeaction = event['data']['Result']      
                result_checked = True
                break
            
        # если ожидаемое событие не найдено, то сделать таймаут в 300мс
        ole.Sleep(300)
    return response_executeaction


"""Функция, зовущая СБИС.СписокДокументов через CallSabyApi"""
    
 
def list_of_documents():    
    query_id = str(uuid.uuid4())  # генерируем идентификатор запроса (UUID) по которому будем ожидать ответ
    module_method = "ExtSdk2.CallSabyApi"  # метод, который хотим позвать
    parameters_module_method = json.dumps({
                                            "Method": "СБИС.СписокДокументов",
                                            "Params": {
                                                        "Тип": "Доверенность",
                                                    }},
                        ensure_ascii=True)  # сформировать параметры метода ExtSdk2.CallSabyApi.

    # Вызов метода ExtSdk2.CallSabyApi с пройденной аутентификацией
    ole.CallMethod(query_id, guid_module, module_method, parameters_module_method, session_id)

    # Ожидаем ответ через ReadAllObject в цикле по query_id
    result = {}  # Переменная для сохранения результата ExtSdk2.CallSabyApi
    result_checked = False
    while not result_checked:

        events = json.loads(ole.ReadAllObject())  # получить события от плагина и преобразовать в массив json объектов

        # в цикле пройти по каждому событию и найти нужное с ожидаемым query_id
        for event in events:
            if event['type'] == 'Message' and event['queryID'] == query_id:
                # если нужное событие пришло, то записать результат в нужную переменную
                result = event['data']['Result']
                result_checked = True
                print('Метод СБИС.СписокДокументов отработал, смотри логи Плагина')
                break

        # если ожидаемое событие не найдено, то сделать таймаут в 300мс
        ole.Sleep(300)    
    return result['Документ']
   
    
"""Функция, зовущая СБИС.ПрочитатьДокумент через CallSabyApi"""
    
    
def read_document_via_callsabyapi():    
    query_id = str(uuid.uuid4())  # генерируем идентификатор запроса (UUID) по которому будем ожидать ответ
    module_method = "ExtSdk2.CallSabyApi"  # метод, который хотим позвать
    parameters_module_method = json.dumps({
                                            "Method": "СБИС.ПрочитатьДокумент",
                                            "Params": {
                                                        "Идентификатор": "d3927969-cea8-415a-9128-143a35fc6557",
                                                    }},
        ensure_ascii=True)  # сформировать параметры метода ExtSdk2.CallSabyApi.

    # Вызов метода ExtSdk2.CallSabyApi с пройденной аутентификацией
    ole.CallMethod(query_id, guid_module, module_method, parameters_module_method, session_id)

    # Ожидаем ответ через ReadAllObject в цикле по query_id
    result = {}  # Переменная для сохранения результата ExtSdk2.CallSabyApi
    result_checked = False
    while not result_checked:

        events = json.loads(ole.ReadAllObject())  # получить события от плагина и преобразовать в массив json объектов

        # в цикле пройти по каждому событию и найти нужное с ожидаемым query_id
        for event in events:
            if event['type'] == 'Message' and event['queryID'] == query_id:
                # если нужное событие пришло, то записать результат в нужную переменную
                result = event['data']['Result']
                result_checked = True
                print('Метод СБИС.ПрочитатьДокумент отработал, смотри логи Плагина')
                break

        # если ожидаемое событие не найдено, то сделать таймаут в 300мс
        ole.Sleep(300)    
    

"""Функция, зовущая WriteDocumentEx"""   


def WriteDocumentEx():   
    query_id = str(uuid.uuid4())  # генерируем идентификатор запроса (UUID) по которому будем ожидать ответ
    module_method = "ExtSdk2.WriteDocumentEx"  # метод, который хотим позвать
    document_id = "d8e74588-f9e9-4a50-a4f8-82753ab" + str(random.randint(10000, 99999)) #генерирую рандомный ИД документа
    parameters_module_method = json.dumps(
                                            {
                                            "Document": {
                                                "Вложение": [
                                                    {
                                                    "Идентификатор": "8b8d54e2-44ae-4de3-8433-f4a7c86c2c5e",
                                                    "Файл": {
                                                        "ДвоичныеДанные": "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0id2luZG93cy0xMjUxIiA/Pgo81ODp6yDC5fDxz/Du4z0i0cHo0TMiIMLl8PHU7vDsPSI1LjAxIiDI5NTg6es9Ik9OX05TQ0hGRE9QUFJfMkJFMjRlNjJkMmYyYmE1NDk0MmJmZTQ5MDI1YzU1M2NjNjJfMkJFOGYzMTc4ZTdhZThjNDE2NzkwMTc1ZTk1ZTlhZWQ1MjRfMjAyMjAxMjRfMzlDRkM1RjEtREE2RC00Mjg1LUE2OUQtMTg3RURFMjY4RDBGIj4KCiAgPNHi0/fE7urO4e7wIMjkzvLv8D0iMkJFOGYzMTc4ZTdhZThjNDE2NzkwMTc1ZTk1ZTlhZWQ1MjQiIMjkz+7rPSIyQkUyNGU2MmQyZjJiYTU0OTQyYmZlNDkwMjVjNTUzY2M2MiI+CiAgICA80eLO3cTO8u/wIMjNzd7LPSI3NjA1MDE2MDMwIiDI5N3Ezj0iMkJFIiDN4OjszvDjPSLOzs4gJnF1b3Q7yu7s7+Dt6P8gJnF1b3Q70uXt5+7wJnF1b3Q7Ii8+CiAgPC/R4tP3xO7qzuHu8D4KCiAgPMTu6vPs5e3yIMLw5ezI7fTP8D0iMTEuNDQuNDEiIMTg8uDI7fTP8D0iMjQuMDEuMjAyMiIgys3EPSIxMTE1MTMxIiDN4OjsxO7qzu/wPSLR9+XyLfTg6vLz8OAg6CDk7urz7OXt8iDu4SDu8uPw8+fq5SDy7uLg8O7iICji++/u6+3l7ejoIPDg4e7yKSwg7+Xw5eTg9+Ug6Ozz+eXx8uLl7e379SDv8ODiICjk7urz7OXt8iDu4SDu6uDn4O3o6CDz8evz4ykiIM3g6Ozd6u7t0fPh0e7x8j0izs7OICZxdW90O83u4vvpIO7y7/Dg4ujy5ev8JnF1b3Q7IiDP7tTg6vLVxj0ixO7q8+zl7fIg7uEg7vLj8PPn6uUg8u7i4PDu4iAo4vvv7uvt5e3o6CDw4OHu8iksIO/l8OXk4PflIOjs8/nl8fLi5e3t+/Ug7/Dg4iAo5O7q8+zl7fIg7uEg7urg5+Dt6Ogg8/Hr8+MpIiDU8+3q9uj/PSLR19TEzs8iPgogICAgPNHi0ffU4OryIMTg8uDR99Q9IjI0LjAxLjIwMjIiIMru5M7Kwj0iNjQzIiDN7uzl8NH31D0iNDE0ODk0MjYxODk0NTMxIj4KICAgICAgPMjx7/DR99QgxOX0xODy4Mjx7/DR99Q9Ii0iIMTl9M3u7Mjx7/DR99Q9Ii0iLz4KICAgICAgPNHiz/Du5D4KICAgICAgICA8yOTR4j4KICAgICAgICAgIDzR4t7L0/cgyM3N3ss9IjY3MzIwMjA1OTkiIMrPzz0iNjczMjAxMDAxIiDN4OjszvDjPSLPyiAmcXVvdDvL4OLg+CZxdW90Oywgzs7OIi8+CiAgICAgICAgPC/I5NHiPgogICAgICAgIDzA5PDl8T4KICAgICAgICAgIDzA5PDQ1CDD7vDu5D0i4y4gyu7x8vDu7OAiIMTu7D0iMTEiIMjt5OXq8T0iMTU2MDA1IiDK7uTQ5ePo7u09IjQ0IiDT6+j24D0i8+suIMvl8e3g/yIvPgogICAgICAgIDwvwOTw5fE+CiAgICAgICAgPMru7fLg6vIg3evP7vfy4D0iYXYub3Jsb3ZAdGVuc29yLnJ1Ii8+CiAgICAgIDwv0eLP8O7kPgogICAgICA8w/Dz587yPgogICAgICAgIDzO7cblPu7tIOblPC/O7cblPgogICAgICA8L8Pw8+fO8j4KICAgICAgPMPw8+fP7uvz9z4KICAgICAgICA8yOTR4j4KICAgICAgICAgIDzR4t7L0/cgyM3N3ss9IjI2MDAzMDMzODUiIMrPzz0iMjYwMDAxMDAxIiDN4OjszvDjPSLOzs4gJnF1b3Q7ze7i++kgz+7r8/fg8uXr/CZxdW90OyIvPgogICAgICAgIDwvyOTR4j4KICAgICAgICA8wOTw5fE+CiAgICAgICAgICA8wOTw0NQgw+7w7uQ9IuMuIMDh5PPr6O3uIiDI7eTl6vE9IjEyNTQ4NyIgyu7k0OXj6O7tPSI1NiIg0ODp7u09IvAt7SDA4eTz6+jt8ero6SIvPgogICAgICAgIDwvwOTw5fE+CiAgICAgIDwvw/Dz58/u6/P3PgogICAgICA80eLP7urz7z4KICAgICAgICA8yOTR4j4KICAgICAgICAgIDzR4t7L0/cgyM3N3ss9IjI2MDAzMDMzODUiIMrPzz0iMjYwMDAxMDAxIiDN4OjszvDjPSLOzs4gJnF1b3Q7ze7i++kgz+7r8/fg8uXr/CZxdW90OyIvPgogICAgICAgIDwvyOTR4j4KICAgICAgICA8wOTw5fE+CiAgICAgICAgICA8wOTw0NQgw+7w7uQ9IuMuIMDh5PPr6O3uIiDI7eTl6vE9IjEyNTQ4NyIgyu7k0OXj6O7tPSI1NiIg0ODp7u09IvAt7SDA4eTz6+jt8ero6SIvPgogICAgICAgIDwvwOTw5fE+CiAgICAgIDwv0eLP7urz7z4KICAgICAgPMTu6s/u5PLizvLj8CDE4PLgxO7qzvLj8D0iMjQuMDEuMjAyMiIgzeDo7MTu6s7y4/A9IsTu6vPs5e3yIO7hIO7y4/Dz5+rlIPLu4uDw7uIgKOL77+7r7eXt6Ogg8ODh7vIpLCDv5fDl5OD35SDo7PP55fHy4uXt7fv1IO/w4OIgKOTu6vPs5e3yIO7hIO7q4Ofg7ejoIPPx6/PjKSIgze7sxO7qzvLj8D0iNDE0ODk0MjYxODk0NTMxIi8+CiAgICAgIDzI7fTP7uvU1cYxPgogICAgICAgIDzS5erx8sjt9CDH7eD35e09IvDl4Ovo5+D26P8g8SDTz8QiIMjk5e3y6PQ9Is/w6Ozl9+Dt6OUiLz4KICAgICAgICA80uXq8fLI7fQgx+3g9+XtPSLw5eDr6Ofg9uj/IPEg08/EIiDI5OXt8uj0PSLI7fTP5fDl5NLg4esiLz4KICAgICAgICA80uXq8fLI7fQgx+3g9+XtPSIyNC4wMS4yMDIyIDExOjQ0OjQxIiDI5OXt8uj0PSLE4PLgw+XtIi8+CiAgICAgICAgPNLl6vHyyO30IMft4Pfl7T0iNDE0ODk0MjYxODk0NTMxIiDI5OXt8uj0PSLN4Orr4OTt4P/N7uzl8CIvPgogICAgICAgIDzS5erx8sjt9CDH7eD35e09IjI0LjAxLjIwMjIiIMjk5e3y6PQ9Is3g6uvg5O3g/8Tg8uAiLz4KICAgICAgICA80uXq8fLI7fQgx+3g9+XtPSIyNC4wMS4yMDIyIiDI5OXt8uj0PSLO8uPw8+fq4MTg8uAiLz4KICAgICAgICA80uXq8fLI7fQgx+3g9+XtPSIyMCIgyOTl7fLo9D0i0fLg4urgzcTRIi8+CiAgICAgICAgPNLl6vHyyO30IMft4Pfl7T0i8+suIMvl8e3g/ywg5C4gMTEiIMjk5e3y6PQ9ItHq6+DkzeDo7OXt7uLg7ejlIi8+CiAgICAgICAgPNLl6vHyyO30IMft4Pfl7T0iaHR0cHM6Ly9maXgtb25saW5lLnNiaXMucnUvb3BlbmRvYy5odG1sP2d1aWQ9MmRiNTY1NDEtZjQ2NC00YTM3LWFhZWMtMGZlNjhjOTgzYWVlJmFtcDtmMz0xMjkmYW1wO2ZpbGU9OTg3NjdlNmMtOGI1ZC00Yzg1LThiN2ItYTJkNDFhNDg1NTJjJmFtcDt2ZXI9MSZhbXA7ZGF0ZT0yMDIyMDEyNDExNDQ0MCZhbXA7YWNjb3VudD0zMTI3NDkyIiDI5OXt8uj0PSLE7urz7OXt8i7R8fvr6uDN4MLr7ubl7ejlIi8+CiAgICAgICAgPNLl6vHyyO30IMft4Pfl7T0iMjQxNTNlNjEtYTMzZC00YWZhLTk2MmQtYTMwMThiM2EzOGY1IiDI5OXt8uj0PSLM18QiLz4KICAgICAgPC/I7fTP7uvU1cYxPgogICAgPC/R4tH31ODq8j4KICAgIDzS4OHr0ffU4OryPgogICAgICA80eLl5NLu4iDK7uvS7uI9IjExIiDN4Ojs0u7iPSLS7uLg8CC5N2I4MTQ5NDctZjg0Yi00OWJmLThhZTYtYjRkNGI4MWNjY2YyXyhAIyQlXn4uLC8pIiDN4OvR8j0iMjAlIiDN7uzR8vA9IjEiIM7Kxchf0u7iPSI3OTYiINHy0u7iweXnzcTRPSIxNTUuODMiINHy0u7i0/fN4Os9IjE4Ny4wMCIg1uXt4NLu4j0iMTQuMTciPgogICAgICAgIDzA6vbo5z4KICAgICAgICAgIDzB5efA6vbo5z7h5ecg4Or26OfgPC/B5efA6vbo5z4KICAgICAgICA8L8Dq9ujnPgogICAgICAgIDzR8+zN4Os+CiAgICAgICAgICA80fPszeDrPjMxLjE3PC/R8+zN4Os+CiAgICAgICAgPC/R8+zN4Os+CiAgICAgICAgPMTu79Hi5eTS7uIgyu7k0u7iPSIwMzM5MjE4NS05YzcxLTMyNzYtYTg2OC0zYTQ4ZjhkZTlmZjIiIM3g6OzF5Mjn7D0i+PIiIM/w0u7i0ODhPSIxIi8+CiAgICAgICAgPMjt9M/u69TVxjIgx+3g9+XtPSLx8vDg7eAg3ev84fDz8ej/IiDI5OXt8uj0PSLP8Ojs5ffg7ejlIi8+CiAgICAgICAgPMjt9M/u69TVxjIgx+3g9+XtPSIwMzM5MjE4NS05YzcxLTMyNzYtYTg2OC0zYTQ4ZjhkZTlmZjIiIMjk5e3y6PQ9ItjKIi8+CiAgICAgICAgPMjt9M/u69TVxjIgx+3g9+XtPSIwMzM5MjE4NS05YzcxLTMyNzYtYTg2OC0zYTQ4ZjhkZTlmZjIiIMjk5e3y6PQ9Isru5CIvPgogICAgICAgIDzI7fTP7uvU1cYyIMft4Pfl7T0iMDMzOTIxODUtOWM3MS0zMjc2LWE4NjgtM2E0OGY4ZGU5ZmYyIiDI5OXt8uj0PSLI5CIvPgogICAgICAgIDzI7fTP7uvU1cYyIMft4Pfl7T0iMDMzOTIxODUtOWM3MS0zMjc2LWE4NjgtM2E0OGY4ZGU5ZmYyIiDI5OXt8uj0PSLK7uTP7vHy4OL56OrgIi8+CiAgICAgICAgPMjt9M/u69TVxjIgx+3g9+XtPSLS7uLg8CC5N2I4MTQ5NDctZjg0Yi00OWJmLThhZTYtYjRkNGI4MWNjY2YyXyhAIyQlXn4uLC8pIiDI5OXt8uj0PSLN4Ofi4O3o5c/u8fLg4vno6uAiLz4KICAgICAgICA8yO30z+7r1NXGMiDH7eD35e09IiZxdW90O1R5cGUmcXVvdDs6JnF1b3Q70u7i4PAmcXVvdDssJnF1b3Q7Q2F0ZWdvcnkmcXVvdDs6JnF1b3Q70u7i4PD7JnF1b3Q7IiDI5OXt8uj0PSLP7uv/ze7s5e3q6+Dy8/D7Ii8+CiAgICAgIDwv0eLl5NLu4j4KICAgICAgPMLx5ePuzu/rINHy0u7iweXnzcTRwvHl4+49IjE1NS44MyIg0fLS7uLT983g68Lx5ePuPSIxODcuMDAiPgogICAgICAgIDzR8+zN4OvC8eXj7j4KICAgICAgICAgIDzR8+zN4Os+MzEuMTc8L9Hz7M3g6z4KICAgICAgICA8L9Hz7M3g68Lx5ePuPgogICAgICAgIDzK7uvN5fLy7sLxPjExPC/K7uvN5fLy7sLxPgogICAgICA8L8Lx5ePuzu/rPgogICAgPC/S4OHr0ffU4OryPgogICAgPNHiz/Du5M/l8D4KICAgICAgPNHiz+XwIMTg8uDP5fA9IjI0LjAxLjIwMjIiINHu5M7v5fA9ItLu4uDw+yDv5fDl5ODt+yI+CiAgICAgICAgPM7x7c/l8CDN4OjszvHtPSLB5ecg5O7q8+zl7fLgLe7x7e7i4O3o/yIvPgogICAgICA8L9Hiz+XwPgogICAgPC/R4s/w7uTP5fA+CiAgICA8z+7k7+jx4O3yIM7h68/u6+09IjUiINHy4PLz8T0iMSIgzvHtz+7r7T0ixO7r5u3u8fLt++Ug7uH/5+Dt7e7x8ugiPgogICAgICA83ssgyM3N3ss9IjY3MzIwMjA1OTkiIM3g6OzO8OM9Is7B2cXR0sLOINEgzsPQwM3I18XNzc7JIM7SwsXS0dLCxc3NztHS3N4gJnF1b3Q7z9DOyMfCzsTR0sLFzc3A3yDKzszPwM3I3yAmcXVvdDvLwMLA2CZxdW90OzEyMyIgxO7r5u09IiI+CiAgICAgICAgPNTIziDU4Ozo6+j/PSLB5ev88ero6SIgyOz/PSLA6+Xq8eDt5PAiIM7y9+Xx8uLuPSLN6Oru6+Dl4uj3Ii8+CiAgICAgIDwv3ss+CiAgICA8L8/u5O/o8eDt8j4KICA8L8Tu6vPs5e3yPgoKPC/U4OnrPgo=",
                                                        "Имя": "ON_NSCHFDOPPR_2BE24e62d2f2ba54942bfe49025c553cc62_2BE8f3178e7ae8c416790175e95e9aed524_20220124_39CFC5F1-DA6D-4285-A69D-187EDE268D0F.xml"
                                                    },
                                                        "Подпись": [
                                                            {    
                                                            "Файл": {
                                                            "Имя": "ON_NSCHFDOPPR_2BE24e62d2f2ba54942bfe49025c553cc62_2BE8f3178e7ae8c416790175e95e9aed524_20220124_39CFC5F1-DA6D-4285-A69D-187EDE268D0F.xml.sgn",
                                                            "ДвоичныеДанные": "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"
                                                                    },
                                                            "Сертификат":
                                                                    {
                                                                       "Доверенность": [
                                                                           {"ИдентификаторМЧД": "832fa66c-0494-4a09-bf1e-c80def4b6805"}
                                                                       ] 
                                                                    }
                                                            }
                                                                ]
                                                    }
                                                ],
                                                "ДопПоля":"ЭтапВернутьВсеСертификаты",
                                                "Дата": "27.09.2023",
                                                "Номер": "OLA27092023",
                                                "Идентификатор": document_id,
                                                "Контрагент": {
                                                    "СвЮЛ": {
                                                    "ИНН": "2600303385",
                                                    "КПП": "260001001",
                                                    "Название": "Новый получатель"
                                                    }
                                                },
                                                "НашаОрганизация": {
                                                    "СвЮЛ": {
                                                    "ИНН": "6732020599",
                                                    "КПП": "673201001"
                                                    }
                                                },
                                                "Примечание": "Тест ExtSDK2 Степанова",
                                                "Тип": "ДокОтгрИсх"
                                                            }
                                            }
                                         )
    
    # Вызов метода ExtSdk2.ExecuteAction
    ole.CallMethod(query_id, guid_module, module_method, parameters_module_method, session_id)

    # Ожидаем ответ через ReadAllObject в цикле по query_id
    result = {}  # Переменная для сохранения результата ExtSdk2.CallSabyApi
    result_checked = False
    while not result_checked:

        events = json.loads(ole.ReadAllObject())  # получить события от плагина и преобразовать в массив json объектов

        # в цикле пройти по каждому событию и найти нужное с ожидаемым query_id
        for event in events:
            if event['type'] == 'Event':
                # если нужное событие пришло, то записать результат в нужную переменную
                print('Запрос ExtSDK2.WriteDocumentEx ушел, смотри логи Плагина')
                response_executeaction = event['data']['data']['Result']      
                result_checked = True
                break
            
        # если ожидаемое событие не найдено, то сделать таймаут в 300мс
        ole.Sleep(300)
    return response_executeaction      

#response_writedocument = write_document()
#response_executeaction = execute_action(response_writedocument)
#list_of_poas = list_of_documents()
#read_document_via_callsabyapi()
#WriteDocumentEx()