# Semaphores

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

A semaphore is a token that's used to synchronize multiple threads. The
semaphore concept is simple: To enter into a semaphore-protected "critical
section", a thread must first "acquire" the semaphore, through the
{cpp:func}`acquire_sem()` function. When it passes out of the critical
section, the thread "releases" the semaphore through
{cpp:func}`release_sem()`.

The advantage of the semaphore system is that if a thread can't acquire a
semaphore (because the semaphore is yet to be released by the previous
acquirer), the thread blocks in the {cpp:func}`acquire_sem()` call. While
it's blocked, the thread doesn't waste any cycles.

For the full story about semaphores, see "{ref}`Semaphore Overview`".

## Semaphore Functions

::::{abi-group}
:::{cpp:function} status_t acquire_sem(sem_id sem)
:::

:::{cpp:function} status_t acquire_sem_etc(sem_id sem, uint32 count, uint32 flags, bigtime_t timeout)
:::

These functions attempt to acquire the semaphore identified by the
{hparam}`sem` argument. Except in the case of an error, acquire_sem()
doesn't return until the semaphore has actually been acquired.

acquire_sem_etc() is the full-blown acquisition version: It's essentially
the same as acquire_sem(), but, in addition, it lets you acquire a
semaphore more than once, and also provides a timeout facility:

- The {hparam}`count` argument lets you specify that you want the semaphore
  to be acquired {hparam}`count` times. This means that the semaphore's
  thread count is decremented by the specified amount. It's illegal to
  specify a count that's less than 1.

- To enable the timeout, you add {cpp:enumerator}`B_ABSOLUTE_TIMEOUT` or
  {cpp:enumerator}`B_RELATIVE_TIMEOUT` to the {hparam}`flags` argument.
  {hparam}`timeout` to the amount of time, in microseconds, that you're
  willing to wait, measured relative to now (relative timeout), or in
  comparison to the value returned by {cpp:func}`system_time()` (absolute
  timeout). The function returns {cpp:enumerator}`B_TIMED_OUT` if the
  semaphore isn't acquired within the specified time. If you specify a
  relative {hparam}`timeout` of 0 and the semaphore isn't immediately
  available, the function immediately returns
  {cpp:enumerator}`B_WOULD_BLOCK`.

:::{admonition} Warning
:class: warning
The Kernel Kit defines two other semaphore-acquisition flag constants
({cpp:enumerator}`B_CAN_INTERRUPT` and
{cpp:enumerator}`B_CHECK_PERMISSION`). These additional flags are used by
device drivers—adding these flags into a "normal" (or "user-level")
acquisition has no effect. However, you should be aware that the
{cpp:enumerator}`B_CHECK_PERMISSION` flag is always added in to user-level
semaphore acquisition in order to protect system-defined semaphores.
:::

Other than the timeout and the acquisition count, there's no difference
between the two acquisition functions. Specifically, any semaphore can be
acquired through either of these functions; you always release a semaphore
through {cpp:func}`release_sem()` (or {cpp:func}`release_sem_etc()`)
regardless of which function you used to acquire it.

To determine if the semaphore is available, the function looks at the
semaphore's thread count (before decrementing it):

- If the thread count is positive, the semaphore is available and the
  current acquisition succeeds. The acquire_sem() (or acquire_sem_etc())
  function returns immediately upon acquisition.

- If the thread count is zero or less, the calling thread is placed in the
  semaphore's thread queue where it waits for a corresponding
  {cpp:func}`release_sem()` call to de-queue it (or for the timeout to
  expire).

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
	- {cpp:enumerator}`B_NO_ERROR`.
	- The semaphore was successfully acquired.

-
	- {cpp:enumerator}`B_BAD_SEM_ID`.
	- The {hparam}`sem` argument doesn't identify a valid semaphore. It's
possible for a semaphore to become invalid while an acquisitive thread is
waiting in the semaphore's queue. For example, if your thread calls
acquire_sem() on a valid (but unavailable) semaphore, and then some other
thread deletes the semaphore, your thread will return
{cpp:enumerator}`B_BAD_SEM_ID` from its call to acquire_sem().

-
	- {cpp:enumerator}`B_INTERRUPTED`.
	- The acquisition was interrupted by a signal. In this case, the semaphore
has not been acquired.


:::

The other return values apply to acquire_sem_etc() only:

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
	- {cpp:enumerator}`B_BAD_VALUE`.
	- Illegal {hparam}`count` value (less than 1).

-
	- {cpp:enumerator}`B_WOULD_BLOCK`.
	- You specified a relative {hparam}`timeout` of 0 and the semaphore isn't
available.

-
	- {cpp:enumerator}`B_TIMED_OUT`.
	- The timeout expired (for all values of {hparam}`timeout` other than 0).


:::
::::

::::{abi-group}
:::{cpp:function} sem_id create_sem(uint32 thread_count, const char * name)
:::

