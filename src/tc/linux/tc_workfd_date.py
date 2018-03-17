# This file is part of tbot.  tbot is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Description:
#
# just as a demo for the tbot workshop
# simply show, how to send a cmd (in our case "date") to the
# linux console on the DUT
# (2 different possibilities)
#
# Then send again "date" and search for the string
# "Mon" in the output of the date command, and end Testcase
# with True, if found, else end TC with False.
#
# This testcase is a good starting point for writting
# own testcases.
#
# You also can use this testcase for a fast tbot
# test after tbot is installed.
# See config/tbot_test.py for more info
#
# End:

from tbotlib import tbot

# always add some logging info for example which variables
# your testcase uses
# don;t forget to define a default value for a new config variable
# if it makes sense
logging.info("arg: ")

# set board into state linux
tb.set_board_state("linux")

# choose Connection on which the testcase should run
# tb.c_ctrl: Control connection (on LAB PC)
# tb.c_con: Board console (DUT)
# tb.c_cpc: Build PC, if we have one
c = tb.c_con

# simply call linux command "date"
tb.write_lx_cmd_check(c, 'date')

# now another possibility to write the date command
# tbot ends if write fails
tb.eof_write(c, 'date')

# now the command was send, we need to read (or wait)
# for prompt
tb.tbot_expect_prompt(c)

# third possibility
# write command and parse the resulting strings/lines
# until prompt
# here for a demo we search for string "MON"
# if found, testcase ends True
# else False
ret = False
tb.eof_write(c, 'date')
line = 'sdkfhbsjh'
while line != '':
    line = tb.tbot_get_line(c)
    if line != '':
        if 'Mon' in line:
            ret = True
        else:
            logging.error("Fehler erwarte Montag in date")

# compile, install and do tests
# call other testcases with
# tb.eof_call_tc("NAME OF TESTCASE)
# if the testcase must end without error
# or if you are interested in the return value with
# ret = tb.call_tc("NAME OF TESTCASE)

# Always end a testcase with tb.end_tc(True or False)
tb.end_tc(ret)