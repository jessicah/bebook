# BMediaNode
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} explicit BMediaNode::BMediaNode(const char* name)
:::
Call this from your derived node's constructor.
The node is created with a reference count of 1; the count is incremented
each time the
{cpp:func}`~BMediaNode::Acquire`
call is issued, and decremented each time
{cpp:func}`~BMediaNode::Release`
is called. When the reference count becomes zero, the node is deleted.
::::

::::{abi-group}

:::{cpp:function} virtual BMediaNode::~BMediaNode()
:::
You may never delete a {hclass}`BMediaNode` because you don't know for certain when
the Media Server is done with it. Instead, the Media Server maintains a
reference count for the node, and when it is no longer in use, the node
will be deleted automatically.
::::

## Member Functions
::::{abi-group}

:::{cpp:function} BMediaNode* BMediaNode::Acquire()
:::
:::{cpp:function} BMediaNode* BMediaNode::Release()
:::
{hmethod}`Acquire()` returns a pointer to the
node, after incrementing the node's reference count.
{hmethod}`Release()` releases the node by
decrementing its reference count. If the count reaches zero, the node
is deleted and {cpp:enum}`NULL` is returned; otherwise,
a pointer to the node is returned.
:::{admonition} Note
:class: note
Although you usually can't call node member functions directly from
within an application, you can call {hmethod}`Acquire()`
and {hmethod}`Release()` directly if
the node is subclassed within the application itself (rather than in an
add-on).
:::
::::

::::{abi-group}

:::{cpp:function} void BMediaNode::AddNodeKind(uint64 kind)
:::
Adds a kind to the set of kinds supported by the node. This lets the
system know what types of node interfaces are supported by the node's
implementation. Possible values include {cpp:enum}`B_BUFFER_PRODUCER` (which
indicates that the node implements the
{cpp:class}`BBufferProducer`
protocol) and {cpp:enum}`B_PHYSICAL_INPUT` (which indicates that the node implements a physical
input, such as a sound digitizing input device). For a complete list of
kind values, see
{cpp:func}`~Enums::node`.
:::{admonition} Note
:class: note
In general, you don't need to call this function. The base system
classes call {hmethod}`AddNodeKind()` automatically
to set up the node type flags; for example, a
{cpp:class}`BBufferProducer`
automatically calls
`AddNodeKind(B_BUFFER_PRODUCER)`.
The only time it's necessary go call
{hmethod}`AddNodeKind()` is if the node you're implementing is a physical device or
a mixer, in which case you need to add the {cpp:enum}`B_PHYSICAL_INPUT`,
{cpp:enum}`B_PHYSICAL_OUTPUT`, or {cpp:enum}`B_SYSTEM_MIXER` flag.
:::
::::

::::{abi-group}

:::{cpp:function} virtual BMediaAddOn* BMediaNode::AddOn(int32* outInternalID) const = 0
:::
Implement this function to return a pointer to the
{cpp:class}`BMediaAddOn` that
instantiated the node. If the node lives in an application (rather than
in an add-on), return {cpp:enum}`NULL`. If the node is in
an add-on, {hparam}`outInternalID`
should be changed to contain the internal ID number of the node within
the add-on.
::::

::::{abi-group}

:::{cpp:function} virtual status_t BMediaNode::AddTimer(bigtime_t toPerformanceTime, int32 cookie)
:::
:::{cpp:function} void BMediaNode::TimerExpired(bigtime_t notifyPoint, int32 cookie, status_t error = B_OK)
:::
Your node should implement the {hmethod}`AddTimer()`
function to remember the {hparam}`cookie`
and time given. When the time {hparam}`toPerformanceTime` is reached, your node
should call {hmethod}`TimerExpired()` with the
corresponding {hparam}`cookie` value, passing
the recorded {hparam}`toPerformanceTime` value as
the {hparam}`notifyPoint` argument. This
will, in turn, cause the
{cpp:func}`BMediaRoster::SyncToNode`
call that instigated the timer to return to the caller.
Your implementation of {hmethod}`AddTimer()`
should return {cpp:enum}`B_OK` if all is well;
otherwise it should return an appropriate error code.
::::

::::{abi-group}

:::{cpp:function} virtual port_id BMediaNode::ControlPort() const = 0
:::
Returns the port_id of the port to which the node listens for requests.
Your node must implement this to return a valid Kernel Kit port.
::::

::::{abi-group}

