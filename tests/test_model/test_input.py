from dataclasses import dataclass
from typing import List, Optional
from models.input_student_details import InputStudentDetails
from models.input_subject_grades import InputSubjectGrades


@dataclass
class TestInput:
    studentDetails: InputStudentDetails
    subjectGrades: List[InputSubjectGrades]
    birthDate: str
    age: int
    gender: str
    behaviourGrade: int
    notes: Optional[str]
    extraField: Optional[str]