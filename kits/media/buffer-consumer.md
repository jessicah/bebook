:::{cpp:class} BBufferConsumer
:::

# BBufferConsumer

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BBufferConsumer::BBufferConsumer(media_type consumerType)
:::

The {hclass}`BBufferConsumer` constructor. Specify as
{hparam}`consumerType` the type of data the {hclass}`BBufferConsumer`
accepts.

:::{admonition} Note
:class: note
In BeOS Release 4.5.2 and earlier {hparam}`consumerType` has a default
value. It no longer does. You'll have to actually specify the media type
from now on.
:::
::::

::::{abi-group}
:::{cpp:function} BBufferConsumer::~BBufferConsumer()
:::

The {hclass}`BBufferConsumer` destructor. You can augment this to handle
whatever closing-out your consumer node requires.

If your node has created and set {cpp:class}`BBufferGroup`s for any
producers, you should delete them in the destructor.
::::

## Hook Functions

::::{abi-group}
:::{cpp:function} virtual status_t BBufferConsumer::AcceptFormat(const media_destination & destination, media_format* format) = 0
:::

Implement this hook function to check that the specified format is
reasonable for the specified destination, and to fill in any wildcard
fields for which your {hclass}`BBufferConsumer` has specific requirements.

If the format isn't reasonable (or is of a class that's unsuitable for
{hparam}`destination`), return {cpp:enumerator}`B_MEDIA_BAD_FORMAT`.

When {hmethod}`AcceptFormat()` returns {cpp:enumerator}`B_OK`, the Media
Kit will expect a connection request on {hparam}`destination` with the
specified {hparam}`format` not to fail due to a format incompatibility.

:::{admonition} Warning
:class: warning
Don't try to ask the upstream producer about the format; it's waiting
synchronously for your response, and doing so will cause deadlock.
:::
::::

::::{abi-group}
:::{cpp:function} virtual void BBufferConsumer::BufferReceived(BBuffer* buffer) = 0
:::

When a {cpp:class}`BBufferProducer` sends buffers to one of your
{hclass}`BBufferConsumer`'s inputs, it will eventually arrive here, at the
{hmethod}`BufferReceived()` function (usually after first being dispatched
by {cpp:func}`HandleMessage() <BBufferConsumer::HandleMessage>`).

Override this hook function to add the {hparam}`buffer` to your internal
playback queue, or to do whatever your node needs to do with buffers you
consume. If you implement both {cpp:class}`BBufferProducer` and
{hclass}`BBufferConsumer`, it's possible you might examine or alter the
data in the {hparam}`buffer` and then call
{cpp:func}`BBufferProducer::SendBuffer` to send it along to someone else.

If your processing of the buffer is long enough to cause the buffer to
become late, you should still process it as usual, but you should also call
{cpp:func}`NotifyLateProducer() <BBufferConsumer::NotifyLateProducer>` to
let the producer know things are starting to lag.

Information about the contents and timing requirements of the buffer can
be obtained by calling {cpp:func}`BBuffer::Header` on it.

:::{admonition} Warning
:class: warning
If you're writing a node, and receive a buffer with the
{cpp:enumerator}`B_SMALL_BUFFER` flag set, you must recycle the buffer
before returning.
:::
::::

::::{abi-group}
:::{cpp:function} virtual status_t BBufferConsumer::Connected(const media_source & destination, const media_format* format, media_input* outInput) = 0
:::

This hook function is called when a connection is being established to
your input destination from the specified source producer. The connection
will be composed of media data with the specified format (which you've
previously accepted via {cpp:func}`AcceptFormat()
<BBufferConsumer::AcceptFormat>`).

Your implementation of {hmethod}`Connected()` should do whatever
preparation you need to do to handle data input on the connection, and fill
out the {hparam}`outInput` buffer with information about the connection
from your node's point-of-view. You can set {hparam}`outInput`'s
destination field different from destination if destination is a global
connection-establishing input that's used to negotiate a connection, then
create a new input to actually handle the data stream.

:::{admonition} Note
:class: note
Since your {hclass}`BBufferConsumer` has already had the opportunity to
reject the specified format, it's poor form to return an error from this
function. You should only return an error if the resources needed to
establish the connection have become unavailable prior to the time
{hmethod}`Connected()` was called.
:::

