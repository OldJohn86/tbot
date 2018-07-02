# SPDX-License-Identifier: GPL-2.0
#
# Description:
# remove, clone current mainline U-Boot, then
# start tc_board_smartweb_test_ub.py
# End:

from tbotlib import tbot

# set board state for which the tc is valid
tb.set_board_state("u-boot")

# delete old u-boot source tree
tb.workfd = tb.c_ctrl
tb.eof_call_tc("tc_workfd_rm_uboot_code.py")

# cloning needs a bigger timeout, (git clone has no output)
# call get u-boot source
tb.statusprint("get u-boot source")
tb.eof_call_tc("tc_lab_get_uboot_source.py")

# apply local patches
tb.workfd = tb.c_ctrl
tb.eof_call_tc("tc_workfd_goto_uboot_code.py")

tb.config.tc_workfd_apply_local_patches_dir = "/work/hs/tbot/patches/smartweb_uboot_patches"
tb.config.tc_workfd_apply_local_patches_checkpatch_cmd_strict = "no"
tb.config.tc_workfd_apply_local_patches_checkpatch_cmd = 'scripts/checkpatch.pl'
tb.eof_call_tc("tc_workfd_apply_local_patches.py")

# add patchwork patches
tb.statusprint("apply patchwork patches")
tb.config.tc_workfd_apply_patchwork_patches_checkpatch_cmd = 'scripts/checkpatch.pl'
tb.eof_call_tc("tc_workfd_apply_patchwork_patches.py")

# call ub tests
tb.statusprint("call ub test")
tb.eof_call_tc("tc_board_smartweb_test_ub.py")

# save working u-boot bin
c = tb.workfd
p = "/tftpboot/" + tb.config.tftpboardname + "/" + tb.config.ub_load_board_env_subdir + "/"
so = p + "u-boot.bin"
ta = p + "u-boot-latestworking.bin"
tb.eof_call_tc("tc_lab_cp_file.py", ch=c, s=so, t=ta)
so = p + "System.map"
ta = p + "u-boot-latestworking.System.map"
tb.eof_call_tc("tc_lab_cp_file.py", ch=c, s=so, t=ta)
so = p + "boot.bin"
ta = p + "u-boot-latestworking-boot.bin"
tb.eof_call_tc("tc_lab_cp_file.py", ch=c, s=so, t=ta)
so = p + "u-boot-spl.bin"
ta = p + "u-boot-latestworking-spl.bin"
tb.eof_call_tc("tc_lab_cp_file.py", ch=c, s=so, t=ta)
so = p + "u-boot-spl.map"
ta = p + "u-boot-latestworking-spl.System.map"
tb.eof_call_tc("tc_lab_cp_file.py", ch=c, s=so, t=ta)

# power off board at the end
tb.eof_call_tc("tc_lab_poweroff.py")
tb.end_tc(True)
