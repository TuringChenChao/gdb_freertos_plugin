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

def get_word_value_by_address(address):
    if type(address) == int:
        address = hex(address)
        out = gdb.execute("x/1xw "+address, from_tty=False, to_string=True)
    else:
        out = gdb.execute("x/1xw "+address, from_tty=False, to_string=True)
    out = out.replace('~', '').replace('\"', '').replace('\\n', '')
    result = GetAllStrListInText(out, address+r'\s+.*:\s+(0x[0-9a-fA-F]{1,8})')
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
    gdb.execute('set $r0  = '+ str(thread.context.r0), from_tty=False, to_string=True)
    gdb.execute('set $r1  = '+ str(thread.context.r1), from_tty=False, to_string=True)
    gdb.execute('set $r2  = '+ str(thread.context.r2), from_tty=False, to_string=True)
    gdb.execute('set $r3  = '+ str(thread.context.r3), from_tty=False, to_string=True)
    gdb.execute('set $r4  = '+ str(thread.context.r4), from_tty=False, to_string=True)
    gdb.execute('set $r5  = '+ str(thread.context.r5), from_tty=False, to_string=True)
    gdb.execute('set $r6  = '+ str(thread.context.r6), from_tty=False, to_string=True)
    gdb.execute('set $r7  = '+ str(thread.context.r7), from_tty=False, to_string=True)
    gdb.execute('set $r8  = '+ str(thread.context.r8), from_tty=False, to_string=True)
    gdb.execute('set $r9  = '+ str(thread.context.r9), from_tty=False, to_string=True)
    gdb.execute('set $r10 = '+ str(thread.context.r10), from_tty=False, to_string=True)
    gdb.execute('set $r11 = '+ str(thread.context.r11), from_tty=False, to_string=True)
    gdb.execute('set $r12 = '+ str(thread.context.r12), from_tty=False, to_string=True)
    gdb.execute('set $sp  = '+ str(thread.context.sp), from_tty=False, to_string=True)
    gdb.execute('set $lr  = '+ str(thread.context.lr), from_tty=False, to_string=True)
    gdb.execute('set $pc  = '+ str(thread.context.pc), from_tty=False, to_string=True)
    gdb.execute('set $fpscr = 0x0', from_tty=False, to_string=True)

def exception_change_to_lastest_frame():
    out = gdb.execute('bt -1', from_tty=False, to_string=True)
    out = out.replace('~', '').replace('\"', '').replace('\\n', '')
    depth = GetAllStrListInText(out, r'#([0-9]+)\s+')
    depth = int(depth[0], 10)
    # print(depth)
    gdb.execute('select-frame '+str(depth), from_tty=False, to_string=True)
#----------------------        Functions Area End ------------------------------


#----------------------        Class Area         ------------------------------
class freertos():
    def __init__(self):
        self.tasks = []

class arm_context():
    def __init__(self):
        self.r0   = 0
        self.r1   = 0
        self.r2   = 0
        self.r3   = 0
        self.r4   = 0
        self.r5   = 0
        self.r6   = 0
        self.r7   = 0
        self.r8   = 0
        self.r9   = 0
        self.r10  = 0
        self.r11  = 0
        self.r12  = 0
        self.sp   = 0
        self.lr   = 0
        self.pc   = 0

class freertos_thread():
    """
    docstring
    """
    def __init__(self):
        self.number = 0
        self.name = ''
        self.status = ''
        self.context = arm_context()
        self.tcb = 0

