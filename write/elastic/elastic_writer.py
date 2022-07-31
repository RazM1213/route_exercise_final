import datetime
import json
from dataclasses import asdict

from elasticsearch import Elasticsearch

from models.output import Output
from write.writer import Writer


class ElasticWriter(Writer):

    @staticmethod
    def get_elastic_client():
        es_client = Elasticsearch(
            "http://localhost:9200",
            basic_auth=('elastic', "ans=+1=vXek1tAfsPz_u")
        )

        return es_client

    def write(self, output: Output):
        query = json.dumps(asdict(output), indent=4)

        ElasticWriter.get_elastic_client().index(
            index=f"{datetime.datetime.strptime(output.birthDate, '%d/%m/%Y').year}",
            document=query,
            id=output.studentDetails.id,
        )

        print(f"[X] Created a document in elasticsearch for: {output.studentDetails.fullName}")