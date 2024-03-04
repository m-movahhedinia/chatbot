# -*- coding: utf-8 -*-
"""
Created on February 28, 2024

@author: mansour
"""

from ingesters.webpage_ingester import HTMLIngester
from argparse import ArgumentParser


def perform_ingestion(files_location):
    ingestion = HTMLIngester(files_location)
    ingestion.load().send_to_vector_store()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--data_directory", type=str, required=True,
                        help="The directory to read the html files from.")

    args = parser.parse_args()

    perform_ingestion(args.data_directory)
