#----------------------        Import Area        ------------------------------
import gdb
import re
import copy
#----------------------        Import Area End    ------------------------------


#----------------------        Define Area        ------------------------------
#----------------------        Define Area End    ------------------------------


#----------------------        Functions Area     ------------------------------
def GetAllStrListInText(searchtext, searchpattern):
    patternobj = re.compile(searchpattern)
    matchlist = patternobj.findall(searchtext)
    return matchlist

def get_value_by_name(name):
    out = gdb.execute("p/x "+name, from_tty=False, to_string=True)
    out = out.replace('~', '').replace('\"', '').replace('\\n', '')
    result = GetAllStrListInText(out, r'\$[0-9]+\s+=\s+(0x[0-9a-fA-F]{1,8})')
    return int(result[0], 16)

def get_value_by_name1(name):
    out = gdb.execute("p "+name, from_tty=False, to_string=True)
    out = out.replace('~', '').replace('\"', '').replace('\\n', '')
    result = GetAllStrListInText(out, r'\$[0-9]+\s+=.+(0x[0-9a-fA-F]{1,8})')
    return int(result[0], 16)

def get_word_value_by_address(address):
    if type(address) == int:
        address = hex(address)
        out = gdb.execute("x/1xw "+address, from_tty=False, to_string=True)
    else:
        out = gdb.execute("x/1xw "+address, from_tty=False, to_string=True)
    out = out.replace('~', '').replace('\"', '').replace('\\n', '')
    result = GetAllStrListInText(out, address+r'\s*.*:\s+(0x[0-9a-fA-F]{1,8})')
    return int(result[0], 16)

def get_thread_name(thread):
    if type(thread) == int:
        out = gdb.execute('p ((TCB_t *)' + str(thread) + ')->pcTaskName', from_tty=False, to_string=True)
    else:
        out = gdb.execute('p ((TCB_t *)' + thread + ')->pcTaskName', from_tty=False, to_string=True)
    out = out.replace('~', '').replace('\"', '').replace('\\n', '')
    # print(out)
    result = GetAllStrListInText(out, r'\$[0-9]+\s+=\s+(.*)')
    return result[0]

