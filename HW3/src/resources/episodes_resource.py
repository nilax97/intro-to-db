#
# DFF TODO: Accessing database directly from resource is an anti-pattern.
# You did not learn this from me.
#
import pymysql
import json
from services.mongodb_data_service import MongoDB


class Episodes():

    def __init__(self):
        self.db_schema = 'GoT'
        self.db_table = 'episodes'
        self.mongodb = MongoDB(self.db_schema,self.db_table)


    def get_all(self,seasonNum,template={},field_list={},limit=0,offset=0,order_by={}):

        template['seasonNum'] = seasonNum

        result = self.mongodb.query(template=template,field_list=field_list,limit=limit,offset=offset,order_by=order_by)
        return list(result)

    def get_by_number(self,seasonNum,episodeNum):
        template = {'seasonNum':seasonNum,'episodeNum':episodeNum}
        field_list = {}
        limit = 0
        offset = 0

        result = self.mongodb.query(template,field_list,limit,offset)
        return list(result)

if __name__ == "__main__":

    episodes = Episodes()

    all_episodes = episodes.get_all(2)
    print(json.dumps(all_episodes, indent=2))