:::{cpp:function} virtual status_t BMediaNode::DeleteHook(BMediaNode* node)
:::
The {hmethod}`DeleteHook()` function is called
to delete the {hclass}`BMediaNode` object. You
may augment this if you need to perform additional work before the node
is deleted, but you should always either include the line:
:::{code}
delete this;
:::
or you should call through to the inherited form of the function. Return
{cpp:enum}`B_OK` if the node was deleted successfully, otherwise return an
appropriate error code.
::::

::::{abi-group}

:::{cpp:function} virtual status_t BMediaNode::GetNodeAttributes(media_node_attribute* outAttributes, size_t inMaxCount)
:::
Implement this function to fill the {hparam}`outAttributes`
array (which has room for {hparam}`inMaxCount` attributes) with
your node's attributes.
Return {cpp:enum}`B_OK` if all is well, or return an
appropriate error code.
::::

::::{abi-group}

:::{cpp:function} void BMediaNode::HandleBadMessage(int32 message, const void* data, size_t size)
:::
If your node receives a message that neither the node, nor any interface
from which the node is derived, understands the message, pass the message
along to this function, which will work magic to deal with the problem
one way or another. All arguments received by the
{cpp:func}`~BMediaNode::HandleMessage`
function should be passed directly through to
{hmethod}`HandleBadMessage()`.
::::

::::{abi-group}

:::{cpp:function} virtual status_t BMediaNode::HandleMessage(int32 message, const void* data, size_t size)
:::
Given a message received on the control port, this function dispatches
the message to the appropriate {hclass}`BMediaNode` hook function. If the message
doesn't correspond to a hook function, {cpp:enum}`B_ERROR` is returned.
When you implement a media node of your own (derived from
{cpp:class}`BBufferConsumer`,
{cpp:class}`BBufferProducer`,
etc), you always need to call through to
{hmethod}`BMediaNode::HandleMessage()` from your node's implementation of
{hmethod}`HandleMessage()`. This is crucial, to be sure that every ancestor of your
node gets to look at the message and attempt to process it.
For example, if your node inherits from both
{cpp:class}`BBufferProducer` and
{cpp:class}`BBufferConsumer`,
you should call
{cpp:func}`BBufferProducer::HandleMessage` and
{cpp:func}`BBufferConsumer::HandleMessage`,
{hmethod}`then BMediaNode::HandleMessage()`, like
this:
:::{code}
virtual status_t MyBufferProducerConsumer::HandleMessage(int32 message,
         const void* data, size_t size) {
   if (message == SOME_THING_I_DO) {
      DoWhatever();
   }
   else if (BBufferConsumer::HandleMessage(message, data, size) &&
            BBufferProducer::HandleMessage(message, data, size) &&
            BMediaNode::HandleMessage(message, data, size)) {
      BMediaNode::HandleBadMessage(message, data, size);
   }
}
:::
Note that
{cpp:func}`BMediaNode::HandleBadMessage`
is called if none of the
{hmethod}`HandleMessage()` implementations accept the message.
Values of message between 0x60000000 and 0x7FFFFFFF are available for use
by applications. Values below 0x60000000 are reserved for use by the
Media Kit, and typically correspond to specific virtual hook functions
within your node. If you can show just cause for needing to know the
message value for a particular hook, you can try emailing
devsupport@be.com and see if we agree with you, in which case we may
share that information.
Don't reverse-engineer the message values; if you really need to know,
ask us. Otherwise, we won't know that a particular message code number
shouldn't be changed. In general, it's a bad idea to rely on specific
values, although there may be cases in which it's necessary.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- The message was dispatched.
-
	- {cpp:enum}`B_ERROR`
	- The message couldn't be dispatched, possibly because it doesn't correspond to a hook function.
:::
::::

::::{abi-group}

:::{cpp:function} media_node_id BMediaNode::ID() const
:::
Returns the
{cpp:func}`~media::node`
assigned to the node by the Media Server. The
result is 0 if the node hasn't been registered yet, and negative if an
error occurred while attempting to register the node.
::::

::::{abi-group}

:::{cpp:function} uint64 BMediaNode::Kinds() const
:::
Returns a bit mask indicating what interfaces the node implements. See
{cpp:func}`~Enums::node` for a list of valid
interface kinds.
::::

::::{abi-group}

:::{cpp:function} const char* BMediaNode::Name() const
:::
Returns a human-readable string specifying the node's name. This pointer
is only valid until you
{cpp:func}`~BMediaNode::Release`
the node; after that, the pointer may point into empty space.
::::

::::{abi-group}

:::{cpp:function} static int32 BMediaNode::NewChangeTag()
:::
This function, intended primarily for use by
{cpp:class}`BBufferConsumer`
nodes, creates and returns a new change tag value.
::::

