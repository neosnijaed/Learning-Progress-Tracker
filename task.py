import re

import pyisemail

student_collection = dict()

student_submissions = []


def store_student_data(credentials: tuple[str, list[str], str], points: list[int]):
    student_collection[str(len(student_collection) + 1000)] = [credentials, points]


def notify_completed_courses():
    """
    From Dict student_collection = {student_id: [(first_name, last_name, email), [python points, dsa points, db points,
    flask points]]} select student(s) who have their course(s) completed if the points are greater than its max points
    and send them a notification message. Points of completed courses gets subtracted by its max points.
    :return: String as notification message for completing course(s) by student(s)
    """
    courses = ['Python', 'DSA', 'Databases', 'Flask']
    max_points = [600, 400, 480, 550]
    email_student_course_list = list()
    students = set()
    notify_message = ''
    for student_id, data in student_collection.items():
        for i, point in enumerate(data[1]):
            if point >= max_points[i]:
                email_student_course_list.append([data[0][2], data[0][0], data[0][1], courses[i]])
                student_collection[student_id][1][i] -= max_points[i]
    for student_info in email_student_course_list:
        students.add(student_info[0])
        notify_message += (f'To: {student_info[0]}\n'
                           f'Re: Your Learning Progress\n'
                           f'Hello, {student_info[1]} {" ".join(name for name in student_info[2])}! You have '
                           f'accomplished our {student_info[3]}!\n')
    notify_message += f'Total {len(students)} students have been notified.'
    return notify_message


def get_course_details(learning_course: str) -> str:
    """
    From Dict student_collection = {student_id: [(first_name, last_name, email), [python points, dsa points, db points,
    flask points]]} get students top learners for a specific course by sorting students scores in descending order.
    If 2 or more students have identical scores, their ID gets sorted in ascending order.
    Calculate completion progress for each student in selected course as %.
    :param learning_course: Selected course to determine top students.
    :return: String with top learners of selected course.
    """
    courses = ['Python', 'DSA', 'Databases', 'Flask']
    max_points = [600, 400, 480, 550]
    learning_course_caps = (lambda x: x.upper() if x.lower() == 'dsa' else x.title())(learning_course)
    if learning_course_caps not in courses:
        return 'Unknown course.'

    id_scores = {int(student_id): score[1][courses.index(learning_course)] for student_id, score in
                 student_collection.items()}

    id_scores_sorted = dict(sorted(id_scores.items(), key=lambda x: (x[1], x[0])))
    id_scores_sorted = dict(sorted(id_scores_sorted.items(), key=lambda x: x[1], reverse=True))

    for student_id, score in id_scores_sorted.items():
        id_scores_sorted[student_id] = (score, str(round((score / max_points[courses.index(learning_course)]) * 100, 1))
                                        + '%')

    course_details = f'{learning_course_caps}\n'f'id    points    completed'
    for student_id, score in id_scores_sorted.items():
        if score[0] > 0:
            course_details += f'\n{student_id} {score[0]} \t{score[1]}'
    return course_details


def popular_course(most_or_least: str) -> list[str]:
    """
    In Dict student_collection = {student_id: [(first_name, last_name, email), [python points, dsa points, db points,
    flask points]]} for each course [Python, DSA, Databases, Flask] get amount of non-zero points.
    Determine most or least popular course(s) by getting max or least amount of points.
    :param most_or_least: Determine whether to get most or least popular course(s).
    :return: list[str]: Most or least popular course(s).
    """
    enrolled_students_python = len(
        list(filter(lambda x: x > 0, [value[1][0] for value in student_collection.values()])))
    enrolled_students_dsa = len(list(filter(lambda x: x > 0, [value[1][1] for value in student_collection.values()])))
    enrolled_students_db = len(list(filter(lambda x: x > 0, [value[1][2] for value in student_collection.values()])))
    enrolled_students_flask = len(list(filter(lambda x: x > 0, [value[1][3] for value in student_collection.values()])))

    enrolled_students = [enrolled_students_python, enrolled_students_dsa, enrolled_students_db,
                         enrolled_students_flask]
    courses = ['Python', 'DSA', 'Databases', 'Flask']

    if enrolled_students == [0, 0, 0, 0]:
        return ['n/a']
    elif most_or_least == 'most':
        return [courses[i] for i, enrolled_student in enumerate(enrolled_students) if enrolled_student ==
                max(enrolled_students)]
    elif most_or_least == 'least':
        return [courses[i] for i, enrolled_student in enumerate(enrolled_students) if enrolled_student ==
                min(enrolled_students)]


