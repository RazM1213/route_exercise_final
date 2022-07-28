from dataclasses import dataclass
from typing import List


@dataclass
class TestInputSubjectGrades:
    subject: str
    grades: List[int]