import sys
import pymongo
import config

class MongoDB():

   def get_client(self):
      client = pymongo.MongoClient(
       config.mongodb_url
      )
      db = client.test
      return client

   def __init__(self,dbname,tablename):
      self.client = self.get_client()
      self.dbname = dbname
      self.tablename = tablename
      self.table = self.client[self.dbname][self.tablename]

   def query(self,template={},field_list={},limit=0,offset=0,order_by={}):
      field_list['_id'] = 0
      q = self.table.find(template,field_list)
      if len(order_by)>0:
         q = q.sort(order_by,1)
      q = q.skip(int(offset)).limit(int(limit))
      return q