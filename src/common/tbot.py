#!/usr/bin/python
#
# SPDX-License-Identifier: GPL-2.0
#
import os, sys
import logging
import argparse
from tbotlib import tbot
import signal

try:
    tb
except:
    parser = argparse.ArgumentParser(description="tbot automate commandline")
    parser.add_argument("-c", "--cfgfile",
           dest="cfgfile", default="none",
           help="the tbot board configfilename")
    parser.add_argument("-s", "--slabfile",
           dest="labfile", default="none",
           help="the tbot lab configfilename")
    parser.add_argument("-a", "--arguments",
           dest="arguments", default="",
           help="arguments for the testcase, pass the arguments in json format, '{\"var1\" : \"value1\", \"var2\" : \"value2\"}'")
    parser.add_argument("-l", "--logfile",
           dest="logfile", default="default",
           help="the tbot logfilename, if default, tbot creates a defaultnamelogfile")
    parser.add_argument("-t", "--testcase",
           dest="tc", default="none",
           help="the testcase which should be run")
    parser.add_argument("-v", "--verbose",
           action="store_true", dest="verbose", default=False,
           help="be verbose, print all read/write to stdout")
    parser.add_argument("-e", "--event",
           dest="eventsim", default='none',
           help="open eventlogfile and run it")
    parser.add_argument("-p", "--pwfile",
           dest="pwfile", default='password.py',
           help="used password file")
    parser.add_argument('--version', action='version', version='%(prog)s 2018.09')
    args = parser.parse_args()

    args.workdir = os.path.abspath(  # Convert into absolute path string
        os.path.join(  # Current file's grandparent directory
            os.path.join(  # Current file's parent directory
                os.path.dirname(  # Current file's directory
                    os.path.abspath(__file__)  # Current file path
                ),
                os.pardir
            ),
            os.pardir
        )
    )
    print("This version of tbot is deprecated")
    print("You should use the new version of tbot, found on:")
    print("https://github.com/Rahix/tbot")
    print("documentation: https://github.com/Rahix/tbot")
    tb = tbot(args.workdir, args.labfile, args.cfgfile, args.logfile, args.verbose, args.arguments, args.tc, args.eventsim, args.pwfile)

def signal_term_handler(signal, frame):
    print ("GOT signal ", tb)
    tb.event.create_event('main', tb.config.boardname, "WDT", False)
    tb.log.error("WDT Timeout")
    tb.end_tc(False)

signal.signal(signal.SIGTERM, signal_term_handler)

ret = tb.call_tc(tb.starttestcase)
if ret == False:
    tb.end_tc(False)

tb.end_tc(True)
