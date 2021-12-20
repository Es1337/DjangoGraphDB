from django.db import models
from datetime import datetime
from django_neomodel import DjangoNode
from neomodel import StringProperty,\
                     DateTimeProperty, UniqueIdProperty,\
                     RelationshipTo, RelationshipFrom

from neo4japi.models.nodeutils import NodeUtils


class Person(DjangoNode, NodeUtils):
    objects          = models.Manager()
    
    uid              = UniqueIdProperty()
    name             = StringProperty()
    surname          = StringProperty()
    created          = DateTimeProperty(default=datetime.utcnow)

    career_clubs     = RelationshipTo('.club.Club', 'EXPLAYER_OF')
    trophies         = RelationshipTo('.trophy.Trophy', 'WON')

    @property
    def serialize(self):
        return {
            'node_properties': {
                'uid': self.uid,
                'name': self.name,
                'surname': self.surname,
                'created': self.created
            },
        }

    @property
    def serialize_connections(self):
        return [
            {
                'direction': 'TO',
                'nodes_type': 'Club',
                'relationship_variable': 'career_clubs',
                'relationship_type': 'EXPLAYER_OF',
                'nodes_related': self.serialize_relationships(self.career_clubs.all()),
            },
            {
                'direction': 'TO',
                'nodes_type': 'Trophy',
                'relationship_variable': 'trophies',
                'relationship_type': 'WON',
                'nodes_related': self.serialize_relationships(self.trophies.all()),
            }
        ]

    def setup_relationship(self, end_node, rel_type):
        RELS = {
            'career_clubs': self.career_clubs,
            'trophies': self.trophies,
        }

        return RELS[rel_type].connect(end_node)


    class Meta:
        app_label = 'neo4japi'


class Manager(Person):
    managed_club            = RelationshipTo('.club.Club', "MANAGER_OF")
    past_clubs              = RelationshipTo('.club.Club', "EXMANAGER_OF")

    managed_squad           = RelationshipTo('Person', "MANAGER_OF")
    past_managed_players    = RelationshipTo('Person', "EXMANAGER_OF")

    @property
    def serialize(self):
        return {
            'node_properties': {
                'uid': self.uid,
                'name': self.name,
                'surname': self.surname,
                'created': self.created
            },
        }

    @property
    def serialize_connections(self):
        return [
            {
                'direction': 'TO',
                'nodes_type': 'Club',
                'relationship_variable': 'career_clubs',
                'relationship_type': 'EXPLAYER_OF',
                'nodes_related': self.serialize_relationships(self.career_clubs.all()),
            },
            {
                'direction': 'TO',
                'nodes_type': 'Trophy',
                'relationship_variable': 'trophies',
                'relationship_type': 'WON',
                'nodes_related': self.serialize_relationships(self.trophies.all()),
            },
            {
                'direction': 'TO',
                'nodes_type': 'Club',
                'relationship_variable': 'managed_club',
                'relationship_type': 'MANAGER_OF',
                'nodes_related': self.serialize_relationships(self.managed_club.all()),
            },
            {
                'direction': 'TO',
                'nodes_type': 'Club',
                'relationship_variable': 'past_clubs',
                'relationship_type': 'EXMANAGER_OF',
                'nodes_related': self.serialize_relationships(self.past_clubs.all()),
            },
            {
                'direction': 'TO',
                'nodes_type': 'Person',
                'relationship_variable': 'managed_squad',
                'relationship_type': 'MANAGER_OF',
                'nodes_related': self.serialize_relationships(self.managed_squad.all()),
            },
            {
                'direction': 'TO',
                'nodes_type': 'Person',
                'relationship_variable': 'past_managed_players',
                'relationship_type': 'EXMANAGER_OF',
                'nodes_related': self.serialize_relationships(self.past_managed_players.all()),
            },
        ]

    def setup_relationship(self, end_node, rel_type):
        RELS = {
            'career_clubs': self.career_clubs,
            'trophies': self.trophies,
            'managed_club': self.managed_club,
            'past_clubs': self.past_clubs,
            'managed_squad': self.managed_squad,
            'psat_managed_players': self.past_managed_players
        }

        return RELS[rel_type].connect(end_node)

    class Meta:
        app_label = 'neo4japi'

class Player(Person):
    current_club     = RelationshipTo('.club.Club', 'PLAYER_OF')

    manager          = RelationshipFrom('Person', "MANAGER_OF")
    past_managers    = RelationshipFrom('Person', "EXMANAGER_OF")

    @property
    def serialize_connections(self):
        return [
            {
                'direction': 'TO',
                'nodes_type': 'Club',
                'relationship_variable': 'career_clubs',
                'relationship_type': 'EXPLAYER_OF',
                'nodes_related': self.serialize_relationships(self.career_clubs.all()),
            },
            {
                'direction': 'TO',
                'nodes_type': 'Trophy',
                'relationship_variable': 'trophies',
                'relationship_type': 'WON',
                'nodes_related': self.serialize_relationships(self.trophies.all()),
            },
            {
                'direction': 'TO',
                'nodes_type': 'Club',
                'relationship_variable': 'current_club',
                'relationship_type': 'PLAYER_OF',
                'nodes_related': self.serialize_relationships(self.current_club.all()),
            },
            {
                'direction': 'FROM',
                'nodes_type': 'Person',
                'relationship_variable': 'manager',
                'relationship_type': 'MANAGER_OF',
                'nodes_related': self.serialize_relationships(self.manager.all()),
            },
            {
                'direction': 'FROM',
                'nodes_type': 'Person',
                'relationship_variable': 'past_managers',
                'relationship_type': 'EXMANAGER_OF',
                'nodes_related': self.serialize_relationships(self.past_managers.all()),
            },
        ]

    def setup_relationship(self, end_node, rel_type):
        RELS = {
            'career_clubs': self.career_clubs,
            'trophies': self.trophies,
            'current_club': self.current_club,
            'manager': self.manager,
            'psat_managers': self.past_managers
        }

        return RELS[rel_type].connect(end_node)

    class Meta:
        app_label = 'neo4japi'

class Forward(Player):
    #some stats

    class Meta:
        app_label = 'neo4japi'

class Midfielder(Player):
    #some stats

    class Meta:
        app_label = 'neo4japi'