Creates a new semaphore and returns a system-wide {htype}`sem_id` number
that identifies it. The arguments are:

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
	- thread_count
	- Initializes the semaphore's thread count, the counting variable that's
		decremented and incremented as the semaphore is acquired and released
		(respectively). You can pass any non-negative number as the count, but you
		typically pass either 1 or 0.
-
	- name
	- Is an optional string name that you can assign to the semaphore. The name
		is meant to be used only for debugging. A semaphore's name needn't be
		unique—any number of semaphores can have the same name.

:::

Valid {htype}`sem_id` numbers are positive integers. You should always
check the validity of a new semaphore through a construction such as

:::{code} c
if ((my_sem = create_sem(1,"My Semaphore")) < B_OK)
   /* If it's less than B_NO_ERROR, my_sem is invalid. *
:::

create_sem() sets the new semaphore's owner to the team of the calling
thread. Ownership may be re-assigned through the
{cpp:func}`set_sem_owner()` function. When the owner dies (when all the
threads in the team are dead), the semaphore is automatically deleted. The
owner is also signficant in a {cpp:func}`delete_sem()` call: Only those
threads that belong to a semaphore's owner are allowed to delete that
semaphore.

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
	- {cpp:enumerator}`B_BAD_VALUE`.
	- Invalid {hparam}`thread_count` value (less than 0).
-
	- {cpp:enumerator}`B_NO_MEMORY`.
	- Not enough memory to allocate the semaphore's name.
-
	- {cpp:enumerator}`B_NO_MORE_SEMS`.
	- All valid {htype}`sem_id` numbers are being used.

:::
::::

::::{abi-group}
:::{cpp:function} status_t delete_sem(sem_id sem)
:::

Deletes the semaphore identified by the argument. If there are any threads
waiting in the semaphore's thread queue, they're immediately unblocked.

:::{admonition} Warning
:class: warning
This function may only be called from a thread that belongs to the
semaphore's owner.
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
	- {cpp:enumerator}`B_NO_ERROR`.
	- The semaphore was successfully deleted.
-
	- {cpp:enumerator}`B_BAD_SEM_ID`.
	- {hparam}`sem` is invalid, or the calling thread doesn't belong to the team
		that owns the semaphore.

:::
::::

::::{abi-group}
:::{cpp:function} status_t get_sem_count(sem_id sem, int32* thread_count)
:::

:::{admonition} Warning
:class: warning
For amusement purposes only; never predicate your code on this function.
:::

Returns, by reference in {hparam}`thread_count`, the value of the
semaphore's thread count variable:

- A positive thread count (_n_) means that there are no threads in the
  semaphore's queue, and the next _n_ {cpp:func}`acquire_sem()` calls will
  return without blocking.

- If the count is zero, there are no queued threads, but the next
  {cpp:func}`acquire_sem()` call will block.

- A negative count (-_n_) means there are _n_ threads in the semaphore's
  thread queue and the next call to {cpp:func}`acquire_sem()` will block.

By the time this function returns and you get a chance to look at the
{hparam}`thread_count` value, the semaphore's thread count may have
changed. Although watching the thread count might help you while you're
debugging your program, this function shouldn't be an integral part of the
design of your application.

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
	- {cpp:enumerator}`B_NO_ERROR`.
	- Success.
-
	- {cpp:enumerator}`B_BAD_SEM_ID`.
	- {hparam}`sem` is invalid ({hparam}`thread_count` isn't changed).

:::
::::

::::{abi-group}
:::{cpp:function} status_t get_sem_info(sem_id sem, sem_info* info)
:::

:::{cpp:function} status_t get_next_sem_info(team_id team, uint32* cookie, sem_info* info)
:::

Copies information about a particular semaphore into the {htype}`sem_info`
structure designated by {hparam}`info`. The first version of the function
designates the sempahore directly, by {htype}`sem_id`.

The get_next_sem_info() version lets you step through the list of a team's
semaphores through iterated calls on the function. The {hparam}`team`
argument identifies the team you want to look at; a {hparam}`team` value of
0 means the team of the calling thread. The {hparam}`cookie` argument is a
placemark; you set it to 0 on your first call, and let the function do the
rest. The function returns {cpp:enumerator}`B_BAD_VALUE` when there are no
more sempahores to visit:

:::{code} cpp
/* Get the sem_info for every sempahore in this team. */
sem_info info;
int32 cookie = 0;

while (get_next_sem_info(0, &cookie, &info) == B_OK)
   ...
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
	- {cpp:enumerator}`B_NO_ERROR`.
	- Success.
-
	- {cpp:enumerator}`B_BAD_SEM_ID`.
	- Invalid {hparam}`sem` value.
-
	- {cpp:enumerator}`B_BAD_TEAM_ID`.
	- Invalid {hparam}`team` value.

:::
::::

::::{abi-group}
:::{cpp:function} status_t release_sem(sem_id sem)
:::

:::{cpp:function} status_t release_sem_etc(sem_id sem, int32 count, uint32 flags)
:::

