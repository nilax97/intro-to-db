import config
import pandas as pd

from py2neo import data, Graph, NodeMatcher, Node, Relationship, RelationshipMatcher
"""
See https://py2neo.org/v4/
"""

"""
NOTE:
    1. I did some basic testing, debugging, etc. but there may be errors.
    2. You can complain about the errors if you want but my response will be, "No Template for You!"
"""


import uuid


class GotGraph(object):
    """
    This object provides a set of helper methods for creating and retrieving nodes and relationships from
    a Neo4j database holding information about players, teams, fans, comments and their relationships.
    """

    # Note:
    # I tend to avoid object mapping frameworks. Object mapping frameworks are fun in the beginning
    # but tend to be annoying after a while. So, I did not create types Player, Team, etc.
    #


    # Connects to the DB and sets a Graph instance variable.
    # Also creates a NodeMatcher and RelationshipMatcher, which are a py2neo framework classes.
    def __init__(self,  url, auth):

        self._graph = Graph(url,
                            auth=auth
                            )
        self._node_matcher = NodeMatcher(self._graph)
        self._relationship_matcher = RelationshipMatcher(self._graph)

    def run_q(self, qs, args):
        """

        :param qs: Query string that may have {} slots for parameters.
        :param args: Dictionary of parameters to insert into query string.
        :return:  Result of the query, which executes as a single, standalone transaction.
        """
        try:
            tx = self._graph.auto(readonly=False)
            result = self._graph.run(qs, args)
            return result
        except Exception as e:
            print("Run exaception = ", e)

    def run_match(self, labels=None, properties=None):
        """
        Uses a NodeMatcher to find a node matching a "template."
        :param labels: A list of labels that the node must have.
        :param properties: A dictionary of {property_name: property_value} defining the template that the
            node must match.
        :return: An array of Node objects matching the pattern.
        """
        #ut.debug_message("Labels = ", labels)
        #ut.debug_message("Properties = ", json.dumps(properties))

        if labels is not None and properties is not None:
            result = self._node_matcher.match(labels, **properties)
        elif labels is not None and properties is None:
            result = self._node_matcher.match(labels)
        elif labels is None and properties is not None:
            result = self._node_matcher.match(**properties)
        else:
            raise ValueError("Invalid request. Labels and properties cannot both be None.")

        # Convert NodeMatch data into a simple list of Nodes.
        full_result = []
        for r in result:
            full_result.append(r)

        return full_result

    def find_nodes_by_template(self, tmp):
        """

        :param tmp: A template defining the label and properties for Nodes to return. An
         example is { "label": "Fan", "template" { "last_name": "Ferguson", "first_name": "Donald" }}
        :return: A list of Nodes matching the template.
        """
        labels = tmp.get('label', None)
        props = tmp.get("template", None)
        result = self.run_match(labels=labels, properties=props)
        return result

    def create_node(self, label, **kwargs):
        n = Node(label, **kwargs)
        tx = self._graph.begin(autocommit=True)
        tx.create(n)
        return n

class Neo4j():

   def get_graph(self):

      g = GotGraph(url=config.neo_url,
                 auth = config.neo_auth
                 )
      return g


   def __init__(self):
      self.graph = self.get_graph()

   def query(self,table_id="m",template={},field_list={},limit=0,offset=0,order_by={}):

      table_text = {
                  "m" : "m:Movie",
                  "p" : "p:Person",
                  "r" : "(p:Person)-[r:ACTED_IN]->(m:Movie)"
               }

      cond_id = "p" if table_id == "r" else table_id

      conditions_text = " AND ".join([f"{cond_id}." + " = ".join(x) for x in template.items()]) if len(template) > 0 else "TRUE"

      order_text = f"\nORDER BY {table_id}.{order_by}" if len(order_by) > 0 else ""

      offset_text = f"\nSKIP {offset}" if int(offset)>0 else ""

      limit_text = f"\nLIMIT {limit}" if int(limit)>0 else ""

      field_dict = {
                     "m" : "m.title,m.released,m.tagline",
                     "p" : "p.name,p.born",
                     "r" : "m.title,m.released,m.tagline"
                   }

      field_text = ",".join([f"{table_id}." + x for x in field_list.keys()]) if len(field_list)>0 else field_dict[table_id]



      cypher_q = f"""
          match
              ({table_text[table_id]})
          WHERE {conditions_text}
          return {field_text}{order_text}{offset_text}{limit_text}
      """

      res = self.graph.run_q(cypher_q, None)

      df = pd.DataFrame(res)

      return df.to_json(orient='values')