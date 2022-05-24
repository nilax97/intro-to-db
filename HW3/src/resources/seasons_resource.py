#
# DFF TODO: Accessing database directly from resource is an anti-pattern.
# You did not learn this from me.
#
import pymysql
import json
from services.mongodb_data_service import MongoDB


class Seasons():

    def __init__(self):
        self.db_schema = 'GoT'
        self.db_table = 'episodes'
        self.mongodb = MongoDB(self.db_schema,self.db_table)


    def get_all(self):

        template = {}
        field_list = {'episodeTitle': 1, 'episodeAirDate': 1,'_id':0 }
        limit = 0
        offset = 0

        result = self.mongodb.query(template,field_list,limit,offset)
        return list(result)

    def get_by_number(self,seasonNum):
        template = {'seasonNum':seasonNum}
        field_list = {}
        limit = 0
        offset = 0

        result = self.mongodb.query(template,field_list,limit,offset)
        return list(result)

if __name__ == "__main__":

    seasons = Seasons()

    all_season = seasons.get_all()
    print(json.dumps(all_season, indent=2))

