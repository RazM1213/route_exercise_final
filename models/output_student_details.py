from dataclasses import dataclass


@dataclass
class OutputStudentDetails:
    firstName: str
    lastName: str
    fullName: str
    id: int
