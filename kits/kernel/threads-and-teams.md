# Threads And Teams
## Thread and Team Functions
::::{abi-group}


Declared in: kernel/scheduler.h
:::{cpp:function} bigtime_t Threads And Teams::estimate_max_scheduling_latency(thread_id thread = -1)
:::
Returns the scheduling latency, in microseconds, of the specified thread.
Specify a thread_id of -1 to return the scheduling latency of the current
thread.
::::

::::{abi-group}





:::{cpp:function} void Threads And Teams::exit_thread(status_t return_value)
:::
:::{cpp:function} status_t Threads And Teams::kill_thread(thread_id thread)
:::
:::{cpp:function} status_t Threads And Teams::kill_team(team_id team)
:::
:::{code}
status_t on_exit_thread(void (*callback)(void *), void *data)
:::
These functions command one or more threads to halt execution:
:::{list-table}
---
header-rows: 1
---
-
	- Function
	- Description
-
	- exit_thread()
	- Tells the calling thread to exit with a return value as given by the argument. Declaring the return value is only useful if some other thread is sitting in a {cpp:func}`~wait::for` call on this thread. exit_thread() sends a signal to the thread (after caching the return value in a known place).
-
	- kill_thread()
	- Kills the thread given by the argument. The value that the thread will return to {cpp:func}`~wait::for` is undefined and can't be relied upon. kill_thread() is the same as sending a SIGKILLTHR signal to the thread.
-
	- kill_team()
	- Kills all the threads within the given team. Again, the threads' return values are random. kill_team() is the same as sending a SIGKILL signal to any thread in the team. Each of the threads in the team is then handed a SIGKILLTHR signal.
-
	- on_exit_thread()
	- Sets up the specified callback to be executed when the calling thread exits. The callback will receive the pointer data as an input argument.
:::
Exiting a thread is a fairly safe thing to do—since a thread can
only exit itself, it's assumed that the thread knows what it's doing.
Killing some other thread or an entire team is a bit more drastic since
the death certificate(s) will be delivered at an indeterminate time. In
addition, killing a thread can leak memory since resources that were
allocated by the thread may not be freed. Killing an entire team, on the
other hand, won't leak since the system reclaims all resources when the
team dies.
Keep in mind that threads die automatically (and their resources are
reclaimed) if they're allowed to exit naturally. You should only need to
kill a thread if something has gone screwy.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- The thread or team was successfully killed.
-
	- {cpp:enum}`B_BAD_THREAD_ID`.
	- Invalid thread value.
-
	- {cpp:enum}`B_BAD_TEAM_ID`.
	- Invalid team value.
-
	- {cpp:enum}`B_NO_MEMORY`.
	- Returned by on_exit_thread() if there's no memory to construct the internal callback record.
:::
::::

::::{abi-group}


