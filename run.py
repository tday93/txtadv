#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" application description here """

__appname__ = "txtadv"
__author__ = "Trevor Day github.com/tday93"
__version__ = "0.0"
__license__ = "MIT"


from optparse import OptionParser
import logging
import sys
# local imports beow here
from game import game


def main(options):
    """ start your actual app here """
    # check for saved games
    # load saved game if desired
    # start new game if not
    game.main(options)


if __name__ == "__main__":
    # setup arg parsing
    parser = OptionParser()

    # options for logging
    parser.add_option("-L", "--loglevel", dest="log_level",
                      choices=["CRITICAL", "ERROR",
                               "WARNING", "INFO", "DEBUG"],
                      default="ERROR", help="Logging level, default = ERROR")
    parser.add_option("-l", "--logfile", dest="log_file",
                      default="log.txt",
                      help="The file to log to, default = log.txt")
    parser.add_option("-q", "--quiet", action="store_false", dest="verbose",
                      default=True, help="don't print log to stdout")

    # additional options needed can go here

    parser.add_option("-d", "--directory", dest="base_dir", default="./data",
                      help="The directory containing your game data")
    parser.add_option("-S", "--savedir", dest="save_dir", default="./saves",
                      help="The save game directory")
    parser.add_option("-s", "--savename", dest="save_name", default="save1",
                      help="The name for the saved game")

    # get args from optparse
    (options, args) = parser.parse_args()

    # setup logging
    logger = logging.getLogger(__appname__)
    formatter = logging.Formatter(fmt='%(asctime)s %(message)s',
                                  datefmt='%m/%d/%Y %I:%M:%S %p')
    logger.setLevel(logging.DEBUG)

    # file handler for logging
    fh = logging.FileHandler(options.log_file)
    fh.setLevel("DEBUG")

    # console handler for logging
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(options.log_level)

    # set formats for handlers
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # attach handlers to logger
    logger.addHandler(fh)
    if options.verbose:
        logger.addHandler(ch)

    # finally run the actual app
    main(options)
