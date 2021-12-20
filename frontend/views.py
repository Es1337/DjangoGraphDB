from django.shortcuts import render, HttpResponseRedirect
from frontend.forms import PersonInputForm
from neo4japi.utils import fetch_nodes
from mysite.settings import neo_pass
import requests
import json

# Create your views here.
def main(request):
    context = {
        "neo_pass": neo_pass
    }

    return render(request, 'index.html', context=context)

def control_panel(request):

    if request.method == 'POST':
        personForm = PersonInputForm(request.POST)
        if personForm.is_valid():
            return HttpResponseRedirect('/')
    else:
        personForm = PersonInputForm()

    if request.method == 'GET':
        endpoint = request.GET.get('get', 'people')
        print(endpoint)
        r = requests.get('https://djangographdb.appspot.com/api/' + endpoint)
        # print(json.dumps(r.json(), sort_keys=True, indent=4))

        context = {
            'retrievedData': json.dumps(r.json(), sort_keys=True, indent=4)
        }
    else:
        context = {
            'personForm': personForm
        }

    return render(request, 'control_panel.html', context=context)