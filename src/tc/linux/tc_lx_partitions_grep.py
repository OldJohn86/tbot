# SPDX-License-Identifier: GPL-2.0
#
# Description:
#
# check, if all strings in tb.config.tc_lx_ps_partitions are
# in "cat /proc/partitions" output.
#
# End:

from tbotlib import tbot

try:
    tb.config.tc_lx_ps_partitions
except:
    tb.config.tc_lx_ps_partitions = []

logging.info("args: workfd: %s %s", tb.workfd.name, tb.config.tc_lx_ps_partitions)

c = tb.workfd

# set board state for which the tc is valid
tb.set_board_state("linux")

tb.config.tc_workfd_grep_file = 'gnlmpf'
cmd = 'cat /proc/partitions > ' + tb.config.tc_workfd_grep_file
tb.write_lx_cmd_check(c, cmd)

for t in tb.config.tc_lx_ps_partitions:
    tb.config.tc_workfd_grep_string = '"' + t + '"'
    tb.eof_call_tc("tc_workfd_grep.py")

tb.write_lx_cmd_check(c, 'rm ' + tb.config.tc_workfd_grep_file)
tb.end_tc(True)
