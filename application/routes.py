from application import app
from .models import get_all_podcasts, get_featured_resource, get_all_featured_resources, get_all_topics
from flask import json, render_template, request
import requests
from datetime import datetime


@app.route("/")
@app.route("/home")
def home():
    #Get podcasts episodes sorted from most recent to oldest and present it to the user
    distinct_topic_list = get_all_topics()

    #Get the featured resource
    featured_resource = get_featured_resource()
    featured_resource['publish_date'] =  str(featured_resource['releaseDate'])[:10]
    
    return render_template("home.html", featured_resource=featured_resource, title="Home",
                            distinct_topic_list=distinct_topic_list)


@app.route("/podcasts")
def podcasts():
    #Get all podcasts from .models and present it to the user
    podcasts = get_all_podcasts()

    return render_template("podcasts.html", podcasts=podcasts, title="Podcasts")


@app.route("/collection", methods=['GET','POST'])
def collection():
    distinct_topic_list = get_all_topics()
    filters_checked = []
    featured_resources = []

    #Do the following assuming filters have not been cleared
    if request.form.get('clearFilters') == None:
        #Grab any checkbox selections made by user and put them into a list
        filters_checked = request.form.getlist('check')

        #Boolean to check if any checkbox were selected
        filters_exist = bool(filters_checked)
        
        #If user selected any filters, filter resources by those topics, else return all featured resources
        if filters_exist:
            featured_resources = get_all_featured_resources(filter_topics=filters_checked)
        else:
            featured_resources = get_all_featured_resources()
    #If user clicked to clear filters
    else:
        featured_resources = get_all_featured_resources()

    #Loop through the episodes and set a string attribute for displaying the date it was published (released)
    #This should be refactored by just storing this as a field in each podcast episode doc in mongo
    for featured_resource in featured_resources:
        featured_resource['publish_date'] =  str(featured_resource['releaseDate'])[:10]

    return render_template("collection.html", featured_resources=featured_resources, filters_checked=filters_checked,
                            distinct_topic_list=distinct_topic_list, title="Collection")


@app.route("/about-us")
def about_us():
    return render_template("about_us.html", title="About Us")