:::{cpp:function} thread_id Threads And Teams::find_thread(const char* name)
:::
Finds and returns the thread with the given {hparam}`name`. A
{hparam}`name` argument of {cpp:enum}`NULL`
returns the calling thread.
A thread's name is assigned when the thread is spawned. The name can be
changed thereafter through the
{cpp:func}`~rename::thread`
function. Keep in mind
that thread names needn't be unique: If two (or more) threads boast the
same name, a find_thread() call on that name returns the first so-named
thread that it finds. There's no way to iterate through identically-named
threads.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_NAME_NOT_FOUND`.
	- {hparam}`name` doesn't identify a valid thread.
:::
::::

::::{abi-group}



:::{cpp:function} status_t Threads And Teams::get_team_info(team_id team, team_info* info)
:::
:::{cpp:function} status_t Threads And Teams::get_next_team_info(int32* cookie, team_info* info)
:::
The functions copy, into the {hparam}`info`
argument, the
{cpp:func}`~team::info` structure for a
particular team. The get_team_info() function retrieves information for
the team identified by {hparam}`team`. For information about the kernel, use
{cpp:enum}`B_SYSTEM_TEAM` as the team argument.
The get_next_team_info() version lets you step through the list of all
teams. The {hparam}`cookie` argument is a placemark; you set it to 0 on your first
call, and let the function do the rest. The function returns {cpp:enum}`B_BAD_VALUE`
when there are no more areas to visit:
:::{code}
/* Get the team_info for every team. */
team_info info;
int32 cookie = 0;
while (get_next_team_info(0, &cookie, &info) == B_OK)
   ...
:::
See
{cpp:func}`~team::info`
for a description of that structure.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- The desired team information was found.
-
	- {cpp:enum}`B_BAD_TEAM_ID`.
	- {hparam}`team` doesn't identify an existing team, or there are no more areas to visit.
:::
::::

::::{abi-group}



:::{cpp:function} status_t Threads And Teams::get_thread_info(thread_id thread, thread_info* info)
:::
:::{cpp:function} status_t Threads And Teams::get_next_thread_info(team_id team, int32* cookie, thread_info* info)
:::
These functions copy, into the {hparam}`info`
argument, the
{cpp:func}`~thread::info`
structure for a particular thread:
The get_thread_info() function gets the
information for the thread identified by {hparam}`thread`.
The get_next_thread_info() function lets you step through the list of a
team's threads through iterated calls. The {hparam}`team` argument identifies the
team you want to look at; a {hparam}`team` value of 0 means the team of the calling
thread. The {hparam}`cookie` argument is a placemark; you set it to 0 on your first
call, and let the function do the rest. The function returns {cpp:enum}`B_BAD_VALUE`
when there are no more threads to visit:
:::{code}
/* Get the thread_info for every thread in this team. */
thread_info info;
int32 cookie = 0;
while (get_next_thread_info(0, &cookie, &info) == B_OK)
   ...
:::
The value of the priority field describes the thread's "urgency"; the
higher the value, the more urgent the thread. The more urgent the thread,
the more attention it gets from the CPU. Expected priority values fall
between 0 and 120.
See "{cpp:func}`~Constants::ThreadPriorities`"
for the full story.
:::{admonition} Warning
:class: warning
:::
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- The thread was found; {hparam}`info` contains valid information.
-
	- {cpp:enum}`B_BAD_VALUE`.
	- {hparam}`thread` doesn't identify an existing thread, {hparam}`team` doesn't identify an existing team, or there are no more threads to visit.
:::
::::

::::{abi-group}


:::{cpp:function} status_t Threads And Teams::rename_thread(thread_id thread, const char* name)
:::
Changes the name of the given thread to {hparam}`name`. The name can be no longer
than {cpp:enum}`B_OS_NAME_LENGTH` (32 characters).
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- The thread was successfully named.
-
	- {cpp:enum}`B_BAD_THREAD_ID`.
	- {hparam}`thread` argument isn't a valid thread_id number.
:::
::::

::::{abi-group}


:::{cpp:function} status_t Threads And Teams::resume_thread(thread_id thread)
:::
Tells a new or suspended thread to begin executing instructions. If the
thread has just been spawned, it enters and executes the thread function
declared in {cpp:func}`~spawn::thread`.
If the thread was previously suspended(through
{cpp:func}`~suspend::thread`),
it continues from where it was suspended.
You can't use this function to wake up a sleeping thread, or to unblock a
thread that's waiting to acquire a semaphore or waiting in a
{cpp:func}`~receive::data`
call. However, you can unblock any of these threads by
suspending and then resuming. Blocked threads that are resumed return
{cpp:enum}`B_INTERRUPTED`.
resume_thread() is the same as sending a
SIGCONT signal to the thread.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- The thread was successfully resumed.
-
	- {cpp:enum}`B_BAD_THREAD_ID`.
	- {hparam}`thread` argument isn't a valid thread_id number.
-
	- {cpp:enum}`B_BAD_THREAD_STATE`.
	- The thread isn't suspended.
:::
::::

::::{abi-group}


:::{cpp:function} int32 Threads And Teams::receive_data(thread_id sender, void* buffer, size_t buffer_size)
:::
Retrieves a message from the thread's message cache. The message will
have been placed there through a previous
{cpp:func}`~send::data`
function call. If the cache is empty, receive_data()
blocks until one shows up—it never returns empty-handed.
The thread_id of the thread that called
{cpp:func}`~send::data`
is returned by reference in the sender argument. Note that there's no guarantee that the
sender will still be alive by the time you get its ID. Also, the value of
sender going into the function is ignored—you can't ask for a
message from a particular sender.
The
{cpp:func}`~send::data`
function copies two pieces of data into a thread's
message cache:
- A single four-byte code that's delivered as receive_data()'s return value,
- and an arbitrarily long data buffer that's copied into receive_data()'s buffer argument (you must allocate and free buffer yourself). The {hparam}`buffer_size` argument tells the function how many bytes of data to copy. If you don't need the data buffer—if the code value returned directly by the function is sufficient—you set {hparam}`buffer` to {cpp:enum}`NULL` and {hparam}`buffer_size` to 0.

Unfortunately, there's no way to tell how much data is in the cache
before you call receive_data():
- If there's more data than buffer can accommodate, the unaccommodated portion is discarded—a second receive_data() call will not read the rest of the message.
- Conversely, if receive_data() asks for more data than was sent, the function returns with the excess portion of buffer unmodified—receive_data() doesn't wait for another {cpp:func}`~send::data` call to provide more data with which to fill up the buffer.

Each receive_data() corresponds to exactly one
{cpp:func}`~send::data`.
Lacking a previous invocation of its mate, receive_data() will block until
{cpp:func}`~send::data`
is called. If you don't want to block, you should call
{cpp:func}`~has::data`
before calling receive_data() (and proceed to
receive_data()
only if {cpp:func}`~has::data`
returns {cpp:enum}`true`).
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- If successful
	- Returns the message's four-byte code.
-
	- {cpp:enum}`B_INTERRUPTED`.
	- A blocked receive_data() call was interrupted by a signal.
:::
::::

::::{abi-group}


:::{cpp:function} status_t Threads And Teams::send_data(thread_id sender, void* buffer, size_t buffer_size)
:::
send_data() copies a message into thread's message cache. The target
thread retrieves the message (and empties the cache) by calling
{cpp:func}`~receive::data`.
There are two parts to the message:
- A single four-byte code passed as an argument to send_data() and returned directly by {cpp:func}`~receive::data`.
- A {hparam}`buffer` of data that's {hparam}`buffer_size` bytes long ({hparam}`buffer` can be {cpp:enum}`NULL`, in which case {hparam}`buffer_size` should be 0). The data is copied into the target thread's cache, and then copied into {cpp:func}`~receive::data`'s {hparam}`buffer` (which must be allocated). The calling threads retain responsibility for freeing their buffers.

In addition to returning the {hparam}`code` directly, and copying the message data
into its {hparam}`buffer` argument,
{cpp:func}`~receive::data`
sets {hparam}`sender` to the id of the thread that sent the message.
send_data() blocks if there's an unread message in the target thread's
cache; otherwise it returns immediately (i.e. it doesn't wait for the
target to call {cpp:func}`~receive::data`.
Analogously, {cpp:func}`~receive::data`
blocks until there's a message to retrieve.
In the following example, the main thread spawns a thread, sends it a
message, and then tells the thread to run:
:::{code}
main()
{
   thread_id other_thread;
   int32 code = 63;
   char *buf = "Hello";
   other_thread = spawn_thread(thread_func, ...);
   send_data(other_thread, code, (void *)buf, strlen(buf));
   resume_thread(other_thread);
   ...
}
:::
To retrieve the message, the target thread calls
{cpp:func}`~receive::data`:
:::{code}
int32 thread_func(void *data)
{
   thread_id sender;
   int32 code;
   char buf[512];
   code = receive_data(&sender, (void *)buf, sizeof(buf));
   ...
}
:::
Keep in mind that the message data is copied into the buffer; you must
allocate adequate storage for the data. If the buffer isn't big enough to
accommodate all the datain the message, the left-over portion is thrown
away. Note, however, that there isn't any way for a thread to determine
how much data has been copied into its message cache.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- The data was successfuly sent.
-
	- {cpp:enum}`B_BAD_THREAD_ID`.
	- {hparam}`thread` doesn't identify a valid thread.
-
	- {cpp:enum}`B_NO_MEMORY`.
	- The target couldn't allocate enough memory for its copy of buffer.
-
	- {cpp:enum}`B_INTERRUPTED`.
	- The function blocked, but a signal unblocked it.
:::
::::

::::{abi-group}


:::{cpp:function} bool Threads And Teams::has_data(thread_id thread)
:::
has_data() returns {cpp:enum}`true` if
{hparam}`thread` has a message in its message cache.
Ostensibly, you use this function before calling
{cpp:func}`~send::data` or
{cpp:func}`~receive::data`
to avoid blocking:
:::{code}
if (!has_data(target_thread))
   err = send_data(target_thread, ...);
/* or */
if (has_data(find_thread(NULL))
   code = receive_data(...);
:::
This works for
{cpp:func}`~receive::data`,
but notice that there's a race condition between the
has_data() and
{cpp:func}`~send::data`
calls. Another thread could send a message to the target in the interim.
::::

::::{abi-group}



:::{cpp:function} status_t Threads And Teams::set_thread_priority(thread_id thread, int32 new_priority)
:::
:::{cpp:function} int32 Threads And Teams::suggest_thread_priority(uint32 what = B_DEFAULT_MEDIA_PRIORITY, int32 period = 0, bigtime_t jitter = 0, bigtime_t length = 0)
:::
Declared in:  kernel/scheduler.h
set_thread_priority() resets the given thread's priority to {hparam}`new_priority`.
The priority is expected to be between 0 and 120.
See "Thread Priorities"
for a description of the priority scheme, and
"Thread Priority Values"
for a list of pre-defined priority constants.
suggest_thread_priority() takes information about a thread and returns a
suggested priority that you can pass to set_thread_priority() (or, more
likely, to
{cpp:func}`~spawn::thread`).
The {hparam}`what` value is a bit mask that indicates the type of activities the
thread will be used for. The possible values are listed in
Suggested Thread Priorities.
{hparam}`period` is the number of times per second the thread needs to be run
(specify 0 if it needs to run continuously). {hparam}`jitter` is an estimate, in
microseconds, of how much the period can vary as long as the average
stays at {hparam}`period` times per second.
{hparam}`length` is an approximation of the amount of time, in microseconds, the
thread will typically run per invocation (i.e., the amount of time that
will pass between the moment it receives a message, through processing
it, until it's again waiting for another message).
For example, if you're spawning a thread to handle video refresh for a
computer game, and you want the display to update 30 times per second,
you might use code similar to the following:
:::{code}
int32 priority;
priority = suggest_thread_priority(B_LIVE_3D_RENDERING, 30, 1000, 150);
th = spawn_thread(func, "render_thread", priority, NULL)
:::
This spawns the rendering thread with a priority appropriate for a thread
for live 3D rendering which wants to be run 30 times per second, with a
variation of only 1000 microseconds. Each invocation of the thread's code
is estimated to take 150 microseconds. Obviously the jitter and length
values would have to be tuned to the particular application.
set_thread_priority() returns…
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- Positive integers.
	- If the function is successful, the previous priority is returned.
-
	- {cpp:enum}`B_BAD_THREAD_ID`.
	- {hparam}`thread` doesn't identify a valid thread.

:::
::::

::::{abi-group}



:::{cpp:function} status_t Threads And Teams::snooze(bigtime_t microseconds, int32 new_priority)
:::
:::{cpp:function} status_t Threads And Teams::snooze_until(bigtime_t microseconds, int timebase)
:::
snooze() blocks the calling thread for
the given number of {hparam}`microseconds`.
snooze_until() blocks until an absolute time measured in the given
{hparam}`timebase`. Currently, the only allowed value for {hparam}`timebase` is
{cpp:enum}`B_SYSTEM_TIMEBASE`, which measures time against the system clock (as
reported by {cpp:func}`~system::time`).
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- 
The thread went to sleep and is now awake.

-
	- {cpp:enum}`B_INTERRUPTED`.
	- 
The thread received a signal while it was sleeping.

:::
::::

::::{abi-group}


:::{cpp:function} thread_id Threads And Teams::spawn_thread(thread_func func, const char* name, int32 priority, void* data)
:::
Creates a new thread and returns its thread_id identifier (a positive
integer). The arguments are:
:::{list-table}
---
header-rows: 1
---
-
	- Parameter
	- Description
-
	- func
	- Is a pointer to a thread function. This is the function that the thread will execute when it's told to run. See "The Thread Function" for details.
-
	- name
	- Is the name that you wish to give the thread. It can be, at most, {cpp:enum}`B_OS_NAME_LENGTH` (32) characters long.
-
	- priority
	- Is the CPU priority level of the thread. This value should be between 0 and 120; he higher the priority, the more attention the thread gets. See Thread Priorities for a description of the priorities, and Thread Priority Values for a list of priority constants.
-
	- data
	- Is forwarded as the argument to the thread function.
:::
A newly spawned thread is in a suspended state
({cpp:enum}`B_THREAD_SUSPENDED`). To
tell the thread to run, you pass its thread_id to the
{cpp:func}`~resume::thread`
function. The thread will continue to run until the thread function
exits, or until the thread is explicitly killed (through a signal or a
call to {cpp:func}`~exit::thread`,
{cpp:func}`~kill::thread`, or
{cpp:func}`~kill::team`).
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_NO_MORE_THREADS`.
	- All thread_id numbers are currently in use.
