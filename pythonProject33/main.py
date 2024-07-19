import sqlite3


conn = sqlite3.connect('students.db')
conn.text_factory = lambda x: str(x, 'utf-8', 'ignore')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL
)
''')


cursor.execute('''
CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    subject TEXT NOT NULL,
    grade REAL NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id)
)
''')


conn.commit()
conn.close()

import sqlite3

class University:
    def __init__(self, name):
        self.name = name
        self.conn = sqlite3.connect('students.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                age INTEGER
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS grades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                subject TEXT,
                grade REAL,
                FOREIGN KEY (student_id) REFERENCES students (id)
            )
        ''')
        self.conn.commit()

    def clear_tables(self):
        self.cursor.execute("DELETE FROM students")
        self.cursor.execute("DELETE FROM grades")
        self.conn.commit()

    def add_student(self, name, age):
        try:
            self.cursor.execute("INSERT INTO students (name, age) VALUES (?, ?)", (name, age))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Ошибка при добавлении студента: {e}")

    def add_grade(self, student_id, subject, grade):
        try:
            self.cursor.execute("INSERT INTO grades (student_id, subject, grade) VALUES (?, ?, ?)", (student_id, subject, grade))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Ошибка при добавлении оценки: {e}")

    def get_students(self, subject=None):
        try:
            if subject:
                self.cursor.execute('''
                    SELECT students.name, students.age, grades.subject, grades.grade
                    FROM students
                    JOIN grades ON students.id = grades.student_id
                    WHERE grades.subject = ?
                ''', (subject,))
            else:
                self.cursor.execute('''
                    SELECT students.name, students.age, grades.subject, grades.grade
                    FROM students
                    JOIN grades ON students.id = grades.student_id
                ''')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Ошибка при получении списка студентов: {e}")
            return []

    def close(self):
        self.conn.close()


uni = University("Urban")


uni.clear_tables()


uni.add_student("Ivan", 26)
uni.add_student("Ilya", 24)
uni.add_student("Anna", 22)
uni.add_student("Maria", 23)


uni.add_grade(1, "Python", 4.8)
uni.add_grade(1, "Math", 4.5)
uni.add_grade(2, "PHP", 4.3)
uni.add_grade(2, "HTML", 4.2)
uni.add_grade(3, "Python", 4.7)
uni.add_grade(3, "Math", 4.6)
uni.add_grade(4, "PHP", 4.4)
uni.add_grade(4, "HTML", 4.3)


students = uni.get_students()
for student in students:
    print(student)


uni.close()