On entry, {hparam}`outInput`'s name field contains the name given the
connection by the producer (this may be an empty string if the producer
didn't assign a name). Your consumer should always make sure there's a
valid name here, because it's a bad thing to have unnamed connections, and
there's no guarantee that the producer will fill this in. If you don't have
a good, descriptive name for a connection, the name should minimally
contain the name of the node and a number that makes the connection's name
unique (such as "MyNode Input 1" or "MyNode Output 3").

If you want the producer to use a specific {cpp:class}`BBufferGroup` (for
example, if you want a video producer to fill {cpp:class}`BDirectWindow`
buffers), you should create the {cpp:class}`BBufferGroup` here, then call
{cpp:func}`BBufferProducer::SetBufferGroup` to set the producer's buffer
group:

:::{code} cpp
BBufferGroup *buffers = new BBufferGroup;
BMediaRoster::Roster()->SetOutputBuffersFor(producer, buffers);
:::

Return {cpp:enumerator}`B_OK` if the connection is started safely,
otherwise, return an appropriate error code.
::::

::::{abi-group}
:::{cpp:function} virtual void BBufferConsumer::Disconnected(const media_source& producer, const media_destination& whichInput) = 0
:::

This hook function is called when a connection is being terminated. You
should do whatever needs to be done in order to ensure that future
inquiries about the {cpp:func}`media_source <media::source>` connected to
the {cpp:func}`media_input <media::input>` indicated by
{hparam}`whichInput` reference {htype}`media_source`::{htype}`null` (or, if
another connection is later established on the input, that producer).

If your consumer node has created and set a {cpp:class}`BBufferGroup` for
the producer, you shouldn't delete or reclaim it here, because the producer
has a clone of the {cpp:class}`BBufferGroup` that references the same
buffers; deleting the {cpp:class}`BBufferGroup` would free those buffers,
leaving the producer in deadlock. Instead, delete (or reclaim) the when
{cpp:func}`Connected() <BBufferConsumer::Connected>` is called again, and
be sure to delete any remaining {cpp:class}`BBufferGroup`s in your
destructor.
::::

::::{abi-group}
:::{cpp:function} virtual void BBufferConsumer::DisposeInputCookie(int32 cookie) = 0
:::

If the cookie value you return in {cpp:func}`GetNextInput()
<BBufferConsumer::GetNextInput>` is a pointer to an object that needs to be
deleted when the iteration process is completed, be sure to implement
{hmethod}`DisposeInputCookie()` to do so.
::::

::::{abi-group}
:::{cpp:function} virtual status_t BBufferConsumer::GetLatencyFor(const media_destination& forWhom, bigtime_t* outLatency, media_node_id* outTimeSource) = 0
:::

Implement this hook function to calculate the total latency for the
{cpp:func}`media_destination <media::destination>` specified by
{hparam}`forWhom` and store the resulting value in {hparam}`outLatency`.
Also, return the time source your node is slaved to in
{hparam}`outTimeSource`.

If your node is a {cpp:class}`BBufferProducer`

Return {cpp:enumerator}`B_OK` if you successfully compute the latency;
otherwise, return an appropriate error.
::::

::::{abi-group}
:::{cpp:function} virtual status_t BBufferConsumer::GetNextInput(int32 * cookie, media_input* outInput) = 0
:::

The first time a client calls this function, the value pointed to by
cookie will be 0. You should fill the buffer pointed to by
{hparam}`outInput` with information about your first input, and set the
value at {hparam}`cookie` to something (other than zero) that will let you
keep track of what to return the next time {hmethod}`GetNextInput()` is
called.

Each successive call to {hmethod}`GetNextInput()` will pass back, in
{hparam}`cookie`, the value you returned in {hparam}`cookie` the last time
the function was called by that client, and you should fill
{hparam}`outInput` with information about the next input, and store a new
value in {hparam}`cookie` to continue to track your progress through the
inputs.

:::{admonition} Note
:class: note
Whenever this function is called with a value of zero in cookie, you must
start over with the first input.
:::

When you reach the last input, return {cpp:enumerator}`B_BAD_INDEX` to
indicate that there aren't any more inputs.
::::

::::{abi-group}
:::{cpp:function} virtual status_t BBufferConsumer::HandleMessage(int32 message, const void* data, size_t size)
:::

When your node derived from {hclass}`BBufferConsumer` receives a message
on its control port, you should try dispatching it by calling
{hmethod}`HandleMessage()`. If {hclass}`BBufferConsumer` doesn't understand
the message, it'll return {cpp:enumerator}`B_ERROR` and you can try
dispatching it to another class from which your node is derived, or handle
it yourself.

If this function returns {cpp:enumerator}`B_OK`, the message has been
handled.

See also: {cpp:func}`BMediaNode::HandleMessage`, "{cpp:func}`About
Multiple Virtual Inheritance
<TheMediaKit::AboutMultipleVirtualInheritance>`"
::::

::::{abi-group}
:::{cpp:function} virtual void BBufferConsumer::ProducerDataStatus(const media_destination & destination, int32 status, bigtime_t atPerformanceTime) = 0
:::

This hook function is called to inform your consumer about changes in the
availability of buffers from the producer that's connected to the input
destination. The status argument specifies what change has occurred, and
{hparam}`atPerformanceTime` indicates when the change happened (or when it
will happen).

This lets you keep track of which inputs you should await data from; for
example, if your consumer is processing data arriving from four producers,
and one of them stops sending buffers to the consumer, the producer that's
stopping will cause a call to {hmethod}`ProducerDataStatus()` to let you
know not to await buffers anymore. This way, you know that when buffers
have arrived from the other three inputs, it's okay to begin processing the
buffers.

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
	- {cpp:enumerator}`B_DATA_NOT_AVAILABLE`
	- The producer doesn't have any data available.
-
	- {cpp:enumerator}`B_DATA_AVAILABLE`
	- The producer has data available.
-
	- {cpp:enumerator}`B_PRODUCER_STOPPED`
	- The producer has been stopped.

:::
::::

::::{abi-group}
:::{cpp:function} virtual status_t BBufferConsumer::SeekTagRequested(const media_destination& destination, bigtime_t inTargetTime, uint32 inFlags, media_seek_tag* outSeekTag, bigtime_t* outTaggedTime, uint32* outFlags)
:::

This function is provided to aid in supporting media formats in which the
outer encapsulation layer doesn't supply timing information. Producers will
tag the buffers they generate with seek tags; these tags can be used to
locate key frames in the media data.

It's the consumer's job to match up seek tags with performance times. As
the consumer processes each incoming buffer, it should cache the seek tag
and the performance time at which it occurs (if there's a tag on the
buffer). When the producer needs to know the seek tag and corresponding
time that's closest to a given performance time, this function is
resonsible for returning that information.

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
	- No error.
-
	- Other errors.
	- Depend on the node's implementation.

:::

See also: "{ref}`Seek Tags`"
::::

## Member Functions

::::{abi-group}
:::{cpp:function} media_type BBufferConsumer::ConsumerType()
:::

Returns the type of media the {hclass}`BBufferConsumer` consumes.
::::

::::{abi-group}
:::{cpp:function} void BBufferConsumer::NotifyLateProducer(const media_source & source, bigtime_t howLate, bigtime_t performanceTime)
:::

Notifies the {cpp:class}`BBufferProducer` specified by source that it's
running late by {hparam}`howLate` microseconds; the notification conditions
as of the specified {hparam}`performanceTime`. Call this function when you
detect that data is arriving too late and the run mode is
{cpp:enumerator}`B_DECREASE_PRECISION`,
{cpp:enumerator}`B_INCREASE_LATENCY`, or {cpp:enumerator}`B_DROP_DATA` (any
of which permits adjustment of the media playback to maintain timeliness).

The producer should process this notification immediately and take the
appropriate action.
::::

::::{abi-group}
:::{cpp:function} static status_t BBufferConsumer::RegionToClipData(const BRegion* region, int32* format, int32* ioSize, void* data)
:::

Converts a {cpp:class}`BRegion` into the clipping format used internally
by the Media Kit. Prior to calling {hmethod}`RegionToClipData()`,
{hparam}`ioSize` is set to the size of the buffer pointed to by
{hparam}`data`. On return, {hparam}`format` is the format of the clipping
data, {hparam}`ioSize` is changed to the actual number of bytes of data
returned, and {hparam}`data` contains the actual clipping data.

The clip data format is described in the section "{ref}`Video Clipping`".

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
	- Clip data returned without errors.
-
	- {cpp:enumerator}`B_NO_MEMORY`.
	- The data buffer isn't big enough.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BBufferConsumer::RequestAdditionalBuffer(const media_source& source, BBuffer* previousBuffer, void* _reserved_ = NULL)
:::

:::{cpp:function} status_t BBufferConsumer::RequestAdditionalBuffer(const media_source& source, bigtime_t startTime, void* _reserved_ = NULL)
:::

Asks the upstream producer specified by {hparam}`source` to immediately
send the next buffer, instead of waiting until the appropriate time. The
most obvious use for this function is in cases where a codec requires
multiple buffers in order to decode a frame of output (MPEG is a good
example).

The requested buffer can be identified either by a {hparam}`startTime`
parameter, which indicates the time for which a buffer is requested, or by
a {hparam}`previousBuffer`, which specifies the buffer prior to the one
being requested.

This function will cause the producer's
{cpp:func}`AdditionalBufferRequested()
<BBufferProducer::AdditionalBufferRequested>` function to be called.

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
	- The change was requested successfully.
-
	- {cpp:enumerator}`B_MEDIA_BAD_SOURCE`.
	- The source isn't valid.
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- The {hparam}`previousBuffer` pointer is {cpp:expr}`NULL`.
-
	- {cpp:enumerator}`B_TIMEOUT`.
	- The request to the Media Server timed out.
-
	- {cpp:enumerator}`Port errors`.
	- An error occurred communicating with the Media Server.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BBufferConsumer::RequestFormatChange(const media_source& source, const media_destination& destination, media_format& toFormat, void* userData, const media_destination& changeTag, void* _reserved_ = NULL)
:::

:::{cpp:function} virtual status_t BBufferConsumer::FormatChanged(const media_source& source, const media_destination& destination, media_format& newFormat) = 0
:::

{hmethod}`RequestFormatChange()` requests that the producer
{hparam}`source` connected to the consumer {hparam}`destination` change the
format it produces to the format specified by {hparam}`toFormat`. The Media
Kit returns in {hparam}`changeTag` the tag value that will be received by
your {cpp:func}`RequestCompleted() <BMediaNode::RequestCompleted>` function
once the change takes effect; the change tag lets you match up the call to
{cpp:func}`RequestCompleted() <BMediaNode::RequestCompleted>` with this
request. This function will receive a {ref}`media_request_info` structure
with the indicated {hparam}`userData` and {hparam}`changeTag`.

{hmethod}`FormatChanged()` is called by the upstream producer when the
media format your node will be receiving changes, and indicates the new
format in {hparam}`newFormat` and the change tag value at which the new
format will take effect in {hparam}`changeTag`. You should implement this
function so your node will know that the data format is going to change.
Note that this may be called in response to your {cpp:func}`AcceptFormat()
<BBufferConsumer::AcceptFormat>` call, if your {cpp:func}`AcceptFormat()
<BBufferConsumer::AcceptFormat>` call alters any wildcard fields in the
specified format.

:::{admonition} Note
:class: note
Because {hmethod}`FormatChanged()` is called by the producer, you don't
need to (and shouldn't) ask it if the new format is acceptable.
:::

If the format change isn't possible, return an appropriate error from
{hmethod}`FormatChanged()`; this error will be passed back to the producer
that initiated the new format negotiation in the first place.

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
	- No error.
-
	- {cpp:enumerator}`B_MEDIA_BAD_SOURCE`.
	- The specified {hparam}`source` isn't valid.
-
	- {cpp:enumerator}`B_MEDIA_BAD_DESTINATION`.
	- The specified {hparam}`destination` is invalid.
-
	- Port errors.
	- See Ports.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BBufferConsumer::SendLatencyChange(const media_source& source, const media_destination& destination, bigtime_t newLatency, uint32 flags = 0)
:::

Lets the upstream producer know that the consumer node's latency has
changed. {hparam}`newLatency` indicates your new latency, in microseconds.
The flags are currently unused and should always be 0.

You should call this whenever something happens to cause a change in your
latency.

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
	- No error.
-
	- {cpp:enumerator}`B_MEDIA_BAD_SOURCE`.
	- The {hparam}`source` is invalid.
-
	- {cpp:enumerator}`B_MEDIA_BAD_DESTINATION`.
	- The {hparam}`destination` is invalid.
-
	- {cpp:enumerator}`B_TIMED_OUT`.
	- The attempt to communicate with the Media Server timed out.
-
	- Port errors.
	- An error occurred communicating with the Media Server.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BBufferConsumer::SetOutputBuffersFor(const media_source& source, const media_destination& destination, BBufferGroup* group, void* userData, int32* changeTag, bool willReclaim = false, void* _reserved_ = NULL)
:::

Specifies that the {cpp:class}`BBufferGroup` group will provide the
buffers for the connection between source and destination. If
{hparam}`willReclaim` is {cpp:expr}`false`, the Media Kit will dispose of
the group for you; you can forget about it once this call returns.
Otherwise, you're informing the Media Server that you want the group back,
and that you'll delete it when you're done with it.

The Media Kit returns in {hparam}`changeTag` the tag value that will be
received by your {cpp:func}`RequestCompleted()
<BMediaNode::RequestCompleted>` function once the change takes effect; the
change tag lets you match up the call to {cpp:func}`RequestCompleted()
<BMediaNode::RequestCompleted>` with this request. This function will
receive a {ref}`media_request_info` structure with the indicated
{hparam}`userData` and {hparam}`changeTag`.

The ability to request that certain buffers be used by a particular output
can save you from having to perform unnecessary copies; you might be able
to use {cpp:class}`BBuffer`s that represent a graphics card frame buffer,
for example, so that a video producer's output goes directly to video
memory.

:::{admonition} Note
:class: note
Before reclaiming your buffers, be sure to call
`SetOutputBuffersFor(output, NULL)` to let the Media Kit know your producer
no longer has permission to use them. If you forget this step, the producer
will hang onto the buffers until it's deleted, and your
{cpp:func}`BBufferGroup::ReclaimAllBuffers` call will hang, possibly
forever.
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
	- The change was requested successfully.
-
	- Other errors.
	- The change could not be made.

:::
::::

::::{abi-group}
:::{cpp:function} static status_t BBufferConsumer::SetOutputEnabled(const media_source& source, const media_destination& destination, bool enabled, void* userData, int32* changeTag, void* _reserved_ = NULL)
:::

Specifies whether or not the specified output should be transmitting
buffers to the destination. If {hparam}`enabled` is {cpp:expr}`true`, the
producer should transmit buffers; otherwise it should not.

The Media Kit returns in {hparam}`changeTag` the tag value that will be
received by your {cpp:func}`RequestCompleted()
<BMediaNode::RequestCompleted>` function once the change takes effect; the
change tag lets you match up the call to {cpp:func}`RequestCompleted()
<BMediaNode::RequestCompleted>` with this request. This function will
receive a {htype}`media_request_info` structure with the indicated
{hparam}`userData` and {hparam}`changeTag`.

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
	- The change was requested successfully.
-
	- {cpp:enumerator}`B_MEDIA_BAD_SOURCE`
	- The source is invalid.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BBufferConsumer::SetVideoClippingFor(const media_source& output, const media_destination& destination, const int16* shortsList, int32 shortCount, const media_video_display_info& display, void* userData, int32* changeTag, void* _reserved_ = NULL)
:::

This function requests that video buffers sent by the specified output to
the specified destination clip all its writing in buffers it sends to the
{hclass}`BBufferConsumer` to the clipping region described by
{hparam}`shortsList` and {hparam}`shortCount`. The clip data format is
described in the section "{ref}`Video Clipping`".

The Media Kit returns in changeTag the tag value that will be received by
your {cpp:func}`RequestCompleted() <BMediaNode::RequestCompleted>` function
once the change takes effect; the change tag lets you match up the call to
{cpp:func}`RequestCompleted() <BMediaNode::RequestCompleted>` with this
request. This function will receive a {ref}`media_request_info` structure
with the indicated {hparam}`userData` and {hparam}`changeTag`.

The {ref}`media_video_display_info` structure referenced by display
describes the current configuration of the video in terms of color space,
resolution, and so forth.

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
	- The clipping request has been sent without errors.
-
	- {cpp:enumerator}`B_MEDIA_BAD_CLIP_FORMAT`
	- The clipping data isn't formatted correctly.
-
	- Port errors
	- See {ref}`Ports`.

:::
::::
