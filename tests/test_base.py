import json
import os
import datetime
from typing import List
from config import path_config
from models.input import Input
from models.output import Output
from transform.student.student_transformer import StudentTransformer
from send_generated_input_script.rabbit_mq_publisher import RabbitMqPublisher
from tests.test_model.test_input import TestInput


class TestBase:

    STUDENTS_DIR_PATH = path_config.STUDENTS_DIR_PATH

    @staticmethod
    def parse_output(input_model: TestInput) -> Output:
        return StudentTransformer().parse_output(input_model.__dict__)

    @staticmethod
    def read_from_file(filepath: str) -> json:

        TestBase.get_docs(1)

        with open(filepath, "r") as text_file:
            json_data = json.loads(text_file.read())

        return json_data

    @staticmethod
    def send_body(publisher: RabbitMqPublisher, body: TestInput):
        publisher.publish(str(json.dumps(body.__dict__)))

    @staticmethod
    def get_input_model(body):
        return Input(**json.loads(body))

    @staticmethod
    def get_docs(expected_docs: int, timeout_sec: int = 3000) -> List:
        date = datetime.datetime.now() + datetime.timedelta(milliseconds=timeout_sec)
        if expected_docs == 0:
            while date > datetime.datetime.now():
                if len(os.listdir(TestBase.STUDENTS_DIR_PATH)) != 0:
                    return os.listdir(TestBase.STUDENTS_DIR_PATH)
            return os.listdir(TestBase.STUDENTS_DIR_PATH)
        else:
            while len(os.listdir()) != expected_docs and date > datetime.datetime.now():
                result = os.listdir(TestBase.STUDENTS_DIR_PATH)
                if len(result) == expected_docs:
                    return result
            return os.listdir(TestBase.STUDENTS_DIR_PATH)