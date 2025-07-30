import json
import os
# 1. **Create a `Student` class** with the following attributes:

    #    - Name
    #    - Roll Number
    #    - Dictionary of subjects and marks
class Student:
    def __init__(self, name, roll_number, marks):
        self.name = name
        self.roll_number = roll_number
        self.marks = marks

# 2. **Add methods** to:

    #    - Add/update marks for a subject

    def add_or_update_mark(self, subject_to_update, updated_marks):
        list_1 = []
        for i in self.marks.keys():
            list_1.append(i)
        if subject_to_update in list_1:
            self.marks[subject_to_update] = updated_marks
            return "the updated marks list: "
        else:
            return "please exit and enter the correct subject"
    #    - Calculate average marks
    
    def average(self):
        marks_list = list(self.marks.values())
        return sum(marks_list)/len(marks_list)
    #    - Determine grade based on average:
    #      - A: 90+
    #      - B: 75–89
    #      - C: 60–74
    #      - D: 40–59
    #      - F: <40
    def grade(self):
        if self.average() >= 90:
            return "A"
        elif 75 <= self.average() < 90:
            return "B"
        elif 60 <= self.average() < 75:
            return "C"
        elif 40 <= self.average() < 60:
            return "D"
        else:
            return "F"

    def to_dict(self):
        return {
            'name': self.name,
            'roll_number': self.roll_number,
            'marks': self.marks
        }
    
    def from_dict(data):
        student = Student(data['name'], data['roll_number'], data['marks'])
        return student
# 3. **File Handling:**

    #    - Save student data to a file in JSON format
    #    - Load student data from the file.
def save_students(students, filename):
    with open(filename, 'w') as f:
        json.dump([s.to_dict() for s in students], f, indent=4)

def load_students(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, 'r') as f:
        data = json.load(f)
        return [Student.from_dict(d) for d in data]

def find_student(students, roll_number):
    for s in students:
        if s.roll_number == roll_number:
            return s
    return None

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

# 4. **User Interaction:**

    #    - Menu-driven interface to:
    #      - Add a new student
    #      - Update marks
    #      - View student report
    #      - Save and exit
# 5. ** Sort students by average marks and display the top 3 performers.**

def main():
    filename = "stud.json"
    students = load_students(filename)

    while True:
        print("\n--- Student Management Menu ---")
        print("1. Add new student")
        print("2. Update marks")
        print("3. View student report")
        print("4. Display top 3 performers")
        print("5. Save and exit")
        choice = input("Enter your choice: ")

        #      - Add a new student
        if choice == '1':
            name = input("enter name of the student: ")
            roll = input("enter the student roll_number: ")
            subjects = int(input("enter the total number of subjects: "))
            marks={}
            for i in range(subjects):
                subject = input("enter the subject: ")
                marks_of_subject = int(input("enter the marks: "))
                marks[subject] = marks_of_subject
            if find_student(students, roll):
                print("Student with this roll number already exists.")
            else:
                students.append(Student(name, roll, marks))
                print("Student added.")

        #      - Update marks
        elif choice == '2':
            roll = input("Enter roll number: ")
            student = find_student(students, roll)
            if not student:
                print("Student not found.")
            else:
                subject = input("Enter subject: ")
                try:
                    mark = int(input("Enter mark: "))
                except ValueError:
                    print("Invalid mark.")
                    continue
                student.add_or_update_mark(subject, mark)
                print("Mark updated.")
        #      - View student report
        elif choice == '3':
            roll = input("Enter roll number: ")
            student = find_student(students, roll)
            if not student:
                print("Student not found.")
            else:
                display_report(student)
    
        elif choice == '4':
            if not students:
                print("No students to display.")
            else:
                display_top_students(students)

        elif choice == '5':
            save_students(students, filename)
            print("Data saved. Exiting.")
            break

        else:
            print("Invalid choice. Please try again.")
if __name__ == "__main__":
    main()
