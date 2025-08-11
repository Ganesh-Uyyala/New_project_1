import sqlite3
import json

# Database Setup
def setup_database():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            roll_number TEXT PRIMARY KEY,
            name TEXT,
            marks TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Student Class
class Student:
    def __init__(self, name, roll_number, marks):
        self.name = name
        self.roll_number = roll_number
        self.marks = marks

    def add_or_update_mark(self, subject, updated_marks):
        self.marks[subject] = updated_marks

    def average(self):
        return sum(self.marks.values()) / len(self.marks)

    def grade(self):
        avg = self.average()
        if avg >= 90:
            return "A"
        elif avg >= 75:
            return "B"
        elif avg >= 60:
            return "C"
        elif avg >= 40:
            return "D"
        else:
            return "F"

    def save_to_db(self):
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO students (roll_number, name, marks)
            VALUES (?, ?, ?)
        ''', (self.roll_number, self.name, json.dumps(self.marks)))
        conn.commit()
        conn.close()

    @staticmethod
    def load_from_db(roll_number):
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute('SELECT name, roll_number, marks FROM students WHERE roll_number = ?', (roll_number,))
        row = cursor.fetchone()
        conn.close()
        if row:
            name, roll_number, marks_json = row
            marks = json.loads(marks_json)
            return Student(name, roll_number, marks)
        return None

    @staticmethod
    def load_all_students():
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute('SELECT name, roll_number, marks FROM students')
        rows = cursor.fetchall()
        conn.close()
        return [Student(name, roll, json.loads(marks)) for name, roll, marks in rows]

# Utility Functions
def display_report(student):
    print(f"\nName: {student.name}")
    print(f"Roll Number: {student.roll_number}")
    print("Marks:")
    for subject, mark in student.marks.items():
        print(f"  {subject}: {mark}")
    print(f"Average: {student.average():.2f}")
    print(f"Grade: {student.grade()}")

def display_top_students(students, top_n=3):
    sorted_students = sorted(students, key=lambda s: s.average(), reverse=True)
    print(f"\nTop {top_n} Performers:")
    for i, student in enumerate(sorted_students[:top_n], 1):
        print(f"{i}. {student.name} (Roll: {student.roll_number}) - Avg: {student.average():.2f}, Grade: {student.grade()}")

# Main Menu
def main():
    setup_database()

    while True:
        print("\n--- Student Management Menu ---")
        print("1. Add new student")
        print("2. Update marks")
        print("3. View student report")
        print("4. Display top 3 performers")
        print("5. Save and Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter name of the student: ")
            roll = input("Enter the student roll number: ")
            if Student.load_from_db(roll):
                print("Student with this roll number already exists.")
                continue
            subjects = int(input("Enter the total number of subjects: "))
            marks = {}
            for _ in range(subjects):
                subject = input("Enter subject: ")
                mark = int(input("Enter marks: "))
                marks[subject] = mark
            student = Student(name, roll, marks)
            student.save_to_db()
            print("Student added.")

        elif choice == '2':
            roll = input("Enter roll number: ")
            student = Student.load_from_db(roll)
            if not student:
                print("Student not found.")
                continue
            subject = input("Enter subject to update: ")
            mark = int(input("Enter new mark: "))
            student.add_or_update_mark(subject, mark)
            student.save_to_db()
            print("Mark updated.")

        elif choice == '3':
            roll = input("Enter roll number: ")
            student = Student.load_from_db(roll)
            if not student:
                print("Student not found.")
            else:
                display_report(student)

        elif choice == '4':
            students = Student.load_all_students()
            if not students:
                print("No students to display.")
            else:
                display_top_students(students)

        elif choice == '5':
            print("Exiting. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
