import glob
import json
from html.parser import HTMLParser

import pandas as pd


class ViewParser(HTMLParser):
  def __init__(self):
    super().__init__()
    self.has_title = False
    self.links = []
    self.thumbnails = []
    self.titles = []

  def handle_starttag(self, tag, attrs):
    attrs = dict(attrs)
    if tag == "a" and "href" in attrs and "id" in attrs and "analysis_program-contents" in attrs["id"]:
      self.links.append(attrs["href"])

    if tag == "img" and "data-original" in attrs:
      self.thumbnails.append(attrs["data-original"])

    if tag == "p" and "class" in attrs and "txt-article" in attrs['class']:
      self.has_title = True

  def handle_endtag(self, tag):
    pass

  def handle_data(self, data):
    if self.has_title:
      self.titles.append(data)
      self.has_title = False

  def output(self):
    if len(self.titles) == len(self.links) and len(self.titles) == len(self.thumbnails):
      return [
          {
              "title": self.titles[i],
              "link": self.links[i],
              "thumbnail": self.thumbnails[i],
          }
          for i in range(len(self.titles))
      ]
    else:
      print("Error: titles, links, thumbnails length not match")
      return []


def main():
  song_list = []
  for filename in glob.glob("data/articles_list/*.json"):
    with open(filename, "r") as f:
      json_dict = json.load(f)
      html = json_dict.get("view")

      if html is None:
        continue

      parser = ViewParser()
      parser.feed(html)
      song_list.extend(parser.output())

  df = pd.DataFrame(song_list)
  df.sort_values(by=["link"], inplace=True)
  df.to_csv("./articles.csv", index=False)


if __name__ == "__main__":
  main()
