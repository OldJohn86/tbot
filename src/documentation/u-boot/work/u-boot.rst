.. |Warning| image:: ./images/Warning-icon.png
   :height: 80
   :width: 80

.. |Help| image:: ./images/help.gif
   :height: 80
   :width: 80

.. |Tip| image:: ./images/tip.gif
   :height: 80
   :width: 80


U-Boot
######

Current Versions
================

Das U-Boot (or just "U-Boot" for short) is Open Source Firmware for Embedded Power Architecture®, ARM, MIPS, x86 and other processors. The U-Boot project is hosted by DENX, where you can also find the project home page: http://www.denx.de/wiki/U-Boot/

The current version of the U-Boot source code can be retrieved from the DENX "git" repository.

You can browse the "git" repositories at http://git.denx.de/

The trees can be accessed through the git, HTTP, and rsync protocols. For example you can use one of the following commands to create a local clone of one of the source trees:

::

  git clone git://git.denx.de/u-boot.git u-boot/
  git clone http://git.denx.de/u-boot.git u-boot/
  git clone rsync://git.denx.de/u-boot.git u-boot/

For details please see here.

Official releases of U-Boot are also available through FTP. Compressed tar archives can downloaded from the directory ftp://ftp.denx.de/pub/u-boot/. 

.. raw:: pdf

   PageBreak

Get U-Boot code for the beagleboneblack
======================================

define some PATH variables
--------------------------

Export our workdirectory:


::

  $ export TBOT_BASEDIR=/work/hs/tbot
  $ 

and cd into it


::

  $ cd $TBOT_BASEDIR
  $ 

.. raw:: pdf

   PageBreak

clone the U-Boot code
---------------------

Now we simply clone the U-Boots source code with git:


::

  $ git clone  git://git.denx.de/u-boot u-boot-am335x_evm 
  Cloning into 'u-boot-am335x_evm'...                                                           
  remote: Counting objects: 501780, done.                                                       
  remote: Compressing objects: 100% (85102/85102), done.                                        
  remote: Total 501780 (delta 412960), reused 497673 (delta 409125)                             
  Receiving objects: 100% (501780/501780), 102.72 MiB | 1.13 MiB/s, done.                       
  Resolving deltas: 100% (412960/412960), done.                                                 
  Checking connectivity... done.                                                                
  $                                                       


cd into it


::

  $ cd u-boot-am335x_evm
  $ 

checkout the branch you want to test


::

  $ git checkout master
  Already on 'master'
  Your branch is up-to-date with 'origin/master'.
  $ 

just for the records, print some info of the branch


::

  $ git describe --tags
  v2017.09-396-g6ca43a5
  $ 

.. raw:: pdf

   PageBreak

setup toolchain
===============

This depends on the toolchain you use.


::

  $ export ARCH=arm
  $ printenv PATH | grep --color=never /home/hs/.buildman-toolchains/gcc-4.9.0-nolibc/arm-unknown-linux-gnueabi/bin
  $ export PATH=/home/hs/.buildman-toolchains/gcc-4.9.0-nolibc/arm-unknown-linux-gnueabi/bin:$PATH
  $ export CROSS_COMPILE=arm-unknown-linux-gnueabi-
  $ 

If you have no toolchain installed, may you try buildman (see U-Boot code
tools/buildman) to fetch a toolchain:

::

   cd /path/to/u-boot
   PATH=$PATH:`pwd`/tools/buildman
   buildman --fetch-arch arm

.. raw:: pdf

   PageBreak

compile U-Boot for the beagleboneblack
=====================================


Add the path to the dtc command to your PATH variable


::

  $ printenv PATH | grep --color=never /work/tbot2go/tbot/dtc
  $ export PATH=/work/tbot2go/tbot/dtc:$PATH
  $ 


clean the source code


::

  $ make mrproper
  $ 

configure source for the beagleboneblack


::

  $ make am335x_evm_defconfig
    HOSTCC  scripts/basic/fixdep
    HOSTCC  scripts/kconfig/conf.o
    SHIPPED scripts/kconfig/zconf.tab.c
    SHIPPED scripts/kconfig/zconf.lex.c
    SHIPPED scripts/kconfig/zconf.hash.c
    HOSTCC  scripts/kconfig/zconf.tab.o
    HOSTLD  scripts/kconfig/conf
  #
  # configuration written to .config
  #
  $ 

Now compile it


