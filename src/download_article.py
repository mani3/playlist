import argparse
import logging
import os
import sys

import pandas as pd
import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def download_article(url):
  response = requests.get(url)
  return response.text


def normalize_title(title: str):
  return title.replace("（", "(").replace("）", ")")


def include_song_list(title: str):
  return "SONG LIST" in title


def main(args):
  logger.info(f"starting auto_play.py with args: {args}")

  if args.csv_file is None:
    logger.error("csv file is not provided")
    return 1

  df = pd.read_csv(args.csv_file)

  for index, row in df.iterrows():
    title = normalize_title(row["title"])

    if not include_song_list(title):
      continue

    url = row["link"]
    article = download_article(url)

    dirname = "data/articles"
    filename = os.path.join(dirname, f"{title}.html")

    if os.path.exists(filename):
      logger.info(f"file {filename} already exists")
      continue

    os.makedirs(dirname, exist_ok=True)
    with open(os.path.join(dirname, f"{title}.html"), "w") as f:
      f.write(article)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-f", "--csv-file", required=True, help="CSV file path")
  args = parser.parse_args()
  sys.exit(main(args))