def set_context(thread):
    gdb.execute('set $ar0  = '+ str(thread.context.ar0), from_tty=False, to_string=True)
    gdb.execute('set $ar1  = '+ str(thread.context.ar1), from_tty=False, to_string=True)
    gdb.execute('set $ar2  = '+ str(thread.context.ar2), from_tty=False, to_string=True)
    gdb.execute('set $ar3  = '+ str(thread.context.ar3), from_tty=False, to_string=True)
    gdb.execute('set $ar4  = '+ str(thread.context.ar4), from_tty=False, to_string=True)
    gdb.execute('set $ar5  = '+ str(thread.context.ar5), from_tty=False, to_string=True)
    gdb.execute('set $ar6  = '+ str(thread.context.ar6), from_tty=False, to_string=True)
    gdb.execute('set $ar7  = '+ str(thread.context.ar7), from_tty=False, to_string=True)
    gdb.execute('set $ar8  = '+ str(thread.context.ar8), from_tty=False, to_string=True)
    gdb.execute('set $ar9  = '+ str(thread.context.ar9), from_tty=False, to_string=True)
    gdb.execute('set $ar10 = '+ str(thread.context.ar10), from_tty=False, to_string=True)
    gdb.execute('set $ar11 = '+ str(thread.context.ar11), from_tty=False, to_string=True)
    gdb.execute('set $ar12 = '+ str(thread.context.ar12), from_tty=False, to_string=True)
    gdb.execute('set $ar13 = '+ str(thread.context.ar13), from_tty=False, to_string=True)
    gdb.execute('set $ar14 = '+ str(thread.context.ar14), from_tty=False, to_string=True)
    gdb.execute('set $ar15 = '+ str(thread.context.ar15), from_tty=False, to_string=True)
    gdb.execute('set $ar16 = '+ str(thread.context.ar16), from_tty=False, to_string=True)
    gdb.execute('set $ar17 = '+ str(thread.context.ar17), from_tty=False, to_string=True)
    gdb.execute('set $ar18 = '+ str(thread.context.ar18), from_tty=False, to_string=True)
    gdb.execute('set $ar19 = '+ str(thread.context.ar19), from_tty=False, to_string=True)
    gdb.execute('set $ar20 = '+ str(thread.context.ar20), from_tty=False, to_string=True)
    gdb.execute('set $ar21 = '+ str(thread.context.ar21), from_tty=False, to_string=True)
    gdb.execute('set $ar22 = '+ str(thread.context.ar22), from_tty=False, to_string=True)
    gdb.execute('set $ar23 = '+ str(thread.context.ar23), from_tty=False, to_string=True)
    gdb.execute('set $ar24 = '+ str(thread.context.ar24), from_tty=False, to_string=True)
    gdb.execute('set $ar25 = '+ str(thread.context.ar25), from_tty=False, to_string=True)
    gdb.execute('set $ar26 = '+ str(thread.context.ar26), from_tty=False, to_string=True)
    gdb.execute('set $ar27 = '+ str(thread.context.ar27), from_tty=False, to_string=True)
    gdb.execute('set $ar28 = '+ str(thread.context.ar28), from_tty=False, to_string=True)
    gdb.execute('set $ar29 = '+ str(thread.context.ar29), from_tty=False, to_string=True)
    gdb.execute('set $ar30 = '+ str(thread.context.ar30), from_tty=False, to_string=True)
    gdb.execute('set $ar31 = '+ str(thread.context.ar31), from_tty=False, to_string=True)
    gdb.execute('set $ar32 = '+ str(thread.context.ar32), from_tty=False, to_string=True)
    gdb.execute('set $ar33 = '+ str(thread.context.ar33), from_tty=False, to_string=True)
    gdb.execute('set $ar34 = '+ str(thread.context.ar34), from_tty=False, to_string=True)
    gdb.execute('set $ar35 = '+ str(thread.context.ar35), from_tty=False, to_string=True)
    gdb.execute('set $ar36 = '+ str(thread.context.ar36), from_tty=False, to_string=True)
    gdb.execute('set $ar37 = '+ str(thread.context.ar37), from_tty=False, to_string=True)
    gdb.execute('set $ar38 = '+ str(thread.context.ar38), from_tty=False, to_string=True)
    gdb.execute('set $ar39 = '+ str(thread.context.ar39), from_tty=False, to_string=True)
    gdb.execute('set $ar40 = '+ str(thread.context.ar40), from_tty=False, to_string=True)
    gdb.execute('set $ar41 = '+ str(thread.context.ar41), from_tty=False, to_string=True)
    gdb.execute('set $ar42 = '+ str(thread.context.ar42), from_tty=False, to_string=True)
    gdb.execute('set $ar43 = '+ str(thread.context.ar43), from_tty=False, to_string=True)
    gdb.execute('set $ar44 = '+ str(thread.context.ar44), from_tty=False, to_string=True)
    gdb.execute('set $ar45 = '+ str(thread.context.ar45), from_tty=False, to_string=True)
    gdb.execute('set $ar46 = '+ str(thread.context.ar46), from_tty=False, to_string=True)
    gdb.execute('set $ar47 = '+ str(thread.context.ar47), from_tty=False, to_string=True)
    gdb.execute('set $ar48 = '+ str(thread.context.ar48), from_tty=False, to_string=True)
    gdb.execute('set $ar49 = '+ str(thread.context.ar49), from_tty=False, to_string=True)
    gdb.execute('set $ar50 = '+ str(thread.context.ar50), from_tty=False, to_string=True)
    gdb.execute('set $ar51 = '+ str(thread.context.ar51), from_tty=False, to_string=True)
    gdb.execute('set $ar52 = '+ str(thread.context.ar52), from_tty=False, to_string=True)
    gdb.execute('set $ar53 = '+ str(thread.context.ar53), from_tty=False, to_string=True)
    gdb.execute('set $ar54 = '+ str(thread.context.ar54), from_tty=False, to_string=True)
    gdb.execute('set $ar55 = '+ str(thread.context.ar55), from_tty=False, to_string=True)
    gdb.execute('set $ar56 = '+ str(thread.context.ar56), from_tty=False, to_string=True)
    gdb.execute('set $ar57 = '+ str(thread.context.ar57), from_tty=False, to_string=True)
    gdb.execute('set $ar58 = '+ str(thread.context.ar58), from_tty=False, to_string=True)
    gdb.execute('set $ar59 = '+ str(thread.context.ar59), from_tty=False, to_string=True)
    gdb.execute('set $ar60 = '+ str(thread.context.ar60), from_tty=False, to_string=True)
    gdb.execute('set $ar61 = '+ str(thread.context.ar61), from_tty=False, to_string=True)
    gdb.execute('set $ar62 = '+ str(thread.context.ar62), from_tty=False, to_string=True)
    gdb.execute('set $ar63 = '+ str(thread.context.ar63), from_tty=False, to_string=True)
    gdb.execute('set $windowbase  = '+ str(thread.context.windowbase), from_tty=False, to_string=True)
    gdb.execute('set $windowstart = '+ str(thread.context.windowstart), from_tty=False, to_string=True)
    gdb.execute('set $pc  = '+ str(thread.context.pc), from_tty=False, to_string=True)
    gdb.execute('set $ps  = '+ str(thread.context.ps), from_tty=False, to_string=True)
    gdb.execute('set $exccause  = '+ str(thread.context.exccause), from_tty=False, to_string=True)
    gdb.execute('set $excvaddr  = '+ str(thread.context.excvaddr), from_tty=False, to_string=True)
    gdb.execute('set $epc1  = '+ str(thread.context.epc1), from_tty=False, to_string=True)
    gdb.execute('set $excsave1  = '+ str(thread.context.excsave1), from_tty=False, to_string=True)