::

  $ make -s DTC_FLAGS="-S 0xb000" all
  *** Your GCC is older than 6.0 and will not be supported starting in v2018.01.
  arch/arm/dts/am335x-pxm50.dtb: Warning (unit_address_format): Node /ocp/i2c@4819c000/egalax_ts@04 unit name should not have\
    leading 0s
  ===================== WARNING ======================
  This board uses CONFIG_DM_I2C_COMPAT. Please remove
  (possibly in a subsequent patch in your series)
  before sending patches to the mailing list.
  ====================================================
  $ 

after U-Boot is compiled, copy the resulting binaries we need later to our tftpboot directory.



::

  $ scp  u-boot.bin pi@192.168.1.110:/srv/tftpboot//beagleboneblack/tbot/u-boot.bin
  pi@192.168.1.110's password: 
  u-boot.bin\
    100%  494KB 493.8KB/s   00:00
  $ 
  $ scp  u-boot.img pi@192.168.1.110:/srv/tftpboot//beagleboneblack/tbot/u-boot.img
  pi@192.168.1.110's password: 
  u-boot.img\
    100%  716KB 715.7KB/s   00:00
  $ 
  $ scp  MLO pi@192.168.1.110:/srv/tftpboot//beagleboneblack/tbot/MLO
  pi@192.168.1.110's password: 
  MLO\
    100%   92KB  92.4KB/s   00:00
  $ 

We also copy the u-boot.dtb file to our tftp directory, as we do some
testing with it later.


::

  $ scp  u-boot.dtb pi@192.168.1.110:/srv/tftpboot//beagleboneblack/tbot/u-boot.dtb
  pi@192.168.1.110's password: 
  u-boot.dtb\
    100%   44KB  44.0KB/s   00:00
  $ 

.. raw:: pdf

   PageBreak

U-Boot installation
===================

install U-Boot
--------------

for this example, we install the new U-Boot on the SD card, as we use SD card bootmode.


::

  => print tbot_upd_uboot load_uboot upd_uboot
  tbot_upd_uboot=run load_uboot;run upd_uboot
  load_uboot=tftp ${load_addr_r} ${ubfile}
  upd_uboot=fatwrite mmc 1:1 ${load_addr_r} u-boot.img ${filesize}
  => 

tfpt the new u-boot image into ram and write it to the sd card.


::

  => run tbot_upd_uboot
  link up on port 0, speed 100, full duplex
  Using ethernet@4a100000 device
  TFTP from server 192.168.3.1; our IP address is 192.168.3.20
  Filename 'beagleboneblack/tbot/u-boot.img'.
  Load address: 0x81000000
  Loading: *#################################################################
  	 #################################################################
  	 ##############
  	 1.1 MiB/s
  done
  Bytes transferred = 732904 (b2ee8 hex)
  writing u-boot.img
  732904 bytes written
  => 

install SPL
-----------

for this example, we install the new SPL on the SD card, as we use SD card bootmode.


::

  => print tbot_upd_spl load_mlo upd_mlo
  tbot_upd_spl=run load_mlo;run upd_mlo
  load_mlo=tftp ${load_addr_r} ${mlofile}
  upd_mlo=fatwrite mmc 1:1 ${load_addr_r} mlo ${filesize}
  => 

tfpt the new SPL image into ram and write it to the sd card.


::

  => run tbot_upd_spl
  link up on port 0, speed 100, full duplex
  Using ethernet@4a100000 device
  TFTP from server 192.168.3.1; our IP address is 192.168.3.20
  Filename 'beagleboneblack/tbot/MLO'.
  Load address: 0x81000000
  Loading: *###################
  	 1 MiB/s
  done
  Bytes transferred = 94652 (171bc hex)
  writing mlo
  94652 bytes written
  => 

.. raw:: pdf

   PageBreak

Tool Installation
=================

U-Boot uses a special image format when loading the Linux kernel or ramdisk or other images. This image contains (among other things) information about the time of creation, operating system, compression type, image type, image name and CRC32 checksums.

The tool :redtext:`mkimage` is used to create such images or to display the information they contain. When using the ELDK_, the :redtext:`mkimage` command is already included with the other ELDK_ tools.

If you don't use the ELDK_ then you should install :redtext:`mkimage` in some directory that is in your command search PATH, for instance:

::

  $ cp tools/mkimage /usr/local/bin/

mkimage is readily available in several distributions; for example, in Ubuntu_ it is part of the :redtext:`u-boot-tools` package, so it can be installed with:

::

  $ sudo apt-get install u-boot-tools