-
	- {cpp:enum}`B_NO_MEMORY`.
	- Not enough memory to allocate the resources for another thread.
:::
::::

::::{abi-group}


:::{cpp:function} status_t Threads And Teams::suspend_thread(thread_id thread)
:::
Halts the execution of the given thread, but doesn't kill the thread
entirely. The thread remains suspended (suspend_thread() blocks) until
it's told to run through the
{cpp:func}`~resume::thread`
function. Nothing prevents you from suspending your own thread, i.e.:
:::{code}
suspend_thread(find_thread(NULL));
:::
Of course, this is only smart if you have some other thread that will
resume you later.
You can suspend any thread, regardless of its current state. But be
careful: If the thread is blocked on a semaphore (for example), the
subsequent
{cpp:func}`~resume::thread`
call will "hop over" the semaphore acquisition.
Suspensions don't nest. A single
{cpp:func}`~resume::thread` unsuspends a thread
regardless of the number of suspend_thread() calls it has received.
suspend_thread() is the same as sending a
SIGSTOP signal to the thread.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- The thread is now suspended.
-
	- {cpp:enum}`B_BAD_THREAD_ID`.
	- thread isn't a valid thread_id number.
:::
::::

::::{abi-group}


:::{cpp:function} status_t Threads And Teams::wait_for_thread(thread_id thread, status_t* exit_value)
:::
This function causes the calling thread to wait until thread (the "target
thread") has died. If thread is suspended (or freshly spawned),
wait_for_thread() will resume it.
When the target thread is dead, the value that was returned by its thread
function (or imposed by
{cpp:func}`~exit::thread`)
is returned in {hparam}`exit_value`. If the
target thread was killed (by
{cpp:func}`~kill::thread` or
{cpp:func}`~kill::team`),
or if the thread function doesn't return a value, the value returned in
{hparam}`exit_value` will be unreliable.
You must pass a valid pointer as the second argument to
wait_for_thread(). You mustn't pass
{cpp:enum}`NULL` even if you're not interested in
the return value.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- The target is now dead.
-
	- {cpp:enum}`B_BAD_THREAD_ID`.
	- {hparam}`thread` isn't a valid thread_id number.
-
	- {cpp:enum}`B_INTERRUPTED`.
	- The target was killed by a signal. This includes {cpp:func}`~kill::thread`, {cpp:func}`~kill::team`, and {cpp:func}`~exit::thread`.
:::
::::

## Thread and Team Structures and Types
::::{abi-group}



:::{code}
typedef int32 team_id ;
typedef int32 thread_id ;
:::
These id numbers uniquely identify teams and threads, respecitvely.
::::

::::{abi-group}


:::{code}
typedef struct {
    team_id   team;
    int32     thread_count;
    int32     image_count;
    int32     area_count;
    thread_id debugger_nub_thread;
    port_id   debugger_nub_port;
    int32     argc;
    char      args[64];
    uid_t     uid;
    gid_t     gid;
} team_info;
:::
The team_info structure returns information about a team. To retrieve one
of these structures, use
{cpp:func}`~get::team` or
{cpp:func}`~get::next`.
The first field is obvious; the next three reasonably so: They give the
number of threads that have been spawned, images that have been loaded,
and areas that have been created or cloned within this team.
The debugger fields are used by the, uhm, the…debugger?
The argc field is the number of command line arguments that were used to
launch the team; args is a copy of the first 64 characters from the
command line invocation. If this team is an application that was launched
through the user interface (by double-clicking, or by accepting a dropped
icon), then argc is 1 and args is the name of the application's
executable file.
uid and gid identify the user
and group that "owns" the team. You can use
these values to play permission games.
::::

::::{abi-group}


:::{code}
typedef int32 (*thread_func)(void *data);
:::
thread_func is the prototype for a thread's thread function. You specify
a thread function by passing a thread_func as the first argument to
{cpp:func}`~spawn::thread`;
the last argument to
{cpp:func}`~spawn::thread`
is forwarded as the thread function's data argument. When the thread function exits, the
spawned thread is automatically killed. To retrieve a thread_func's
return value, some other thread must be waiting in a
{cpp:func}`~wait::for`
call.
Note that
{cpp:func}`~spawn::thread`
doesn't copy the data that data points to. It
simply passes the pointer through literally. Never pass a pointer that's
allocated locally (on the stack).
::::

::::{abi-group}


:::{code}
typedef struct {
    thread_id    thread;
    team_id      team;
    char         name[B_OS_NAME_LENGTH];
    thread_state state;
    sem_id       sem;
    int32        priority;
    bigtime_t    user_time;
    bigtime_t    kernel_time;
    void *       stack_base;
    void *       stack_end;
} thread_info
:::
The thread_info structure contains information about a thread. To
retrieve one of these structure, use
{cpp:func}`~get::thread` or
{cpp:func}`~get::next`.
The thread, team,
and name fields contain the indicated information.
state describes what the thread is currently doing (see
{cpp:func}`~thread::state` for
the list of states). If the thread is waiting to acquire a semaphore, sem
is that semaphore.
priority is a value that indicates the level of attention the thread gets
(see Thread Priority).
user_time and kernel_time
are the amounts of time, in microseconds, the
thread has spent executing user code and the amount of time the kernel
has run on the thread's behalf, respectively.
stack_base and stack_end
are pointers to the first byte and last bytes in
the thread's execution stack. Currently, the stack size is fixed at
around 256k.
:::{admonition} Warning
:class: warning
The two stack pointers are currently inverted such that stack_base is
less than stack_end.
(In a stack-grows-down world, the base should be
greater than the end.)
:::
::::

## Thread and Team Constants
::::{abi-group}


:::{code}
#define B_SYSTEM_TEAM ...
:::
Use this constant as the first argument to
{cpp:func}`~get::team`
to get team information about the kernel).
::::

