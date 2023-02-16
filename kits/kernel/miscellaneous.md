# Miscellaneous Functions And Constants

:::{list-table}
---
header-rows: 0
align: left
widths: auto
---
-
	- Declared in:

	- kernel/OS.h

-
	- Library:

	- libroot.so


:::

## Functions

::::{abi-group}
:::{cpp:function} void clear_caches(void* addr, size_t len, uint32 flags)
:::

Declared in: kernel/image.h

This function clears or invalidates the instruction and data caches. You
should only need this function if you're generating code on the fly, or if
you're performing a timing loop and you want to start with fresh caches (to
get a "worst case" estimate).

The parameters are:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Parameter

	- Description

-
	- addr
	- Is the starting address of a section of memory that corresponds to a
		section of one of the caches.
-
	- len
	- Is the length, in bytes, of the instruction or data segment that you want
		to clear or invalidate.
-
	- flags
	- Is one or both of {cpp:enumerator}`B_INVALIDATE_ICACHE` and
		{cpp:enumerator}`B_FLUSH_DCACHE`.

:::

By invalidating a section of the instruction cache, you cause the
instructions in that section to be reloaded next time they're needed.
Flushing the data cache causes the in-memory copy of the data to be written
out to the cache.
::::

::::{abi-group}
:::{cpp:function} void debugger(const char* string)
:::

Throws the calling thread into the debugger. The {hparam}`string` argument
becomes the debugger's first utterance.
::::

::::{abi-group}
:::{cpp:function} int disable_debugger(int state)
:::

Instructs the kernel to send a signal for all exceptions, even those that
don't normally trigger the debugger. If the application doesn't have a
handler installed for the exception, the team dies without triggering the
debugger. {hparam}`state` should be nonzero to turn on this functionality
or 0 to turn it off.
::::

::::{abi-group}
:::{cpp:function} bigtime_t set_alarm(bigtime_t time, uint32 mode)
:::

Tells the kernel to send the SIGALRM signal at some point in the future,
as defined by the arguments:

-   If {hparam}`mode` is {cpp:enumerator}`B_PERIODIC_ALARM`, the signal is
sent every {hparam}`time` microseconds, starting as soon as set_alarm()
function returns.

-   If {hparam}`mode` is {cpp:enumerator}`B_ONE_SHOT_ABOLUTE_ALARM`, the
signal is sent once (only) after {hparam}`time` microseconds have elapsed
measured from the time the system was booted. If that point has already
passed, the signal is sent immediately.

-   If {hparam}`mode` is {cpp:enumerator}`B_ONE_SHOT_RELATIVE_ALARM`, the
signal is sent once (only) after {hparam}`time` microseconds have elapsed
from the time set_alarm() returns.

When the signal is sent, the SIGALRM handler is called (you set the
handler through the normal means, by calling the Posix signal() function).
The handler runs in the thread that set the alarm.

:::{admonition} Warning
:class: warning
From within the SIGALRM handler, you mustn't call anything that would
cause the kernel scheduler to run. Just about the only safe call you can
make from your signal handler is {cpp:func}`release_sem() <release::sem>`.
:::

The most recent alarm requested cancels any previous request. For example,
in this sequence…

:::{code} c
/* Ask for an alarm ten seconds from now. */
set_alarm(10e6, B_ONE_SHOT_RELATIVE_ALARM);

/* Ask for an alarm one second from now. */
set_alarm(10e5, B_ONE_SHOT_RELATIVE_ALARM);
:::

…only the second alarm request will be fulfilled the first requested is
cancelled when the second set_alarm() call is made. This applies to all
alarm types; for example, a one-shot alarm request will cancel an active
periodic alarm.

To explicitly cancel the previous alarm request without installing a new
alarm, do this:

:::{code} c
set_alarm(B_INFINITE_TIMEOUT, B_PERIODIC_ALARM);
:::

This cancels the previous alarm request regardless of the type of alarm.
::::

::::{abi-group}
:::{cpp:function} void set_signal_stack(void* ptr, size_t size)
:::

Declared in: posix/signal.be.h

Sets the location and size of the stack that's used by the thread's signal
handlers.
::::

## Constants

::::{abi-group}
:::{cpp:enumerator} B_INFINITE_TIMEOUT
:::

:::{code} c
B_INFINITE_TIMEOUT
:::

The inifinite timeout value can be used to specify, to timeout-accepting
functions, that you're willing to wait forever.
::::

::::{abi-group}
:::{cpp:enumerator} B_OS_NAME_LENGTH
:::

:::{code} c
B_OS_NAME_LENGTH
:::

This constant gives the maximum length of the name of a thread, semaphore,
port, area, or other operating system bauble.
::::

::::{abi-group}
:::{cpp:enumerator} B_PAGE_SIZE
:::

:::{code} c
B_PAGE_SIZE
:::

The {cpp:enumerator}`B_PAGE_SIZE` constant gives the size, in bytes, of a
page of RAM.
::::
