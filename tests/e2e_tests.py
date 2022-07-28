import os.path
from models.output import Output
from generators.model_generator import ModelGenerator
from send_generated_input_script.rabbit_mq_publisher import RabbitMqPublisher
from unittest import TestCase
from tests.test_base import TestBase


class E2ETest(TestCase, TestBase):

    def setUp(self):
        self.rabbitmq_publisher = RabbitMqPublisher()
        os.chdir(TestBase.STUDENTS_DIR_PATH)
        if os.path.exists(TestBase.STUDENTS_DIR_PATH):
            for file in os.listdir(TestBase.STUDENTS_DIR_PATH):
                os.remove(os.path.join(TestBase.STUDENTS_DIR_PATH, file))

    def test_output_parse(self):
        input_model = ModelGenerator.generate_input_model()
        parsed_output = TestBase.parse_output(input_model)

        TestBase.send_body(self.rabbitmq_publisher, input_model)

        output_model = Output(**TestBase.read_from_file(f"{TestBase.STUDENTS_DIR_PATH}/{TestBase.get_docs(1)[0]}"))

        self.assertEqual(output_model.studentDetails, parsed_output.studentDetails.__dict__)
        for subject in range(len(parsed_output.subjectGrades)):
            self.assertEqual(output_model.subjectGrades[subject], parsed_output.subjectGrades[subject].__dict__)
        self.assertEqual(output_model.totalAvg, parsed_output.totalAvg)
        self.assertEqual(output_model.birthDate, parsed_output.birthDate)
        self.assertEqual(output_model.age, parsed_output.age)
        self.assertEqual(output_model.gender, parsed_output.gender)
        self.assertEqual(output_model.isGoodBehaviour, parsed_output.isGoodBehaviour)
        self.assertEqual(output_model.age, input_model.age)
        self.assertEqual(output_model.studentDetails['firstName'], input_model.studentDetails['firstName'])
        self.assertEqual(output_model.studentDetails['lastName'], input_model.studentDetails['lastName'])
        self.assertEqual(output_model.studentDetails['id'], input_model.studentDetails['id'])

    def test_valid_file_name_capitalized(self):
        input_model = ModelGenerator.generate_input_model()

        input_model.studentDetails['firstName'] = 'test'
        input_model.studentDetails['lastName'] = 'tester'

        TestBase.send_body(self.rabbitmq_publisher, input_model)

        self.assertEqual(['Test_Tester.txt'], TestBase.get_docs(1))

    def test_valid_file_name_hyphen_lastname(self):
        input_model = ModelGenerator.generate_input_model()

        input_model.studentDetails['firstName'] = 'Test'
        input_model.studentDetails['lastName'] = 'Ben Test'

        TestBase.send_body(self.rabbitmq_publisher, input_model)

        self.assertEqual(['Test_Ben-Test.txt'], TestBase.get_docs(1))

    def test_send_same_body_twice(self):
        input_model = ModelGenerator.generate_input_model()

        TestBase.send_body(self.rabbitmq_publisher, input_model)
        TestBase.send_body(self.rabbitmq_publisher, input_model)

        self.assertTrue(1, len(TestBase.get_docs(1)))

    def test_two_text_files_saved_success(self):
        input_model_1 = ModelGenerator.generate_input_model()
        input_model_2 = ModelGenerator.generate_input_model()

        TestBase.send_body(self.rabbitmq_publisher, input_model_1)
        TestBase.send_body(self.rabbitmq_publisher, input_model_2)

    def test_send_non_json_body(self):
        input_body = """a"""

        with self.assertRaises(Exception):
            TestBase.send_body(self.rabbitmq_publisher, input_body)

        self.assertEqual(0, len(TestBase.get_docs(0)))

    def test_extra_field_body_text_file_saved_success(self):
        input_model = ModelGenerator.generate_input_model()
        input_model.extraField = "test"

        TestBase.send_body(self.rabbitmq_publisher, input_model)

    def test_missing_student_details_body_failure(self):
        input_model = ModelGenerator.generate_input_model()
        input_model.studentDetails = None

        TestBase.send_body(self.rabbitmq_publisher, input_model)

        self.assertEqual(0, len(TestBase.get_docs(0)))

    def test_missing_first_name_body(self):
        input_model = ModelGenerator.generate_input_model()
        input_model.studentDetails['firstName'] = None

        TestBase.send_body(self.rabbitmq_publisher, input_model)

        self.assertEqual(0, len(TestBase.get_docs(0)))

    def test_missing_last_name_body(self):
        input_model = ModelGenerator.generate_input_model()
        input_model.studentDetails['lastName'] = None

        TestBase.send_body(self.rabbitmq_publisher, input_model)

        self.assertEqual(0, len(TestBase.get_docs(0)))

    def test_missing_id_body(self):
        input_model = ModelGenerator.generate_input_model()
        input_model.studentDetails['id'] = None

        TestBase.send_body(self.rabbitmq_publisher, input_model)

        self.assertEqual(0, len(TestBase.get_docs(0)))

    def test_missing_subject_grades_body(self):
        input_model = ModelGenerator.generate_input_model()
        input_model.subjectGrades = None

        TestBase.send_body(self.rabbitmq_publisher, input_model)

        self.assertEqual(0, len(TestBase.get_docs(0)))

    def test_missing_subject_body(self):
        input_model = ModelGenerator.generate_input_model()
        input_model.subjectGrades[0]['subject'] = None

        TestBase.send_body(self.rabbitmq_publisher, input_model)

        self.assertEqual(0, len(TestBase.get_docs(0)))

    def test_missing_grades_body(self):
        input_model = ModelGenerator.generate_input_model()
        input_model.subjectGrades[0]['grades'] = None

        TestBase.send_body(self.rabbitmq_publisher, input_model)

        self.assertEqual(0, len(TestBase.get_docs(0)))

    def test_missing_birtdate_body(self):
        input_model = ModelGenerator.generate_input_model()
        input_model.birthDate = None

        TestBase.send_body(self.rabbitmq_publisher, input_model)

        self.assertEqual(0, len(TestBase.get_docs(0)))

    def test_missing_age_body(self):
        input_model = ModelGenerator.generate_input_model()
        input_model.age = None

        TestBase.send_body(self.rabbitmq_publisher, input_model)

        self.assertEqual(0, len(TestBase.get_docs(0)))

    def test_missing_gender_body(self):
        input_model = ModelGenerator.generate_input_model()
        input_model.gender = None

        TestBase.send_body(self.rabbitmq_publisher, input_model)

        self.assertEqual(0, len(TestBase.get_docs(0)))

    def test_missing_behaviour_grade_body(self):
        input_model = ModelGenerator.generate_input_model()
        input_model.behaviourGrade = None

        TestBase.send_body(self.rabbitmq_publisher, input_model)

        self.assertEqual(0, len(TestBase.get_docs(0)))

    def test_invalid_value_first_name_body(self):
        input_model = ModelGenerator.generate_input_model()
        input_model.studentDetails['firstName'] = 'Raz1'

        TestBase.send_body(self.rabbitmq_publisher, input_model)

        self.assertEqual(0, len(TestBase.get_docs(0)))

    def test_invalid_value_last_name_body(self):
        input_model = ModelGenerator.generate_input_model()
        input_model.studentDetails['lastName'] = 'Matzliah1'

        TestBase.send_body(self.rabbitmq_publisher, input_model)

        self.assertEqual(0, len(TestBase.get_docs(0)))

    def test_invalid_value_id_body(self):
        input_model = ModelGenerator.generate_input_model()
        input_model.studentDetails['id'] = 3227175701

        TestBase.send_body(self.rabbitmq_publisher, input_model)

        self.assertEqual(0, len(TestBase.get_docs(0)))

    def test_invalid_value_subject_body(self):
        input_model = ModelGenerator.generate_input_model()
        input_model.subjectGrades[0]['subject'] = 'Test1'

        TestBase.send_body(self.rabbitmq_publisher, input_model)

        self.assertEqual(0, len(TestBase.get_docs(0)))

    def test_invalid_value_grades_body(self):
        input_model = ModelGenerator.generate_input_model()
        input_model.subjectGrades[0]['grades'] = [101, 90, 80]

        TestBase.send_body(self.rabbitmq_publisher, input_model)

        self.assertEqual(0, len(TestBase.get_docs(0)))

    def test_invalid_value_birtdate_body(self):
        input_model = ModelGenerator.generate_input_model()
        input_model.birthDate = '30/02/2000'

        TestBase.send_body(self.rabbitmq_publisher, input_model)

        self.assertEqual(0, len(TestBase.get_docs(0)))

    def test_invalid_value_age_body(self):
        input_model = ModelGenerator.generate_input_model()
        input_model.age = -1

        TestBase.send_body(self.rabbitmq_publisher, input_model)

        self.assertEqual(0, len(TestBase.get_docs(0)))

    def test_invalid_value_gender_body(self):
        input_model = ModelGenerator.generate_input_model()
        input_model.gender = 'invalid_gender'

        TestBase.send_body(self.rabbitmq_publisher, input_model)

        self.assertEqual(0, len(TestBase.get_docs(0)))

    def test_invalid_value_behaviour_grade_body(self):
        input_model = ModelGenerator.generate_input_model()
        input_model.behaviourGrade = 11

        TestBase.send_body(self.rabbitmq_publisher, input_model)

        self.assertEqual(0, len(TestBase.get_docs(0)))

    def test_invalid_type_student_details_body(self):
        input_model = ModelGenerator.generate_input_model()
        input_model.studentDetails = []

        TestBase.send_body(self.rabbitmq_publisher, input_model)

        self.assertEqual(0, len(TestBase.get_docs(0)))

    def test_invalid_type_first_name_body(self):
        input_model = ModelGenerator.generate_input_model()
        input_model.studentDetails['firstName'] = 1

        TestBase.send_body(self.rabbitmq_publisher, input_model)

        self.assertEqual(0, len(TestBase.get_docs(0)))

    def test_invalid_type_last_name_body(self):
        input_model = ModelGenerator.generate_input_model()
        input_model.studentDetails['lastName'] = 1

        TestBase.send_body(self.rabbitmq_publisher, input_model)

        self.assertEqual(0, len(TestBase.get_docs(0)))

    def test_invalid_type_id_body(self):
        input_model = ModelGenerator.generate_input_model()
        input_model.studentDetails['id'] = 'test'

        TestBase.send_body(self.rabbitmq_publisher, input_model)

        self.assertEqual(0, len(TestBase.get_docs(0)))

    def test_invalid_type_subject_grades_body(self):
        input_model = ModelGenerator.generate_input_model()
        input_model.subjectGrades = {}

        TestBase.send_body(self.rabbitmq_publisher, input_model)

        self.assertEqual(0, len(TestBase.get_docs(0)))

    def test_invalid_type_grades_body(self):
        input_model = ModelGenerator.generate_input_model()
        input_model.subjectGrades[0]['grades'] = 100

        TestBase.send_body(self.rabbitmq_publisher, input_model)

        self.assertEqual(0, len(TestBase.get_docs(0)))

    def test_invalid_type_birthdate_body(self):
        input_model = ModelGenerator.generate_input_model()
        input_model.birthDate = 27062000

        TestBase.send_body(self.rabbitmq_publisher, input_model)

        self.assertEqual(0, len(TestBase.get_docs(0)))

    def test_invalid_type_age_body(self):
        input_model = ModelGenerator.generate_input_model()
        input_model.age = 'a'

        print(input_model)

        TestBase.send_body(self.rabbitmq_publisher, input_model)

        self.assertEqual(0, len(TestBase.get_docs(0)))

    def test_invalid_type_gender_body(self):
        input_model = ModelGenerator.generate_input_model()
        input_model.gender = 1

        TestBase.send_body(self.rabbitmq_publisher, input_model)

        self.assertEqual(0, len(TestBase.get_docs(0)))

    def test_invalid_type_behaviour_grade_body(self):
        input_model = ModelGenerator.generate_input_model()
        input_model.behaviourGrade = '12'

        TestBase.send_body(self.rabbitmq_publisher, input_model)

        self.assertEqual(0, len(TestBase.get_docs(0)))

    def test_body_with_notes_text_file_saved_success(self):
        input_model = ModelGenerator.generate_input_model()
        input_model.notes = "test"

        TestBase.send_body(self.rabbitmq_publisher, input_model)

        self.assertEqual(1, len(TestBase.get_docs(1)))

    def test_invalid_type_notes_body(self):
        input_model = ModelGenerator.generate_input_model()
        input_model.notes = [1]

        TestBase.send_body(self.rabbitmq_publisher, input_model)

        self.assertEqual(0, len(TestBase.get_docs(0)))

    def test_birthdate_not_compatible_with_age(self):
        input_model = ModelGenerator.generate_input_model()
        input_model.birthDate = "27/06/2000"
        input_model.age = 30

        TestBase.send_body(self.rabbitmq_publisher, input_model)

        self.assertEqual(0, len(TestBase.get_docs(0)))

    def test_valid_body_after_invalid_body(self):
        invalid_input_model = ModelGenerator.generate_input_model()
        valid_input_model = ModelGenerator.generate_input_model()

        invalid_input_model.studentDetails['firstName'] = None

        TestBase.send_body(self.rabbitmq_publisher, invalid_input_model)
        TestBase.send_body(self.rabbitmq_publisher, valid_input_model)

        self.assertEqual(1, len(TestBase.get_docs(1)))