def exception_change_to_lastest_frame():
    out = gdb.execute('bt -1', from_tty=False, to_string=True)
    out = out.replace('~', '').replace('\"', '').replace('\\n', '')
    depth = GetAllStrListInText(out, r'#([0-9]+)\s+')
    depth = int(depth[0], 10)
    # print(depth)
    gdb.execute('select-frame '+str(depth), from_tty=False, to_string=True)

def freertos_get_contex(topofstack, thread):
    solicited_flag  = get_word_value_by_address(topofstack+0)
    if solicited_flag == 0:
        thread.context.ar0 = get_word_value_by_address(topofstack+4)
        thread.context.ar1 = topofstack
        thread.context.ps  = get_word_value_by_address(topofstack+8)
        thread.context.pc  = get_value_by_name1('vPortYield')+3
        thread.context.windowbase = 0
        thread.context.windowstart = 1
        thread.context.ar2    = 0
        thread.context.ar3    = 0
        thread.context.ar4    = 0
        thread.context.ar5    = 0
        thread.context.ar6    = 0
        thread.context.ar7    = 0
        thread.context.ar8    = 0
        thread.context.ar9    = 0
        thread.context.ar10   = 0
        thread.context.ar11   = 0
        thread.context.ar12   = 0
        thread.context.ar13   = 0
        thread.context.ar14   = 0
        thread.context.ar15   = 0
        thread.context.ar16   = 0
        thread.context.ar17   = 0
        thread.context.ar18   = 0
        thread.context.ar19   = 0
        thread.context.ar20   = 0
        thread.context.ar21   = 0
        thread.context.ar22   = 0
        thread.context.ar23   = 0
        thread.context.ar24   = 0
        thread.context.ar25   = 0
        thread.context.ar26   = 0
        thread.context.ar27   = 0
        thread.context.ar28   = 0
        thread.context.ar29   = 0
        thread.context.ar30   = 0
        thread.context.ar31   = 0
        thread.context.ar32   = 0
        thread.context.ar33   = 0
        thread.context.ar34   = 0
        thread.context.ar35   = 0
        thread.context.ar36   = 0
        thread.context.ar37   = 0
        thread.context.ar38   = 0
        thread.context.ar39   = 0
        thread.context.ar40   = 0
        thread.context.ar41   = 0
        thread.context.ar42   = 0
        thread.context.ar43   = 0
        thread.context.ar44   = 0
        thread.context.ar45   = 0
        thread.context.ar46   = 0
        thread.context.ar47   = 0
        thread.context.ar48   = 0
        thread.context.ar49   = 0
        thread.context.ar50   = 0
        thread.context.ar51   = 0
        thread.context.ar52   = 0
        thread.context.ar53   = 0
        thread.context.ar54   = 0
        thread.context.ar55   = 0
        thread.context.ar56   = 0
        thread.context.ar57   = 0
        thread.context.ar58   = 0
        thread.context.ar59   = 0
        thread.context.ar60   = 0
        thread.context.ar61   = 0
        thread.context.ar62   = 0
        thread.context.ar63   = 0
    else:
        thread.context.ps  = get_word_value_by_address(topofstack+8)
        thread.context.pc  = get_word_value_by_address(topofstack+4)
        thread.context.windowbase = 0
        thread.context.windowstart = 1
        thread.context.ar0    = get_word_value_by_address(topofstack+12)
        thread.context.ar1    = get_word_value_by_address(topofstack+16)
        thread.context.ar2    = get_word_value_by_address(topofstack+20)
        thread.context.ar3    = get_word_value_by_address(topofstack+24)
        thread.context.ar4    = get_word_value_by_address(topofstack+28)
        thread.context.ar5    = get_word_value_by_address(topofstack+32)
        thread.context.ar6    = get_word_value_by_address(topofstack+36)
        thread.context.ar7    = get_word_value_by_address(topofstack+40)
        thread.context.ar8    = get_word_value_by_address(topofstack+44)
        thread.context.ar9    = get_word_value_by_address(topofstack+48)
        thread.context.ar10   = get_word_value_by_address(topofstack+52)
        thread.context.ar11   = get_word_value_by_address(topofstack+56)
        thread.context.ar12   = get_word_value_by_address(topofstack+60)
        thread.context.ar13   = get_word_value_by_address(topofstack+64)
        thread.context.ar14   = get_word_value_by_address(topofstack+68)
        thread.context.ar15   = get_word_value_by_address(topofstack+72)
        thread.context.ar16   = 0
        thread.context.ar17   = 0
        thread.context.ar18   = 0
        thread.context.ar19   = 0
        thread.context.ar20   = 0
        thread.context.ar21   = 0
        thread.context.ar22   = 0
        thread.context.ar23   = 0
        thread.context.ar24   = 0
        thread.context.ar25   = 0
        thread.context.ar26   = 0
        thread.context.ar27   = 0
        thread.context.ar28   = 0
        thread.context.ar29   = 0
        thread.context.ar30   = 0
        thread.context.ar31   = 0
        thread.context.ar32   = 0
        thread.context.ar33   = 0
        thread.context.ar34   = 0
        thread.context.ar35   = 0
        thread.context.ar36   = 0
        thread.context.ar37   = 0
        thread.context.ar38   = 0
        thread.context.ar39   = 0
        thread.context.ar40   = 0
        thread.context.ar41   = 0
        thread.context.ar42   = 0
        thread.context.ar43   = 0
        thread.context.ar44   = 0
        thread.context.ar45   = 0
        thread.context.ar46   = 0
        thread.context.ar47   = 0
        thread.context.ar48   = 0
        thread.context.ar49   = 0
        thread.context.ar50   = 0
        thread.context.ar51   = 0
        thread.context.ar52   = 0
        thread.context.ar53   = 0
        thread.context.ar54   = 0
        thread.context.ar55   = 0
        thread.context.ar56   = 0
        thread.context.ar57   = 0
        thread.context.ar58   = 0
        thread.context.ar59   = 0
        thread.context.ar60   = 0
        thread.context.ar61   = 0
        thread.context.ar62   = 0
        thread.context.ar63   = 0

