import datetime
import string
import random
from tests.test_model.test_input import TestInput
from tests.test_model.test_input_student_details import TestInputStudentDetails
from tests.test_model.test_input_subject_grades import TestInputSubjectGrades


class ModelGenerator:

    @staticmethod
    def generate_input_model():
        first_name = ''.join(random.choices(string.ascii_uppercase, k=8))
        last_name = ''.join(random.choices(string.ascii_uppercase, k=8))
        id = random.randint(111111111, 999999999)
        subject = ''.join(random.choices(string.ascii_uppercase, k=8))
        grades = [random.randint(1, 100) for i in range(3)]
        birth_date = datetime.datetime(random.randint(1900, 2010), random.randint(1,10), random.randint(1,28)).strftime("%d/%m/%Y")
        age = (datetime.datetime.now() - datetime.datetime.strptime(birth_date, "%d/%m/%Y")).days // 365
        gender = random.choice(["זכר", "נקבה", "אחר"])
        behaviour_grade = random.randint(1, 10)
        notes = None
        extra_field = None

        return TestInput(
            TestInputStudentDetails(firstName=first_name, lastName=last_name, id=id).__dict__,
            [TestInputSubjectGrades(subject=subject, grades=grades).__dict__],
            birth_date,
            age,
            gender,
            behaviour_grade,
            notes,
            extra_field
        )