::::{abi-group}


:::{code}
#define B_SYSTEM_TIMEBASE ...
:::
The system timebase constant is used as a basis for time measurement in
the {cpp:func}`~snooze::until`
function. (Currently, it's the only timebase available.)
::::

::::{abi-group}













:::{code}
enum be_task_flags {
    B_DEFAULT_MEDIA_PRIORITY,
    B_OFFLINE_PROCESSING,
    B_STATUS_RENDERING,
    B_USER_INPUT_HANDLING,
    B_LIVE_VIDEO_MANIPULATION,
    B_VIDEO_PLAYBACK,
    B_VIDEO_RECORDING,
    B_LIVE_AUDIO_MANIPULATION,
    B_AUDIO_PLAYBACK,
    B_AUDIO_RECORDING,
    B_LIVE_3D_RENDERING,
    B_NUMBER_CRUNCHING
};
:::
Declared in: kernel/scheduler.h
:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_DEFAULT_MEDIA_PRIORITY`.
	- The thread isn't doing anything specialized.
-
	- {cpp:enum}`B_OFFLINE_PROCESSING`.
	- The thread is doing non-real-time computations.
-
	- {cpp:enum}`B_STATUS_RENDERING`.
	- The thread is rendering a status or preview display.
-
	- {cpp:enum}`B_USER_INPUT_HANDLING`.
	- The thread is handling user input.
-
	- {cpp:enum}`B_LIVE_VIDEO_MANIPULATION`.
	- The thread is processing live video (filtering, compression, decompression, etc.).
-
	- {cpp:enum}`B_VIDEO_PLAYBACK`.
	- The thread is playing back video from a hardware device.
-
	- {cpp:enum}`B_VIDEO_RECORDING`.
	- The thread is recording video from a hardware device.
-
	- {cpp:enum}`B_LIVE_AUDIO_MANIPULATION`.
	- The thread is doing real-time manipulation of live audio data (filtering, compression, decompression, etc.).
-
	- {cpp:enum}`B_AUDIO_PLAYBACK`.
	- The thread is playing back audio from a hardware device.
-
	- {cpp:enum}`B_AUDIO_RECORDING`.
	- The thread is recording audio from a hardware device.
-
	- {cpp:enum}`B_LIVE_3D_RENDERING`.
	- The thread is performing live 3D rendering.
-
	- {cpp:enum}`B_NUMBER_CRUNCHING`.
	- The thread is doing data processing.
:::
These constants describe what the thread is designed to do. You use these
constants when asking for a suggested priority (see
{cpp:func}`~suggest::thread`).
:::{admonition} Warning
:class: warning
These constants may not be used as actual thread priority
values—do not pass one of these values as the priority argument to
{cpp:func}`~spawn::thread`.
:::
::::

::::{abi-group}








Time-Sharing PriorityValueB_LOW_PRIORITY5B_NORMAL_PRIORITY10B_DISPLAY_PRIORITY15B_URGENT_DISPLAY_PRIORITY20
Real-Time PriorityValueB_REAL_TIME_DISPLAY_PRIORITY100B_URGENT_PRIORITY110B_REAL_TIME_PRIORITY120
The thread priority values are used to set the "urgency" of a thread.
Although you can reset a thread's priority through
{cpp:func}`~set::thread`,
the priority is initially—and almost always permanently—set
in {cpp:func}`~spawn::thread`.
::::

::::{abi-group}








:::{code}
enum { ... } thread_state
:::
:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_THREAD_RUNNING`.
	- The thread is currently receiving attention from a CPU.
-
	- {cpp:enum}`B_THREAD_READY`.
	- The thread is waiting for its turn to receive attention.
-
	- {cpp:enum}`B_THREAD_SUSPENDED`.
	- The thread has been suspended or is freshly-spawned and is waiting to start.
-
	- {cpp:enum}`B_THREAD_WAITING`.
	- The thread is waiting to acquire a semaphore. The sem field of the thread's {cpp:func}`~thread::info` structure will tell you which semaphore.
-
	- {cpp:enum}`B_THREAD_RECEIVING`.
	- The thread is sitting in a {cpp:func}`~receive::data` function call.
-
	- {cpp:enum}`B_THREAD_ASLEEP`.
	- The thread is sitting in a {ref}`snooze()` call.
:::
A thread's state tells you what the thread is currently doing. To get the
state, look in the state field of the
{cpp:func}`~thread::info`
structure (retrieved through
{cpp:func}`~get::thread`).
::::
