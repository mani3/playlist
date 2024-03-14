
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

  articles = [retrieve_article(article['link']) for article in article_links if "SONG LIST" in article['title']]

  with open(args.yaml_path) as f:
    data = yaml.load(f, Loader=yaml.SafeLoader)

  old_df = pd.DataFrame(data)
  old_df = old_df.drop(['index'], axis=1)

  new_df = pd.DataFrame(articles)
  new_df['date'] = pd.to_datetime(new_df['date']).astype(str)

  df = pd.concat([old_df, new_df], ignore_index=True)
  df = df.drop_duplicates(subset=["date"], keep="first")
  df.sort_values(by=["date"], inplace=True)

  playlist = df.reset_index().to_dict(orient="records")
  playlist = [p for p in playlist if p.pop('index', None)]

  yml = yaml.dump(playlist, allow_unicode=True)
  with open(args.yaml_path, "w") as f:
    f.write(yml)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--url", type=str)
  parser.add_argument("--yaml-path", type=str, default="workloads/playlist/playlist.yml")
  args = parser.parse_args()
  main(args)
