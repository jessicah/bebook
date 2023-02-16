# Kernel Functions

The kernel exports a number of functions that device drivers can call. The
device driver accesses these functions directly in the kernel, not through
a library.

Remember, when writing a driver that calls one of these functions, to link
against _KERNEL_. This will instruct the loader to dynamically locate the
symbols in the current kernel when the driver is loaded.

## acquire_spinlock(), release_spinlock(), spinlock











:::{code} c
typedef vlong spinlock
:::

Declared in: drivers/KernelExport.h

Spinlocks are mutually exclusive locks that are used to protect sections
of code that must execute atomically. Unlike semaphores, spinlocks can be
safely used when interrupts are disabled (in fact, you must have interrupts
disabled).

To create a spinlock, simply declare a spinlock variable and initialize it
0:

:::{code} c
spinlock lock = 0;
:::

The functions acquire and release the lock spinlock. When you acquire and
release a spinlock, you must have interrupts disabled; the structure of
your code will look like this:

:::{code} c
cpu_status former = disable_interrupts();
acquire_spinlock(&lock);

/* critical section goes here*/

release_spinlock(&lock);
restore_interrupts(former);
:::

The spinlock should be held as briefly as possible, and acquisition must
not be nested within the critical section.

Spinlocks are designed for use in a multi-processor system (on a single
processor system simply turning off interrupts is enough to guarantee that
the critical section will be atomic). Nonetheless, you can use spinlocks on
a single processor—you don't have to predicate your code based on the
number of CPUs in the system.

## add_timer(), cancel_timer(), timer_hook, qent, timer















:::{code} c
typedef int32 (*timer_hook)(timer*)
:::

:::{code} c
struct quent {
    int64 key;
    qent* next;
    qent* prev;
}
:::

:::{code} c
struct timer {
    qent   entry;
    uint16   flags;
    uint16   cpu;
    timer_hook hook;
    bigtime_t   period;
}
:::

Declared in: drivers/KernelExport.h

add_timer() installs a new timer interrupt. A timer interrupt causes the
specified {hparam}`hookFunction` to be called when the desired amount of
time has passed. On entry, you should pass a pointer to a {htype}`timer`
structure in {hparam}`theTimer`; this will be filled out with data
describing the new timer interrupt you've installed. The {hparam}`flags`
argument provides control over how the timer functions, which affects the
meaning of the {hparam}`period` argument as follows:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Constant

	- Description

-
	- {cpp:enumerator}`B_ONE_SHOT_ABSOLUTE_TIMER`
	- The timer will fire once at the system time specified by {hparam}`period`.
-
	- {cpp:enumerator}`B_ONE_SHOT_RELATIVE_TIMER`
	- The timer will fire once in approximately {hparam}`period` microseconds.
-
	- {cpp:enumerator}`B_PERIODIC_TIMER`
	- The timer will fire every {hparam}`period` microseconds, starting in
		{hparam}`period` microseconds.

:::

cancel_timer() cancels the specified timer. If it's already fired, it
returns {cpp:expr}`true`; otherwise {cpp:expr}`false` is returned. It's
guaranteed that once cancel_timer() returns, if the timer was in the
process of running when cancel_timer() was called, the timer function will
be finished executing. The only exception to this is if cancel_timer() was
called from inside a timer handler (in which case trying to wait for the
handler to finish running would result in deadlock).

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`B_OK`.
	- The timer was installed (add_timer() only).
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- The timer couldn't be installed because the period was invalid (probably
		because a relative time or period was negative; unfortunately, Be hasn't
		mastered the intricacies of installing timers to fire in the past).

:::

## call_all_cpus()





Declared in: drivers/KernelExport.h

Calls the function specified by {hparam}`func` on all CPUs. The
{hparam}`cookie` can be anything your needs require.

## disable_interrupts(), restore_interrupts(), cpu_status











:::{code} c
typedef ulong cpu_status
:::

Declared in:  drivers/KernelExport.h

These functions disable and restore interrupts on the CPU that the caller
is currently running on. disable_interrupts() returns its previous state
(i.e. whether or not interrupts were already disabled).
restore_interrupts() restores the previous status of the CPU, which should
be the value that disable_interrupts() returned:

