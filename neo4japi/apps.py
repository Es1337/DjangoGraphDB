from django.apps import AppConfig


class Neo4JapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'neo4japi'

    def ready(self):
        pass
