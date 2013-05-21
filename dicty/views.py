from django.http import HttpResponse
from django.shortcuts import render
from django.http import Http404
from time import sleep
import urllib

import json
import cPickle
import os

dictyPath = os.path.abspath(os.path.dirname(__file__))
dataPath = os.path.join(dictyPath, "../data")
picklePath = os.path.join(dataPath, 'Pickles')


def index(request):
    #sleep(3)
    return render(request, 'dicty/index.html', {})


def others(request, sub):
    #sleep(3)
    try:
        return render(request, 'dicty/'+sub, {})
    except:
        raise Http404


def api(request, sub):
    #sleep(3)
    if sub == "":
        return render(request, 'dicty/api.html', {})
    if sub == "experiment": #/api/experiment
        return HttpResponse(json.dumps(wholeDict["experiment"], indent=4),
                            content_type="application/json")
    if sub == "profile": #/api/profile?ddbs=,,,&species=
        selectedSpecies = request.GET.get("species")
        selectedDDBs = str(request.GET.get("ddbs")).split(",")
        subset = wholeDict.get("profile"+str(selectedSpecies))
        if subset:
            filtered = {
                sel: subset.get(getDDB(sel))
                for sel in selectedDDBs
            }
            return HttpResponse(json.dumps(filtered, indent=4),
                                content_type="application/json")
        else:
            return HttpResponse("Hi. Bad params", content_type="text/plain")
    if sub == "allGenes": #/api/allGenes
        return HttpResponse(json.dumps(wholeDict["allGenes"], indent=4),
                            content_type="application/json")
    if sub == "comparison": #/api/comparison?ddb=DDB_G0273069
        selectedDDB = str(request.GET.get("ddb"))
        filtered = {exp["species"]: {
            "info": exp,
            "data": wholeDict["profile"+exp["species"]].get(
                getDDB(selectedDDB))
        } for exp in wholeDict["experiment"]}
        return HttpResponse(json.dumps(filtered, indent=4),
                            content_type="application/json")
    if sub == "wingy":
        temp = 'http://dictyexpress.biolab.si/script/get_volcano_new.py'
        add = '?pass1=rnaseq&user1=rnaseq&gene_gid_list=%s&org=%s'
        params = (request.GET.get("ddbs"), request.GET.get("type"))
        f = urllib.urlopen(temp+add % params)
        return HttpResponse(f.read(), content_type="text/plain")
    raise Http404
    #return HttpResponse(json.dumps(wholeDict, indent=4))


def getDDB(ddbOrNameOrJgi):
    gene = wholeDict["convertGenes"].get(ddbOrNameOrJgi)
    if gene:
        return gene["ddb"]
    else:
        return ddbOrNameOrJgi


def loadExperiment():
    pickleFile = os.path.join(picklePath, 'experiment.cPickle')
    dataFile = os.path.join(dataPath, 'experiment.txt')
    if not os.path.exists(pickleFile):
        f = open(dataFile, 'r')
        experiment = []
        header = 1
        for line in f:
            if line[0] != '#':
                if not header:
                    splits = line[:-1].split("\t")
                    experiment.append({
                        "species": splits[0],
                        "strain": splits[1],
                        "growth": splits[2]
                    })
                header = 0
        f.close()
        cPickle.dump(experiment, open(pickleFile, 'wb'))

    experiment = cPickle.load(open(pickleFile, "rb"))
    wholeDict["experiment"] = experiment
    #print json.dumps({"experiment": experiment}, indent=4)


def loadProfile(folder):
    pickleFile = os.path.join(picklePath, 'profile'+folder+'.cPickle')
    dataFile = os.path.join(dataPath, folder, 'normalized_data_set.txt')
    if not os.path.exists(pickleFile):
        f = open(dataFile, 'r')
        profile = {}
        header = 1
        for line in f:
            if line[0] != "#":
                if not header:
                    splits = line[:-1].split("\t")
                    ix = getDDB(splits[0])
                    profile[ix] = map(
                        lambda (x1, x2): (float(x1)+float(x2))/2,
                        zip(splits[1:8], splits[8:15])
                    )
                header = 0
        f.close()
        cPickle.dump(profile, open(pickleFile, 'wb'))

    profile = cPickle.load(open(pickleFile, "rb"))
    wholeDict["profile"+folder] = profile
    #print json.dumps({"profile": profile}, indent=4)


def loadAllGenes():
    pickleFile = os.path.join(picklePath, 'allGenes.cPickle')
    dataFile = os.path.join(dataPath, 'orthologs.txt')
    if not os.path.exists(pickleFile):
        f = open(dataFile, 'r')
        header = 1
        allGenes = {}
        convertGenes = {}
        for line in f:
            if line[0] != '#':
                if not header:
                    splits = line[:-1].split("\t")
                    allGenes[splits[0]] = {
                        "name": splits[0],
                        "ddb": splits[1],
                        "jgi_id": splits[2]
                    }
                    convertGenes[splits[0]] = {
                        "name": splits[0],
                        "ddb": splits[1],
                        "jgi_id": splits[2]
                    }
                    convertGenes[splits[1]] = {
                        "name": splits[0],
                        "ddb": splits[1],
                        "jgi_id": splits[2]
                    }
                    convertGenes[splits[2]] = {
                        "name": splits[0],
                        "ddb": splits[1],
                        "jgi_id": splits[2]
                    }
                header = 0
        f.close()
        cPickle.dump((allGenes, convertGenes), open(pickleFile, 'wb'))

    (allGenes, convertGenes) = cPickle.load(open(pickleFile, "rb"))
    wholeDict["allGenes"] = allGenes
    wholeDict["convertGenes"] = convertGenes
    #print json.dumps({"allGenes": allGenes}, indent=4)

if not os.path.exists(dataPath):
    os.makedirs(dataPath)
if not os.path.exists(picklePath):
    os.makedirs(picklePath)
wholeDict = {}

try:
    loadAllGenes()
except IOError:
    print "Data file missing"
try:
    loadProfile('D. discoideum')
except IOError:
    print "Data file missing"
try:
    loadProfile('D. purpureum')
except IOError:
    print "Data file missing"
try:
    loadExperiment()
except IOError:
    print "Data file missing"
