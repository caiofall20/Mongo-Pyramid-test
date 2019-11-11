from bson import ObjectId, json_util
from pyramid.view import view_config

@view_config(route_name='home', renderer='home.pt')
def home(request):
    if request.method == "POST":
        vidId = request.params["id"]
        try:
            thumbVid = request.db.videos.find_one({"_id": ObjectId(vidId)})
            if int(request.params["thumb"]) == 1:
                likesVid = thumbVid["likes"] + 1
                request.db.videos.update_one(
                    {"_id": ObjectId(vidId)},
                    {"$set": {"likes": likesVid}}
                )
            else:
                vidDislikes = thumbVid["dislikes"] + 1
                request.db.videos.update_one(
                    {"_id": ObjectId(vidId)},
                    {"$set": {"dislikes": vidDislikes}}
                )
        except Exception:
            print(Exception)
        finally:
            vid = request.db.videos.find({})
            if vid.count() > 0:
                return {
                    'videos': vid,
                    'empty': False
                }
            else:
                return {
                    'empty': True
                }
    else:
        vid = request.db.videos.find({})
        if vid.count() > 0:
            return {
                'videos': vid,
                'empty': False,
            }
        else:
            return { 
                'empty': True,
            }

@view_config(route_name='add', renderer='add.pt')
def add(request):
    on_insert = False
    error = False
    if request.method == "POST":
        on_insert = True
        title = request.params["title"]
        subTitle = request.params["subTitle"] or "None"
        url = request.params["url"]
        theme = request.params["theme"]
        description = request.params["description"] or "None"

        vidId = url.split("watch?v=")[-1]

        if subTitle=="None": subTitle = title
        if description=="None": description = title

        try:
            request.db.videos.insert_one(
                {
                    "title": title,
                    "subTitle": subTitle,
                    "vidId": vidId,
                    "theme": theme,
                    "description": description,
                    "likes": 0,
                    "dislikes": 0
                }
            )
        except Exception as e:
            print(e)
            error = True
        finally:
            return { 
                "on_insert": on_insert,
                "error": error,
            }
    else:
        return { 
                "on_insert": on_insert,
                "error": error,
            }

@view_config(route_name='rank', renderer='rank.pt')
def rank(request):
    vids = request.db.videos.find({})
    rank = []
    themeMusic = [0,0,0]
    themeGames = [0,0,0]
    themeArt = [0,0,0]
    themeCritic = [0,0,0]
    themeNews = [0,0,0]
    for vid in vids:
        if vid["theme"] == "Music": 
            themeMusic[0] += vid["likes"]
            themeMusic[1] += vid["dislikes"]
            themeMusic[2] += vid["likes"]-(vid["dislikes"]/2)
        elif vid["theme"] == "Games": 
            themeGames[0] += vid["likes"]
            themeGames[1] += vid["dislikes"]
            themeGames[2] += vid["likes"]-(vid["dislikes"]/2)
        elif vid["theme"] == "Art": 
            themeArt[0] += vid["likes"]
            themeArt[1] += vid["dislikes"]
            themeArt[2] += vid["likes"]-(vid["dislikes"]/2)
        elif vid["theme"] == "Critic": 
            themeCritic[0] += vid["likes"]
            themeCritic[1] += vid["dislikes"]
            themeCritic[2] += vid["likes"]-(vid["dislikes"]/2)
        elif vid["theme"] == "News": 
            themeNews[0] += vid["likes"]
            themeNews[1] += vid["dislikes"]
            themeNews[2] += vid["likes"]-(vid["dislikes"]/2)
    
    rank.append({"theme": "Music","likes": themeMusic[0], "dislikes": themeMusic[1], "score": themeMusic[2]})
    rank.append({"theme": "Games","likes": themeGames[0], "dislikes": themeGames[1], "score": themeGames[2]})
    rank.append({"theme": "Art","likes": themeArt[0], "dislikes": themeArt[1], "score": themeArt[2]})
    rank.append({"theme": "Critic","likes": themeCritic[0], "dislikes": themeCritic[1], "score": themeCritic[2]})
    rank.append({"theme": "News","likes": themeNews[0], "dislikes": themeNews[1], "score": themeNews[2]})

    sortedRank = sorted(rank, key = lambda i: i['score'], reverse=True)
    return { "rank": sortedRank }
    