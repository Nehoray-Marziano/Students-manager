import sqlite3


class course:
    def __init__(self, id, course_name, student, number_of_students, class_id, course_length):
        self.id = id
        self.course_name = course_name
        self.student = student
        self.number_of_students = number_of_students
        self.class_id = class_id
        self.course_length = course_length
        self.isAvailable = True


class courses:
    def __init__(self, dbconn):  # getting the connection
        self.dbconn = dbconn

    def insert(self, course):  # add a course to the table
        tmp_cursor = self.dbconn.cursor()
        tmp_cursor.execute("""
        INSERT INTO courses (id, course_name, student, number_of_students, class_id, course_length) VALUES (?,?,?,?,?,?)
        """, [course.id, course.course_name, course.student, course.number_of_students, course.class_id,
              course.course_length])
        self.dbconn.commit()

    def find(self, id):  # find a course from the table
        tmp_cursor = self.dbconn.cursor()
        tmp_cursor.execute("""
        SELECT * FROM courses WHERE id = ? 
        """, [id])
        self.dbconn.commit()
        return course(*tmp_cursor.fetchone())

    def deleteCourse(self, courseID):
        c = self.dbconn.cursor()
        c.execute("""
                    DELETE FROM courses WHERE id = ?
                """, (courseID, ))
        self.dbconn.commit()

    def changeAvailability(self, courseID):
        currCourse = self.find(courseID)
        currCourse.isAvailable = False


class student:
    def __init__(self, grade, count):
        self.grade = grade
        self.count = count


class students:
    def __init__(self, dbconn):
        self.dbconn = dbconn

    def insert(self, student):  # adding a grade
        tmp_cursor = self.dbconn.cursor()
        tmp_cursor.execute("""
        INSERT INTO students (grade,count) VALUES (?,?)
        """, [student.grade, student.count])
        self.dbconn.commit()

    def find(self, grade):
        tmp_cursor = self.dbconn.cursor()
        tmp_cursor.execute("""
        SELECT * FROM students WHERE grade = ? 
        """, [grade])
        self.dbconn.commit()
        return student(*tmp_cursor.fetchone())

    def reduceAmount(self, grade, nos):  # reducing the number of the students who assigned to classroom
        currGrade = self.find(grade)
        tmp_cursor = self.dbconn.cursor()
        tmp_cursor.execute("""
        UPDATE students
        SET count = ?
        WHERE grade = ?
        """, [currGrade.count - nos, grade])
        self.dbconn.commit()


class classroom:
    def __init__(self, id, location, current_course_id, current_course_time_left):
        self.id = id
        self.location = location
        self.current_course_id = current_course_id
        self.current_course_time_left = current_course_time_left
        self.isAvailable = True


class classrooms:
    def __init__(self, dbconn):
        self.dbconn = dbconn

    def insert(self, classroom):  # add a classroom
        tmp_cursor = self.dbconn.cursor()
        tmp_cursor.execute("""
        INSERT INTO classrooms(id, location, current_course_id, current_course_time_left) VALUES (?,?,?,?)
        """, [classroom.id, classroom.location, classroom.current_course_id, classroom.current_course_time_left])
        self.dbconn.commit()

    def find(self, id):  # find a classroom
        tmp_cursor = self.dbconn.cursor()
        tmp_cursor.execute("""
        SELECT * FROM classrooms WHERE id = ?
        """, [id])
        self.dbconn.commit()
        tmp_out = tmp_cursor.fetchone()
        return classroom(tmp_out[0], tmp_out[1], tmp_out[2], tmp_out[3])


    def getClassbyCourseID(self, courseID):
        tmp_cursor = self.dbconn.cursor()
        tmp_cursor.execute("""
                SELECT * FROM classrooms WHERE current_course_id = ?
                """, [courseID])
        self.dbconn.commit()
        return classroom(tmp_cursor.fetchone())

    def reduceTimeLeft(self, my_classroom):  # reducing time left ov each course on the list by -1 each iteration

            self.dbconn.execute("""     
                      UPDATE classrooms 
                      SET current_course_time_left = current_course_time_left - ? 
                      WHERE current_course_id = ?
                 """, [1, my_classroom.current_course_id])
            self.dbconn.commit()

    def getAllClr1(self):
        c = self.dbconn.cursor()
        all3 = c.execute("""
            SELECT * FROM classrooms
        """).fetchall()
        self.dbconn.commit()
        return [classroom(*row) for row in all3]

    def checkTimeLeft(self, courseID):
        return self.getClassbyCourseID(courseID).current_course_time_left

    def deleteCourseFromTable(self, classroomID):
        self.updateClassroom(0, 0, classroomID)
        self.dbconn.commit()

    def updateClassroom(self, classCurrCourseID, classTime, classID):
        c = self.dbconn.cursor()
        c.execute("""     
                        UPDATE classrooms 
                        SET current_course_id = ?,
                        current_course_time_left = ? 
                        WHERE id = ?
                        """, [classCurrCourseID, classTime, classID])
        self.dbconn.commit()


