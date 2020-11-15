from application import app
from .models import get_all_podcasts, get_all_podcast_episodes, get_featured_resource, get_all_featured_resources, get_all_topics
from flask import json, render_template, request
import requests
from datetime import datetime

@app.route("/")
@app.route("/home")
def home():
    #Get podcasts episodes sorted from most recent to oldest and present it to the user
    podcast_episodes = get_all_podcast_episodes()

    #Get the featured resource
    featured_resource = get_featured_resource()
    featured_resource['publish_date'] =  str(featured_resource['publish_date'])[:10]

    #Loop to set a datetime object within each episode object
    for ep in podcast_episodes:
        ep.release_date = ep.release_date[:10]
        time_in_datetime = datetime.strptime(ep.release_date, "%Y-%m-%d")
        ep.set_podcast_episode_datetime_release(time_in_datetime)
    #Sort my list according to the datetime value I input (most recent eps should display first)
    podcast_episodes.sort(reverse=True, key=lambda x: x.release_date_datetime)
    return render_template("home.html", podcast_episodes=podcast_episodes, featured_resource=featured_resource, title="Home")

@app.route("/podcasts")
def podcasts():
    #Get all podcasts from .models and present it to the user
    podcasts = get_all_podcasts()

    return render_template("podcast_shows.html", podcasts=podcasts, title="Podcasts")

@app.route("/podcast-episodes")
def podcast_episodes():
    #Get podcasts episodes sorted from most recent to oldest and present it to the user
    podcast_episodes = get_all_podcast_episodes()

    #Loop to set a datetime object within each episode object
    for ep in podcast_episodes:
        ep.release_date = ep.release_date[:10]
        time_in_datetime = datetime.strptime(ep.release_date, "%Y-%m-%d")
        ep.set_podcast_episode_datetime_release(time_in_datetime)
    #Sort my list according to the datetime value I input (most recent eps should display first)
    podcast_episodes.sort(reverse=True, key=lambda x: x.release_date_datetime)

    return render_template("podcast_episodes.html", podcast_episodes=podcast_episodes, title="Episodes")

@app.route("/about-us")
def about_us():
    return render_template("about_us.html", title="About Us")


@app.route("/archives", methods=['GET','POST'])
def archives():
    distinct_topic_list = get_all_topics()
    
    topic_keyword = request.form.get('topic_keyword')
    
    #If a search term exists, filter by it, else return all featured resources
    if topic_keyword is not None:
        featured_resources = get_all_featured_resources(topic_keyword=topic_keyword)
    else:
        featured_resources = get_all_featured_resources()
    
    for featured_resource in featured_resources:
        featured_resource['publish_date'] =  str(featured_resource['publish_date'])[:10]

    return render_template("archives.html", featured_resources=featured_resources, distinct_topic_list=distinct_topic_list, title="Archives")
