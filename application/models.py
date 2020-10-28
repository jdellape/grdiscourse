#This is where I will maintain the business object definition and retrieval

import requests

#For Podcasts

PODCAST_IDS = ['1495107302','591157388','1289898626','1212429230','1072608281']

FETCH_ALL_PODCASTS_URL = 'https://itunes.apple.com/lookup?id={0}&entity=podcast'.format(','.join(PODCAST_IDS))

FINAL_ARTWORK_DIMENSIONS = '300x300'

#Podcast Episodes
FETCH_RECENT_PODCAST_EPISODES_URL = 'https://itunes.apple.com/lookup?id={0}&entity=podcastEpisode&limit=25'.format(','.join(PODCAST_IDS))

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
                faithful in our cultural context."
}

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

class PodcastEpisode:
    def __init__(self, episode_name, episode_url, episode_player_url, release_date, short_description, long_description, artwork):
        self.episode_name = episode_name
        self.episode_url = episode_url
        self.episode_player_url = episode_player_url
        self.release_date = release_date
        self.short_description = short_description
        self.long_description = long_description
        self.artwork = artwork

    def set_podcast_episode_datetime_release(self, release_date_datetime):
        self.release_date_datetime = release_date_datetime
    
    def reset_artwork_dimensions(self, artwork):
        artwork_url_chunks = artwork.split("/")
        original_last_chunk = artwork_url_chunks[-1]
        artwork_url_chunks.pop()
        new_last_chunk = FINAL_ARTWORK_DIMENSIONS + original_last_chunk[7:]
        artwork_url_chunks.append(new_last_chunk)
        artwork_url_chunks[0] = artwork_url_chunks[0] + "/"
        self.artwork = "/".join(artwork_url_chunks)

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

def get_all_podcast_episodes():
    #Get all podcast information according to the podcast IDS of interest
    api_response = requests.get(FETCH_RECENT_PODCAST_EPISODES_URL)
    podcast_episodes_json = api_response.json()
    podcast_episodes_results = podcast_episodes_json['results']
    podcast_episodes = []
    for result in podcast_episodes_results:
        episode = ""
        try:
            episode = PodcastEpisode(result['trackName'], result['trackViewUrl'], result['episodeUrl'], result['releaseDate'], 
                            result['shortDescription'], result['description'], result['artworkUrl160'])
            episode.reset_artwork_dimensions(episode.artwork)
            podcast_episodes.append(episode)
        except:
            pass

    return podcast_episodes