::::{abi-group}

:::{cpp:function} media_node BMediaNode::Node() const
:::
Returns the
{cpp:func}`~media::node`
structure that will be used by an application when
accessing this node via the media roster.
::::

::::{abi-group}

:::{cpp:function} virtual void BMediaNode::NodeRegistered()
:::
The Media Server calls this hook function after the node has been
registered.
::::

::::{abi-group}

:::{cpp:function} status_t BMediaNode::NodeStopped(bigtime_t whenPerformanceTime) const
:::
When you've finished handling a stop request (buffers will no longer be
flowing), call this function. If anyone is listening for stop
notifications from you, they'll be notified. The {hparam}`whenPerformanceTime`
argument should be the performance time of the stop command that was
handled.
Anyone listening for node stop messages will be notified; this lets
applications running in offline (rendering) mode know when the node has
actually completed its work.
If your node is a
{cpp:class}`BBufferProducer`,
downstream consumers will be notified
that your node stopped (automatically, no less) through the
`BBufferConsumer::ProducerDataStatus(B_PRODUCER_STOPPED)`
call. This lets offline rendering nodes know when each of their inputs have
no more data to send for the current roll.
:::{admonition} Note
:class: note
This is especially important for nodes that can be run
in {cpp:enum}`B_OFFLINE` mode.
:::
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- No error.
-
	- Other errors.
	- Unable to communicate with the Media Server, or an  error occurred communicating with other nodes.
:::
::::

::::{abi-group}

:::{cpp:function} virtual void BMediaNode::Preroll()
:::
This hook function may be called before your node receives a
{cpp:func}`~BMediaNode::Start`
message if the application using the node calls
{cpp:func}`BMediaRoster::PrerollNode`.
This gives the node a chance to prepare the
media so that when the media is started, the response is as fast as
possible.
::::

::::{abi-group}

:::{cpp:function} status_t BMediaNode::ReportError(node_error whichError, const BMessage* info = NULL)
:::
Transmits the error code specified by {hparam}`whichError` to anyone that's
receiving notifications from this node (see
{cpp:func}`BMediaRoster::StartWatching`
and {cpp:func}`BMediaRoster::StopWatching`
on  ). If {hparam}`info` isn't {cpp:enum}`NULL`, it's used as
a model message for the error notification message.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- The error report was sent without error.
-
	- BMessageerrors.
	- The message couldn't be sent.
:::
::::

::::{abi-group}

:::{cpp:function} virtual status_t BMediaNode::RequestCompleted(const media_request_info& info = NULL)
:::
This function is called whenever a request issued by the node is
completed. The {hparam}`info` structure describes the results
of the request.
The change_tag field in the
{hparam}`info` structure identifies the request that has
been completed; this is the same value passed into the function that
initiated the request.
Return {cpp:enum}`B_OK` if you're happy, otherwise return
an appropriate error code.
::::

::::{abi-group}

:::{cpp:function} run_mode BMediaNode::RunMode() const
:::
{hmethod}`RunMode()` returns the node's current
{cpp:func}`~Enums::run`
setting.
The {hmethod}`SetRunMode()` hook function is called
when someone requests that your node's run mode be changed.
::::

::::{abi-group}

:::{cpp:function} virtual void BMediaNode::Seek(bigtime_t mediaTime, bigtime_t performanceTime)
:::
This hook function is called when a node is asked to seek to the
specified {hparam}`mediaTime` by a call to the
{cpp:class}`BMediaRoster`.
The specified {hparam}`performanceTime`, the time at
which the node should begin the seek operation, may be in the future.
:::{admonition} Note
:class: note
Your node is required to queue at least one each of start, stop, and
seek requests, so that applications can establish, for example, both the
start and stop time without having to monitor your node's progress. The
actual size of these three queues is up to you. When the specified time
arrives, the request should be filled.
:::
A {hparam}`mediaTime` value of 0 indicates the
beginning of the media data.
::::

::::{abi-group}

