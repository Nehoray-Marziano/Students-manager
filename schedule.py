import os
from PL import courses, classrooms, students, Repo
import PL


def print_table(list_of_tuples):
    for item in list_of_tuples:
        print(item)


def main():
    did_enter = False
    repo = Repo()
    clr_list = repo.getAllClr()
    clr_size = len(clr_list)
    counter = 1
    tmp_courses = courses(repo.dbconn)
    tmp_classrooms = classrooms(repo.dbconn)

    while os.path.exists('schedule.db') and repo.checkCoursesLength():
        did_enter = True
        courses_list = repo.getAllCourses()
        if counter == 1: #if it is the first iteration
            i = 0
            successfully_added = 0
            while successfully_added < clr_size and i < len(courses_list):
                tmpCourse = courses_list[i]  # filling up the classrooms
                curr_clrs = PL.classrooms(repo.dbconn)
                isAvailable = curr_clrs.find(tmpCourse.class_id)
                if isAvailable.current_course_id == 0:
                    curr_clrs.updateClassroom(tmpCourse.id, tmpCourse.course_length, tmpCourse.class_id)
                    curr_stud = PL.students(repo.dbconn)
                    curr_stud.reduceAmount(tmpCourse.student, tmpCourse.number_of_students)
                    successfully_added = successfully_added + 1

                    out_classroom = curr_clrs.find(tmpCourse.class_id)
                    if counter == 1:
                        print('(' + str(counter-1) + ') ' + out_classroom.location + ': ' + tmpCourse.course_name + ' is schedule to start')


                i = i + 1
            counter = counter + 1

        elif counter != 1:
            new_clr = repo.getAllClr()
            our_courses = courses(repo.dbconn)
            for tmp_classroom in new_clr:
                if tmp_classroom.current_course_id != 0:
                    out_course = our_courses.find(tmp_classroom.current_course_id)
                    if tmp_classroom.current_course_time_left == 1:     # meaning it is about to be over
                        tmp_classrooms.reduceTimeLeft(tmp_classroom)
                        print('(' + str(counter-1) + ') ' + tmp_classroom.location + ': ' + out_course.course_name + ' is done')
                        tmp_courses.deleteCourse(tmp_classroom.current_course_id)
                        tmp_classrooms.deleteCourseFromTable(tmp_classroom.id)
                        allCourses = repo.getAllCourses()
                        if len(allCourses) > 0:
                            for course1 in allCourses:
                                if course1.class_id == tmp_classroom.id:
                                    tmp_classrooms.updateClassroom(course1.id, course1.course_length, tmp_classroom.id)
                                    curr_stud1 = PL.students(repo.dbconn)
                                    curr_stud1.reduceAmount(course1.student, course1.number_of_students)
                                    print('(' + str(counter - 1) + ') ' + tmp_classroom.location + ': ' + course1.course_name + ' is schedule to start')
                                    break
                        elif len(allCourses) == 0:
                            break
                    elif tmp_classroom.current_course_time_left > 1:       # time-left>0
                        print('(' + str(counter - 1) + ') ' + tmp_classroom.location + ': occupied by ' + out_course.course_name)
                        tmp_classrooms.reduceTimeLeft(tmp_classroom)
            counter = counter + 1
        studentsList = repo.getAllStudentsT()
        classroomsList = repo.getAllClrT()
        coursesList = repo.getAllCoursesT()
        print("courses")
        print_table(coursesList)
        print("classrooms")
        print_table(classroomsList)
        print("students")
        print_table(studentsList)
        repo.dbconn.commit()

    if did_enter == False:      #if there are no courses
        studentsList = repo.getAllStudentsT()
        classroomsList = repo.getAllClrT()
        coursesList = repo.getAllCoursesT()
        print("courses")
        print_table(coursesList)
        print("classrooms")
        print_table(classroomsList)
        print("students")
        print_table(studentsList)
        repo.dbconn.commit()




if __name__ == '__main__':
    main()
