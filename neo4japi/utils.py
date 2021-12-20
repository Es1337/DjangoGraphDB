from .models import (
        Trophy,
        League,
        Club,
        Person,
        Player,
        Manager,
        Midfielder,
        Forward
    )

MODEL_CLASSES = {
    'Trophy': Trophy,
    'League': League,
    'Club': Club,
    'Person': Person,
    'Player': Player,
    'Manager': Manager,
    'Midfielder': Midfielder,
    'Forward': Forward
}

def get_node(node_info):
    result = MODEL_CLASSES[node_info['node_type']].nodes.get(uid=node_info['uid'])
    print(result)
    return result

def filter_nodes(node_type, name_search, surname_search, country):
    node_set = node_type.nodes

    if node_type.__name__ == 'League':
        node_set.filter(country__icontains=country)

    if node_type.__name__ == 'Trophy':
        pass

    if node_type.__name__ == 'Person'     \
    or node_type.__name__ == 'Player'     \
    or node_type.__name__ == 'Manager'    \
    or node_type.__name__ == 'Midfielder' \
    or node_type.__name__ == 'Forward':
        node_set.filter(surname__icontains=surname_search)

    node_set.filter(name__icontains=name_search)

    return node_set

def count_nodes(count_info):
    count = {}

    node_type = count_info['node_type']
    name      = count_info['name']
    surname   = count_info['surname']
    country   = count_info['country']

    node_set = filter_nodes(MODEL_CLASSES[node_type], name, surname, country)
    count['count'] = len(node_set)

    return count

def fetch_nodes(fetch_info):
    node_type       = fetch_info['node_type']
    name            = fetch_info['name']
    surname         = fetch_info['surname']
    country         = fetch_info['country']
    limit           = fetch_info['limit']
    start           = ((fetch_info['page'] - 1) * limit)
    end             = start + limit
    node_set        = filter_nodes(MODEL_CLASSES[node_type], name, surname, country)
    fetched_nodes   = node_set[start:end]

    return [node.serialize for node in fetched_nodes]

def fetch_node_details(node_info):
    node_type   = node_info['node_type']
    uid         = node_info['uid']
    node        = MODEL_CLASSES[node_type].nodes.get(uid=uid)
    node_details = node.serialize

    node_details['node_connections'] = []
    if (hasattr(node, 'serialize_connections')):
        node_details['node_connections'] = node.serialize_connections

    return node_details