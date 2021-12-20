from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.parsers import JSONParser

from neomodel import db

from neo4japi.models.person import Person

from .serialisers import (
    PersonSerialiser,
    TrophySerialiser, 
    LeagueSerialiser, 
    ClubSerialiser,
    PlayerSerialiser,
    ManagerSerialiser
)
from .forms import (
    PersonForm,
    PlayerForm,
    ManagerForm, 
    TrophyForm, 
    LeagueForm, 
    ClubForm
)
from .utils import (
    count_nodes,
    fetch_nodes,
    fetch_node_details,
    get_node,
)

# Create your views here.
@csrf_exempt
def connect(request):
    '''
    Connect two nodes with a relationship
    '''
    if request.method == 'POST':
        data = JSONParser().parse(request)

        try:
            start_node_info = {
                'node_type': data['start_node_type'],
                'uid': data['start_node_uid']
            }
            start_node = get_node(start_node_info)
        except ObjectDoesNotExist:
            return HttpResponse(status=404)

        try:
            end_node_info = {
                'node_type': data['end_node_type'],
                'uid': data['end_node_uid']
            }
            end_node = get_node(end_node_info)
        except ObjectDoesNotExist:
            return HttpResponse(status=404)

        rel = start_node.setup_relationship(end_node, data['rel_type'])

        return JsonResponse({"success": rel})

    return JsonResponse({
        "start_node_type": '',
        'start_node_uid':'',
        'end_node_type': '',
        'end_node_uid':  '',
        'rel_type':      ''}, 
        json_dumps_params={'indent':4})


@csrf_exempt
def person(request):
    """
    List all people, or create a new person
    """
    if request.method == 'GET':
        fetch_info = {
            'node_type': 'Person',
            'name': request.GET.get('n', ''),
            'surname': request.GET.get('s', ''),
            'country': '',
            'limit': 50,
            'page': int(request.GET.get('p', 1))
        }

        people = fetch_nodes(fetch_info)
        return JsonResponse(people, safe=False, json_dumps_params={'indent':4, 'sort_keys': True})

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        pf = PersonForm(data)

        if pf.is_valid():
            pf.save()
            return JsonResponse(pf.data, status=201, json_dumps_params={'indent':4, 'sort_keys': True})

        return JsonResponse(pf.errors, status=400)
    
@csrf_exempt
def person_detail(request, uid):
    """
    Retrieve, update or delete a person by uid
    """
    try:
        node_info = {
            'node_type': 'Person',
            'uid': uid,
        }
        person = fetch_node_details(node_info)
    except ObjectDoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        return JsonResponse(person, json_dumps_params={'indent':4, 'sort_keys': True})

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serialiser = PersonSerialiser(person, data=data)

        if serialiser.is_valid():
            serialiser.save()
            return JsonResponse(serialiser.data, json_dumps_params={'indent':4, 'sort_keys': True})

        return JsonResponse(serialiser.errors, status=400)

    elif request.method == 'DELETE':
        person.delete()
        return HttpResponse(status=204)

@csrf_exempt
def trophy(request):
    """
    List all trophies, or create a new trophy
    """
    if request.method == 'GET':
        fetch_info = {
            'node_type': 'Trophy',
            'name': request.GET.get('n', ''),
            'surname': '',
            'country': '',
            'limit': 50,
            'page': int(request.GET.get('p', 1))
        }

        trophies = fetch_nodes(fetch_info)
        return JsonResponse(trophies, safe=False, json_dumps_params={'indent':4, 'sort_keys': True})

    elif request.method == 'POST':
        data = JSONParser().parse(request)

        tf = TrophyForm(data)

        if tf.is_valid():
            tf.save()
            return JsonResponse(tf.data, status=201, json_dumps_params={'indent':4, 'sort_keys': True})

        return JsonResponse(tf.errors, status=400)

@csrf_exempt
def trophy_detail(request, uid):
    """
    Retrieve, update or delete a trophy by uid
    """
    try:
        node_info = {
            'node_type': 'Trophy',
            'uid': uid,
        }
        trophy = fetch_node_details(node_info)
    except ObjectDoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        return JsonResponse(trophy, json_dumps_params={'indent':4, 'sort_keys': True})

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serialiser = TrophySerialiser(trophy, data=data)

        if serialiser.is_valid():
            serialiser.save()
            return JsonResponse(serialiser.data, json_dumps_params={'indent':4, 'sort_keys': True})

        return JsonResponse(serialiser.errors, status=400)

    elif request.method == 'DELETE':
        trophy.delete()
        return HttpResponse(status=204)

@csrf_exempt
def league(request):
    """
    List all leagues, or create a new league
    """
    if request.method == 'GET':
        fetch_info = {
            'node_type': 'League',
            'name': '',
            'surname': '',
            'country': request.GET.get('c', ''),
            'limit': 50,
            'page': int(request.GET.get('p', 1))
        }

        leagues = fetch_nodes(fetch_info)
        return JsonResponse(leagues, safe=False, json_dumps_params={'indent':4, 'sort_keys': True})

    elif request.method == 'POST':
        data = JSONParser().parse(request)

        lf = LeagueForm(data)

        if lf.is_valid():
            lf.save()
            return JsonResponse(lf.data, status=201, json_dumps_params={'indent':4, 'sort_keys': True})

        return JsonResponse(lf.errors, status=400)

