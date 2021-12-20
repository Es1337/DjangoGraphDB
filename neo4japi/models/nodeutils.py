from abc import ABCMeta
from neomodel import db

class NodeUtils:
    __metaclass__ = ABCMeta

    def serialize_relationships(self, nodes):
        serialized_nodes = []

        for node in nodes:
            serialized_node = node.serialize

            results, columns = self.cypher('''
                    MATCH (n), (m) 
                    WHERE ID(n) = $self and m.uid = $end_node
                    MATCH (n)-[rel]-(m)
                    RETURN type(rel) as node_relationship
                ''',
                {'end_node': node.uid}
            )
            serialized_node['node_relationship'] = results[0][0]

            serialized_nodes.append(serialized_node)

        return serialized_nodes