import atexit
import sqlite3
import sys

from PL import student, course, classroom, Repo

dbcon = sqlite3.connect('schedule.db')
filePath = open(sys.argv[1], 'r')  # r?
with dbcon:
    cursor = dbcon.cursor()


def print_table(list_of_tuples):
    for item in list_of_tuples:
        print(item)


def main(args):  # read the lines from the file in order to create the tables
    inputfilename = args[1]
    our_repo = Repo()
    atexit.register(our_repo._close)
    our_repo.create_courses()
    our_repo.create_classrooms()
    our_repo.create_students()
    dbcon.commit()
    i = 1
    with open(inputfilename) as file:
        for line in file:
            globalID = 1
            splited_list = []
            other_line = line.replace('\n', '')
            stringList = other_line.split(',')
            if stringList[0] == 'S':  #student case
                i = 1
                while i < 3:
                    splited_list.append(stringList[i].strip())
                    i = i + 1
                s = student(splited_list[0], splited_list[1])
                our_repo.students.insert(s)

            if stringList[0] == 'C':  #course case
                i = 1
                while i < 7:
                    stringList[i] = stringList[i].strip()
                    i = i + 1
                stringList[4] = int(stringList[4])
                stringList[5] = int(stringList[5])
                stringList[6] = int(stringList[6])
                crs = course(stringList[1], stringList[2], stringList[3], stringList[4], stringList[5], stringList[6])
                our_repo.courses.insert(crs)
                globalID = globalID + 1

            if stringList[0] == 'R':  ##classroom case
                i = 1
                while i < 3:
                    stringList[i] = stringList[i].strip()
                    i = i + 1
                rm = classroom(stringList[1], stringList[2], 0, 0)
                our_repo.classrooms.insert(rm)
    studentsList = our_repo.getAllStudentsT()
    classroomsList = our_repo.getAllClrT()
    coursesList = our_repo.getAllCoursesT()
    print("courses")
    print_table(coursesList)
    print("classrooms")
    print_table(classroomsList)
    print("students")
    print_table(studentsList)


if __name__ == '__main__':
    main(sys.argv)
