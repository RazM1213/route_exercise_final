import pydantic
from custom_exceptions.id_format_exception import IdFormatException
from custom_exceptions.name_format_exception import NameFormatException
import re


class InputStudentDetails(pydantic.BaseModel):
    firstName: str
    lastName: str
    id: int

    @pydantic.validator("firstName")
    def firstname_validation(cls, value):
        if re.search("[!@#$%^&*()|.,/;-]", value) or any(char.isdigit() for char in value):
            raise NameFormatException(value=value, message=f"First name should not contain digits or special chars. ({value})")
        return value

    @pydantic.validator("lastName")
    def lastname_validation(cls, value):
        if re.search("[!@#$%^&*()|.,/;]", value) or any(char.isdigit() for char in value):
            raise NameFormatException(value=value, message=f"Last name should not contain digits or special chars. ({value})")
        return value

    @pydantic.validator("id")
    def id_validation(cls, value):
        if len(str(value)) != 9:
            raise IdFormatException(value=value, message=f"Id should contain 9 digits. ({value})")
        return value



