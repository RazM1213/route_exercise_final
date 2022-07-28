from datetime import datetime
import pydantic
from mappings.gender_mapping import gender_mapping
from typing import Optional, List
from custom_exceptions.age_format_exception import AgeFormatException
from custom_exceptions.behaviour_grade_format_exception import BehaviourGradeFormatException
from custom_exceptions.date_format_exception import DateFormatException
from custom_exceptions.gender_format_exception import GenderFormatException
from models.input_student_details import InputStudentDetails
from models.input_subject_grades import InputSubjectGrades


class Input(pydantic.BaseModel):

    studentDetails: InputStudentDetails
    subjectGrades: List[InputSubjectGrades]
    birthDate: str
    age: int
    gender: str
    behaviourGrade: int
    notes: Optional[str]

    @pydantic.validator('birthDate')
    def validate_birthdate(cls, value):
        try:
            datetime.strptime(str(value), '%d/%m/%Y')
        except ValueError:
            raise DateFormatException(value=value, message=f"Invalid date format. ({value})")
        return value

    @pydantic.root_validator
    def validate_age(cls, values: dict):
        if (datetime.now() - datetime.strptime(values["birthDate"], "%d/%m/%Y")).days // 365 != values["age"]:
            raise AgeFormatException(value=values["age"], message=f"Age does not match birth date. ({values['age']}) ({values['birthDate']})")
        return values

    @pydantic.validator('gender')
    def validate_gender(cls, value):
        if value not in gender_mapping.keys():
            raise GenderFormatException(value=value, message=f"Gender must be זכר/נקבה/אחר ({value})")
        return value

    @pydantic.validator("behaviourGrade")
    def validate_behaviour_grade(cls, value):
        if value < 1 or value > 10:
            raise BehaviourGradeFormatException(value=value, message=f"Behaviour grade must be between 1 and 10. ({value})")
        return value