:::{cpp:function} virtual void BMediaNode::SetTimeSource(BTimeSource* timeSource)
:::
:::{cpp:function} BTimeSource* BMediaNode::TimeSource() const
:::
The {hmethod}`SetTimeSource()` hook function
is called when someone has requested
that the node be slaved to a new time source. Augment this function to
make whatever adjustments you need to make to operate at the new time
scale.
{hmethod}`TimeSource()` returns a pointer to the
{cpp:class}`BTimeSource`
to which the node is
currently slaved. If no time source has been explicitly requested, the
system time source is in use, and that's what gets returned.
:::{admonition} Warning
:class: warning
The
{cpp:class}`BTimeSource`
object returned by {hmethod}`TimeSource()` is only valid
until the next call to
{cpp:func}`~BMediaNode::HandleMessage`
on that object. Therefore, if your node runs more than one thread, you need
to serialize calls to {hmethod}`TimeSource()` (as
well as usage of the returned objects) with calls to
{cpp:func}`~BMediaNode::HandleMessage`
This isn't a problem if you follow the recommended policy of running a
single thread that monitors the service port with
{cpp:func}`~read::port`
and calls
{cpp:func}`~BMediaNode::HandleMessage`
only when a message is actually received.
:::
::::

::::{abi-group}

:::{cpp:function} virtual void BMediaNode::Start(bigtime_t performanceTime)
:::
This hook function is called when a node is started by a call to the
{cpp:class}`BMediaRoster`.
The specified {hparam}`performanceTime`, the time
at which the node should start running, may be in the future.
:::{admonition} Note
:class: note
Your node is required to queue at least one each of start, stop, and
seek requests, so that applications can establish, for example, both the
start and stop time without having to monitor your node's progress. The
actual size of these three queues is up to you. When the specified time
arrives, the request should be filled.
:::
::::

::::{abi-group}

:::{cpp:function} virtual void BMediaNode::Stop(bigtime_t performanceTime, bool immediate)
:::
This hook function is called when a node is stopped by a call to the
{cpp:class}`BMediaRoster`.
The specified {hparam}`performanceTime`, the time at
which the node should stop, may be in the future.
If {hparam}`immediate` is {cpp:enum}`true`,
your node should ignore the {hparam}`performanceTime` value
and synchronously stop performance. When {hmethod}`Stop()`
returns, you're promising not to write into any
{cpp:class}`BBuffer`s
you may have received from your downstream
consumers, and you promise not to send any more buffers until
{cpp:func}`~BMediaNode::Start`
is called again.
:::{admonition} Note
:class: note
Your node is required to queue at least one each of start, stop, and
seek requests, so that applications can establish, for example, both the
start and stop time without having to monitor your node's progress. The
actual size of these three queues is up to you. When the specified time
arrives, the request should be filled.
:::
Nodes must recycle all buffers they may be holding onto when they're
stopped.
::::

::::{abi-group}

:::{cpp:function} virtual void BMediaNode::TimeWarp(bigtime_t atRealTime, bigtime_t newPerformanceTime)
:::
This hook function is called when the time source to which the node
is slaved is repositioned (via a seek operation) such that there will be a
sudden jump in the performance time progression as seen by the node. The
{hparam}`newPerformanceTime` argument indicates the new
performance time; the change should occur at the real time specified by the
{hparam}`atRealTime` argument.
The node should respond to this call by preparing for this change, so a
serious stutter, failure, or acceleration in performance doesn't occur.
Appropriate measures should be taken to minimize the impact on the
performance quality; for example, a segment of the sound could be looped
or skipped smoothly.
Your implementation of {hmethod}`TimeWarp()` should call through to
{hmethod}`BMediaNode::TimeWarp()`
as well as all other inherited forms of {hmethod}`TimeWarp()`.
::::

::::{abi-group}

:::{cpp:function} status_t BMediaNode::WaitForMessage(bigtime_t waitUntil, uint32 flags = 0, void* _reserved_ = NULL)
:::
This function waits until either real time specified by
{hparam}`waitUntil` or a
message is received on the control port.. The {hparam}`flags` are currently unused
and should be 0.
When a message is received, the appropriate
{cpp:func}`~BMediaNode::HandleMessage`
calls are made given the class derivation of the node:
- {cpp:func}`BMediaNode::HandleMessage` is always called first.
- If the node is derived from {cpp:class}`BBufferProducer`, and the message hasn't been handled yet, {cpp:func}`BBufferProducer::HandleMessage` is called.
- If the node is derived from {cpp:class}`BBufferConsumer`, and the message hasn't been handled yet, {cpp:func}`BBufferConsumer::HandleMessage` is called.
- If the node is derived from {cpp:class}`BFileInterface`, and the message hasn't been handled yet, {cpp:func}`BFileInterface::HandleMessage` is called.
- If the node is derived from {cpp:class}`BControllable`, and the message hasn't been handled yet, {cpp:func}`BControllable::HandleMessage` is called.
- If the node is derived from {cpp:class}`BTimeSource`, and the message hasn't been handled yet, {cpp:func}`BTimeSource::HandleMessage` is called.
- If the message still hasn't been handled, the most-derived interface's {hmethod}`HandleMessage()` function is called.
- If the message hasn't been handled, {cpp:func}`~BMediaNode::HandleBadMessage` is called.