class freertos_check_tasks(gdb.Command):
    def __init__(self, rtos):
        super(freertos_check_tasks, self).__init__("freertos_check_tasks", gdb.COMMAND_DATA)
        self.freertos = rtos
        self.check_done = False

    def invoke(self, arg, from_tty):
        if self.check_done == False:
            total_task_number = 0

            # get current thread info
            current_thread = freertos_thread()
            current_thread.number = total_task_number
            current_thread.status = 'running'
            current_thread.name = get_thread_name('pxCurrentTCB')
            current_thread.tcb = get_value_by_name('pxCurrentTCB')
            xpsr = get_value_by_name('$xPSR')
            # handler mode
            if (xpsr & 0xf) != 0:
                # exception callstack
                current_thread.status = 'running, but interrupted by exception ' + str(xpsr & 0xf)
                current_thread.context.r0  = get_value_by_name('$r0')
                current_thread.context.r1  = get_value_by_name('$r1')
                current_thread.context.r2  = get_value_by_name('$r2')
                current_thread.context.r3  = get_value_by_name('$r3')
                current_thread.context.r4  = get_value_by_name('$r4')
                current_thread.context.r5  = get_value_by_name('$r5')
                current_thread.context.r6  = get_value_by_name('$r6')
                current_thread.context.r7  = get_value_by_name('$r7')
                current_thread.context.r8  = get_value_by_name('$r8')
                current_thread.context.r9  = get_value_by_name('$r9')
                current_thread.context.r10 = get_value_by_name('$r10')
                current_thread.context.r11 = get_value_by_name('$r11')
                current_thread.context.r12 = get_value_by_name('$r12')
                current_thread.context.sp  = get_value_by_name('$sp')
                current_thread.context.lr  = get_value_by_name('$lr')
                current_thread.context.pc  = get_value_by_name('$pc')
                self.freertos.tasks.append(copy.deepcopy(current_thread))
                total_task_number += 1

                # thread callstack
                current_thread.number = total_task_number
                current_thread.status = 'running'
                # get context from psp
                psp = get_value_by_name('$psp')
                current_thread.context.r0  = get_word_value_by_address(psp+0)
                current_thread.context.r1  = get_word_value_by_address(psp+4)
                current_thread.context.r2  = get_word_value_by_address(psp+8)
                current_thread.context.r3  = get_word_value_by_address(psp+12)
                current_thread.context.r12 = get_word_value_by_address(psp+16)
                current_thread.context.lr  = get_word_value_by_address(psp+20)
                current_thread.context.pc  = get_word_value_by_address(psp+24)
                xpsr  = get_word_value_by_address(psp+28)
                if (xpsr & 0x200) == 0:
                    # not 8B aligned
                    current_thread.context.sp  = psp+32
                else:
                    current_thread.context.sp  = psp+32+4
                # change frame to the lastest one
                exception_change_to_lastest_frame()
                # untrusted values
                current_thread.context.r4  = get_value_by_name('$r4')
                current_thread.context.r5  = get_value_by_name('$r5')
                current_thread.context.r6  = get_value_by_name('$r6')
                current_thread.context.r7  = get_value_by_name('$r7')
                current_thread.context.r8  = get_value_by_name('$r8')
                current_thread.context.r9  = get_value_by_name('$r9')
                current_thread.context.r10 = get_value_by_name('$r10')
                current_thread.context.r11 = get_value_by_name('$r11')
                exec_return = get_value_by_name('$lr')
                # print(hex(exec_return))
                if (exec_return & 0x10) != 0:
                    #do not use FPU
                    current_thread.context.sp = current_thread.context.sp
                else:
                    #do use FPUs
                    current_thread.context.sp += 17*4
                self.freertos.tasks.append(copy.deepcopy(current_thread))
                total_task_number += 1
            # thread mode
            else:
                current_thread.context.r0  = get_value_by_name('$r0')
                current_thread.context.r1  = get_value_by_name('$r1')
                current_thread.context.r2  = get_value_by_name('$r2')
                current_thread.context.r3  = get_value_by_name('$r3')
                current_thread.context.r4  = get_value_by_name('$r4')
                current_thread.context.r5  = get_value_by_name('$r5')
                current_thread.context.r6  = get_value_by_name('$r6')
                current_thread.context.r7  = get_value_by_name('$r7')
                current_thread.context.r8  = get_value_by_name('$r8')
                current_thread.context.r9  = get_value_by_name('$r9')
                current_thread.context.r10 = get_value_by_name('$r10')
                current_thread.context.r11 = get_value_by_name('$r11')
                current_thread.context.r12 = get_value_by_name('$r12')
                current_thread.context.sp  = get_value_by_name('$sp')
                current_thread.context.lr  = get_value_by_name('$lr')
                current_thread.context.pc  = get_value_by_name('$pc')
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
                            thread.tcb = get_value_by_name('(pxReadyTasksLists['+str(i)+']).xListEnd.pxNext') - 4
                        else:
                            thread.tcb = get_value_by_name('(pxReadyTasksLists['+str(i)+']).xListEnd.pxNext'+'->pxNext'*j) - 4
                        if thread.tcb == current_thread.tcb:
                            # if the ready task is the current task, do nothing
                            # print('(pxReadyTasksLists['+str(i)+']) ' + str(j))
                            continue
                        thread.name = get_thread_name(thread.tcb)
                        topofstack = get_value_by_name('((TCB_t *)'+str(thread.tcb)+')->pxTopOfStack')
                        thread.context.r4  = get_word_value_by_address(topofstack+0)
                        thread.context.r5  = get_word_value_by_address(topofstack+4)
                        thread.context.r6  = get_word_value_by_address(topofstack+8)
                        thread.context.r7  = get_word_value_by_address(topofstack+12)
                        thread.context.r8  = get_word_value_by_address(topofstack+16)
                        thread.context.r9  = get_word_value_by_address(topofstack+20)
                        thread.context.r10 = get_word_value_by_address(topofstack+24)
                        thread.context.r11 = get_word_value_by_address(topofstack+28)
                        exec_return = get_word_value_by_address(topofstack+32)
                        if (exec_return & 0x10) != 0:
                            # do not use FPU
                            thread.context.r0  = get_word_value_by_address(topofstack+36)
                            thread.context.r1  = get_word_value_by_address(topofstack+40)
                            thread.context.r2  = get_word_value_by_address(topofstack+44)
                            thread.context.r3  = get_word_value_by_address(topofstack+48)
                            thread.context.r12 = get_word_value_by_address(topofstack+52)
                            thread.context.lr  = get_word_value_by_address(topofstack+56)
                            thread.context.pc  = get_word_value_by_address(topofstack+60)
                            xpsr = get_word_value_by_address(topofstack+64)
                            if (xpsr & 0x200) == 0:
                                # not 8B aligned
                                thread.context.sp  = topofstack+68
                            else:
                                thread.context.sp  = topofstack+68+4
                        else:
                            # do use FPU
                            thread.context.r0  = get_word_value_by_address(topofstack+16*4+36)
                            thread.context.r1  = get_word_value_by_address(topofstack+16*4+40)
                            thread.context.r2  = get_word_value_by_address(topofstack+16*4+44)
                            thread.context.r3  = get_word_value_by_address(topofstack+16*4+48)
                            thread.context.r12 = get_word_value_by_address(topofstack+16*4+52)
                            thread.context.lr  = get_word_value_by_address(topofstack+16*4+56)
                            thread.context.pc  = get_word_value_by_address(topofstack+16*4+60)
                            xpsr = get_word_value_by_address(topofstack+16*4+64)
                            if (xpsr & 0x200) == 0:
                                # not 8B aligned
                                thread.context.sp  = topofstack+68+33*4
                            else:
                                thread.context.sp  = topofstack+68+4+33*4
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
                        thread.tcb = get_value_by_name('(*pxDelayedTaskList)->xListEnd.pxNext') - 4
                    else:
                        thread.tcb = get_value_by_name('(*pxDelayedTaskList)->xListEnd.pxNext'+'->pxNext'*i) - 4
                    thread.name = get_thread_name(thread.tcb)
                    topofstack = get_value_by_name('((TCB_t *)'+str(thread.tcb)+')->pxTopOfStack')
                    thread.context.r4  = get_word_value_by_address(topofstack+0)
                    thread.context.r5  = get_word_value_by_address(topofstack+4)
                    thread.context.r6  = get_word_value_by_address(topofstack+8)
                    thread.context.r7  = get_word_value_by_address(topofstack+12)
                    thread.context.r8  = get_word_value_by_address(topofstack+16)
                    thread.context.r9  = get_word_value_by_address(topofstack+20)
                    thread.context.r10 = get_word_value_by_address(topofstack+24)
                    thread.context.r11 = get_word_value_by_address(topofstack+28)
                    exec_return = get_word_value_by_address(topofstack+32)
                    if (exec_return & 0x10) != 0:
                        # do not use FPU
                        thread.context.r0  = get_word_value_by_address(topofstack+36)
                        thread.context.r1  = get_word_value_by_address(topofstack+40)
                        thread.context.r2  = get_word_value_by_address(topofstack+44)
                        thread.context.r3  = get_word_value_by_address(topofstack+48)
                        thread.context.r12 = get_word_value_by_address(topofstack+52)
                        thread.context.lr  = get_word_value_by_address(topofstack+56)
                        thread.context.pc  = get_word_value_by_address(topofstack+60)
                        xpsr = get_word_value_by_address(topofstack+64)
                        if (xpsr & 0x200) == 0:
                            # not 8B aligned
                            thread.context.sp  = topofstack+68
                        else:
                            thread.context.sp  = topofstack+68+4
                    else:
                        # do use FPU
                        thread.context.r0  = get_word_value_by_address(topofstack+16*4+36)
                        thread.context.r1  = get_word_value_by_address(topofstack+16*4+40)
                        thread.context.r2  = get_word_value_by_address(topofstack+16*4+44)
                        thread.context.r3  = get_word_value_by_address(topofstack+16*4+48)
                        thread.context.r12 = get_word_value_by_address(topofstack+16*4+52)
                        thread.context.lr  = get_word_value_by_address(topofstack+16*4+56)
                        thread.context.pc  = get_word_value_by_address(topofstack+16*4+60)
                        xpsr = get_word_value_by_address(topofstack+16*4+64)
                        if (xpsr & 0x200) == 0:
                            # not 8B aligned
                            thread.context.sp  = topofstack+68+33*4
                        else:
                            thread.context.sp  = topofstack+68+4+33*4
                    self.freertos.tasks.append(copy.deepcopy(thread))
                    total_task_number += 1
            delayed_task_no = get_value_by_name('(*pxOverflowDelayedTaskList)->uxNumberOfItems')
            if delayed_task_no != 0:
                for i in range(delayed_task_no):
                    thread = freertos_thread()
                    thread.number = total_task_number
                    thread.status = 'delayed'
                    if i == 0:
                        thread.tcb = get_value_by_name('(*pxOverflowDelayedTaskList)->xListEnd.pxNext') - 4
                    else:
                        thread.tcb = get_value_by_name('(*pxOverflowDelayedTaskList)->xListEnd.pxNext'+'->pxNext'*i) - 4
                    thread.name = get_thread_name(thread.tcb)
                    topofstack = get_value_by_name('((TCB_t *)'+str(thread.tcb)+')->pxTopOfStack')
                    thread.context.r4  = get_word_value_by_address(topofstack+0)
                    thread.context.r5  = get_word_value_by_address(topofstack+4)
                    thread.context.r6  = get_word_value_by_address(topofstack+8)
                    thread.context.r7  = get_word_value_by_address(topofstack+12)
                    thread.context.r8  = get_word_value_by_address(topofstack+16)
                    thread.context.r9  = get_word_value_by_address(topofstack+20)
                    thread.context.r10 = get_word_value_by_address(topofstack+24)
                    thread.context.r11 = get_word_value_by_address(topofstack+28)
                    exec_return = get_word_value_by_address(topofstack+32)
                    if (exec_return & 0x10) != 0:
                        # do not use FPU
                        thread.context.r0  = get_word_value_by_address(topofstack+36)
                        thread.context.r1  = get_word_value_by_address(topofstack+40)
                        thread.context.r2  = get_word_value_by_address(topofstack+44)
                        thread.context.r3  = get_word_value_by_address(topofstack+48)
                        thread.context.r12 = get_word_value_by_address(topofstack+52)
                        thread.context.lr  = get_word_value_by_address(topofstack+56)
                        thread.context.pc  = get_word_value_by_address(topofstack+60)
                        xpsr = get_word_value_by_address(topofstack+64)
                        if (xpsr & 0x200) == 0:
                            # not 8B aligned
                            thread.context.sp  = topofstack+68
                        else:
                            thread.context.sp  = topofstack+68+4
                    else:
                        # do use FPU
                        thread.context.r0  = get_word_value_by_address(topofstack+16*4+36)
                        thread.context.r1  = get_word_value_by_address(topofstack+16*4+40)
                        thread.context.r2  = get_word_value_by_address(topofstack+16*4+44)
                        thread.context.r3  = get_word_value_by_address(topofstack+16*4+48)
                        thread.context.r12 = get_word_value_by_address(topofstack+16*4+52)
                        thread.context.lr  = get_word_value_by_address(topofstack+16*4+56)
                        thread.context.pc  = get_word_value_by_address(topofstack+16*4+60)
                        xpsr = get_word_value_by_address(topofstack+16*4+64)
                        if (xpsr & 0x200) == 0:
                            # not 8B aligned
                            thread.context.sp  = topofstack+68+33*4
                        else:
                            thread.context.sp  = topofstack+68+4+33*4
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
                        thread.tcb = get_value_by_name('(xSuspendedTaskList).xListEnd.pxNext') - 4
                    else:
                        thread.tcb = get_value_by_name('(xSuspendedTaskList).xListEnd.pxNext'+'->pxNext'*i) - 4
                    thread.name = get_thread_name(thread.tcb)
                    topofstack = get_value_by_name('((TCB_t *)'+str(thread.tcb)+')->pxTopOfStack')
                    thread.context.r4  = get_word_value_by_address(topofstack+0)
                    thread.context.r5  = get_word_value_by_address(topofstack+4)
                    thread.context.r6  = get_word_value_by_address(topofstack+8)
                    thread.context.r7  = get_word_value_by_address(topofstack+12)
                    thread.context.r8  = get_word_value_by_address(topofstack+16)
                    thread.context.r9  = get_word_value_by_address(topofstack+20)
                    thread.context.r10 = get_word_value_by_address(topofstack+24)
                    thread.context.r11 = get_word_value_by_address(topofstack+28)
                    exec_return = get_word_value_by_address(topofstack+32)
                    if (exec_return & 0x10) != 0:
                        # do not use FPU
                        thread.context.r0  = get_word_value_by_address(topofstack+36)
                        thread.context.r1  = get_word_value_by_address(topofstack+40)
                        thread.context.r2  = get_word_value_by_address(topofstack+44)
                        thread.context.r3  = get_word_value_by_address(topofstack+48)
                        thread.context.r12 = get_word_value_by_address(topofstack+52)
                        thread.context.lr  = get_word_value_by_address(topofstack+56)
                        thread.context.pc  = get_word_value_by_address(topofstack+60)
                        xpsr = get_word_value_by_address(topofstack+64)
                        if (xpsr & 0x200) == 0:
                            # not 8B aligned
                            thread.context.sp  = topofstack+68
                        else:
                            thread.context.sp  = topofstack+68+4
                    else:
                        # do use FPU
                        thread.context.r0  = get_word_value_by_address(topofstack+16*4+36)
                        thread.context.r1  = get_word_value_by_address(topofstack+16*4+40)
                        thread.context.r2  = get_word_value_by_address(topofstack+16*4+44)
                        thread.context.r3  = get_word_value_by_address(topofstack+16*4+48)
                        thread.context.r12 = get_word_value_by_address(topofstack+16*4+52)
                        thread.context.lr  = get_word_value_by_address(topofstack+16*4+56)
                        thread.context.pc  = get_word_value_by_address(topofstack+16*4+60)
                        xpsr = get_word_value_by_address(topofstack+16*4+64)
                        if (xpsr & 0x200) == 0:
                            # not 8B aligned
                            thread.context.sp  = topofstack+68+33*4
                        else:
                            thread.context.sp  = topofstack+68+4+33*4
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
                        thread.tcb = get_value_by_name('(xPendingReadyList).xListEnd.pxNext') - 4
                    else:
                        thread.tcb = get_value_by_name('(xPendingReadyList).xListEnd.pxNext'+'->pxNext'*i) - 4
                    thread.name = get_thread_name(thread.tcb)
                    topofstack = get_value_by_name('((TCB_t *)'+str(thread.tcb)+')->pxTopOfStack')
                    thread.context.r4  = get_word_value_by_address(topofstack+0)
                    thread.context.r5  = get_word_value_by_address(topofstack+4)
                    thread.context.r6  = get_word_value_by_address(topofstack+8)
                    thread.context.r7  = get_word_value_by_address(topofstack+12)
                    thread.context.r8  = get_word_value_by_address(topofstack+16)
                    thread.context.r9  = get_word_value_by_address(topofstack+20)
                    thread.context.r10 = get_word_value_by_address(topofstack+24)
                    thread.context.r11 = get_word_value_by_address(topofstack+28)
                    exec_return = get_word_value_by_address(topofstack+32)
                    if (exec_return & 0x10) != 0:
                        # do not use FPU
                        thread.context.r0  = get_word_value_by_address(topofstack+36)
                        thread.context.r1  = get_word_value_by_address(topofstack+40)
                        thread.context.r2  = get_word_value_by_address(topofstack+44)
                        thread.context.r3  = get_word_value_by_address(topofstack+48)
                        thread.context.r12 = get_word_value_by_address(topofstack+52)
                        thread.context.lr  = get_word_value_by_address(topofstack+56)
                        thread.context.pc  = get_word_value_by_address(topofstack+60)
                        xpsr = get_word_value_by_address(topofstack+64)
                        if (xpsr & 0x200) == 0:
                            # not 8B aligned
                            thread.context.sp  = topofstack+68
                        else:
                            thread.context.sp  = topofstack+68+4
                    else:
                        # do use FPU
                        thread.context.r0  = get_word_value_by_address(topofstack+16*4+36)
                        thread.context.r1  = get_word_value_by_address(topofstack+16*4+40)
                        thread.context.r2  = get_word_value_by_address(topofstack+16*4+44)
                        thread.context.r3  = get_word_value_by_address(topofstack+16*4+48)
                        thread.context.r12 = get_word_value_by_address(topofstack+16*4+52)
                        thread.context.lr  = get_word_value_by_address(topofstack+16*4+56)
                        thread.context.pc  = get_word_value_by_address(topofstack+16*4+60)
                        xpsr = get_word_value_by_address(topofstack+16*4+64)
                        if (xpsr & 0x200) == 0:
                            # not 8B aligned
                            thread.context.sp  = topofstack+68+33*4
                        else:
                            thread.context.sp  = topofstack+68+4+33*4
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
                        thread.tcb = get_value_by_name('(xTasksWaitingTermination).xListEnd.pxNext') - 4
                    else:
                        thread.tcb = get_value_by_name('(xTasksWaitingTermination).xListEnd.pxNext'+'->pxNext'*i) - 4
                    thread.name = get_thread_name(thread.tcb)
                    topofstack = get_value_by_name('((TCB_t *)'+str(thread.tcb)+')->pxTopOfStack')
                    thread.context.r4  = get_word_value_by_address(topofstack+0)
                    thread.context.r5  = get_word_value_by_address(topofstack+4)
                    thread.context.r6  = get_word_value_by_address(topofstack+8)
                    thread.context.r7  = get_word_value_by_address(topofstack+12)
                    thread.context.r8  = get_word_value_by_address(topofstack+16)
                    thread.context.r9  = get_word_value_by_address(topofstack+20)
                    thread.context.r10 = get_word_value_by_address(topofstack+24)
                    thread.context.r11 = get_word_value_by_address(topofstack+28)
                    exec_return = get_word_value_by_address(topofstack+32)
                    if (exec_return & 0x10) != 0:
                        # do not use FPU
                        thread.context.r0  = get_word_value_by_address(topofstack+36)
                        thread.context.r1  = get_word_value_by_address(topofstack+40)
                        thread.context.r2  = get_word_value_by_address(topofstack+44)
                        thread.context.r3  = get_word_value_by_address(topofstack+48)
                        thread.context.r12 = get_word_value_by_address(topofstack+52)
                        thread.context.lr  = get_word_value_by_address(topofstack+56)
                        thread.context.pc  = get_word_value_by_address(topofstack+60)
                        xpsr = get_word_value_by_address(topofstack+64)
                        if (xpsr & 0x200) == 0:
                            # not 8B aligned
                            thread.context.sp  = topofstack+68
                        else:
                            thread.context.sp  = topofstack+68+4
                    else:
                        # do use FPU
                        thread.context.r0  = get_word_value_by_address(topofstack+16*4+36)
                        thread.context.r1  = get_word_value_by_address(topofstack+16*4+40)
                        thread.context.r2  = get_word_value_by_address(topofstack+16*4+44)
                        thread.context.r3  = get_word_value_by_address(topofstack+16*4+48)
                        thread.context.r12 = get_word_value_by_address(topofstack+16*4+52)
                        thread.context.lr  = get_word_value_by_address(topofstack+16*4+56)
                        thread.context.pc  = get_word_value_by_address(topofstack+16*4+60)
                        xpsr = get_word_value_by_address(topofstack+16*4+64)
                        if (xpsr & 0x200) == 0:
                            # not 8B aligned
                            thread.context.sp  = topofstack+68+33*4
                        else:
                            thread.context.sp  = topofstack+68+4+33*4
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
#----------------------        Class Area End     ------------------------------

#----------------------        Main Area          ------------------------------
rtos = freertos()
freertos_check_tasks(rtos)
freertos_switch_task(rtos)
#----------------------        Main Area End      ------------------------------