:::{code} c
cpu_status former = disable_interrupts();
...
restore_interrupts(former);
:::

As long as the CPU state is properly restored (as shown here), the
disable/restore functions can be nested.

See also: {ref}`install_io_interrupt_handler()`

## dprintf(), set_dprintf_enabled(), panic()













Declared in: drivers/KernelExport.h

dprintf() is a debugging function that has the same syntax and behavior as
standard C printf(), except that it writes its output to the serial port at
a data rate of 19,200 bits per second. The output is sent to
/dev/ports/serial4 on BeBoxes, /dev/modem on Macs, and /dev/ports/serial1
on Intel machines. By default, dprintf() is disabled.

set_dprintf_enabled() enables dprintf() if the {hparam}`enabled` flag is
{cpp:expr}`true`, and disables it if the flag is {cpp:expr}`false`. It
returns the previous enabled state, thus permitting intelligent nesting:

:::{code} c
/* Turn on dprintf */
bool former = set_dprintf_enabled(true);
...
/* Now restore it to its previous state. */
set_dprintf_enabled(former);
:::

panic() is similar to dprintf(), except it hangs the computer after
printing the message.

## get_memory_map(), physical_entry







:::{code} c
typedef struct {
    void*address;
    ulong size;
} physical_entry
:::

Declared in: drivers/KernelExport.h

Returns the physical memory chunks that map to the virtual memory that
starts at address and extends for {hparam}`numBytes`. Each chunk of
physical memory is returned as a {htype}`physical_entry` structure; the
series of structures is returned in the table array. (which you have to
allocate yourself). {hparam}`numEntries` is the number of elements in the
array that you're passing in. As shown in the example, you should lock the
memory that you're about to inspect:

:::{code} c
physical_entry table[count];
lock_memory(addr, extent, 0);
get_memory_map(addr, extent, table, count);
. . .
unlock_memory(someAddress, someNumberOfBytes, 0);
:::

The end of the table array is indicated by ({hparam}`size` == 0):

:::{code} c
long k;
while (table[k].size > 0) {
   /* A legitimate entry */
   if (++k == count) {
      /* Not enough entries */
      break; }
}
:::

If all of the entries have non-zero sizes, then table wasn't big enough;
call get_memory_map() again with more table entries.

The function always returns {cpp:enumerator}`B_OK`.

See also: {cpp:func}`lock_memory() <lock::memory>`, start_isa_dma()

## has_signals_pending()





Declared in: drivers/KernelExport.h

Returns a bitmask of the currently pending signals for the current thread.
{hparam}`thr` should always be {cpp:expr}`NULL`; passing other values will
yield meaningless results. has_signals_pending() returns 0 if no signals
are pending.

## install_io_interrupt_handler(), remove_io_interrupt_handler()









Declared in:  drivers/KernelExport.h

install_io_interrupt_handler() adds the handler function to the chain of
functions that will be called each time the specified interrupt occurs.
This function should have the following syntax:

:::{code} c
int32 handler(void*data)
:::

The data passed to install_io_interrupt_handler() will be passed to the
handler function each time it's called. It can be anything that might be of
use to the {hparam}`handler`, or {cpp:expr}`NULL`. If the interrupt handler
must return one of the following values:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Constant

	- Description

-
	- {cpp:enumerator}`B_UNHANDLED_INTERRUPT`
	- The interrupt handler didn't handle the interrupt; the kernel will keep
		looking for someone to handle it.
-
	- {cpp:enumerator}`B_HANDLED_INTERRUPT`
	- The interrupt handler handled the interrupt. The kernel won't keep looking
		for a handler to handle it.
-
	- {cpp:enumerator}`B_INVOKE_SCHEDULER`
	- The interrupt handler handled the interrupt. This tells the kernel to
		invoke the scheduler immediately after the handler returns.

:::

If {cpp:enumerator}`B_INVOKE_SCHEDULER` is returned by the interrupt
handler, the kernel will immediately invoke the scheduler, to dispatch
processor time to tasks that need handling. This is especially useful if
your interrupt handler has released a semaphore (see
{ref}`release_sem_etc()` in the Kernel Kit).

