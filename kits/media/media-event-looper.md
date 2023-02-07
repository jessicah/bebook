# BMediaEventLooper
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} explicit BMediaEventLooper::BMediaEventLooper(uint32* apiVersion = B_BEOS_VERSION)
:::
You need to override this function to handle your node's initialization
needs. The {hparam}`apiVersion` argument indicates the version of the BeOS API the
object was written for; you should let the default value be
used—this will cause your node to inherit the API version of the
BeOS version you're compiling under.
::::

::::{abi-group}

:::{cpp:function} virtual BMediaEventLooper::~BMediaEventLooper()
:::
Calls
{cpp:func}`~BMediaEventLooper::Quit`
to stop the control thread and free allocated memory.
::::

## Member Functions
::::{abi-group}

:::{cpp:function} virtual void BMediaEventLooper::CleanUpEvent(const media_timed_event* event)
:::
Implement this function to clean up after custom events you've created
and added to your queue. It's called when a custom event is removed from
the queue, to let you handle any special tidying-up that the event might
require.
::::

::::{abi-group}

:::{cpp:function} virtual void BMediaEventLooper::ControlLoop()
:::
This function waits for messages, pops events off the queue, and calls
{cpp:func}`~BMediaEventLooper::DispatchEvent`.
It's called automatically when the {hclass}`BMediaEventLooper` is
{cpp:func}`~BMediaEventLooper::Run`.
:::{admonition} Warning
:class: warning
If you choose to reimplement this function, be very careful; it's very
easy to cause Bad Things to happen.
:::
::::

::::{abi-group}

:::{cpp:function} thread_id BMediaEventLooper::ControlThread()
:::
Returns the control thread's
{cpp:func}`~thread::id`.
::::

::::{abi-group}

:::{cpp:function} void BMediaEventLooper::DispatchEvent(const media_timed_event* event, bigtime_t lateness, bool realTimeEvent = false)
:::
Calls
{cpp:func}`~BMediaEventLooper::HandleEvent`
to let your code handle the specified event. If your
code doesn't handle it, this function may have a default handler to
process it. In general, you won't call this function.
{hclass}`BMediaEventLooper` compensates your
performance time by adding the event latency (see
{cpp:func}`~BMediaEventLooper::SetEventLatency`)
and the scheduling latency (or, for
real-time events, only the scheduling latency).
It's the control loop's job to remove the event from the queue; this
function doesn't do that.
::::

::::{abi-group}

:::{cpp:function} BTimedEventQueue* BMediaEventLooper::EventQueue()
:::
:::{cpp:function} BTimedEventQueue* BMediaEventLooper::RealTimeQueue()
:::
{hmethod}`EventQueue()` returns a
pointer to the
{cpp:class}`BTimedEventQueue`
used by the
message handler. {hmethod}`RealTimeQueue()` returns a pointer to the
{cpp:class}`BTimedEventQueue`
used to queue real-time events.
:::{admonition} Note
:class: note
Events in the real-time queue are handled according to their real time,
while events in the normal event queue are handled based on their
performance time. So the values of the time stamps on events in these two
queues are handled differently; keep this in mind if you need to peek
into the queues yourself.
:::
::::

::::{abi-group}

:::{cpp:function} virtual void BMediaEventLooper::ControlLoop(const media_timed_event* event, bigtime_t lateness, bool realTimeEvent = false)
:::
Implement this function to handle incoming media events. The {hparam}`event`
argument references a
{cpp:func}`~media::timed`
structure that describes the
event. {hparam}`lateness` indicates how late the
event is, and {hparam}`realTimeEvent` is
{cpp:enum}`true` if the event needs to be handled in real time.
The {hclass}`BMediaEventLooper` will call this function from the
{cpp:func}`~BMediaEventLooper::DispatchEvent`
function. It's the control loop's job to remove the event from the queue.
::::

::::{abi-group}

