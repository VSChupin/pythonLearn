import unittest
from employee import Employee

class TestEmp(unittest.TestCase):
    
    def setUp(self):
        
        self.current_emp = Employee('Vova', 'Nikkers', 4000)
        
    def test_give_defult_raise(self):
        defult_raise = self.current_emp.give_raise()
        self.assertEqual(defult_raise, 9000)

    def test_give_custom_raise(self):
        
        custom_raise = self.current_emp.give_raise(1000)
        self.assertEqual(custom_raise, 5000)
        
unittest.main()