class Repo:
    def __init__(self):
        self.dbconn = sqlite3.connect('schedule.db')
        self.courses = courses(self.dbconn)
        self.students = students(self.dbconn)
        self.classrooms = classrooms(self.dbconn)

    def _close(self):
        self.dbconn.commit()
        self.dbconn.close()

    def create_courses(self):  # creating the courses' table
        self.dbconn.executescript("""
            CREATE TABLE courses (
                id INTEGER PRIMARY KEY ,
                course_name TEXT NOT NULL ,
                student TEXT NOT NULL ,
                number_of_students INTEGER NOT NULL ,
                class_id INTEGER REFERENCES classrooms(id) ,
                course_length INTEGER NOT NULL 
            ); 
            """)
        self.dbconn.commit()

    def create_students(self):  # creating the courses' table
        self.dbconn.execute("""
                    CREATE TABLE students (
                    grade TEXT PRIMARY KEY,
                    count INTEGER NOT NULL 
                    );
                    """)
        self.dbconn.commit()

    def create_classrooms(self):  # creating the courses' table
        tmp_cursor = self.dbconn.cursor()
        tmp_cursor.execute("""
                    CREATE TABLE classrooms(
                    id INTEGER PRIMARY KEY ,
                    location TEXT NUT NULL ,
                    current_course_id INTEGER NOT NULL ,
                    current_course_time_left INTEGER NOT NULL 
                    );
                    """)
        self.dbconn.commit()

    def getAllCourses(self):  # gets all the courses as a list of courses todo: may need to change
        c = self.dbconn.cursor()
        all1 = c.execute("""
            SELECT * FROM courses
        """).fetchall()
        self.dbconn.commit()
        return [course(*row) for row in all1]

    def getAllCoursesT(self):  # gets all the courses as a list of courses todo: may need to change
        c = self.dbconn.cursor()
        all1 = c.execute("""
            SELECT * FROM courses
        """).fetchall()
        self.dbconn.commit()
        return all1

    def getAllStudents(self):  # gets all the students as a list of student
        c = self.dbconn.cursor()
        all2 = c.execute("""
            SELECT * FROM students
        """).fetchall()
        self.dbconn.commit()
        return [student(*row) for row in all2]

    def getAllStudentsT(self):  # gets all the students as a list of student
        c = self.dbconn.cursor()
        all2 = c.execute("""
            SELECT * FROM students
        """)
        self.dbconn.commit()
        return all2.fetchall()

    def getAllClr(self):
        c = self.dbconn.cursor()
        all3 = c.execute("""
            SELECT * FROM classrooms
        """).fetchall()
        self.dbconn.commit()
        return [classroom(*row) for row in all3]

    def getAllClrT(self):
        c = self.dbconn.cursor()
        all3 = c.execute("""
            SELECT * FROM classrooms
        """).fetchall()
        self.dbconn.commit()
        return all3

    def checkCoursesLength(self):
        all4 = self.getAllCourses()
        if len(all4) == 0:
            return False
        else:
            return True