:::{cpp:function} virtual void BMediaEventLooper::NodeRegistered()
:::
The Media Server calls this hook function after the node has been
registered. This is derived from
{cpp:class}`BMediaNode`;
{hclass}`BMediaEventLooper` implements it to call
{cpp:func}`~BMediaEventLooper::Run`
automatically when the node is registered; if you implement
{hmethod}`NodeRegistered()` you should call through to
{cpp:func}`BMediaNode::NodeRegistered`
after you've done your custom operations.
::::

::::{abi-group}

:::{cpp:function} void BMediaEventLooper::Quit()
:::
Closes the node's control port and closes the control thread. Blocks
until the control thread is gone.
::::

::::{abi-group}

:::{cpp:function} void BMediaEventLooper::Run()
:::
Spawns and runs the control thread; this is called automatically by the
default {cpp:func}`~BMediaEventLooper::NodeRegistered`
implementation. If you override
{cpp:func}`~BMediaEventLooper::NodeRegistered`,
be sure you call through to the default implementation, or call
{hmethod}`Run()`.
::::

::::{abi-group}

:::{cpp:function} bigtime_t BMediaEventLooper::SchedulingLatency() const
:::
Returns the scheduling latnecy, in microseconds, of the node.
::::

::::{abi-group}

:::{cpp:function} void BMediaEventLooper::SetBufferDuration(bigtime_t duration)
:::
:::{cpp:function} bigtime_t BMediaEventLooper::BufferDuration() const
:::
{hmethod}`SetBufferDuration()` sets the duration
of the node's buffers. The duration is clamped to 0 if it's less than 0.
{hmethod}`BufferDuration()` returns the duration
of the nodes' buffers.
::::

::::{abi-group}

:::{cpp:function} void BMediaEventLooper::SetEventLatency(bigtime_t latency)
:::
:::{cpp:function} bigtime_t BMediaEventLooper::EventLatency() const
:::
{hmethod}`SetEventLatency()` sets the event latency. The event latency is the
upstream and downstream algorithmic latency of your node—but should
not include scheduling latency. This latency is taken into account by the
{hclass}`BMediaEventLooper` when deciding when to pop events off the queue for you
to process.
{hmethod}`EventLatency()` returns the event latency.
::::

::::{abi-group}

:::{cpp:function} void BMediaEventLooper::SetOfflineTime(bigtime_t offlineTime)
:::
:::{cpp:function} virtual bigtime_t BMediaEventLooper::OfflineTime()
:::
{hmethod}`SetOfflineTime()` sets the time that
{hmethod}`OfflineTime()` will return.
Augment {hmethod}`OfflineTime()` to compute the node's current time; it's called by
the Media Kit when it's in offline mode. Update any appropriate internal
information as well, then call through to the {hclass}`BMediaEventLooper`
implementation.
::::

::::{abi-group}

:::{cpp:function} void BMediaEventLooper::SetPriority(int32 priority)
:::
:::{cpp:function} int32 BMediaEventLooper::Priority() const
:::
{hmethod}`SetPriority()` sets the control thread's priority. Values less than 0 are
clamped to 0, and values greater than 120 are clamped to 120.
{hmethod}`Priority()` returns the control thread's current priority.
::::

::::{abi-group}

:::{cpp:function} void BMediaEventLooper::SetRunState(run_state state)
:::
:::{cpp:function} run_state BMediaEventLooper::RunState() const
:::
{hmethod}`SetRunState()` sets the node's current run state.
{hmethod}`RunState()` returns the current run state.
::::

## Constants
::::{abi-group}

Declared in: media/MediaEventLooper.h
:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_IN_DISTRESS`.
	- The node is experiencing problems.
-
	- {cpp:enum}`B_UNREGISTERED`.
	- The node hasn't been registered with the Media roster yet.
-
	- {cpp:enum}`B_STOPPED`.
	- The node isn't running.
-
	- {cpp:enum}`B_STARTED`.
	- The node is running.
-
	- {cpp:enum}`B_QUITTING`.
	- The node's in the process of shutting down.
-
	- {cpp:enum}`B_TERMINATED`.
	- The node has been terminated.
-
	- {cpp:enum}`B_USER_RUN_STATES`.
	- Base for user-defined run states.
:::
::::