The {hparam}`flags` parameter is a bitmask of options. The only option
currently defined is {cpp:enumerator}`B_NO_ENABLE_COUNTER`. By default, the
OS keeps track of the number of functions handling a given interrupt. If
this counter changes from 0 to 1, then the system enables the irq for that
interrupt. Conversely, if the counter changes from 1 to 0, the system
disables the irq. Setting the {cpp:enumerator}`B_NO_ENABLE_COUNTER` flag
instructs the OS to ignore the handler for the purpose of enabling and
disabling the irq.

install_io_interrupt_handler() returns {cpp:enumerator}`B_OK` if
successful in installing the handler, and {cpp:enumerator}`B_ERROR` if not.
An error occurs when either the {hparam}`interrupt_number` is out of range
or there is not enough room left in the interrupt chain to add the handler.

remove_io_interrupt() removes the named interrupt from the interrupt
chain. It returns {cpp:enumerator}`B_OK` if successful in removing the
handler, and {cpp:enumerator}`B_ERROR` if not.

## kernel_debugger(), add_debugger_command(), remove_debugger_command(), load_driver_symbols(), kprintf(), parse_expression()

























Declared in: drivers/KernelExport.h

kernel_debugger() drops the calling thread into a debugger that writes its
output to the serial port at 19,200 bits per second, just as
{ref}`dprintf()` does. This debugger produces string as its first message;
it's not affected by {ref}`set_dprintf_enabled()`.

kernel_debugger() is identical to the {ref}`debugger()` function
documented in the Kernel Kit, except that it works in the kernel and
engages a different debugger. Drivers should use it instead of
{ref}`debugger()`.

add_debugger_command() registers a new command with the kernel debugger.
When the user types in the command name, the kernel debugger calls
{hparam}`func` with the remainder of the command line as
{hparam}`argc`/{hparam}`argv`-style arguments. The {hparam}`help` string
for the command is set to help.

remove_debugger_command() removes the specified kernel debugger command.

load_driver_symbols() loads symbols from the specified kernel driver into
the kernel debugger. {hparam}`driver_name` is the path-less name of the
driver which must be located in one of the standard kernel driver
directories. The function returns {cpp:enumerator}`B_OK` on success and
{cpp:enumerator}`B_ERROR` on failure.

kprintf() outputs messages to the serial port. It should be used instead
of {ref}`dprintf()` from new debugger commands because {ref}`dprintf()`
depends too much upon the state of the kernel to be reliable from within
the debugger.

parse_expression() takes a C expression and returns the result. It only
handles integer arithmetic. The logical and relational operations are
accepted. It can also supports variables and assignments. This is useful
for strings with multiple expressions, which should be separated with
semicolons. Finally, the special variable "." refers to the value from the
previous expression. This function is designed to help implement new
debugger commands.

## lock_memory(), unlock_memory()









Declared in: drivers/KernelExport.h

lock_memory() makes sure that all the memory beginning at the specified
virtual {hparam}`address` and extending for {hparam}`numBytes` is resident
in RAM, and locks it so that it won't be paged out until unlock_memory() is
called. It pages in any of the memory that isn't resident at the time it's
called. It is typically used in preparation for a DMA transaction.

The {hparam}`flags` field contains a bitmask of options. Currently, two
options, {cpp:enumerator}`B_DMA_IO` and {cpp:enumerator}`B_READ_DEVICE`,
are defined. {cpp:enumerator}`B_DMA_IO` should be set if any part of the
memory range will be modified by something other than the CPU while it's
locked, since that change won't otherwise be noticed by the system and the
modified pages may not be written to disk by the virtual memory system.
Typically, this sort of change is performed through DMA.
{cpp:enumerator}`B_READ_DEVICE`, if set, indicates that the caller intends
to fill the memory (read from the device). If cleared, it indicates the
memory will be written to the device and will not be altered.

unlock_memory() releases locked memory and should be called with the same
flags as passed into the corresponding lock_memory() call.

