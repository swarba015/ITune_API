#########################################
##### Name:   Nuzhat Zahan                      #####
##### Uniqname:   znuzhat                  #####
#########################################

import json
import requests
import webbrowser

class Media():
  """
    A class representing a generic media item.

    Attributes:
        title (str): The title of the media.
        author (str): The author or creator of the media.
        release_year (str): The release year of the media.
        url (str): A URL link to the media.

    Methods:
        info(): Returns a formatted string with the media's title, author, and release year.
        length(): Returns the length of the media. Should be implemented in subclasses.
    """
  def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL", json =None):

    if json is None:
      self.title = title
      self.author = author
      self.release_year = release_year
      self.url = url

    else:
      if json.get("trackName") is not None:
        self.title = json.get('trackName',"No Title")
      else:
        self.title = json.get('collectionName',"No Title")
      self.author = json.get('artistName',"No Author")
      self.release_year = json.get('releaseDate',"No Release Year").split("-")[0]
      if json.get("trackViewUrl") is not None:
        self.url = json.get('trackViewUrl',"No URL")
      else:
        self.url = json.get('collectionViewUrl',"No URL")

  def info(self):
      return f"{self.title} by {self.author} ({self.release_year})"

  def length(self):
    return 0

class Song(Media):
  """
    A class representing a song, inherited from the Media class.

    Attributes:
        album (str): The album the song is from.
        genre (str): The genre of the song.
        track_length (int): The length of the song in milliseconds.

    Methods:
        info(): Returns a formatted string with the song's title, author, release year, and genre.
        length(): Returns the length of the song in seconds.
    """
  def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL", album = "No Album" , genre = "No Genre", track_length = 0,json = None):
    super().__init__(title, author,release_year,url,json)

    if json is None:
      self.album = album
      self.genre = genre
      self.track_length = track_length
    else:     
      self.album = json.get('collectionName',"No Author")
      self.genre = json.get('primaryGenreName',"No Genre")
      self.track_length = int(json.get('trackTimeMillis',0))

  def info(self):
    return super().info() + f" [{self.genre}]"

  def length(self):
    return round(self.track_length * 0.001)



class Movie(Media):
  """
    A class representing a movie, inherited from the Media class.

    Attributes:
        rating (str): The content advisory rating of the movie.
        movie_length (int): The length of the movie in milliseconds.

    Methods:
        info(): Returns a formatted string with the movie's title, author, release year, and rating.
        length(): Returns the length of the movie in minutes.
    """

  def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL", rating = "No Rating" , movie_length = 0,json=None):

    super().__init__(title, author,release_year,url,json)

    if json is None:
      self.rating = rating
      self.movie_length = movie_length
    else:
      self.rating = json.get('contentAdvisoryRating',"No Rating")
      self.movie_length = int(json.get('trackTimeMillis',0))
      
  def info(self):
    return super().info() + f" [{self.rating}]"

  def length(self):
    return round(self.movie_length * 1.66667e-5)


def fetching_information(term, limit=20):
    """
    Fetches information from the iTunes API.

    Args:
        term (str): The search term.
        limit (int): The number of results to return.

    Returns:
        list: A list of dictionaries with the search results.
    """
    Base_URL = "https://itunes.apple.com/search"
    params = {'term': term, 'limit': limit}
    resp = requests.get(Base_URL, params)
    result_object = resp.json()
    return result_object["results"]

def creating_objects(data):
    """
    Creates media objects based on the search results.

    Args:
        data (list): A list of dictionaries with the search results.

    Returns:
        dict: A dictionary with lists of media objects, separated by media type.
    """
    movie_lst = []
    song_lst = []
    other_media = []

    for info in data:
        if info.get('kind') == 'feature-movie':
            movie_lst.append(Movie(json=info))
        elif info.get('kind') == 'song':
            song_lst.append(Song(json=info))
        else:
            other_media.append(Media(json=info))

    media_dic = {'movie': movie_lst, 'song': song_lst, 'other_media': other_media}
    return media_dic

# Other classes, functions, etc. should go here


def print_object(obj):
    """
    Prints the information of each media object in a dictionary.

    Args:
        obj (dict): A dictionary with lists of media objects, separated by media type.
    """
    for key, value in obj.items():
        print("\n", key.upper())
        for index, media in enumerate(value):
            print(f"{index}. {media.info()}")

def preview_media(obj):
    """
    Opens a URL link to preview a media object.

    Args:
        obj (dict): A dictionary with lists of media objects, separated by media type.
    """
    media_type = input("\nWhich media type do you wnat to preview? (movie/song/other_media): ").lower()
    if media_type in obj:
        for index, media in enumerate(obj[media_type]):
            print(f"{index}. {media.info()}")
        index = int(input("\nEnter number of the media you want to preview: "))
        if 0 <= index < len(obj[media_type]):
            media_to_preview = obj[media_type][index]
            print(f"{media_to_preview.url}")
            webbrowser.open(media_to_preview.url)

        else:
            print("Invalid number")
    else:
        print("Invalid media type")

if __name__ == "__main__":
    # your control code for Part 4 (interactive search) should go here
    pass

while True:
    search = input("\nEnter a search term or type 'exit' to quit: ")
    if search.lower() == "exit":
        break

    try:
        data = fetching_information(search)
        obj_list = creating_objects(data)
        print_object(obj_list)

        while True:
            preview = input("\nDo you want to preview any media? (yes/no): ").lower()
            if preview == "yes":
                preview_media(obj_list)
                break
            elif preview == "no":
                print("Have a good day!")
                break
            elif preview == "exit":
                break
            else:
                search = preview
                data = fetching_information(search)
                obj_list = creating_objects(data)
                print_object(obj_list) 
    except Exception as e:yes
        print("An error occurred:", e)
