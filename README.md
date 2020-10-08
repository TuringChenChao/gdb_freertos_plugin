# gdb_freertos_plugin
This repo is for freertos plugin in GDB

## How to use it?
'''
source -v freertos.py
{"token":35,"outOfBandRecord":[],"resultRecords":{"resultClass":"done","results":[]}}
freertos_check_tasks
No:0, Task Name: IDLE, '\000' <repeats 11 times>, Task Status: running, Task TCB: 0x20001e10, Task PC: 0x8002dca
No:1, Task Name: vTaskLED4\000\000\000\000\000\000, Task Status: delayed, Task TCB: 0x20001ba0, Task PC: 0x8001c30
No:2, Task Name: vTaskLED3\000\000\000\000\000\000, Task Status: delayed, Task TCB: 0x20001330, Task PC: 0x8001c30
No:3, Task Name: Tmr Svc\000\000\000\000\000\000\000\000, Task Status: suspended, Task TCB: 0x20002358, Task PC: 0x8003d4c
{"token":42,"outOfBandRecord":[],"resultRecords":{"resultClass":"done","results":[]}}
freertos_switch_task 2
switch to vTaskLED3\000\000\000\000\000\000 task
{"token":49,"outOfBandRecord":[],"resultRecords":{"resultClass":"done","results":[]}}
bt
#0  vTaskDelay (xTicksToDelay=250) at FreeRTOS/tasks.c:981
#1  0x08000552 in vTaskLED3 (pvParameters=0x0) at src/main.c:278
#2  0x08004210 in pxPortInitialiseStack (pxTopOfStack=0x0, pxCode=0xa5a5a5a5, pvParameters=0x8000553 <vTaskLED3+26>) at FreeRTOS/portable/GCC/ARM_CM4F/port.c:253
Backtrace stopped: previous frame identical to this frame (corrupt stack?)
{"token":61,"outOfBandRecord":[],"resultRecords":{"resultClass":"done","results":[]}}
'''
