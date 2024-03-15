import argparse
import logging
import os
import sys

import pandas as pd
import requests
import yaml

from article_parser import ArticleParser
from song_list_parser import ViewParser

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def retrieve_article(url):
  response = requests.get(url)
  html = response.text
  parser = ArticleParser()
  parser.feed(html)
  return parser.output()


def main(args):
  if not args.url:
    logger.error("No URL provided")
    sys.exit(os.EX_NOINPUT)

  response = requests.get(args.url)
  html = response.text

  parser = ViewParser()
  parser.feed(html)
  article_links = parser.output()

  articles = [retrieve_article(article["link"]) for article in article_links if "SONG LIST" in article["title"]]
  articles = [article for article in articles if article]

  with open(args.yaml_path) as f:
    data = yaml.load(f, Loader=yaml.SafeLoader)

  if data is None:
    logger.error("No data")
    return

  old_df = pd.DataFrame(data)
  print(old_df)

  new_df = pd.DataFrame(articles)
  new_df["date"] = pd.to_datetime(new_df["date"]).astype(str)
  print(new_df)

  if new_df.empty:
    logger.error("No new data")
    return

  df = pd.concat([old_df, new_df], ignore_index=True)
  df = df.drop_duplicates(subset=["date"], keep="first")
  df.sort_values(by=["date"], inplace=True)
  print(df)

  playlist = df.reset_index(drop=True).to_dict(orient="records")
  playlist = [p for p in playlist if p.pop("index", None)]
  print(playlist)

  yml = yaml.dump(playlist, allow_unicode=True)
  with open(args.yaml_path, "w") as f:
    f.write(yml)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--url", type=str)
  parser.add_argument("--yaml-path", type=str, default="workloads/playlist/playlist.yml")
  args = parser.parse_args()
  main(args)