def qemu_start_arm_cpu(port):
    # print(port)
    # qemu = subprocess.Popen([   "qemu-system-arm",
    #                             "-machine", "cm7_virtual",
    #                             "-kernel", "/home/cer1991/ARM/QEMU_Startup/out/qemu_startup.elf",
    #                             "-gdb", "tcp::"+str(port),
    #                             "-nographic"],
    #                             bufsize=0,
    #                             stdin=subprocess.PIPE,
    #                             stdout=subprocess.PIPE,
    #                             stderr=subprocess.PIPE,
    #                             shell=False)
    # time.sleep(2)
    qemu = None
    return qemu

def gdb_create_new_inferior(port, image_file):
    # print('enter create new inferior')
    out = gdb.execute('add-inferior -exec '+ image_file +' -no-connection', from_tty=False, to_string=True)
    out = out.replace('~', '').replace('\"', '').replace('\\n', '')
    # print(out)
    result = GetAllStrListInText(out, r'Added inferior ([0-9]+)')
    inferior_no = result[0]
    out = gdb.execute('inferior '+inferior_no, from_tty=False, to_string=True)
    out = out.replace('~', '').replace('\"', '').replace('\\n', '')
    # print(out)
    out = gdb.execute('target extended-remote localhost:'+str(port), from_tty=False, to_string=True)
    out = out.replace('~', '').replace('\"', '').replace('\\n', '')
    # print(out)
    return inferior_no
#----------------------        Functions Area End ------------------------------


#----------------------        Class Area         ------------------------------
class freertos():
    def __init__(self):
        self.tasks = []

class xtensa_context():
    def __init__(self):
        self.ar0    = 0
        self.ar1    = 0
        self.ar2    = 0
        self.ar3    = 0
        self.ar4    = 0
        self.ar5    = 0
        self.ar6    = 0
        self.ar7    = 0
        self.ar8    = 0
        self.ar9    = 0
        self.ar10   = 0
        self.ar11   = 0
        self.ar12   = 0
        self.ar13   = 0
        self.ar14   = 0
        self.ar15   = 0
        self.ar16   = 0
        self.ar17   = 0
        self.ar18   = 0
        self.ar19   = 0
        self.ar20   = 0
        self.ar21   = 0
        self.ar22   = 0
        self.ar23   = 0
        self.ar24   = 0
        self.ar25   = 0
        self.ar26   = 0
        self.ar27   = 0
        self.ar28   = 0
        self.ar29   = 0
        self.ar30   = 0
        self.ar31   = 0
        self.ar32   = 0
        self.ar33   = 0
        self.ar34   = 0
        self.ar35   = 0
        self.ar36   = 0
        self.ar37   = 0
        self.ar38   = 0
        self.ar39   = 0
        self.ar40   = 0
        self.ar41   = 0
        self.ar42   = 0
        self.ar43   = 0
        self.ar44   = 0
        self.ar45   = 0
        self.ar46   = 0
        self.ar47   = 0
        self.ar48   = 0
        self.ar49   = 0
        self.ar50   = 0
        self.ar51   = 0
        self.ar52   = 0
        self.ar53   = 0
        self.ar54   = 0
        self.ar55   = 0
        self.ar56   = 0
        self.ar57   = 0
        self.ar58   = 0
        self.ar59   = 0
        self.ar60   = 0
        self.ar61   = 0
        self.ar62   = 0
        self.ar63   = 0
        self.windowbase = 0
        self.windowstart = 0
        self.exccause   = 0
        self.excvaddr   = 0
        self.pc = 0
        self.epc1 = 0
        self.ps   = 0
        self.excsave1 = 0

class freertos_thread():
    """
    freertos task handle
    """
    def __init__(self):
        self.number = 0
        self.name = ''
        self.status = ''
        self.ar_number = 64
        self.context = xtensa_context()
        self.tcb = 0

