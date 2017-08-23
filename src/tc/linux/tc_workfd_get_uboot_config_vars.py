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
# start with
# python2.7 src/common/tbot.py -c tbot.cfg -t tc_workfd_get_uboot_config_vars.py
#
# try to get some configuration variables from the U-Boot
# source code, and save them in config variables.
#
# 'CONFIG_SYS_SDRAM_BASE' saved in tb.config.tc_ub_memory_ram_ws_base
# tb.config.tc_ub_memory_ram_ws_base_alt = tc_ub_memory_ram_ws_base + 0x100000
# tb.config.tc_ub_memory_ram_big depended on CONFIG_SYS_ARCH
# if CONFIG_SYS_ARCH == powerpc than yes else no
# 
# End:

from tbotlib import tbot

c = tb.c_ctrl
savefd = tb.workfd
tb.workfd = c

if (tb.config.tc_ub_memory_ram_ws_base == 'undef'):
    # Try to get the SDRAM Base
    tb.uboot_config_option = 'CONFIG_SYS_SDRAM_BASE'
    tb.eof_call_tc("tc_workfd_get_uboot_config_hex.py")
    tb.config.tc_ub_memory_ram_ws_base = tb.config_result

if (tb.config.tc_ub_memory_ram_ws_base_alt == 'undef'):
    try:
        tmp = int(tb.config.tc_ub_memory_ram_ws_base, 16)
    except:
        tb.end_tc(False)
    tmp += 1024 * 1024
    tb.config.tc_ub_memory_ram_ws_base_alt = hex(tmp)

if (tb.config.tc_ub_memory_ram_big == 'undef'):
    # Try to get CONFIG_SYS_ARCH
    tb.uboot_config_option = 'CONFIG_SYS_ARCH'
    tb.eof_call_tc("tc_workfd_get_uboot_config_string.py")
    if tb.config_result == 'powerpc':
        tb.config.tc_ub_memory_ram_big = 'yes'
    else:
        tb.config.tc_ub_memory_ram_big = 'no'

logging.info("detected: %s %s %s", tb.config.tc_ub_memory_ram_ws_base, tb.config.tc_ub_memory_ram_ws_base_alt,
             tb.config.tc_ub_memory_ram_big)

tb.workfd = savefd
tb.end_tc(True)
