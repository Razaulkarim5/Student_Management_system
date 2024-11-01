import json

class Person: # person class
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address

    def display_person_info(self):# method inside person class
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Address: {self.address}")


class Student(Person): #student class inherit person class
    def __init__(self, name, student_id, age, address):
        super().__init__(name, age, address)
        self.student_id = student_id
        self.grades = {}
        self.courses = []

    def add_grade(self, subject, grade):
        self.grades[subject] = grade
        print(f"Grade {grade} added for {self.name} in {subject}.")

    def enroll_course(self, course):
        self.courses.append(course)
        print(f"Student {self.name} (ID: {self.student_id}) enrolled in {course.course_name} (Code: {course.course_code}).")

    def display_student_info(self):
        print("Student Information:")
        print(f"Name: {self.name}")
        print(f"ID: {self.student_id}")
        print(f"Age: {self.age}")
        print(f"Address: {self.address}")
        print("Enrolled Courses:", ', '.join(course.course_name for course in self.courses))
        print("Grades:", self.grades)


class Course:# class course
    def __init__(self, course_name, course_code, instructor):
        self.course_name = course_name
        self.course_code = course_code
        self.instructor = instructor
        self.students = []

    def add_student(self, student):
        self.students.append(student)
        student.enroll_course(self)

    def display_course_info(self):
        print("Course Information:")
        print(f"Course Name: {self.course_name}")
        print(f"Code: {self.course_code}")
        print(f"Instructor: {self.instructor}")
        print("Enrolled Students:", ', '.join(student.name for student in self.students))


class StudentManagementSystem:# class student Management
    def __init__(self):
        self.students = {}
        self.courses = {}

    def add_student(self):
        name = input("Enter Name: ")
        age = int(input("Enter Age: "))
        address = input("Enter Address: ")
        student_id = input("Enter Student ID: ")
        student = Student(name, student_id, age, address)
        self.students[student_id] = student
        print(f"Student {name} (ID: {student_id}) added successfully.")

    def add_course(self):
        course_name = input("Enter Course Name: ")
        course_code = input("Enter Course Code: ")
        instructor = input("Enter Instructor Name: ")
        course = Course(course_name, course_code, instructor)
        self.courses[course_code] = course
        print(f"Course {course_name} (Code: {course_code}) created with instructor {instructor}.")

    def enroll_student_in_course(self):
        student_id = input("Enter Student ID: ")
        course_code = input("Enter Course Code: ")
        if student_id in self.students and course_code in self.courses:
            student = self.students[student_id]
            course = self.courses[course_code]
            course.add_student(student)
        else:
            print("Invalid student ID or course code.")

    def add_grade_for_student(self):
        student_id = input("Enter Student ID: ")
        course_code = input("Enter Course Code: ")
        grade = input("Enter Grade: ")
        if student_id in self.students and course_code in self.courses:
            student = self.students[student_id]
            if any(course.course_code == course_code for course in student.courses):
                student.add_grade(course_code, grade)
            else:
                print(f"{student.name} is not enrolled in {course_code}.")
        else:
            print("Invalid student ID or course code.")

    def display_student_details(self):
        student_id = input("Enter Student ID: ")
        if student_id in self.students:
            self.students[student_id].display_student_info()
        else:
            print("Student not found.")

    def display_course_details(self):
        course_code = input("Enter Course Code: ")
        if course_code in self.courses:
            self.courses[course_code].display_course_info()
        else:
            print("Course not found.")

    def save_data(self):
        data = {
            "students": {student_id: {"name": student.name, "age": student.age, "address": student.address,
                                      "grades": student.grades, "courses": [course.course_code for course in student.courses]}
                         for student_id, student in self.students.items()},
            "courses": {course_code: {"course_name": course.course_name, "instructor": course.instructor,
                                      "students": [student.student_id for student in course.students]}
                        for course_code, course in self.courses.items()}
        }
        with open("student_profile_details.json", "w") as f:# creating json file to store data  Studentt's information
            json.dump(data, f)
        print("All student and course data saved successfully.")

    def load_data(self):
        try:
            with open("student_profile_details.json", "r") as f:
                data = json.load(f)
            for student_id, info in data["students"].items():
                student = Student(info["name"], student_id, info["age"], info["address"])
                student.grades = info["grades"]
                self.students[student_id] = student
            for course_code, info in data["courses"].items():
                course = Course(info["course_name"], course_code, info["instructor"])
                self.courses[course_code] = course
                for student_id in info["students"]:
                    if student_id in self.students:
                        course.add_student(self.students[student_id])
            print("Data loaded successfully.")
        except FileNotFoundError:
            print("No data file found.")

    def menu(self):
        while True:
            print("\n==== Student Management System ====")
            print("1. Add New Student")
            print("2. Add New Course")
            print("3. Enroll Student in Course")
            print("4. Add Grade for Student")
            print("5. Display Student Details")
            print("6. Display Course Details")
            print("7. Save Data to File")
            print("8. Load Data from File")
            print("0. Exit")
            choice = input("Select Option: ")

            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.add_course()
            elif choice == "3":
                self.enroll_student_in_course()
            elif choice == "4":
                self.add_grade_for_student()
            elif choice == "5":
                self.display_student_details()
            elif choice == "6":
                self.display_course_details()
            elif choice == "7":
                self.save_data()
            elif choice == "8":
                self.load_data()
            elif choice == "0":
                print("Exiting Student Management System. Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")

if __name__ == "__main__":
    system = StudentManagementSystem()
    system.menu()
