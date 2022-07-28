from dataclasses import dataclass
from typing import Optional, List
from models.output_student_details import OutputStudentDetails
from models.output_subject_grades import OutputSubjectGrades


@dataclass
class Output:
    studentDetails: OutputStudentDetails
    subjectGrades: List[OutputSubjectGrades]
    totalAvg: float
    birthDate: str
    age: int
    gender: str
    isGoodBehaviour: str
    notes: Optional[str] = None
