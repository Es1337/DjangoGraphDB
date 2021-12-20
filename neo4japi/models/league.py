from django.db import models
from datetime import datetime
from django_neomodel import DjangoNode
from neomodel import StructuredNode, StringProperty,\
                     DateTimeProperty, UniqueIdProperty,\
                     RelationshipTo, DateProperty,\
                     IntegerProperty
from neomodel.relationship_manager import RelationshipFrom
from neo4japi.models.nodeutils import NodeUtils

class League(DjangoNode, NodeUtils):
    uid                 = UniqueIdProperty()
    name                = StringProperty()
    country             = StringProperty()
    created             = DateTimeProperty(default=datetime.utcnow)

    clubs_participating = RelationshipFrom('.club.Club', 'PLAYS_IN')

    @property
    def serialize(self):
        return {
            'node_properties': {
                'uid': self.uid,
                'name': self.name,
                'country': self.country,
            },
        }

    @property
    def serialize_connections(self):
        return [
            {
                'direction': 'FROM',
                'nodes_type': 'Club',
                'relationship_variable': 'clubs_participating',
                'relationship_type': 'PLAYS_IN',
                'nodes_related': self.serialize_relationships(self.clubs_participating.all()),
            }
        ]

    def setup_relationship(self, end_node, rel_type):
        RELS = {
            'clubs_participating': self.clubs_participating
        }

        return RELS[rel_type].connect(end_node)

    class Meta:
        app_label = 'neo4japi'