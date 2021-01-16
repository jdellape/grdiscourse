#This is where I will maintain the business object definition and retrieval
from application import db
import requests
from datetime import datetime

#For Podcasts

PODCAST_IDS = ['1495107302','591157388','1289898626','1212429230','1072608281','1094878688','998360427','1069930513','582049752']

FETCH_ALL_PODCASTS_URL = 'https://itunes.apple.com/lookup?id={0}&entity=podcast'.format(','.join(PODCAST_IDS))

FINAL_ARTWORK_DIMENSIONS = '300x300'

#Not finding podcast description via api so building a dict {id:description} to store
PODCAST_DESCRIPTIONS = {
  "591157388"  : "Join VeggieTales and What’s in the Bible? creator Phil Vischer and co-host Skye Jethani \
                (author, senior editor Christianity Today’s Leadership Journal) for a fast-paced and often \
                funny conversation about pop culture, media, theology and the fun, fun, fun of living a \
                thoughtful Christian life in an increasingly post-Christian culture.",
  "1495107302" : "The world is different on the other side of a pandemic. The same kinds people who were \
                ignored are now in the center of the conversation. The question is: when people are ready \
                to listen, what do you have to say? The Disruptors: Season 2 is hosted by Esau McCaulley \
                and features a series of disruptive conversations with Lecrae, Taylor Schumann, David Swanson, \
                Justin Giboney, Beth Moore, Robert Chao Romero, and more",
  "1289898626" : "The Church Politics Podcast is where you can get in-depth political analysis from a Christian worldview with Michael Wear & Justin Giboney",
  "1212429230" : "Welcome to Truth’s Table with Michelle Higgins, Christina Edmondson, and Ekemini Uwan. We are \
                  Black Christian women who love truth and seek it out wherever it leads us. We will share our \
                  perspectives on race, politics, gender, current events, and pop culture that are filtered \
                  through our Christian faith. So pull up a chair and have a seat at the table with us. Learn more at TruthsTable.com",
  "1072608281" : "Q educates and equips Christians to engage our cultural moment. Our method of learning is simple: \
                 exposure, conversation and collaboration. Listen to the Q Podcast to learn, explore and consider how you can be \
                faithful in our cultural context.",
  '1094878688' : "Each week the editors of Christianity Today go beyond hashtags and hot-takes and set aside time to explore the \
                 reality behind a major cultural event.",
  '998360427'  : "A program for Christ-followers who want to participate more effectively in God’s work both at home and to the \
                 ends of the earth.",
  '1069930513' : "Churches Planting Churches is a podcast produced by Acts 29 in partnership with The Gospel Coalition. \
                 Tony Merida talks with various church planters, pastors, theologians, and innovators; sharing stories and \
                 insights to help you serve Christ’s church more faithfully and effectively.",
  '582049752'  : "Seminary Dropout- It’s not full on academia like in seminary, but that’s not to say that theology nerds \
                 won’t like it as well, because it’s not Youth Camp either. There’s no Greek or Hebrew translation home work, \
                 but there are also no trust falls. There will be fun, insightful, personal, thoughtful and engaging interviews \
                 with Christian leaders, thinkers, bloggers, authors and theologians."
}

#Modeling Podcast show information. Needs to be moved to a MongoDB collection.
class Podcast:
    def __init__(self, _id, name, web_page, artwork):
        self._id = _id
        self.name = name
        self.web_page = web_page
        self.artwork = artwork

    def reset_artwork_dimensions(self, artwork):
        artwork_url_chunks = artwork.split("/")
        original_last_chunk = artwork_url_chunks[-1]
        artwork_url_chunks.pop()
        new_last_chunk = FINAL_ARTWORK_DIMENSIONS + original_last_chunk[7:]
        artwork_url_chunks.append(new_last_chunk)
        artwork_url_chunks[0] = artwork_url_chunks[0] + "/"
        self.artwork = "/".join(artwork_url_chunks)
    
    def set_description(self):
        self.description = PODCAST_DESCRIPTIONS[str(self._id)]

#Get data related to all the podcasts we recommend (as defined by ids above)
def get_all_podcasts():
    #Get all podcast information according to the podcast IDS of interest
    api_response = requests.get(FETCH_ALL_PODCASTS_URL)
    podcast_json = api_response.json()
    podcast_results = podcast_json['results']
    podcasts = [Podcast(podcast['collectionId'], podcast['collectionName'], podcast['collectionViewUrl'], podcast['artworkUrl600']) for podcast in podcast_results]
    for podcast in podcasts:
        podcast.reset_artwork_dimensions(podcast.artwork)
        podcast.set_description()
    return podcasts

#Functions for retrieving data from MongoDB collection
def get_featured_resource():
    #Get mongo cursor object for featured_resources collection and grab current resource to feature
    featured_resource_cursor = db.featured_resources.find({"currentFeature":True}).limit(1)
    featured_resource =  ""
    for resource in featured_resource_cursor:
        featured_resource = resource

    return featured_resource

def get_all_featured_resources(filter_topics=None):
    #Query MongoDB to select featured resources given the topic filters selected by user
    all_featured_resources =  []

    if filter_topics is not None:
        all_featured_resources = list(db.featured_resources.find({ "topics" : { "$in" : filter_topics} }).sort("releaseDate", -1))
    else:
        all_featured_resources = list(db.featured_resources.find().sort("releaseDate", -1))

    return all_featured_resources

def get_all_topics():
    #Get a set of all the topics within featured_resources collection
    distinct_topic_list = db.featured_resources.distinct("topics")
    distinct_topic_list = list(filter(None, distinct_topic_list)) 

    #Return all distinct topics 
    return distinct_topic_list





