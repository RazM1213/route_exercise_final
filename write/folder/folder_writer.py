import json
import os
from dataclasses import asdict
from config import path_config
from models.output import Output
from write.writer import Writer


class FolderWriter(Writer):

    @staticmethod
    def get_file_name(output: Output):
        first_name = output.studentDetails.firstName.title()
        last_name = output.studentDetails.lastName.title().replace(' ', '-')
        file_name = f"{first_name}_{last_name}.txt"

        return file_name

    def write(self, output: Output):
        folder_path = path_config.STUDENTS_DIR_PATH

        complete_path = os.path.join(folder_path, FolderWriter.get_file_name(output))

        with open(complete_path, 'w') as file:
            data = json.dumps(asdict(output), indent=4)
            file.write(data)

        print(f"[X] Created text file for: {output.studentDetails.fullName}")

