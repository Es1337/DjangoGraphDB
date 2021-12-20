from django.db import models
from datetime import datetime
from django_neomodel import DjangoNode
from neomodel import StructuredNode, StringProperty,\
                     DateTimeProperty, UniqueIdProperty,\
                     RelationshipTo, DateProperty,\
                     IntegerProperty
from neomodel.relationship_manager import RelationshipFrom
from neo4japi.models.nodeutils import NodeUtils

class Trophy(DjangoNode, NodeUtils):
    uid              = UniqueIdProperty()
    name             = StringProperty()
    date_won         = DateProperty()
    created          = DateTimeProperty(default=datetime.utcnow)

    club_winners = RelationshipFrom('.club.Club', 'WON')
    winners_list = RelationshipFrom('.person.Person', 'WON')

    @property
    def serialize(self):
        return {
            'node_properties': {
                'uid': self.uid,
                'name': self.name,
                'date_won': self.date_won,
                'created': self.created
            },
        }

    @property
    def serialize_connections(self):
        return [
            {
                'direction': 'FROM',
                'nodes_type': 'Club',
                'relationship_variable': 'club_winners',
                'relationship_type': 'WON',
                'nodes_related': self.serialize_relationships(self.club_winners.all()),
            },
            {
                'direction': 'FROM',
                'nodes_type': 'Person',
                'relationship_variable': 'winners_list',
                'relationship_type': 'WON',
                'nodes_related': self.serialize_relationships(self.winners_list.all()),
            },
        ]

    def setup_relationship(self, end_node, rel_type):
        RELS = {
            'club_winners': self.club_winners,
            'winners_list': self.winners_list,
        }

        return RELS[rel_type].connect(end_node)

    class Meta:
        app_label = 'neo4japi'