@csrf_exempt
def league_detail(request, uid):
    """
    Retrieve, update or delete a league by uid
    """
    try:
        node_info = {
            'node_type': 'League',
            'uid': uid,
        }
        league = fetch_node_details(node_info)
    except ObjectDoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        return JsonResponse(league, json_dumps_params={'indent':4, 'sort_keys': True})

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serialiser = LeagueSerialiser(league, data=data)

        if serialiser.is_valid():
            serialiser.save()
            return JsonResponse(serialiser.data, json_dumps_params={'indent':4, 'sort_keys': True})

        return JsonResponse(serialiser.errors, status=400)

    elif request.method == 'DELETE':
        league.delete()
        return HttpResponse(status=204)

@csrf_exempt
def club(request):
    """
    List all clubs, or create a new club
    """
    if request.method == 'GET':
        fetch_info = {
            'node_type': 'Club',
            'name': request.GET.get('n', ''),
            'surname': '',
            'country': '',
            'limit': 50,
            'page': int(request.GET.get('p', 1))
        }

        clubs = fetch_nodes(fetch_info)
        return JsonResponse(clubs, safe=False, json_dumps_params={'indent':4, 'sort_keys': True})

    elif request.method == 'POST':
        data = JSONParser().parse(request)

        cf = ClubForm(data)

        if cf.is_valid():
            cf.save()
            return JsonResponse(cf.data, status=201, json_dumps_params={'indent':4, 'sort_keys': True})

        return JsonResponse(cf.errors, status=400)

@csrf_exempt
def club_detail(request, uid):
    """
    Retrieve, update or delete a club by uid
    """
    try:
        node_info = {
            'node_type': 'Club',
            'uid': uid,
        }
        club = fetch_node_details(node_info)
    except ObjectDoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        return JsonResponse(club, json_dumps_params={'indent':4, 'sort_keys': True})

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serialiser = ClubSerialiser(club, data=data)

        if serialiser.is_valid():
            serialiser.save()
            return JsonResponse(serialiser.data, json_dumps_params={'indent':4, 'sort_keys': True})

        return JsonResponse(serialiser.errors, status=400)

    elif request.method == 'DELETE':
        club.delete()
        return HttpResponse(status=204)

@csrf_exempt
def player(request):
    """
    List all players, or create a new player
    """
    if request.method == 'GET':
        fetch_info = {
            'node_type': 'Player',
            'name': request.GET.get('n', ''),
            'surname': request.GET.get('s', ''),
            'country': '',
            'limit': 50,
            'page': int(request.GET.get('p', 1))
        }

        players = fetch_nodes(fetch_info)
        return JsonResponse(players, safe=False, json_dumps_params={'indent':4, 'sort_keys': True})

    elif request.method == 'POST':
        data = JSONParser().parse(request)

        pf = PlayerForm(data)

        if pf.is_valid():
            pf.save()
            return JsonResponse(pf.data, status=201, json_dumps_params={'indent':4, 'sort_keys': True})

        return JsonResponse(pf.errors, status=400)

@csrf_exempt
def player_detail(request, uid):
    """
    Retrieve, update or delete a player by uid
    """
    try:
        node_info = {
            'node_type': 'Player',
            'uid': uid,
        }
        player = fetch_node_details(node_info)
    except ObjectDoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        return JsonResponse(player, json_dumps_params={'indent':4, 'sort_keys': True})

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serialiser = PlayerSerialiser(player, data=data)

        if serialiser.is_valid():
            serialiser.save()
            return JsonResponse(serialiser.data, json_dumps_params={'indent':4, 'sort_keys': True})

        return JsonResponse(serialiser.errors, status=400)

    elif request.method == 'DELETE':
        player.delete()
        return HttpResponse(status=204)

@csrf_exempt
def manager(request):
    """
    List all managers, or create a new manager
    """
    if request.method == 'GET':
        fetch_info = {
            'node_type': 'Manager',
            'name': request.GET.get('n', ''),
            'surname': request.GET.get('s', ''),
            'country': '',
            'limit': 50,
            'page': int(request.GET.get('p', 1))
        }

        managers = fetch_nodes(fetch_info)
        return JsonResponse(managers, safe=False, json_dumps_params={'indent':4, 'sort_keys': True})

    elif request.method == 'POST':
        data = JSONParser().parse(request)

        mf = ManagerForm(data)

        if mf.is_valid():
            mf.save()
            return JsonResponse(mf.data, status=201, json_dumps_params={'indent':4, 'sort_keys': True})

        return JsonResponse(mf.errors, status=400)

@csrf_exempt
def manager_detail(request, uid):
    """
    Retrieve, update or delete a manager by uid
    """
    try:
        node_info = {
            'node_type': 'Manager',
            'uid': uid,
        }
        manager = fetch_node_details(node_info)
    except ObjectDoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        return JsonResponse(manager, json_dumps_params={'indent':4, 'sort_keys': True})

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serialiser = ManagerSerialiser(manager, data=data)

        if serialiser.is_valid():
            serialiser.save()
            return JsonResponse(serialiser.data, json_dumps_params={'indent':4, 'sort_keys': True})

        return JsonResponse(serialiser.errors, status=400)

    elif request.method == 'DELETE':
        manager.delete()
        return HttpResponse(status=204)