In Fedora_ the package name is :redtext:`uboot-tools`, and the command to install it is:

::

  $ sudo dnf install uboot-tools

Finally, if you're building with OpenEmbedded_ or `Yocto Project`_, you would want to add the :redtext:`u-boot-fw-utils` recipe to your image. 

.. raw:: pdf

   PageBreak

U-Boot Command Line Interface
=============================

The following section describes the most important commands available in U-Boot. Please note that U-Boot is highly configurable, so not all of these commands may be available in the configuration of U-Boot installed on your hardware, or additional commands may exist. You can use the help command to print a list of all available commands for your configuration.

For most commands, you do not need to type in the full command name; instead it is sufficient to type a few characters. For instance, help can be abbreviated as h.

|Warning| The behaviour of some commands depends on the configuration of U-Boot and on the definition of some variables in your U-Boot environment.

Almost all U-Boot commands expect numbers to be entered in hexadecimal input format. (Exception: for historical reasons, the sleep command takes its argument in decimal input format.)

Be careful not to use edit keys besides 'Backspace', as hidden characters in things like environment variables can be very difficult to find. 

.. raw:: pdf

   PageBreak

Information Commands
--------------------

bdinfo - print Board Info structure
...................................


::

  => help bdinfo
  bdinfo - print Board Info structure
  
  Usage:
  bdinfo 
  => 

The :redtext:`bdinfo` command (:redtext:`bdi`) prints the information that U-Boot passes about the board such as memory addresses and sizes, clock frequencies, MAC address, etc. This information is mainly needed to be passed to the Linux kernel. 



::

  => bdi
  arch_number = 0x00000E05
  boot_params = 0x80000100
  DRAM bank   = 0x00000000
  -> start    = 0x80000000
  -> size     = 0x20000000
  baudrate    = 115200 bps
  TLB addr    = 0x9FFF0000
  relocaddr   = 0x9FF4E000
  reloc off   = 0x1F74E000
  irq_sp      = 0x9DF21EC0
  sp start    = 0x9DF21EB0
  Early malloc usage: 184 / 400
  fdt_blob = 9df21ed8
  => 

.. raw:: pdf

   PageBreak

coninfo - print console devices and informations
................................................


::

  => help conin
  coninfo - print console devices and information
  
  Usage:
  coninfo 
  => 

The :redtext:`coninfo` command (:redtext:`conin`) displays information about the available console I/O devices. 


::

  => conin
  List of available devices:
  serial@44e09000 00000007 IO stdin stdout stderr 
  serial   00000003 IO 
  => 

The output contains the device name, flags, and the current usage. For example, the output

::

  serial@44e09000 00000003 IO stdin stdout stderr 
  
means that the serial device provides input (flag 'I') and output (flag 'O') functionality and is currently assigned to the 3 standard I/O streams stdin, stdout and stderr. 

.. raw:: pdf

   PageBreak

.. include:: u-boot-flinfo.rst

.. raw:: pdf

   PageBreak

.. include:: u-boot-help.rst

.. raw:: pdf

   PageBreak

.. include:: u-boot-memory.rst


.. raw:: pdf

   PageBreak

.. include:: u-boot-mw.rst

.. raw:: pdf

   PageBreak

.. include:: u-boot-nm.rst

.. raw:: pdf

   PageBreak

.. include:: u-boot-loop.rst

.. raw:: pdf

   PageBreak

.. include:: u-boot-execution.rst

.. raw:: pdf

   PageBreak

.. include:: u-boot-download.rst

.. raw:: pdf

   PageBreak

.. include:: u-boot-env.rst

.. raw:: pdf

   PageBreak

.. include:: u-boot-fdt.rst

.. raw:: pdf

   PageBreak

.. include:: u-boot-special.rst

.. raw:: pdf

   PageBreak

.. include:: u-boot-misc.rst

.. raw:: pdf

   PageBreak

.. include:: u-boot-vars.rst

.. raw:: pdf

   PageBreak

.. include:: u-boot-script.rst

.. raw:: pdf

   PageBreak

.. include:: u-boot-testpy.rst


links
=====

.. _tbot: https://github.com/hsdenx/tbot

.. _ELDK: http://www.denx.de/wiki/DULG/ELDK

.. _Ubuntu: http://www.ubuntu.com/

.. _Fedora: http://fedoraproject.org/

.. _OpenEmbedded: http://openembedded.org/wiki/Main_Page

.. _`Yocto Project`: https://www.yoctoproject.org/
