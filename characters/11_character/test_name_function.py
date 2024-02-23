import unittest
from name_function import get_formatted_name

class NamesTestCase(unittest.TestCase):
    """Тесты для 'name_function.py'."""
    
    def test_first_last_name(self): 
        """Имена вида 'Janis Joplin' работают правильно?"""
        formatted_name = get_formatted_name('vova', 'chupin')
        self.assertEqual(formatted_name, 'Vova Chupin')
    
    def test_first_middle_last_name(self):
        """Имена вида 'Vova Chupin Serg' работают правильно?"""

        formatted_name = get_formatted_name('vova', 'chupin', 'serg')
        self.assertEqual(formatted_name, 'Vova Serg Chupin')
        

unittest.main()