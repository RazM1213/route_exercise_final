class GradeFormatException(Exception):
    
    def __init__(self, value: str, message: str):

        super().__init__(message)
        self.value = value
        self.message = message
