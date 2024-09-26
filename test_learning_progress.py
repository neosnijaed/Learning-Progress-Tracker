import unittest

import task

student = task.Student()


class TestLearningProgress(unittest.TestCase):
    def test_check_first_name(self):
        invalid_names = ('-Joe', '\'Joe', 'Joe-', 'Joe\'', 'J3oe', 'J?oe', 'J', 'J-\'oe', 'J\'-oe', 'Stanisław', 'Oğuz')
        for name in invalid_names:
            student.first_name = name
            self.assertFalse(student.check_first_name())

    def test_check_last_name(self):
        invalid_names = (['-Joe', 'Rogan'], ['Joe', 'Rogan-'], ['\'Joe', 'Rogan'], ['Joe', 'Rogan\''])
        for names in invalid_names:
            student.last_name = names
            self.assertFalse(student.check_last_name())

    def test_check_email(self):
        invalid_emails = ('joeraeganmail.com', 'jraegan@gmailcom', '@gmail.com', 'jr@')
        for email in invalid_emails:
            student.email = email
            self.assertFalse(student.check_email())

    def test_check_unique_email(self):
        student.first_name = 'Joe'
        student.last_name = ['Rogan']
        student.email = 'jrogan@mail.com'
        task.store_student_data((student.first_name, student.last_name, student.email), [0, 0, 0, 0])
        self.assertFalse(student.check_unique_email())

    def test_check_credentials(self):
        student.first_name = 'Joe'
        student.last_name = ['Rogan']
        student.email = 'daejin@mail.com'
        self.assertEqual(student.check_credentials(), 'The student has been added.')

        invalid_names = ('-Joe', '\'Joe', 'Joe-', 'Joe\'', 'J3oe', 'J?oe', 'J', 'J-\'oe', 'J\'-oe', 'Stanisław', 'Oğuz')
        for name in invalid_names:
            student.first_name = name
            self.assertEqual(student.check_credentials(), 'Incorrect first name.')

        student.first_name = 'Joe'
        invalid_names = (['-Joe', 'Rogan'], ['Joe', 'Rogan-'], ['\'Joe', 'Rogan'], ['Joe', 'Rogan\''])
        for names in invalid_names:
            student.last_name = names
            self.assertEqual(student.check_credentials(), 'Incorrect last name.')

        student.last_name = ['Rogan']
        invalid_emails = ('daejinseongmail.com', 'daejin@gmailcom', '@gmail.com', 'dj@')
        for email in invalid_emails:
            student.email = email
            self.assertEqual(student.check_credentials(), 'Incorrect email.')

        student.email = 'jrogan@mail.com'
        task.store_student_data((student.first_name, student.last_name, student.email), [0, 0, 0, 0])
        self.assertEqual(student.check_credentials(), 'This email is already taken.')

        student.email = 'joerogan@gmail.com'
        self.assertEqual(student.check_credentials(), 'The student has been added.')

    def test_add_points(self):
        invalid_user_input = ('100', '10', '10', '10', '10')
        self.assertEqual(task.add_points(invalid_user_input), 'No student is found for id=100')

        task.store_student_data(('Joe', ['Rogan'], 'jrogan@gmail.com'), [0, 0, 0, 0])
        invalid_user_inputs = (('1000', '10', '10'), ('1000', '?', '10', '10', '10'),
                               ('1000', '-1', '10', '10', '10'))
        for user_input in invalid_user_inputs:
            self.assertEqual(task.add_points(user_input), 'Incorrect points format.')

        valid_user_input = ('1000', '10', '10', '10', '10')
        self.assertEqual(task.add_points(valid_user_input), 'Points updated.')

    def test_get_student_info(self):
        self.assertEqual(task.get_student_info('1000'), '1000 points: Python=10; DSA=10; Databases=10; Flask=10')

    def test_popular_course(self):
        task.store_student_data(('Elysha', ['Quinlan'], 'address0@mail.com'), [8, 7, 7, 5])
        task.store_student_data(('Beatrisa', ['Jegar'], 'address1@mail.com'), [7, 6, 9, 7])
        task.store_student_data(('Hedwig', ['Wally'], 'address2@mail.com'), [6, 5, 5, 0])
        task.store_student_data(('Shoshana', ['Utica'], 'address3@mail.com'), [8, 0, 8, 6])
        task.store_student_data(('Joe', ['Raegan'], 'address4@mail.com'), [7, 0, 0, 0])
        task.store_student_data(('Lee', ['Fred'], 'address5@mail.com'), [9, 0, 0, 5])

        self.assertEqual(task.popular_course('most'), ['Python'])
        self.assertEqual(task.popular_course('least'), ['DSA'])

        del task.student_collection
        task.student_collection = {}
        task.store_student_data(('Elysha', ['Quinlan'], 'address0@mail.com'), [10, 10, 10, 10])
        task.store_student_data(('Beatrisa', ['Jegar'], 'address1@mail.com'), [5, 5, 5, 5])
        task.store_student_data(('Hedwig', ['Wally'], 'address2@mail.com'), [5, 5, 5, 5])
        task.store_student_data(('Shoshana', ['Utica'], 'address3@mail.com'), [2, 2, 2, 2])
        task.store_student_data(('Joe', ['Raegan'], 'address4@mail.com'), [1, 1, 1, 1])
        task.store_student_data(('Lee', ['Fred'], 'address5@mail.com'), [9, 9, 9, 9])

        self.assertEqual(task.popular_course('most'), ['Python', 'DSA', 'Databases', 'Flask'])
        self.assertEqual(task.popular_course('least'), ['Python', 'DSA', 'Databases', 'Flask'])

        del task.student_collection
        task.student_collection = {}
        task.store_student_data(('Elysha', ['Quinlan'], 'address0@mail.com'), [0, 0, 0, 0])
        task.store_student_data(('Beatrisa', ['Jegar'], 'address1@mail.com'), [0, 0, 0, 0])

        self.assertEqual(task.popular_course('most'), ['n/a'])

    def test_submissions_course(self):
        task.student_submissions = [
            [8, 7, 7, 5],
            [7, 6, 9, 7],
            [6, 5, 5, 1],
            [8, 0, 8, 6],
            [7, 0, 0, 2],
            [9, 0, 0, 5]
        ]
        self.assertEqual(task.submissions_course('highest'), ['Python', 'Flask'])
        self.assertEqual(task.submissions_course('lowest'), ['DSA'])

        del task.student_submissions
        task.student_submissions = [
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.assertEqual(task.submissions_course('highest'), ['n/a'])

    def test_difficulty_course(self):
        task.student_submissions = [
            [8, 7, 5, 5],
            [7, 6, 7, 7],
            [6, 5, 1, 1],
            [8, 0, 6, 6],
            [7, 0, 2, 2],
            [9, 0, 5, 5]
        ]
        self.assertEqual(task.difficulty_course('easiest'), ['Python'])
        self.assertEqual(task.difficulty_course('hardest'), ['Databases', 'Flask'])

        del task.student_submissions
        task.student_submissions = [
            [0, 0, 0, 0], [0, 0, 0, 0]
        ]
        self.assertEqual(task.difficulty_course('easiest'), ['n/a'])

    def test_get_course_statistics(self):
        task.store_student_data(('Joe', ['Rogan'], 'jrogan.mail.com'), [0, 0, 0, 0])
        task.student_submissions = [[0, 0, 0, 0], [0, 0, 0, 0]]
        self.assertEqual(task.get_course_statistics(),
                         'Most popular: Python, DSA, Databases, Flask\n'
                         'Least popular: n/a\n'
                         'Highest activity: n/a\n'
                         'Lowest activity: n/a\n'
                         'Easiest course: n/a\n'
                         'Hardest course: n/a'
                         )
        task.student_submissions = [
            [8, 7, 5, 5],
            [7, 6, 7, 7],
            [6, 5, 1, 1],
            [8, 0, 6, 6],
            [7, 0, 2, 2],
            [9, 0, 5, 5]
        ]
        self.assertEqual(task.get_course_statistics(),
                         'Most popular: Python, DSA, Databases, Flask\n'
                         'Least popular: n/a\n'
                         'Highest activity: Python, Databases, Flask\n'
                         'Lowest activity: DSA\n'
                         'Easiest course: Python\n'
                         'Hardest course: Databases, Flask'
                         )

    def test_notify_completed_courses(self):
        task.store_student_data(('John', ['Doe'], 'johnd@email.net'), [600, 400, 0, 0])
        task.store_student_data(('Jane', ['Spark'], 'jspark@yahoo.com'), [0, 0, 0, 0])
        self.assertEqual(task.notify_completed_courses(),
                         'To: johnd@email.net\n'
                         'Re: Your Learning Progress\n'
                         'Hello, John Doe! You have accomplished our Python!\n'
                         'To: johnd@email.net\n'
                         'Re: Your Learning Progress\n'
                         'Hello, John Doe! You have accomplished our DSA!\n'
                         'Total 1 students have been notified.')


if __name__ == '__main__':
    unittest.main()
