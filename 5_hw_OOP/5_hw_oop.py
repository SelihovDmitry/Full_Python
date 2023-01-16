from statistics import mean

class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def add_courses(self, course_name):
        self.finished_courses.append(course_name)

    def put_a_rating(self, lector, course, grade):
        if isinstance(lector, Lecturer) and course in self.courses_in_progress and course in lector.courses_attached:
            if course in lector.grades:
                lector.grades[course] += [grade]
            else:
                lector.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __avg_rating(self, grades):
        res = 0
        for v in grades.values():
            res += sum(v) / len(v)  # сумма средних по всем предметам
        return res / len(grades)  # общее среднее - сумма средних / длину словаря (кол-во предметов)

    def __str__(self):
        print(f'Имя: {self.name}\nФамилия: {self.surname}')
        print(f'Средняя оценка за домашние задания: {self.__avg_rating(self.grades)}')
        print(f'Курсы в процессе изучения: {", ".join(self.courses_in_progress)}')
        return f'Завершенные курсы: {", ".join(self.finished_courses)}'

    def __lt__(self, other):
        if isinstance(other, Student):
            return self.__avg_rating(self.grades) < other.__avg_rating(other.grades)
        else:
            return 'Не Студент'


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __avg_rating(self, grades):
        res = 0
        for v in grades.values():
            res += sum(v) / len(v)  # сумма средних по всем предметам
        return res / len(grades)  # общее среднее - сумма средних / длину словаря (кол-во предметов)

    def __str__(self):
        res = f'Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {self.__avg_rating(self.grades)}'
        return res

    def __lt__(self, other):
        if isinstance(other, Lecturer):
            return self.__avg_rating(self.grades) < other.__avg_rating(other.grades)
        else:
            return 'Не лектор'


class Rewiever(Mentor):

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        res = f'Имя: {self.name}\nФамилия: {self.surname}'
        return res


# ====================Наполнение ================
student_1 = Student('Dmitrii', 'Selikhov', 'male')
student_1.courses_in_progress += ['Python', 'Git']
student_1.add_courses('school')

student_2 = Student('Ekaterina', 'Romanova', 'female')
student_2.courses_in_progress += ['Python', 'Git']
student_2.add_courses('Math')

rewiever_Python = Rewiever('Aleksei', 'Kuzmin')
rewiever_Python.courses_attached += ['Python']

rewiever_Git = Rewiever('Anna', 'German')
rewiever_Git.courses_attached += ['Git']

lector_Python = Lecturer('Ivan', 'Petrov')
lector_Python.courses_attached += ['Python']
lector_Git = Lecturer('Mariya', 'Konova')
lector_Git.courses_attached += ['Git']

rewiever_Python.rate_hw(student_1, 'Python', 8)
rewiever_Python.rate_hw(student_1, 'Python', 7)
rewiever_Python.rate_hw(student_2, 'Python', 9)
rewiever_Python.rate_hw(student_2, 'Python', 7)

rewiever_Git.rate_hw(student_1, 'Git', 9)
rewiever_Git.rate_hw(student_2, 'Git', 7)
student_1.put_a_rating(lector_Python, 'Python', 10)
student_2.put_a_rating(lector_Python, 'Python', 8)
student_1.put_a_rating(lector_Git, 'Git', 9)
student_2.put_a_rating(lector_Git, 'Git', 8)

students = [student_1, student_2]
lectors = [lector_Python, lector_Git]

def avg_rating_student(students, course):
    res = 0
    cnt = 0
    for student in students:
        if student.grades.get(course, 0) != 0: # проверяем что студент изучает данный курс
            res += mean(student.grades[course]) # сумма средних по студентам в рамках курса
            cnt += 1
    return res / cnt if cnt > 0 else f'Никто не изучает курс: {course}'

def avg_rating_lector(lectors, course):
    res = 0
    cnt = 0
    for lector in lectors:
        if lector.grades.get(course, 0) != 0: # проверяем что лектор читает данный курс
            res += mean(lector.grades[course])
            cnt += 1 # для подсчета лекторов, которые ведут данный курс
    return res / cnt if cnt > 0 else f'Никто не читает курс: {course}'


#==============ПРОВЕРКА===================

print(student_1.grades)
print(student_2.grades)
print(lector_Python.grades)
print(lector_Git.grades)
print('Ревьюеры:')
print(rewiever_Python)
print(rewiever_Git)
print('Лекторы:')
print(lector_Python)
print(lector_Git)
print('Студенты:')
print(student_1)
print(student_2)
print(lector_Python > lector_Git)
print(student_1 < student_2)
print(avg_rating_student(students, 'Python'))
print(avg_rating_student(students, 'Git'))
print(avg_rating_student(students, 'SQL'))
print(avg_rating_lector(lectors, 'Python'))
print(avg_rating_lector(lectors, 'Git'))
print(avg_rating_lector(lectors, 'JS'))

