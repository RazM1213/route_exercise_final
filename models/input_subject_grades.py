import re
from typing import List
import pydantic
from custom_exceptions.grade_format_exception import GradeFormatException
from custom_exceptions.name_format_exception import NameFormatException


class InputSubjectGrades(pydantic.BaseModel):
    subject: str
    grades: List[int]

    @pydantic.validator("subject")
    def subject_validation(cls, value):
        if re.search("[!@#$%^&*()|.,/;]", value) or any(char.isdigit() for char in value):
            raise NameFormatException(value=value, message=f"Subject name should not contain digits or special chars. ({value})")
        return value

    @pydantic.validator("grades")
    def grade_validation(cls, value):
        for grade in value:
            if not 0 <= int(grade) <= 100:
                raise GradeFormatException(value=value, message=f"Grade should be between 1 and 100. ({grade})")
        return value
