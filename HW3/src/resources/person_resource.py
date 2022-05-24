#
# DFF TODO: Accessing database directly from resource is an anti-pattern.
# You did not learn this from me.
#
import pymysql
import json
from services.neo4j_data_service import Neo4j


class Person():

    def __init__(self):
        self.neo4j = Neo4j()


    def get_all(self):


        result = self.neo4j.query(table_id="p")
        return list(result)

    def get_movie(self,person):
        sp = "\""
        template = {'name':sp+person+sp}

        result = self.neo4j.query(table_id="r",template=template)
        return list(result)

if __name__ == "__main__":

    person = Person()

    all_person = person.get_all()
    print(json.dumps(all_person, indent=2))