def submissions_course(highest_or_lowest: str) -> list[str]:
    """
    From student_submissions = list(list(python points, dsa points, db points, flask points)) for each course
    [Python, DSA, Databases, Flask] get amount of non-zero points.
    Determine highest or lowest submissions course(s) by getting max or min amount of points.
    :param highest_or_lowest: Determine whether to get course(s) with highest or lowest submissions.
    :return: list[str]: Course(s) with highest or lowest submissions.
    """
    submissions_python = len(
        list(filter(lambda x: x > 0, [points[0] for points in student_submissions])))
    submissions_dsa = len(list(filter(lambda x: x > 0, [points[1] for points in student_submissions])))
    submissions_db = len(list(filter(lambda x: x > 0, [points[2] for points in student_submissions])))
    submissions_flask = len(list(filter(lambda x: x > 0, [points[3] for points in student_submissions])))

    submissions = [submissions_python, submissions_dsa, submissions_db, submissions_flask]
    courses = ['Python', 'DSA', 'Databases', 'Flask']

    if submissions == [0, 0, 0, 0]:
        return ['n/a']
    elif highest_or_lowest == 'highest':
        return [courses[i] for i, submission in enumerate(submissions) if submission == max(submissions)]
    elif highest_or_lowest == 'lowest':
        return [courses[i] for i, submission in enumerate(submissions) if submission == min(submissions)]


def difficulty_course(easiest_or_hardest: str) -> list[str]:
    """
    From student_submissions = list(list(python points, dsa points, db points, flask points)) for each course
    [Python, DSA, Databases, Flask] calculate average of score points.
    Determine easiest or hardest course(s) by getting min or max average points.
    :param easiest_or_hardest: Determine whether to get course(s) with highest or lowest average points.
    :return: List of course(s) with highest or lowest average points.
    """
    difficulty_python = (lambda x: sum(x) / len(x) if len(x) != 0 else 0)([points[0] for points in student_submissions
                                                                           if points[0] > 0])
    difficulty_dsa = (lambda x: sum(x) / len(x) if len(x) != 0 else 0)([points[1] for points in student_submissions
                                                                        if points[1] > 0])
    difficulty_db = (lambda x: sum(x) / len(x) if len(x) != 0 else 0)([points[2] for points in student_submissions
                                                                       if points[2] > 0])
    difficulty_flask = (lambda x: sum(x) / len(x) if len(x) != 0 else 0)([points[3] for points in student_submissions
                                                                          if points[3] > 0])

    difficulties = [difficulty_python, difficulty_dsa, difficulty_db, difficulty_flask]
    courses = ['Python', 'DSA', 'Databases', 'Flask']

    if difficulties == [0, 0, 0, 0]:
        return ['n/a']
    elif easiest_or_hardest == 'easiest':
        return [courses[i] for i, difficulty in enumerate(difficulties) if difficulty == max(difficulties)]
    elif easiest_or_hardest == 'hardest':
        return [courses[i] for i, difficulty in enumerate(difficulties) if difficulty == min(difficulties)]


def get_course_statistics() -> str:
    popular_courses = popular_course("most")
    submissions = submissions_course("highest")
    easiest_courses = difficulty_course("easiest")
    return (f'Most popular: {", ".join(course for course in popular_courses)}\n'
            f'Least popular: '
            f'{", ".join(course for course in popular_course("least")) if len(popular_courses) < 4 else "n/a"}\n'
            f'Highest activity: {", ".join(course for course in submissions)}\n'
            f'Lowest activity: '
            f'{", ".join(course for course in submissions_course("lowest")) if len(submissions) < 4 else "n/a"}\n'
            f'Easiest course: {", ".join(course for course in easiest_courses)}\n'
            f'Hardest course: '
            f'{", ".join(course for course in difficulty_course("hardest")) if len(easiest_courses) < 4 else "n/a"}')