class freertos_check_tasks(gdb.Command):
    def __init__(self, rtos):
        super(freertos_check_tasks, self).__init__("freertos_check_tasks", gdb.COMMAND_DATA)
        self.freertos = rtos
        self.check_done = False

    def invoke(self, arg, from_tty):
        # parameter = arg.split(' ')
        # ar_number = parameter[0]
        if self.check_done == False:
            total_task_number = 0

            # get current thread info
            current_thread = freertos_thread()
            current_thread.number = total_task_number
            current_thread.status = 'running'
            current_thread.name = get_thread_name('pxCurrentTCB')
            current_thread.tcb = get_value_by_name('pxCurrentTCB')
            xpsr = get_value_by_name('nvic_irq_execution_number')
            # handler mode
            if xpsr != 0:
                # exception callstack
                current_thread.status = 'running, but interrupted by exception ' + str(xpsr)
                current_thread.context.ar0  = get_value_by_name('$ar0')
                current_thread.context.ar1  = get_value_by_name('$ar1')
                current_thread.context.ar2  = get_value_by_name('$ar2')
                current_thread.context.ar3  = get_value_by_name('$ar3')
                current_thread.context.ar4  = get_value_by_name('$ar4')
                current_thread.context.ar5  = get_value_by_name('$ar5')
                current_thread.context.ar6  = get_value_by_name('$ar6')
                current_thread.context.ar7  = get_value_by_name('$ar7')
                current_thread.context.ar8  = get_value_by_name('$ar8')
                current_thread.context.ar9  = get_value_by_name('$ar9')
                current_thread.context.ar10 = get_value_by_name('$ar10')
                current_thread.context.ar11 = get_value_by_name('$ar11')
                current_thread.context.ar12 = get_value_by_name('$ar12')
                current_thread.context.ar13 = get_value_by_name('$ar13')
                current_thread.context.ar14 = get_value_by_name('$ar14')
                current_thread.context.ar15 = get_value_by_name('$ar15')
                current_thread.context.ar16 = get_value_by_name('$ar16')
                current_thread.context.ar17 = get_value_by_name('$ar17')
                current_thread.context.ar18 = get_value_by_name('$ar18')
                current_thread.context.ar19 = get_value_by_name('$ar19')
                current_thread.context.ar20 = get_value_by_name('$ar20')
                current_thread.context.ar21 = get_value_by_name('$ar21')
                current_thread.context.ar22 = get_value_by_name('$ar22')
                current_thread.context.ar23 = get_value_by_name('$ar23')
                current_thread.context.ar24 = get_value_by_name('$ar24')
                current_thread.context.ar25 = get_value_by_name('$ar25')
                current_thread.context.ar26 = get_value_by_name('$ar26')
                current_thread.context.ar27 = get_value_by_name('$ar27')
                current_thread.context.ar28 = get_value_by_name('$ar28')
                current_thread.context.ar29 = get_value_by_name('$ar29')
                current_thread.context.ar30 = get_value_by_name('$ar30')
                current_thread.context.ar31 = get_value_by_name('$ar31')
                current_thread.context.ar32 = get_value_by_name('$ar32')
                current_thread.context.ar33 = get_value_by_name('$ar33')
                current_thread.context.ar34 = get_value_by_name('$ar34')
                current_thread.context.ar35 = get_value_by_name('$ar35')
                current_thread.context.ar36 = get_value_by_name('$ar36')
                current_thread.context.ar37 = get_value_by_name('$ar37')
                current_thread.context.ar38 = get_value_by_name('$ar38')
                current_thread.context.ar39 = get_value_by_name('$ar39')
                current_thread.context.ar40 = get_value_by_name('$ar40')
                current_thread.context.ar41 = get_value_by_name('$ar41')
                current_thread.context.ar42 = get_value_by_name('$ar42')
                current_thread.context.ar43 = get_value_by_name('$ar43')
                current_thread.context.ar44 = get_value_by_name('$ar44')
                current_thread.context.ar45 = get_value_by_name('$ar45')
                current_thread.context.ar46 = get_value_by_name('$ar46')
                current_thread.context.ar47 = get_value_by_name('$ar47')
                current_thread.context.ar48 = get_value_by_name('$ar48')
                current_thread.context.ar49 = get_value_by_name('$ar49')
                current_thread.context.ar50 = get_value_by_name('$ar50')
                current_thread.context.ar51 = get_value_by_name('$ar51')
                current_thread.context.ar52 = get_value_by_name('$ar52')
                current_thread.context.ar53 = get_value_by_name('$ar53')
                current_thread.context.ar54 = get_value_by_name('$ar54')
                current_thread.context.ar55 = get_value_by_name('$ar55')
                current_thread.context.ar56 = get_value_by_name('$ar56')
                current_thread.context.ar57 = get_value_by_name('$ar57')
                current_thread.context.ar58 = get_value_by_name('$ar58')
                current_thread.context.ar59 = get_value_by_name('$ar59')
                current_thread.context.ar60 = get_value_by_name('$ar60')
                current_thread.context.ar61 = get_value_by_name('$ar61')
                current_thread.context.ar62 = get_value_by_name('$ar62')
                current_thread.context.ar63 = get_value_by_name('$ar63')
                current_thread.context.windowbase  = get_value_by_name('$windowbase')
                current_thread.context.windowstart  = get_value_by_name('$windowstart')
                current_thread.context.pc  = get_value_by_name('$pc')
                current_thread.context.ps  = get_value_by_name('$ps')
                current_thread.context.exccause  = get_value_by_name('$exccause')
                current_thread.context.excvaddr  = get_value_by_name('$excvaddr')
                current_thread.context.epc1      = get_value_by_name('$epc1')
                current_thread.context.excsave1  = get_value_by_name('$excsave1')
                self.freertos.tasks.append(copy.deepcopy(current_thread))
                total_task_number += 1

                # thread callstack
                current_thread.number = total_task_number
                current_thread.status = 'running'
                topofstack = get_value_by_name('((TCB_t *)'+str(current_thread.tcb)+')->pxTopOfStack')
                freertos_get_contex(topofstack, current_thread)
                self.freertos.tasks.append(copy.deepcopy(current_thread))
                total_task_number += 1
            # thread mode
            else:
                current_thread.context.ar0  = get_value_by_name('$ar0')
                current_thread.context.ar1  = get_value_by_name('$ar1')
                current_thread.context.ar2  = get_value_by_name('$ar2')
                current_thread.context.ar3  = get_value_by_name('$ar3')
                current_thread.context.ar4  = get_value_by_name('$ar4')
                current_thread.context.ar5  = get_value_by_name('$ar5')
                current_thread.context.ar6  = get_value_by_name('$ar6')
                current_thread.context.ar7  = get_value_by_name('$ar7')
                current_thread.context.ar8  = get_value_by_name('$ar8')
                current_thread.context.ar9  = get_value_by_name('$ar9')
                current_thread.context.ar10 = get_value_by_name('$ar10')
                current_thread.context.ar11 = get_value_by_name('$ar11')
                current_thread.context.ar12 = get_value_by_name('$ar12')
                current_thread.context.ar13 = get_value_by_name('$ar13')
                current_thread.context.ar14 = get_value_by_name('$ar14')
                current_thread.context.ar15 = get_value_by_name('$ar15')
                current_thread.context.ar16 = get_value_by_name('$ar16')
                current_thread.context.ar17 = get_value_by_name('$ar17')
                current_thread.context.ar18 = get_value_by_name('$ar18')
                current_thread.context.ar19 = get_value_by_name('$ar19')
                current_thread.context.ar20 = get_value_by_name('$ar20')
                current_thread.context.ar21 = get_value_by_name('$ar21')
                current_thread.context.ar22 = get_value_by_name('$ar22')
                current_thread.context.ar23 = get_value_by_name('$ar23')
                current_thread.context.ar24 = get_value_by_name('$ar24')
                current_thread.context.ar25 = get_value_by_name('$ar25')
                current_thread.context.ar26 = get_value_by_name('$ar26')
                current_thread.context.ar27 = get_value_by_name('$ar27')
                current_thread.context.ar28 = get_value_by_name('$ar28')
                current_thread.context.ar29 = get_value_by_name('$ar29')
                current_thread.context.ar30 = get_value_by_name('$ar30')
                current_thread.context.ar31 = get_value_by_name('$ar31')
                current_thread.context.ar32 = get_value_by_name('$ar32')
                current_thread.context.ar33 = get_value_by_name('$ar33')
                current_thread.context.ar34 = get_value_by_name('$ar34')
                current_thread.context.ar35 = get_value_by_name('$ar35')
                current_thread.context.ar36 = get_value_by_name('$ar36')
                current_thread.context.ar37 = get_value_by_name('$ar37')
                current_thread.context.ar38 = get_value_by_name('$ar38')
                current_thread.context.ar39 = get_value_by_name('$ar39')
                current_thread.context.ar40 = get_value_by_name('$ar40')
                current_thread.context.ar41 = get_value_by_name('$ar41')
                current_thread.context.ar42 = get_value_by_name('$ar42')
                current_thread.context.ar43 = get_value_by_name('$ar43')
                current_thread.context.ar44 = get_value_by_name('$ar44')
                current_thread.context.ar45 = get_value_by_name('$ar45')
                current_thread.context.ar46 = get_value_by_name('$ar46')
                current_thread.context.ar47 = get_value_by_name('$ar47')
                current_thread.context.ar48 = get_value_by_name('$ar48')
                current_thread.context.ar49 = get_value_by_name('$ar49')
                current_thread.context.ar50 = get_value_by_name('$ar50')
                current_thread.context.ar51 = get_value_by_name('$ar51')
                current_thread.context.ar52 = get_value_by_name('$ar52')
                current_thread.context.ar53 = get_value_by_name('$ar53')
                current_thread.context.ar54 = get_value_by_name('$ar54')
                current_thread.context.ar55 = get_value_by_name('$ar55')
                current_thread.context.ar56 = get_value_by_name('$ar56')
                current_thread.context.ar57 = get_value_by_name('$ar57')
                current_thread.context.ar58 = get_value_by_name('$ar58')
                current_thread.context.ar59 = get_value_by_name('$ar59')
                current_thread.context.ar60 = get_value_by_name('$ar60')
                current_thread.context.ar61 = get_value_by_name('$ar61')
                current_thread.context.ar62 = get_value_by_name('$ar62')
                current_thread.context.ar63 = get_value_by_name('$ar63')
                current_thread.context.windowbase  = get_value_by_name('$windowbase')
                current_thread.context.windowstart  = get_value_by_name('$windowstart')
                current_thread.context.pc  = get_value_by_name('$pc')
                current_thread.context.ps  = get_value_by_name('$ps')
                current_thread.context.exccause  = get_value_by_name('$exccause')
                current_thread.context.excvaddr  = get_value_by_name('$excvaddr')
                current_thread.context.epc1      = get_value_by_name('$epc1')
                current_thread.context.excsave1  = get_value_by_name('$excsave1')
                self.freertos.tasks.append(copy.deepcopy(current_thread))
                total_task_number += 1

            # get ready tasks
            ready_task_list_no = get_value_by_name('sizeof(pxReadyTasksLists)/sizeof(List_t)')
            for i in range(ready_task_list_no):
                ready_task_no = get_value_by_name('pxReadyTasksLists['+str(i)+'].uxNumberOfItems')
                if ready_task_no != 0:
                    for j in range(ready_task_no):
                        thread = freertos_thread()
                        thread.number = total_task_number
                        thread.status = 'ready'
                        if j == 0:
                            thread.tcb = get_value_by_name('(pxReadyTasksLists['+str(i)+']).xListEnd.pxNext'+'->pvOwner')
                        else:
                            thread.tcb = get_value_by_name('(pxReadyTasksLists['+str(i)+']).xListEnd.pxNext'+'->pxNext'*j+'->pvOwner')
                        if thread.tcb == current_thread.tcb:
                            # if the ready task is the current task, do nothing
                            # print('(pxReadyTasksLists['+str(i)+']) ' + str(j))
                            continue
                        thread.name = get_thread_name(thread.tcb)
                        topofstack = get_value_by_name('((TCB_t *)'+str(thread.tcb)+')->pxTopOfStack')
                        freertos_get_contex(topofstack, thread)
                        self.freertos.tasks.append(copy.deepcopy(thread))
                        total_task_number += 1

            # get block tasks
            delayed_task_no = get_value_by_name('(*pxDelayedTaskList)->uxNumberOfItems')
            if delayed_task_no != 0:
                for i in range(delayed_task_no):
                    thread = freertos_thread()
                    thread.number = total_task_number
                    thread.status = 'delayed'
                    if i == 0:
                        thread.tcb = get_value_by_name('(*pxDelayedTaskList)->xListEnd.pxNext'+'->pvOwner')
                    else:
                        thread.tcb = get_value_by_name('(*pxDelayedTaskList)->xListEnd.pxNext'+'->pxNext'*i+'->pvOwner')
                    thread.name = get_thread_name(thread.tcb)
                    topofstack = get_value_by_name('((TCB_t *)'+str(thread.tcb)+')->pxTopOfStack')
                    freertos_get_contex(topofstack, thread)
                    self.freertos.tasks.append(copy.deepcopy(thread))
                    total_task_number += 1
            delayed_task_no = get_value_by_name('(*pxOverflowDelayedTaskList)->uxNumberOfItems')
            if delayed_task_no != 0:
                for i in range(delayed_task_no):
                    thread = freertos_thread()
                    thread.number = total_task_number
                    thread.status = 'delayed'
                    if i == 0:
                        thread.tcb = get_value_by_name('(*pxOverflowDelayedTaskList)->xListEnd.pxNext'+'->pvOwner')
                    else:
                        thread.tcb = get_value_by_name('(*pxOverflowDelayedTaskList)->xListEnd.pxNext'+'->pxNext'*i+'->pvOwner')
                    thread.name = get_thread_name(thread.tcb)
                    topofstack = get_value_by_name('((TCB_t *)'+str(thread.tcb)+')->pxTopOfStack')
                    freertos_get_contex(topofstack, thread)
                    self.freertos.tasks.append(copy.deepcopy(thread))
                    total_task_number += 1

            # get suspend tasks
            suspended_task_no = get_value_by_name('(xSuspendedTaskList).uxNumberOfItems')
            if suspended_task_no != 0:
                for i in range(suspended_task_no):
                    thread = freertos_thread()
                    thread.number = total_task_number
                    thread.status = 'suspended'
                    if i == 0:
                        thread.tcb = get_value_by_name('(xSuspendedTaskList).xListEnd.pxNext'+'->pvOwner')
                    else:
                        thread.tcb = get_value_by_name('(xSuspendedTaskList).xListEnd.pxNext'+'->pxNext'*i+'->pvOwner')
                    thread.name = get_thread_name(thread.tcb)
                    topofstack = get_value_by_name('((TCB_t *)'+str(thread.tcb)+')->pxTopOfStack')
                    freertos_get_contex(topofstack, thread)
                    self.freertos.tasks.append(copy.deepcopy(thread))
                    total_task_number += 1

            # get pending ready tasks
            pending_ready_task_no = get_value_by_name('(xPendingReadyList).uxNumberOfItems')
            if pending_ready_task_no != 0:
                for i in range(pending_ready_task_no):
                    thread = freertos_thread()
                    thread.number = total_task_number
                    thread.status = 'pending_ready'
                    if i == 0:
                        thread.tcb = get_value_by_name('(xPendingReadyList).xListEnd.pxNext'+'->pvOwner')
                    else:
                        thread.tcb = get_value_by_name('(xPendingReadyList).xListEnd.pxNext'+'->pxNext'*i+'->pvOwner')
                    thread.name = get_thread_name(thread.tcb)
                    topofstack = get_value_by_name('((TCB_t *)'+str(thread.tcb)+')->pxTopOfStack')
                    freertos_get_contex(topofstack, thread)
                    self.freertos.tasks.append(copy.deepcopy(thread))
                    total_task_number += 1

            # get deleted tasks
            deleted_ready_task_no = get_value_by_name('(xTasksWaitingTermination).uxNumberOfItems')
            if deleted_ready_task_no != 0:
                for i in range(deleted_ready_task_no):
                    thread = freertos_thread()
                    thread.number = total_task_number
                    thread.status = 'pending_ready'
                    if i == 0:
                        thread.tcb = get_value_by_name('(xTasksWaitingTermination).xListEnd.pxNext'+'->pvOwner')
                    else:
                        thread.tcb = get_value_by_name('(xTasksWaitingTermination).xListEnd.pxNext'+'->pxNext'*i+'->pvOwner')
                    thread.name = get_thread_name(thread.tcb)
                    topofstack = get_value_by_name('((TCB_t *)'+str(thread.tcb)+')->pxTopOfStack')
                    freertos_get_contex(topofstack, thread)
                    self.freertos.tasks.append(copy.deepcopy(thread))
                    total_task_number += 1

            # set flag
            self.check_done = True

        # output tasks' status
        for i in self.freertos.tasks:
            print('No:'+str(i.number)+', Task Name: ' + i.name + ', Task Status: ' + i.status + ', Task TCB: ' + hex(i.tcb)+ ', Task PC: ' + hex(i.context.pc))
            # for j in i.context:
            #     print(j)

