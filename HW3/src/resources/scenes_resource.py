#
# DFF TODO: Accessing database directly from resource is an anti-pattern.
# You did not learn this from me.
#
import pymysql
import json
from services.mongodb_data_service import MongoDB


class Scenes():

    def __init__(self):
        self.db_schema = 'GoT'
        self.db_table = 'episodes'
        self.mongodb = MongoDB(self.db_schema,self.db_table)


    def get_all(self,seasonNum,episodeNum):

        template = {'seasonNum':seasonNum,'episodeNum':episodeNum}
        field_list = {'_id':0, 'scenes':1}
        limit = 0
        offset = 0

        result = self.mongodb.query(template,field_list,limit,offset)
        return result.next()['scenes']

    def get_by_number(self,seasonNum,episodeNum,sceneNum):
        
        template = {'seasonNum':seasonNum,'episodeNum':episodeNum}
        field_list = {'_id':0, 'scenes':1}
        limit = 0
        offset = 0

        result = self.mongodb.query(template,field_list,limit,offset)
        return result.next()['scenes'][sceneNum]

if __name__ == "__main__":

    scenes = Scenes()

    all_scenes = scenes.get_all(2,5)
    print(json.dumps(all_scenes, indent=2))