def add_points(user_input: tuple[str, ...]):
    for num in user_input[1:]:
        if not num.isdigit() or int(num) < 0:
            return 'Incorrect points format.'
    if user_input[0] not in student_collection.keys():
        return f'No student is found for id={user_input[0]}'
    elif len(user_input) != 5:
        return 'Incorrect points format.'
    points = []
    for i, num in enumerate(student_collection[user_input[0]][1]):
        student_collection[user_input[0]][1][i] += int(user_input[i + 1])
        points.append(int(user_input[i + 1]))
    student_submissions.append(points)
    return 'Points updated.'


def get_student_info(user_input: str):
    if user_input not in student_collection.keys():
        return f'No student is found for id={user_input}.'
    else:
        return (f'{user_input} points: Python={student_collection[user_input][1][0]}; '
                f'DSA={student_collection[user_input][1][1]}; '
                f'Databases={student_collection[user_input][1][2]}; '
                f'Flask={student_collection[user_input][1][3]}')


class Student:
    def __init__(self):
        self.first_name = ''
        self.last_name = []
        self.email = ''

    def set_credentials(self, user_input: list[str]) -> None:
        self.first_name = user_input[0]
        self.last_name = user_input[1:-1]
        self.email = user_input[-1]

    def check_first_name(self) -> bool:
        regexp = "^([a-zA-Z]+[\'-]?)+[a-zA-Z]+$"
        if re.match(regexp, self.first_name):
            return True
        return False

    def check_last_name(self) -> bool:
        regexp = "^([a-zA-Z]+[\'-]?)+[a-zA-Z]+$"
        for name in self.last_name:
            if re.match(regexp, name):
                continue
            else:
                return False
        return True

    def check_email(self) -> bool:
        return pyisemail.is_email(self.email, allow_gtld=False)

    def check_unique_email(self) -> bool:
        for credentials in student_collection.values():
            if self.email in credentials[0]:
                return False
        return True

    def check_credentials(self) -> str:
        if not self.check_first_name():
            return 'Incorrect first name.'
        elif not self.check_last_name():
            return 'Incorrect last name.'
        elif not self.check_email():
            return 'Incorrect email.'
        elif not self.check_unique_email():
            return 'This email is already taken.'
        else:
            store_student_data((self.first_name, self.last_name, self.email), [0, 0, 0, 0])
            return 'The student has been added.'


def main():
    print("Learning Progress Tracker")

    while True:
        user_input = input().strip()
        if len(user_input) == 0:
            print('No input.')
        elif user_input == 'exit':
            print('Bye!')
            break
        elif user_input == 'back':
            print('Enter \'exit\' to exit the program.')
        elif user_input == 'add students':
            print('Enter student credentials or \'back\' to return:')
            while True:
                credentials = input().strip()
                if credentials == 'back':
                    print(f'Total {len(student_collection)} students have been added.')
                    break
                elif len(credentials.split()) < 3:
                    print('Incorrect credentials.')
                    continue
                student = Student()
                student.set_credentials(credentials.split())
                print(student.check_credentials())
                del student
        elif user_input == 'list':
            if len(student_collection) == 0:
                print('No students found.')
            else:
                print('Students:')
                print(*student_collection.keys(), sep='\n')
        elif user_input == 'add points':
            print('Enter an id and points or \'back\' to return:')
            while True:
                points = input().strip()
                if points == 'back':
                    break
                print(add_points(tuple(points.split())))
        elif user_input == 'find':
            print('Enter an id or \'back\' to return:')
            while True:
                student_id = input().strip()
                if student_id == 'back':
                    break
                print(get_student_info(student_id))
        elif user_input == 'statistics':
            print('Type the name of a course to see details or \'back\' to quit:')
            print(get_course_statistics())
            while True:
                course = input().strip()
                if course == 'back':
                    break
                print(get_course_details(course))
        elif user_input == 'notify':
            print(notify_completed_courses())
        else:
            print('Error: unknown command!')


if __name__ == '__main__':
    main()