The release_sem() function de-queues the thread that's waiting at the head
of the semaphore's thread queue (if any), and increments the semaphore's
thread count. release_sem_etc() does the same, but for count threads.

Normally, releasing a semaphore automatically invokes the kernel's
scheduler. In other words, when your thread calls release_sem(), you're
pretty much guaranteed that some other thread will be switched in
immediately afterwards, even if your thread hasn't gotten its fair share of
CPU time. If you want to subvert this automatism, call release_sem_etc()
with a {hparam}`flags` value of {cpp:enumerator}`B_DO_NOT_RESCHEDULE`.
Preventing the automatic rescheduling is particularly useful if you're
releasing a number of different semaphores all in a row: By avoiding the
rescheduling you can prevent some unnecessary context switching.

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
	- {cpp:enumerator}`B_NO_ERROR`.
	- The semaphore was successfully released.
-
	- {cpp:enumerator}`B_BAD_SEM_ID`.
	- Invalid {hparam}`sem` value.
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- Invalid {hparam}`count` value (less than zero; release_sem_etc() only).

:::

See also: {cpp:func}`acquire_sem()`
::::

::::{abi-group}
:::{cpp:function} status_t set_sem_owner(sem_id sem, team_id team)
:::

Transfers ownership of the designated semaphore to {hparam}`team`. A
semaphore can only be owned by one team at a time; by setting a semaphore's
owner, you remove it from its current owner.

There are no restrictions on who can own a semaphore, or on who can
transfer ownership. In practice, however, the only reason you should ever
transfer ownership is if you're writing a device driver and you need to
bequeath a semaphore to the kernel (the team of which is known, for this
purpose, as {cpp:enumerator}`B_SYSTEM_TEAM`).

Semaphore ownership is meaningful for two reasons:

1. When a team dies (when all its threads are dead), the semaphores that are
  owned by that team are deleted.

2. Threads can only by deleted by threads that belongs to a semaphore's
  owner.

To discover a semaphore's owner, use the {cpp:func}`get_sem_info()`
function.

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
	- {cpp:enumerator}`B_NO_ERROR`.
	- Ownership was successfully transferred.
-
	- {cpp:enumerator}`B_BAD_SEM_ID`.
	- Invalid {hparam}`sem` value.
-
	- {cpp:enumerator}`B_BAD_TEAM_ID`.
	- Invalid {hparam}`team` value.

:::
::::

## Semaphore Structures and Types

### sem_id

:::{code} c
typedef int32 sem_id;
:::

{htype}`sem_id` numbers identify semaphores. The id is assigned when the
semaphore is created ({cpp:func}`create_sem()`). The values are unique
across the system.

### sem_info

:::{code} c
typedef struct sem_info {
    sem_id    sem;
    team_id   team;
    char      name[B_OS_NAME_LENGTH];
    int32     count;
    thread_id latest_holder;
}
:::

The {htype}`sem_info` structure supplies information about a semaphore. You
retrieve the structure through the {cpp:func}`get_sem_info()` function. The
information in the {htype}`sem_info` structure is guaranteed to be
internally consistent, but the structure as a whole should be consider to
be out-of-date as soon as you receive it. It provides a picture of a
semaphore as it exists just before the info-retrieving function returns.

The fields are:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Field

	- Description

-
	- sem.
	- The {htype}`sem_id` number of the semaphore.
-
	- team.
	- The {htype}`team_id` of the semaphore's owner.
-
	- name.
	- The name assigned to the semaphore.
-
	- count.
	- The semaphore's thread count.
-
	- latest_holder.
	- The thread that most recently acquired the semaphore.

:::

:::{admonition} Warning
:class: warning
The {hparam}`lastest_holder` field is highly undependable; in some cases,
the kernel doesn't even record the semaphore acquirer. Although you can use
this field as a hint while debugging, you shouldn't take it too seriously.
Love, Mom.
:::

## Semaphore Constants

### Semaphore Control Flags

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
	- {cpp:enumerator}`B_CAN_INTERRUPT`
	- Tells the kernel that the semaphore can be interrupted by a signal.
-
	- {cpp:enumerator}`B_DO_NOT_RESCHEDULE`
	- Tells the scheduler not to run after a semaphore is released. In other
		words, the thread that just released the semaphore gets to keep running.
-
	- {cpp:enumerator}`B_CHECK_PERMISSION`
	- Makes sure that the semaphore acquirer/releaser is running at the proper
		level. This is always added into user-level acquisition and release.
-
	- {cpp:enumerator}`B_RELATIVE_TIMEOUT`
	- Used to set a timeout that's relative to now.
-
	- {cpp:enumerator}`B_ABSOLUTE_TIMEOUT`
	- Used to set a timeout that's measured against the system clock.
-
	- {cpp:enumerator}`B_TIMEOUT`
	- Obsolete; use {cpp:enumerator}`B_RELATIVE_TIMEOUT`.

:::

These constants are combined to form the {hparam}`flag` argument to the
{cpp:func}`acquire_sem_etc()` and {cpp:func}`release_sem_etc()` functions.
