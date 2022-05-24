from flask import Flask, Response, request
from flask_cors import CORS
import json
from datetime import datetime
from resources.seasons_resource import Seasons
from resources.episodes_resource import Episodes
from resources.scenes_resource import Scenes
from resources.movie_resource import Movie
from resources.person_resource import Person

import rest_utils

app = Flask(__name__)
CORS(app)

def default_json(t):
    return f'{t}'

##################################################################################################################

@app.route('/')
def hello_world():
    return '<u>Hello World!</u>'

@app.route("/seasons", methods=["GET"])
def get_seasons():
    msg = seasons.get_all()
    rsp = Response(json.dumps(msg,default=default_json), status=200, content_type="application/json")
    return rsp

@app.route("/seasons/<seasonNum>", methods=["GET"])
def get_season_by_number(seasonNum):
    msg = seasons.get_by_number(int(seasonNum))
    rsp = Response(json.dumps(msg,default=default_json), status=200, content_type="application/json")
    return rsp

@app.route("/seasons/<seasonNum>/episodes", methods=["GET"])
def get_episodes(seasonNum):
    request_inputs = rest_utils.RESTContext(request)

    if request_inputs.args is None:
        request_inputs.args = {}

    if request_inputs.fields is None:
        request_inputs.fields = {}
    else:
        request_inputs.fields = dict.fromkeys(request_inputs.fields,1)

    if request_inputs.limit is None:
        request_inputs.limit = 0

    if request_inputs.offset is None:
        request_inputs.offset = 0

    if request_inputs.order_by is None:
        request_inputs.order_by = {}



    msg = episodes.get_all(int(seasonNum),
                            template=request_inputs.args,
                            field_list=request_inputs.fields,
                            limit=request_inputs.limit,
                            offset=request_inputs.offset,
                            order_by=request_inputs.order_by)
    rsp = Response(json.dumps(msg,default=default_json), status=200, content_type="application/json")
    return rsp

@app.route("/seasons/<seasonNum>/episodes/<episodeNum>", methods=["GET"])
def get_episode_by_number(seasonNum,episodeNum):
    msg = episodes.get_by_number(int(seasonNum),int(episodeNum))
    rsp = Response(json.dumps(msg,default=default_json), status=200, content_type="application/json")
    return rsp

@app.route("/seasons/<seasonNum>/episodes/<episodeNum>/scenes", methods=["GET"])
def get_scenes(seasonNum,episodeNum):
    msg = scenes.get_all(int(seasonNum),int(episodeNum))
    rsp = Response(json.dumps(msg,default=default_json), status=200, content_type="application/json")
    return rsp

@app.route("/seasons/<seasonNum>/episodes/<episodeNum>/scenes/<sceneNum>", methods=["GET"])
def get_scene_by_number(seasonNum,episodeNum,sceneNum):
    msg = scenes.get_by_number(int(seasonNum),int(episodeNum),int(sceneNum))
    rsp = Response(json.dumps(msg,default=default_json), status=200, content_type="application/json")
    return rsp

@app.route("/movie", methods=["GET"])
def get_movie():

    request_inputs = rest_utils.RESTContext(request)

    if request_inputs.args is None:
        request_inputs.args = {}

    if request_inputs.fields is None:
        request_inputs.fields = {}
    else:
        request_inputs.fields = dict.fromkeys(request_inputs.fields,1)

    if request_inputs.limit is None:
        request_inputs.limit = 0

    if request_inputs.offset is None:
        request_inputs.offset = 0

    if request_inputs.order_by is None:
        request_inputs.order_by = {}

    msg = movie.get_all(template=request_inputs.args,
                        field_list=request_inputs.fields,
                        limit=request_inputs.limit,
                        offset=request_inputs.offset,
                        order_by=request_inputs.order_by)
    rsp = Response(msg, status=200, content_type="application/json")
    return rsp

@app.route("/person", methods=["GET"])
def get_person():
    msg = person.get_all()
    rsp = Response(msg, status=200, content_type="application/json")
    return rsp

@app.route("/person/<name>/acted_in", methods=["GET"])
def get_acted_in(name):
    msg = person.get_movie(name)
    rsp = Response(msg, status=200, content_type="application/json")
    return rsp



if __name__ == '__main__':
    seasons = Seasons()
    episodes = Episodes()
    scenes = Scenes()
    movie = Movie()
    person = Person()
    app.run(host="0.0.0.0", port=5003)
