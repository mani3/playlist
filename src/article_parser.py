import glob
import logging
from html.parser import HTMLParser

import pandas as pd
import yaml

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ArticleParser(HTMLParser):
  def __init__(self):
    super().__init__()
    self.article_stack = []

    self.flags = {
        "date": False,
        "body": False,
        "playlist": False,
        "playlist_name": False,
    }
    self.date = None
    self.playlist_name = None
    self.song_list = []

    self.title = None
    self.artist = None

  def handle_starttag(self, tag, attrs):
    attrs = dict(attrs)

    if tag == "time" and "class" in attrs and "date" in attrs["class"]:
      self.flags["date"] = True

    # オンエアー楽曲のテキスト
    if tag == "div" and "class" in attrs and "txt-detail-body" in attrs['class']:
      self.flags["body"] = True

    if tag == "" and "class" in attrs and "txt-article" in attrs['class']:
      self.has_title = True

  def handle_endtag(self, tag):
    pass

  def handle_data(self, data):
    if self.flags["date"]:
      self.date = data.strip()
      self.flags["date"] = False

    if "Today’s Playlist" in data:
      self.flags["playlist"] = True
      self.flags["playlist_name"] = True
    elif "5時台" in data:
      # Tody's Playlist から 5時台のテキストまでがプレイリスト
      self.flags["playlist"] = False
    elif self.flags["playlist"] and data.strip().startswith("♪"):
      self.flags["playlist_name"] = False
      name = data.strip().replace("♪", "")
      if "／" in name:
        title, artist = name.split("／")
        self.song_list.append({"title": title.strip(), "artist": artist.strip()})
    elif self.flags["playlist_name"]:
      if self.playlist_name is None:
        self.playlist_name = data.strip()
      else:
        self.playlist_name += data.strip()
    elif self.flags["playlist"] and not self.flags["playlist_name"]:
      if "♪" == data.strip():

        self.title = None
        self.artist = None
      elif "♪" in data.strip():
        name = data.strip().replace("♪", "")
        if "／" in name:
          title, artist = name.split("／")
          if title and self.title is None:
            self.title = title.strip()
          if artist and self.artist is None:
            self.artist = artist.strip()
          if self.title is not None and self.artist is not None:
            self.song_list.append({"title": self.title.strip(), "artist": self.artist.strip()})
      elif "／" in data.strip():
        title, artist = data.strip().split("／")
        if title and self.title is None:
          self.title = title.strip()
        if artist and self.artist is None:
          self.artist = artist.strip()

        if self.title is not None and self.artist is not None:
          self.song_list.append({"title": self.title, "artist": self.artist})
          self.title = None
          self.artist = None
      elif data.strip():
        name = data.strip().replace("／", "")
        if not name:
          pass
        else:
          if self.title is None:
            self.title = name
          elif self.artist is None:
            self.artist = name

          if self.title is not None and self.artist is not None:
            self.song_list.append({"title": self.title, "artist": self.artist})
            self.title = None
            self.artist = None
      else:
        self.title = None
        self.artist = None

  def output(self):
    if self.playlist_name is not None and len(self.song_list) > 0:
      return {
          "date": self.date,
          "playlist_name": self.playlist_name,
          "song_list": self.song_list,
      }
    else:
      logger.error("Error: date, playlist_name, song_list is not found")
      return {}


def main():
  data_list = []
  filenames = glob.glob("./data/articles/*.html")

  for filename in filenames:
    with open(filename, "r") as f:
      data = f.read()

    parser = ArticleParser()
    parser.feed(data)
    output = parser.output()
    if output:
      data_list.append(output)
    else:
      logger.error(f"Error: {filename} is not found")

  df = pd.DataFrame(data_list)
  df.sort_values(by=["date"], inplace=True)
  yml = yaml.dump(df.reset_index().to_dict(orient="records"), allow_unicode=True)

  with open("./playlist.yml", "w") as f:
    f.write(yml)


if __name__ == "__main__":
  main()
