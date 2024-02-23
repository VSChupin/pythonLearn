class AnonymousSurvey():
    """Сбор анонимных ответов на вопросы."""

    def __init__(self, question):
        self.question = question
        self.responses = []

    def show_question(self):
        """Выводит вопрос"""
        print(self.question)
        
    def store_response(self, new_response):
        """Сохраняет один ответ на вопрос"""
        self.responses.append(new_response)

    def show_result(self): 
        """Выводит полученные ответы"""
        print("Результат опроса: ")
        for response in self.responses:
            print('- '+ response)
            

# new_survey = AnonymousSurvey('сколько тебе лет?')
# new_survey.show_question()
# new_survey.store_response('29')
# new_survey.show_result()