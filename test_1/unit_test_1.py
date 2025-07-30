import unittest
from task_1 import Student

class TestStudent(unittest.TestCase):
    def setUp(self):
        self.student1 = Student("ganesh","258", {"Maths":90, "English":88, "History":77})
        self.student2 = Student("madhu","226", {"Maths":80, "English":98, "History":70})
    
    def test_init_student1(self):
        self.assertEqual(self.student1.name, "ganesh")
        self.assertEqual(self.student1.roll_number, "258")
        self.assertEqual(self.student1.marks, {"Maths":90, "English":88, "History":77})
    def test_init_student2(self):
        self.assertEqual(self.student2.name, "madhu") 

    def test_update_marks(self):
        result = self.student1.add_or_update_mark("Maths", 95)
        self.assertEqual(self.student1.marks["Maths"],95)
        self.assertEqual(result, "the updated marks list: ")   