class freertos_switch_task(gdb.Command):
    def __init__(self, rtos):
        super(freertos_switch_task, self).__init__("freertos_switch_task", gdb.COMMAND_DATA)
        self.freertos = rtos

    def invoke(self, arg, from_tty):
        task_no = int(arg, 10)
        for thread in self.freertos.tasks:
            if task_no == thread.number:
                print('switch to '+ thread.name + ' task')
                set_context(thread)

class qemu_freertos_tasks(gdb.Command):
    def __init__(self, rtos):
        super(qemu_freertos_tasks, self).__init__("qemu_freertos_tasks", gdb.COMMAND_DATA)
        self.freertos = rtos
        self.qemu = {}

    def invoke(self, arg, from_tty):
        parameter = arg.split(' ')
        image_file = parameter[0]
        restore_cmd = parameter[1]
        # print(image_file)
        # print(restore_cmd)

        port = 1234
        for thread in self.freertos.tasks:
            self.qemu['port'] = port
            port += 1
            if thread.number == 0:
                self.qemu['device'] = None
                self.qemu['inferior'] = '1'
                if thread.status.find('exception') >= 0:
                    gdb.execute('thread name '+thread.status[thread.status.find('exception'):], from_tty=False, to_string=True)
                else:
                    gdb.execute('thread name '+thread.name, from_tty=False, to_string=True)
            else:
                self.qemu['device'] = qemu_start_arm_cpu(self.qemu['port'])
                self.qemu['inferior'] = gdb_create_new_inferior(self.qemu['port'], image_file)
                gdb.execute('source -v '+restore_cmd, from_tty=False, to_string=True)
                set_context(thread)
                gdb.execute('thread name '+thread.name, from_tty=False, to_string=True)
        out = gdb.execute('inferior 1', from_tty=False, to_string=True)
        # print(out)

class freertos_heap_check(gdb.Command):
    def __init__(self, rtos):
        super(freertos_heap_check, self).__init__("freertos_heap_check", gdb.COMMAND_DATA)
        self.freertos = rtos

    def invoke(self, arg, from_tty):
        task_no = int(arg, 10)
        for thread in self.freertos.tasks:
            if task_no == thread.number:
                print('switch to '+ thread.name + ' task')
                set_context(thread)
#----------------------        Class Area End     ------------------------------

#----------------------        Main Area          ------------------------------
rtos = freertos()
freertos_check_tasks(rtos)
freertos_switch_task(rtos)
# qemu_freertos_tasks(rtos)
# freertos_heap_check(rtos)
#----------------------        Main Area End      ------------------------------
