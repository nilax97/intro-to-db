#
# DFF TODO: Accessing database directly from resource is an anti-pattern.
# You did not learn this from me.
#
import pymysql
import json
from services.neo4j_data_service import Neo4j


class Movie():

    def __init__(self):
        self.neo4j = Neo4j()


    def get_all(self,template={},field_list={},limit=0,offset=0,order_by={}):

        result = self.neo4j.query(table_id='m',template=template,field_list=field_list,limit=limit,offset=offset,order_by=order_by)
        return list(result)

if __name__ == "__main__":

    movie = Movie()

    all_movie = movie.get_all()
    print(json.dumps(all_episodes, indent=2))

