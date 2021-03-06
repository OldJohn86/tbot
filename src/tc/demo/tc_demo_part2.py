# SPDX-License-Identifier: GPL-2.0
#
# Description:
# start tc:
# - call tc_demo_get_ub_code.py
# - call tc_demo_compile_install_test.py
# End:

from tbotlib import tbot

# set wordkfd to the connection we want to work on
tb.workfd = tb.c_ctrl

# go into u-boot code
tb.eof_call_tc("tc_workfd_goto_uboot_code.py")

# set specific settings for this demo
tb.config.workfd_get_patchwork_number_user = 'tbot'
tb.config.tc_workfd_apply_patchwork_patches_blacklist = []
tb.config.tc_workfd_get_patchwork_number_list_order = '-delegate'

# get current list of patches in ToDo list
tb.statusprint("get patchwork patches")
tb.eof_call_tc("tc_workfd_get_patchwork_number_list.py")

# add patchwork patches to U-Boot code
tb.statusprint("apply patchwork patches")
tb.config.tc_workfd_apply_patchwork_patches_checkpatch_cmd = 'scripts/checkpatch.pl'
tb.eof_call_tc("tc_workfd_apply_patchwork_patches.py")

# now compile, install and test the new source on the board
tb.eof_call_tc("tc_demo_compile_install_test.py")
tb.end_tc(True)