Each of these functions returns {cpp:enumerator}`B_OK` if successful and
{cpp:enumerator}`B_ERROR` if not. The main reason that lock_memory() would
fail is that you're attempting to lock more memory than can be paged in.

## map_physical_memory()





Declared in: drivers/KernelExport.h

This function allows you to map the memory in physical memory starting at
{hparam}`physicalAddress` and extending for {hparam}`numBytes` bytes into
your team's address space. The kernel creates an area named
{hparam}`areaName` mapped into the memory address {hparam}`virtualAddress`
and returns its {htype}`area_id` to the caller. {hparam}`numBytes` must be
a multiple of {cpp:enumerator}`B_PAGE_SIZE` (4096).

{hparam}`spec` must be either {cpp:enumerator}`B_ANY_KERNEL_ADDRESS` or
{cpp:enumerator}`B_ANY_KERNEL_BLOCK_ADDRESS`. If {hparam}`spec` is
{cpp:enumerator}`B_ANY_KERNEL_ADDRESS`, the memory will begin at an
arbitrary location in the kernel address space. If spec is
{cpp:enumerator}`B_ANY_KERNEL_BLOCK_ADDRESS`, then the memory will be
mapped into a memory location aligned on a multiple of
{cpp:enumerator}`B_PAGE_SIZE`.

{hparam}`protection` is a bitmask consisting of the fields
{cpp:enumerator}`B_READ_AREA` and {cpp:enumerator}`B_WRITE_AREA`, as
discussed in {cpp:func}`create_area() <create::area>`.

{cpp:func}`create_area() <create::area>` returns an {htype}`area_id` for
the newly-created memory if successful or an error code on failure. The
error codes are the same as those for {cpp:func}`create_area()
<create::area>`.

## motherboard_version(), io_card_version()









Declared in: drivers/KernelExport.h

These functions return the current versions of the motherboard and of the
I/O card. These functions are only available on PowerPC-based systems
(they're intended for use on the BeBox).

## platform()





Declared in: drivers/KernelExport.h

Returns the current platform, as defined in kernel/OS.h.

## register_kernel_daemon(), unregister_kernel_daemon()









Declared in: drivers/KernelExport.h

Adds or removes daemons from the kernel. A kernel daemon function is
executed approximately once every {hparam}`freq`/10 seconds. The kernel
calls {hparam}`func` with the arguments {hparam}`arg` and an iteration
value that increases by {hparam}`freq` on successive calls to the daemon
function.

## send_signal_etc()





Declared in: drivers/KernelExport.h

This function is a counterpart to send_signal() in the Posix layer, which
is not exported for drivers.

{hparam}`thid` is the {htype}`thread_id` of the thread the signal should
be sent to, and {hparam}`sig` is the signal type to send, just like in
send_signal(). The {hparam}`flags` argument can be used to specify flags to
control the function:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Constant

	- Description

-
	- {cpp:enumerator}`B_CHECK_PERMISSION`
	- The signal will only be sent if the destination thread's uid and euid are
		the same as the caller's.
-
	- {cpp:enumerator}`B_DO_NOT_RESCHEDULE`
	- The kernel won't call the scheduler after sending the signal. You should
		specify this flag when calling send_signal_etc() from an interrupt handler.

:::

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`B_OK`.
	- The signal was sent.
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- The signal type is invalid.
-
	- {cpp:enumerator}`B_BAD_THREAD_ID`.
	- The thread ID is invalid.
-
	- {cpp:enumerator}`B_NOT_ALLOWED`.
	- The permission check failed (if {cpp:enumerator}`B_CHECK_PERMISSION` was
		specified).

:::

## spawn_kernel_thread()





Declared in:  drivers/KernelExport.h

This function is a counterpart to {cpp:func}`spawn_thread()
<spawn::thread>` in the Kernel Kit, which is not exported for drivers. It
has the same syntax as the Kernel Kit function, but is able to spawn
threads in the kernel's memory space.

## spin()





Declared in:  drivers/KernelExport.h

Executes a delay loop lasting at least the specified number of
microseconds. It could last longer, due to rounding errors, interrupts, and
context switches.
