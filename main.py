from write.folder.folder_writer import FolderWriter
from pipeline import Pipeline
from transform.student.student_transformer import StudentTransformer
from read.rabbit_mq.rabbit_mq_reader import RabbitMqReader


def main():
    rabbit_mq_reader = RabbitMqReader()
    folder_writer = FolderWriter()
    student_transformer = StudentTransformer()
    pipeline = Pipeline(rabbit_mq_reader, folder_writer, student_transformer)

    pipeline.run()


if __name__ == "__main__":
    main()

