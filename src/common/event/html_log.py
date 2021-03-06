# SPDX-License-Identifier: GPL-2.0
#
import logging
import sys
import os

class html_log(object):
    """create a html log file after tbot hs finished

    create a nicer log ... see for an example:

    http://xeidos.ddns.net/tbot/id_189/html_log.html

    the created html file needs the css file:

    https://github.com/hsdenx/tbot/blob/testing/log/multiplexed_tbotlog.css

    and "myscript.js" for local usage.

    - **parameters**, **types**, **return** and **return types**::
    :param arg1: tb
    :param arg2: filename which gets created, place tb.workdir
    """
    def __init__(self, tb, htmlfile):
        self.tb = tb
        self.ev = self.tb.event
        self.htmlfile = htmlfile
        self.fd = open(self.tb.resultdir + '/' + self.htmlfile, 'w')
        self.dotnr = 0
        self.htmlid = 0
        self.conlog = ''
        self.cpclog = ''
        self.ctrlog = ''
        self.canmlog = ''

    def create_htmlfile(self):
        """create the html file
        """
        self._write_html_header()
        self._write_log()
        self._write_html_bottom()
        self.fd.close()
        w = self.tb.workdir
        r = self.tb.resultdir
        cmd = 'cp ' + w + '/log/multiplexed_tbotlog.css ' + r
        os.system(cmd)
        cmd = 'cp ' + w + '/log/myscript.js ' + r
        os.system(cmd)
 
    def _write_html_header(self):
        self.fd.write('<html>\n')
        self.fd.write('<head>\n')
        self.fd.write('<link rel="stylesheet" type="text/css" href="multiplexed_tbotlog.css">\n')
        #self.fd.write('<script src="http://code.jquery.com/jquery.min.js"></script>\n')
        self.fd.write('<script src="myscript.js"></script>\n')
        self.fd.write('<script>\n')
        self.fd.write('$(document).ready(function () {\n')
        self.fd.write('    // Add expand/contract buttons to all block headers\n')
        self.fd.write('    btns = "<span class=\\"block-expand hidden\\">[+] </span>" +\n')
        self.fd.write('        "<span class=\\"block-contract\\">[-] </span>";\n')
        self.fd.write('    $(".block-header").prepend(btns);\n')
        self.fd.write('\n')
        self.fd.write('    // Pre-contract all blocks which passed, leaving only problem cases\n')
        self.fd.write('    // expanded, to highlight issues the user should look at.\n')
        self.fd.write('    // Only top-level blocks (sections) should have any status\n')
        self.fd.write('    passed_bcs = $(".block-content:has(.status-pass)");\n')
        self.fd.write('    // Some blocks might have multiple status entries (e.g. the status\n')
        self.fd.write('    // report), so take care not to hide blocks with partial success.\n')
        self.fd.write('    passed_bcs = passed_bcs.not(":has(.status-fail)");\n')
        self.fd.write('    passed_bcs = passed_bcs.not(":has(.status-xfail)");\n')
        self.fd.write('    passed_bcs = passed_bcs.not(":has(.status-xpass)");\n')
        self.fd.write('    passed_bcs = passed_bcs.not(":has(.status-skipped)");\n')
        self.fd.write('    // Hide the passed blocks\n')
        self.fd.write('    passed_bcs.addClass("hidden");\n')
        self.fd.write('    // Flip the expand/contract button hiding for those blocks.\n')
        self.fd.write('    bhs = passed_bcs.parent().children(".block-header")\n')
        self.fd.write('    bhs.children(".block-expand").removeClass("hidden");\n')
        self.fd.write('    bhs.children(".block-contract").addClass("hidden");\n')
        self.fd.write('\n')
        self.fd.write('    // Add click handler to block headers.\n')
        self.fd.write('    // The handler expands/contracts the block.\n')
        self.fd.write('    $(".block-header").on("click", function (e) {\n')
        self.fd.write('        var header = $(this);\n')
        self.fd.write('        var content = header.next(".block-content");\n')
        self.fd.write('        var expanded = !content.hasClass("hidden");\n')
        self.fd.write('        if (expanded) {\n')
        self.fd.write('            content.addClass("hidden");\n')
        self.fd.write('            header.children(".block-expand").first().removeClass("hidden");\n')
        self.fd.write('            header.children(".block-contract").first().addClass("hidden");\n')
        self.fd.write('        } else {\n')
        self.fd.write('            header.children(".block-contract").first().removeClass("hidden");\n')
        self.fd.write('            header.children(".block-expand").first().addClass("hidden");\n')
        self.fd.write('            content.removeClass("hidden");\n')
        self.fd.write('        }\n')
        self.fd.write('    });\n')
        self.fd.write('\n')
        self.fd.write('    // When clicking on a link, expand the target block\n')
        self.fd.write('    $("a").on("click", function (e) {\n')
        self.fd.write('        var block = $($(this).attr("href"));\n')
        self.fd.write('        var header = block.children(".block-header");\n')
        self.fd.write('        var content = block.children(".block-content").first();\n')
        self.fd.write('        header.children(".block-contract").first().removeClass("hidden");\n')
        self.fd.write('        header.children(".block-expand").first().addClass("hidden");\n')
        self.fd.write('        content.removeClass("hidden");\n')
        self.fd.write('    });\n')
        self.fd.write('});\n')
        self.fd.write('</script>\n')
        self.fd.write('</head>\n')
        self.fd.write('<body>\n')
        self.fd.write('\n')
        self.fd.write('<tt>\n')
 
    def _write_html_bottom(self):
        self.fd.write('</tt>\n')
        self.fd.write('</body>\n')
        self.fd.write('</html>\n')
        self.fd.write('\n')

    def _write_tc_start_block(self, name):
        self.htmlid += 1
        self.fd.write('<!-- a testcase -->\n')
        self.fd.write('<div class="section block" id="' + str(self.htmlid) + '">\n')
        self.fd.write('<div class="section-header block-header">' + name + '</div>\n')
        self.fd.write('<div class="section-content block-content">\n')
        self.fd.write('<div class="action">\n')
        self.fd.write('<pre>\n')
        self.fd.write('</pre>\n')
        self.fd.write('</div>\n')
        self.fd.write('\n')

    def _write_con_log_block(self):
        if self.conlog == '':
            return
        self.htmlid += 1
        self.fd.write('<!-- console log of testcase -->\n')
        self.fd.write('<div class="stream block" id="' + str(self.htmlid) + '">\n')
        self.fd.write('<div class="stream-header block-header">console</div>\n')
        self.fd.write('<div class="stream-content block-content">\n')
        self.fd.write('<xmp>\n')
        self.fd.write(self.conlog)
        self.fd.write('</xmp>\n')
        self.fd.write('<div class="stream-trailer block-trailer">End stream: console</div>\n')
        self.fd.write('<div class="status-pass"></div>\n')
        self.fd.write('</div>\n')
        self.fd.write('</div>\n')
        self.fd.write('<!-- end of console log of testcase -->\n')
        self.fd.write('\n')

    def _write_cpc_log_block(self):
        if self.cpclog == '':
            return
        self.htmlid += 1
        self.fd.write('<!-- ctrl cpc log of testcase -->\n')
        self.fd.write('<div class="stream block" id="' + str(self.htmlid) + '">\n')
        self.fd.write('<div class="stream-header block-header">ctrl cpc</div>\n')
        self.fd.write('<div class="stream-content block-content">\n')
        self.fd.write('<xmp>\n')
        self.fd.write(self.cpclog)
        self.fd.write('</xmp>\n')
        self.fd.write('<div class="stream-trailer block-trailer">End stream: ctrl cpc</div>\n')
        self.fd.write('<div class="status-pass"></div>\n')
        self.fd.write('</div>\n')
        self.fd.write('</div>\n')
        self.fd.write('<!-- end of ctrl cpc log of testcase -->\n')
        self.fd.write('\n')

    def _write_ctrl_log_block(self):
        if self.ctrlog == '':
            return
        self.htmlid += 1
        self.fd.write('<!-- ctrl log of testcase -->\n')
        self.fd.write('<div class="stream block" id="' + str(self.htmlid) + '">\n')
        self.fd.write('<div class="stream-header block-header">control</div>\n')
        self.fd.write('<div class="stream-content block-content">\n')
        self.fd.write('<xmp>\n')
        self.fd.write(self.ctrlog)
        self.fd.write('</xmp>\n')
        self.fd.write('<div class="stream-trailer block-trailer">End stream: control</div>\n')
        self.fd.write('<div class="status-pass"></div>\n')
        self.fd.write('</div>\n')
        self.fd.write('</div>\n')
        self.fd.write('<!-- end of control log of testcase -->\n')
        self.fd.write('\n')

    def _write_canm_log_block(self):
        if self.canmlog == '':
            return
        self.htmlid += 1
        self.fd.write('<!-- canm log of testcase -->\n')
        self.fd.write('<div class="stream block" id="' + str(self.htmlid) + '">\n')
        self.fd.write('<div class="stream-header block-header">canm</div>\n')
        self.fd.write('<div class="stream-content block-content">\n')
        self.fd.write('<xmp>\n')
        self.fd.write(self.canmlog)
        self.fd.write('</xmp>\n')
        self.fd.write('<div class="stream-trailer block-trailer">End stream: control</div>\n')
        self.fd.write('<div class="status-pass"></div>\n')
        self.fd.write('</div>\n')
        self.fd.write('</div>\n')
        self.fd.write('<!-- end of canm log of testcase -->\n')
        self.fd.write('\n')

    def _write_tc_end(self, name, status):
        ststr = 'Failed'
        if status == 'True':
            ststr = 'OK'

        self.fd.write('<div class="section-trailer block-trailer">' + name + '</div>\n')
        if status == 'True':
            self.fd.write('<div class="status-pass">\n')
        elif status == 'skipped':
            self.fd.write('<div class="status-skipped">\n')
        else:
            self.fd.write('<div class="status-fail">\n')
        self.fd.write('<pre>' + ststr + '\n')
        self.fd.write('</pre>\n')
        self.fd.write('</div>\n')
        self.fd.write('</div>\n')
        self.fd.write('</div>\n')
        self.fd.write('<!-- end of a testcase -->\n')
        self.fd.write('\n')

    def write_log_block(self):
        # write con block need log
        self._write_con_log_block()
        # write cpc block need log
        self._write_cpc_log_block()
        # write ctrl need log
        self._write_ctrl_log_block()
        # write canm need log
        self._write_canm_log_block()
        # write end of tc block (name, status)
        self.conlog = ''
        self.cpclog = ''
        self.ctrlog = ''
        self.canmlog = ''

    def _get_event_id(self, el):
        if 'SET_PTEST_' in el['id']:
            return el['id']
        if el['id'] == 'WDT':
            return el['id']
        if el['id'] == 'ERROR_STRING':
            return el['id']
        if el['id'] == 'Boardname':
            return el['id']
        if el['id'] == 'BoardnameEnd':
            return el['id']
        if el['id'] == 'log':
            return el['id']
        if el['id'] == 'Start':
            return el['id']
        if el['id'] == 'StartFkt':
            return el['id']
        if el['id'] == 'End':
            return el['id']
        return 'none'

    def _get_event_name(self, el):
        if el['id'] == 'SET_PTEST_BEGIN':
            return el['val']
        if el['id'] == 'SET_PTEST_END':
            return el['val']
        #if el['typ'] == 'SET_PTEST_SUBSTART':
        #    return 'undef'
        return el['fname']

    def _get_next_event(self, el):
        if len(el) == 0:
            return ''

        ret = el[0]
        el.pop(0)
        return ret

    def _write_testcase(self, name, evl):
        # write start of tc block need name
        if name != 'StartHTML':
            self._write_tc_start_block(name)

        self.conlog =''
        self.ctrlog =''
        self.cpclog =''
        self.canmlog =''
        el = 'start'
        while el != '':
            el = self._get_next_event(evl)
            if el == '':
                continue
            if el['typ'] != 'EVENT':
                continue
            typ = self._get_event_id(el)
            if typ == 'none':
                continue
            tc_name = self._get_event_name(el)

            if typ == 'Start' or typ == 'Boardname' or typ == 'StartFkt':
                self.write_log_block()
                self._write_testcase(tc_name, evl)

            if typ == 'SET_PTEST_START':
                continue

            if typ == 'SET_PTEST_STOP':
                continue

            if typ == 'SET_PTEST_SUBSTART':
                continue

            if typ == 'SET_PTEST_SUM':
                self.ptest_stat = el['val']
                continue

            if typ == 'SET_PTEST_SUM_ALL':
                self.ptest_stat = el['val']
                self.write_log_block()
                self.conlog += self.ptest_stat
                self.write_log_block()
                continue

            if typ == 'SET_PTEST_BEGIN':
            #if typ == 'SET_PTEST_BEGIN' or typ == 'SET_PTEST_SUBSTART':
                self.ptest_ok = True
                self.ptest_stat = ''
                self.write_log_block()
                self._write_testcase(tc_name, evl)

            if typ == 'SET_PTEST_ERROR':
                self.ptest_ok = False

            # get status (end of TC) parse "End" or "BoardnameEnd" check if name == name !
            if typ == 'End' or typ == 'BoardnameEnd':
                if tc_name != name:
                    print("not sync with tc name\n", tc_name, name)
                status = el['val']
                self.write_log_block()
                self._write_tc_end(name, status)
                return

            #if typ == 'SET_PTEST_SUM_PASS' or typ == 'SET_PTEST_SUM_SKIP' or typ == 'SET_PTEST_SUM_FAIL' or typ == 'SET_PTEST_END':
            if typ == 'SET_PTEST_END':
                self.write_log_block()
                self.conlog += self.ptest_stat
                self.write_log_block()
                #status = 'False'
                #if typ == 'SET_PTEST_SUM_PASS':
                #    status = 'True'
                #if typ == 'SET_PTEST_SUM_SKIP':
                #    status = 'skipped'
                val = 'False'
                if self.ptest_ok:
                    val = 'True'
                self._write_tc_end(tc_name, val)
                return

            if typ == 'WDT':
                wdtstr = '\n\nWDT triggered\n\n'
                self.conlog += wdtstr
                self.ctrlog += wdtstr
                self.cpclog += wdtstr
                continue

            if typ == 'ERROR_STRING':
                wdtstr = '\n\nError String ' + el['val'] + ' found\n\n'
                self.conlog += wdtstr
                self.ctrlog += wdtstr
                self.cpclog += wdtstr
                continue

            if typ == 'log':
                # get list of tb_con log
                # get list of tb_ctrl log
                # print("** ", el['fname'])
                if el['fname'] == 'tb_con':
                    loglin = el['val']
                    if loglin.startswith("r "):
                        self.conlog += loglin[2:]
                    if loglin.startswith("re "):
                        self.conlog += loglin[3:]
                    if loglin.startswith("er "):
                        self.conlog += loglin[2:]
                if el['fname'] == 'tb_ctrl':
                    loglin = el['val']
                    if loglin.startswith("r "):
                        self.ctrlog += loglin[2:]
                    if loglin.startswith("re "):
                        self.ctrlog += loglin[3:]
                if el['fname'] == 'tb_cpc':
                    loglin = el['val']
                    if loglin.startswith("r "):
                        self.cpclog += loglin[2:]
                    if loglin.startswith("re "):
                        self.cpclog += loglin[3:]
                if el['fname'] == 'tb_canm':
                    loglin = el['val']
                    if loglin.startswith("r "):
                        self.canmlog += loglin[2:]
                continue

    def _write_log(self):
        el = list(self.tb.event.event_list)
        self._write_testcase('StartHTML', el)
