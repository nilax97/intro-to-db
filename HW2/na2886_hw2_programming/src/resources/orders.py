import pymysql
import json


class Orders():

    def __init__(self):
        self.db_table = 'orders'
        self.db_schema = 'classicmodels'
        self.db_table_full_name = 'classicmodels.orders'

        # List of the fields, in order, that form the primary key
        self.primary_key_fields = 'orderNumber'


    def _get_connection(self):
        """
        # DFF TODO There are so many anti-patterns here I do not know where to begin.
        :return:
        """

        # DFF TODO OMG. Did this idiot really put password information in source code?
        # Sure. Let's just commit this to GitHub and expose security vulnerabilities
        #
        conn = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="dbuserdbuser",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn

    def _run_query(self,sql):
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            res = cursor.execute(sql)
        except:
            return None
        if res == 0:
            result = None
        else:
            result = cursor.fetchall()
        return result

    def is_float(self,element):
        try:
            float(element)
            return True
        except ValueError:
            return False

    def get_full_table_name(self):
        return self.db_schema + "." + self.db_table

    def get_resource_by_id(self, id):
        """

        :param id: The 'primary key' of the resource instance relative to the collection.
        :return: The resource or None if not found.
        """
        sql = "select * from " + self.db_table_full_name + " where " + self.primary_key_fields + "=" + str(id)
        return self._run_query(sql)


    def get_by_template(self,
                        path=None,
                        template=None,
                        field_list=None,
                        limit=None,
                        offset=None):
        """
        This is a logical abstraction of an SQL SELECT statement.

        Ignore path for now.

        Assume that
            - template is {'customerNumber': 101, 'status': 'Shipped'}
            - field_list is ['customerNumber', 'orderNumber', 'status', 'orderDate']
            - self.get_full_table_name() returns 'classicmodels.orders'
            - Ignore limit for now
            - Ignore offset for now

        This method would logically execute

        select customerNumber, orderNumber, status, orderDate
            from classicmodels.orders
            where
                customerNumber=101 and status='Shipped'

        :param path: The relative path to the resource. Ignore for now.
        :param template: A dictionary of the form {key: value} to be converted to a where clause
        :param field_list: The subset of the fields to return.
        :param limit: Limit on number of rows to return.
        :param offset: Offset in the list of matching rows.
        :return: The rows matching the query.
        """
        sql = "select " + ",".join(field_list) + " from " + self.db_table_full_name + " where " + ' && '.join(["%s='%s'" % (key, value) if not self.is_float(value) else "%s=%s" % (key, value) for (key, value) in template.items()])
        return self._run_query(sql)

    def create(self, new_resource):
        """

        Assume that
            - new_resource is {'customerNumber': 101, 'status': 'Shipped'}
            - self.get_full_table_name() returns 'classicmodels.orders'

        This function would logically perform

        insert into classicmodels.orders(customerNumber, status)
            values(101, 'Shipped')

        :param new_resource: A dictionary containing the data to insert.
        :return: Returns the values of the primary key columns in the order defined.
            In this example, the result would be [101]
        """
        sql = "insert into " + self.db_table_full_name + "(" + ",".join(new_resource.keys()) + ") values (" + ",".join(["'" + x + "'" if not self.is_float(x) else str(x) for x in new_resource.values()]) + ")"
        res = self._run_query(sql)
        if res == None:
            return []
        else:
            return [new_resource[self.primary_key_fields]]

    def update_resource_by_id(self, id, new_values):
        """
        This is a logical abstraction of an SQL UPDATE statement.

        Assume that
            - id is 30100
            - new_values is {'customerNumber': 101, 'status': 'Shipped'}
            - self.get_full_table_name() returns 'classicmodels.orders'

        This method would logically execute.

        update classicmodels.orders
            set customerNumber=101, status=shipped
            where
                orderNumber=30100


        :param id: The 'primary key' of the resource to update
        :new_values: A dictionary defining the columns to update and the new values.
        :return: 1 if a resource was updated. 0 otherwise.
        """

        sql = "update " + self.db_table_full_name + " set " + ' , '.join(["%s='%s'" % (key, value) if not self.is_float(value) else "%s=%s" % (key, value) for (key, value) in new_values.items()]) + " where " + self.primary_key_fields + "=" + str(id)
        res = self._run_query(sql)
        if res == None:
            return 0
        else:
            return 1

    def delete_resource_by_id(self, id):
        """
        This is a logical abstraction of an SQL DELETE statement.

        Assume that
            - id is 30100
            - new_values is {'customerNumber': 101, 'status': 'Shipped'}

        This method would logically execute.

        delete from classicmodels.orders
            where
                orderNumber=30100


        :param id: The 'primary key' of the resource to delete
        :return: 1 if a resource was deleted. 0 otherwise.
        """
        sql = "delete from " + self.db_table_full_name + " where " + self.primary_key_fields + "=" + str(id)
        res = self._run_query(sql)
        if res == None:
            return 0
        else:
            return 1