Once this has been done, {hmethod}`WaitForMessage()`
returns. As you can see, this can be called from your control port to handle much of the work of
processing received messages.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- A message has occurred within the given time period.
-
	- {cpp:enum}`B_TIMED_OUT`
	- The time {hparam}`waitUntil` has arrived without a message being received.
:::
::::

## Constants
::::{abi-group}

Declared in: media/MediaNode.h
The node_error type defines the errors a node
can transmit to
{cpp:class}`BMessenger`s
that have registered to watch the node.
:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_NODE_FAILED_START`
	- The node failed on a {cpp:func}`~BMediaNode::Start` request.
-
	- {cpp:enum}`B_NODE_FAILED_STOP`
	- The node failed on a {cpp:func}`~BMediaNode::Stop` request.
-
	- {cpp:enum}`B_NODE_FAILED_SEEK`
	- The node failed on a {cpp:func}`~BMediaNode::Seek` request.
-
	- {cpp:enum}`B_NODE_FAILED_SET_RUN_MODE`
	- The node's {cpp:func}`~Enums::run` couldn't be set.
-
	- {cpp:enum}`B_NODE_FAILED_TIME_WARP`
	- The node couldn't fulfill a time warp request.
-
	- {cpp:enum}`B_NODE_FAILED_PREROLL`
	- The node failed on a {cpp:func}`~BMediaNode::Preroll` request.
-
	- {cpp:enum}`B_NODE_FAILED_SET_TIME_SOURCE_FOR`
	- The node's time source couldn't be changed.
-
	- {cpp:enum}`B_NODE_IN_DISTRESS`
	- The node is suffering in general.
:::
::::

::::{abi-group}

Declared in: media/MediaNode.h
The run_mode type indicates how a node should cope if its performance
rate deviates from the desired rate.
:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_OFFLINE`
	- Keep data accurate, even if the performance lags or runs too fast. This is typically used when rendering to disk.When in offline mode the node doesn't need to worry about processing buffers at any particular time. Each buffer's performance time should be derived from the time stamped on the buffer, rather than from a {cpp:class}`BTimeSource`. In fact, you'll usually want to call {cpp:func}`~set::thread` to set your node's processing threads to a low priority while the node is in offline mode. This lets software render media to disk in an efficient manner, letting the user continue to work while the render occurs in the background.
-
	- {cpp:enum}`B_RECORDING`
	- Time-stamped buffers are being received from a node capturing them from the real world; these buffers are guaranteed to have a time stamp in the past (they're always "late").Recording mode should be used when data is being sampled from a physical input device. These devices always deliver buffers whose time stamps are in the past (they're stamped with the time at which they were sampled, which is of course in the past, unless you've stolen a time machine from a professor from the 27th century, in which case you're probably running BeOS R127.1 and this book is woefully obsolete).Using {cpp:enum}`B_RECORDING` mode serves to warn other nodes that the time stamps will be in the past.
-
	- {cpp:enum}`B_DECREASE_PRECISION`
	- If the performance starts to lag, try to catch up.In {cpp:enum}`B_DECREASE_PRECISION` mode, your node should attempt to catch up if it falls behind, by playing buffers of media data faster than normal. For audio, this might mean playing back at a higher sampling rate; for video, the frame rate might be temporarily boosted.
-
	- {cpp:enum}`B_INCREASE_LATENCY`
	- If the performance starts to lag, increase playout delay so buffers are delivered with less time to spare before they're needed.If your node gets behind in the {cpp:enum}`B_INCREASE_LATENCY` run mode, your node should increase its internal latency measurement and send call the {cpp:func}`~BBufferProducer::LateNoticeReceived` function in anyone above your node in the media stream.Your node should then try to produce each buffer earlier before the buffer's performance time from that point on, so there's more time for the buffers to reach their destination.This mode is intended to compensate for data streams in which throughput can vary over time. For example, if media data is being streamed over a network, traffic fluctuations may require your node to adapt by adding more buffering (latency).
-
	- {cpp:enum}`B_DROP_DATA`
	- If the performance starts to lag, skip data.When in {cpp:enum}`B_DROP_DATA` mode, your node should simply skip buffers if if falls behind. Note that you still receive the buffers, but you should ignore any that you must in order to keep playing as many buffers as possible at the correct performance times.
:::
::::
