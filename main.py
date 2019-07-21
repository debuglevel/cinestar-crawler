#!/usr/bin/env python3
"""
Module Docstring
"""

# Initialize the crawler woith the ID of your cinema and a movie as a string point.
# To get those IDs, go to cinestar.de and search in the schedule for a link like this:
# https://webticketing2.cinestar.de/#/init/47396/108247
#                                          ^cinemaId
#                                                ^movieId

# Ensure to use python3, as python2 will die if you redirect the output to a file if Unicode occurs.

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
from logzero import logger
import requests

def main(args):
    """ Main entry point of the app """
    #logger.info("Cinestar movie crawler")
    #logger.info(args)

    #logger.info(args.cinema)
    #logger.info(args.movie_start)

    cinema_id = int(args.cinema)
    movie_start = int(args.movie_start)
    errors_in_a_row = 0

    for movie_id in range(movie_start, movie_start+1000):
        result = fetch(cinema_id, movie_id) 
        if result == False:
            #return
            errors_in_a_row += 1

            if errors_in_a_row >= 200:
                return
            
            #pass
        else:
            errors_in_a_row = 0
            logger.info(result)
            print(result)

def fetch(cinemaId, movieId):
    logger.info("Fetching infos for cinema %s, movie %s" % (cinemaId, movieId))
    headers = {
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://webticketing2.cinestar.de/',
            'Origin': 'https://webticketing2.cinestar.de',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
            'DNT': '1',
            'Content-Type': 'application/json;charset=UTF-8',
        }

    data = '{"cinemaId":"'+str(cinemaId)+'","movieSessionId":"'+str(movieId)+'"}'

    response = requests.post('https://webticketing2.cinestar.de/api/1_0/init', headers=headers, data=data)
    #json = 
    logger.info("Got status code %s" % response.status_code)

    if response.status_code == 500:
        return False

    cinema_name = response.json()['session']['cinema']['name']
    movie_name = response.json()['session']['movie']['name']
    movie_hall = response.json()['session']['movieSession']['cinemaHall']
    movie_datetime = response.json()['session']['movieSession']['movieTime']

    return cinema_name+";"+movie_name+";"+movie_hall+";"+movie_datetime

if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("cinema", help="Cinema ID")

    # Required positional argument
    parser.add_argument("movie_start", help="Movie ID to start crawling from")

    args = parser.parse_args()
    main(args)
