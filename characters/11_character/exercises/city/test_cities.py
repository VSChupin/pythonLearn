import unittest
from city_function import city_format

class CityNameCase(unittest.TestCase):
    """Тесты для city_function.py"""

    def test_city_function(self):
        """Работает ли функция?"""

        formatted_city_name = city_format('russia', 'moscow')
        self.assertEqual(formatted_city_name, 'Russia, Moscow')
        
    def test_city_function_population(self):
        """Работает ли функция?"""

        formatted_city_name = city_format('russia', 'moscow', 100)
        self.assertEqual(formatted_city_name, 'Russia, Moscow - population 100')


unittest.main()