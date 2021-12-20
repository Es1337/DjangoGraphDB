from django.db import models
from datetime import datetime
from django_neomodel import DjangoNode
from neomodel import StructuredNode, StringProperty,\
                     DateTimeProperty, UniqueIdProperty,\
                     RelationshipTo, DateProperty,\
                     IntegerProperty
from neomodel.relationship_manager import RelationshipFrom
from neo4japi.models.nodeutils import NodeUtils

class Club(DjangoNode, NodeUtils):
    uid              = UniqueIdProperty()
    name             = StringProperty()
    created          = DateTimeProperty(default=datetime.utcnow)

    league           = RelationshipTo('.league.League', 'PLAYS_IN')
    club_trophies    = RelationshipTo('.trophy.Trophy', 'WON')
    
    squad            = RelationshipFrom('.person.Player', 'PLAYER_OF')
    past_players     = RelationshipFrom('.person.Person', 'EXPLAYER_OF')
    manager          = RelationshipFrom('.person.Manager', 'MANAGER_OF')
    past_managers    = RelationshipFrom('.person.Manager', 'EXMANAGER_OF')
    
    @property
    def serialize(self):
        return {
            'node_properties': {
                'uid': self.uid,
                'name': self.name
            },
        }

    @property
    def serialize_connections(self):
        return [
            {
                'direction': 'TO',
                'nodes_type': 'League',
                'relationship_variable': 'league',
                'relationship_type': 'PLAYS_IN',
                'nodes_related': self.serialize_relationships(self.league.all()),
            },
            {
                'direction': 'TO',
                'nodes_type': 'Trophy',
                'relationship_variable': 'club_trophies',
                'relationship_type': 'WON',
                'nodes_related': self.serialize_relationships(self.club_trophies.all()),
            },
            {
                'direction': 'FROM',
                'nodes_type': 'Player',
                'relationship_variable': 'squad',
                'relationship_type': 'PLAYER_OF',
                'nodes_related': self.serialize_relationships(self.squad.all()),
            },
            {
                'direction': 'FROM',
                'nodes_type': 'Person',
                'relationship_variable': 'past_players',
                'relationship_type': 'EXPLAYER_OF',
                'nodes_related': self.serialize_relationships(self.past_players.all()),
            },
            {
                'direction': 'FROM',
                'nodes_type': 'Manager',
                'relationship_variable': 'manager',
                'relationship_type': 'MANAGER_OF',
                'nodes_related': self.serialize_relationships(self.manager.all()),
            },
            {
                'direction': 'FROM',
                'nodes_type': 'Manager',
                'relationship_variable': 'past_managers',
                'relationship_type': 'EXMANAGER_OF',
                'nodes_related': self.serialize_relationships(self.past_managers.all()),
            },
        ]

    def setup_relationship(self, end_node, rel_type):
        RELS = {
            'league': self.league,
            'club_trophies': self.club_trophies,
            'squad': self.squad,
            'past_players': self.past_players,
            'manager': self.manager,
            'past_managers': self.past_managers,
        }

        return RELS[rel_type].connect(end_node)

    class Meta:
        app_label = 'neo4japi'