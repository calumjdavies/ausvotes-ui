from flask import Flask, render_template
from mongo import db
from bson.objectid import ObjectId

app = Flask(__name__, static_folder="static")
from jinja_markdown import MarkdownExtension

app.jinja_env.add_extension(MarkdownExtension)

@app.route("/")
@app.route("/home")
def root():
    posts = db.blog.find().sort({"date_posted": -1}).limit(6)
    results = db.electorate.find({"id":213})
    for result in results:
        print(result)
    return render_template("index.html", posts=posts)

@app.route("/elections")
def elections():
    elections_ = db.election.find().sort({"id":-1})
    return render_template("elections.html", elections=elections_)

@app.route("/elections/<param_key>=<param_value>")
def elections_filter(param_key, param_value):
    elections_ = db.election.find({param_key:param_value}).sort({"id":-1})
    return render_template("elections.html", elections=elections_)


@app.route("/elections/<id>")
def election(id):
    election = db.election.find({"id":int(id)})
    electorates = db.electorate.find({"election.id":int(id)}).sort({"name":1})

    pollingplaces = db.polling_place.find({"election.id": int(id)}).sort({"name": 1})
    return render_template("election.html", elections=election, electorates=electorates, polling_places=pollingplaces, filter={"all":"all"})

@app.route("/polling_places/election_id=<id>&<param_key>=<param_value>")
def election_filter(id, param_key, param_value):
    election = db.election.find({"id":int(id)})
    print(id, param_key, param_value)
    if param_key == "all":
        places = db.polling_place.find({"election.id": int(id)})
    else: 
        places = db.polling_place.find({"election.id": int(id), param_key: param_value})
    return render_template("election.html", elections=election, polling_places=places, filter={param_key:param_value})

@app.route("/candidates")
def candidates_all():
    return render_template("candidates.html")

@app.route("/blog")
def blogs():
    posts = db.blog.find().sort({"date_posted":-1})
    return render_template("blogs.html", posts=posts)

@app.route("/blog/<id>")
def blog(id):
    post_list = []
    for post in db.blog.find({"_id":ObjectId(id)}):
        print(post )
        post_list.append(post)
        tag_list = post.get("tags")
        
    related_posts = db.blog.find({"$and": [
        {"tags": tag_list},
        {"_id": {
            "$ne": ObjectId(id)
        }}
    ]}).limit(3)
    return render_template("blog.html", posts=post_list, related_posts=related_posts)

@app.route("/new_post")
def new_post():
    tags = "Qld Election"
    title = "2024 Qld State Election Guide"
    preview_text = "Preview text"
    preview_image = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/SMPTE_Color_Bars.svg/1200px-SMPTE_Color_Bars.svg.png"
    with open('blog.html', 'r') as file:  # r to open file in READ mode
        body = file.read()
    from datetime import datetime
    posted_datetime = datetime.now()
    db.blog.insert_one({"title": title, "date_posted":posted_datetime, "body": body, "preview_text": preview_text, "preview_image": preview_image, "tags": tags})
    return "hello"