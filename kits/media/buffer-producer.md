:::{cpp:class} BBufferProducer
:::

# BBufferProducer

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} explicit BBufferProducer::BBufferProducer(media_type producerType)
:::

Constructs the {hclass}`BBufferProducer` object. The
{hparam}`producerType` specifies the type of media data that will be output
by the node.

If the node will produce more than one type of data, your
{hclass}`BBufferProducer` subclass should set the kind to the default
(which is a wildcard value).

If your node has additional latency on startup, you should call
{cpp:func}`SetInitialLatency() <BBufferProducer::SetInitialLatency>` to
record this information. This might be the case if the buffers your node
produces are created from an input signal which refreshes infrequently,
such as a television signal.

:::{admonition} Note
:class: note
In BeOS Release 4.5.2 and earlier, the {hparam}`producerType` has a
default value; it no longer does, and you'll have to specify the media type
yourself.
:::
::::

## Member Functions

::::{abi-group}
:::{cpp:function} virtual status_t BBufferProducer::AdditionalBufferRequested(const media_source& source, media_buffer_id previousBufferID, bigtime_t previousTime, const media_seek_tag* previousTag)
:::

When a consumer calls
{cpp:func}`BBufferConsumer::RequestAdditionalBuffer`, this function is
called as a result. Its job is to call {cpp:func}`SendBuffer()
<BBufferProducer::SendBuffer>` to immediately send the next buffer to the
consumer.

The {hparam}`previousBufferID`, {hparam}`previousTime`, and
{hparam}`previousTag` arguments identify the last buffer the consumer
received. Your node should respond by sending the next buffer after the one
described.

:::{admonition} Note
:class: note
The {hparam}`previousTag` may be {cpp:expr}`NULL`.
:::

Return {cpp:enumerator}`B_OK` if all is well; otherwise return an
appropriate error code.
::::

::::{abi-group}
:::{cpp:function} status_t BBufferProducer::ChangeFormat(const media_source& source, const media_destination& destination, media_format* newFormat)
:::

Informs the destination that the data flowing between source and
destination is immediately changing to the format specified by
{hparam}`newFormat.`

:::{admonition} Warning
:class: warning
You must never call {cpp:func}`SendBuffer() <BBufferProducer::SendBuffer>`
while this call is pending.
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
	- The format change request has been sent without error.
-
	- {cpp:enumerator}`B_MEDIA_CHANGE_IN_PROGRESS`.
	- A mutual exclusion error has occurred with {cpp:func}`SendBuffer()
		<BBufferProducer::SendBuffer>`; {hmethod}`ChangeFormat()` and
		{cpp:func}`SendBuffer() <BBufferProducer::SendBuffer>` can't both be
		running at the same time.
-
	- Other errors.
	- You may receive other errors if the consumer doesn't agree with the new
		format you're requesting.

:::
::::

::::{abi-group}
:::{cpp:function} static status_t BBufferProducer::ClipDataToRegion(int32 format, int32 byteCount, const void* clipData, BRegion* region)
:::

Given {hparam}`byteCount` bytes of clipping data {hparam}`clipDatain` the
specified {hparam}`format`, makes the specified {hparam}`region` match the
clipping region.

The {hparam}`region` you specify must already exist.

The only format currently supported is
{cpp:enumerator}`B_CLIP_SHORT_RUNS`.

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
	- The clip data was converted without error.
-
	- {cpp:enumerator}`B_MEDIA_BAD_CLIP_FORMAT`.
	- The specified clip format is invalid.

:::

See also: {cpp:func}`BBufferConsumer::RegionToClipData`
::::

::::{abi-group}
:::{cpp:function} virtual void BBufferProducer::Connect(status_t status, const media_source& source, const media_destination& destination, const media_format& format, char* ioName)
:::

Implement this hook function to establish a connection between the source
and the destination. The format negotiation is already complete by the time
{hmethod}`Connect()` is called, so you have to accept the specified
{hparam}`format`.

The {hparam}`status` argument indicates whether or not the connection
actually took place; this is the result code returned by the
{cpp:func}`BBufferConsumer::Connected` function or an error code indicating
an error that has occurred during other preparation for the connection.

If {hparam}`status` isn't {cpp:enumerator}`B_OK`, you should release the
{htype}`media_source` that was reserved for this connection by
{cpp:func}`PrepareToConnect() <BBufferProducer::PrepareToConnect>`; this
lets it be used by other connection attempts.

On entry, {hparam}`ioName` contains the connection name specified by the
consumer (this may be different from the name specified by the
{cpp:func}`PrepareToConnect() <BBufferProducer::PrepareToConnect>`
function). On return, {hparam}`ioName` should point to a name for the
connection; if the name really matters to you, copy the name you want the
connection to have back into {hparam}`ioName`; otherwise, you can leave it
alone.
::::

::::{abi-group}
:::{cpp:function} virtual void BBufferProducer::Disconnect(const media_source& source, const media_destination& destination) = 0
:::

Your implementation of {hmethod}`Disconnect()` should terminate the
connection between the specified {hparam}`source` and
{hparam}`destination`. Once you return from this function, you shouldn't
send any further buffers on the connection.

If a {cpp:class}`BBufferGroup` has been specified for your producer (via
the {cpp:func}`SetBufferGroup() <BBufferProducer::SetBufferGroup>`
function), you should delete it here.
::::

::::{abi-group}
:::{cpp:function} virtual status_t BBufferProducer::DisposeOutputCookie(int32 cookie) = 0
:::

Once a client has finished iterating through your outputs via
{cpp:func}`GetNextOutput() <BBufferProducer::GetNextOutput>` calls, it will
call this function with the last value you returned as a {hparam}`cookie`.
This gives you the opportunity to dispose of any memory you may have
allocated for the iteration process.

Return {cpp:enumerator}`B_OK` if the cookie is successfully disposed of
(or if nothing needs to be done); otherwise, return an appropriate error
code.
::::

::::{abi-group}
:::{cpp:function} virtual void BBufferProducer::EnableOutput(const media_source& whichOutput, bool enabled, int32* _deprecated_) = 0
:::

This hook function is called when a consumer's
{cpp:func}`SetOutputEnabled() <BBufferConsumer::SetOutputEnabled>` function
is called. This indicates whether or not the output specified by
{hparam}`whichOutput` needs to be sent buffers. You must implement this
function so that you don't send buffers to outputs that don't need them.
The {hparam}`_deprecated_` argument is no longer used.

By default, output is enabled.
::::

::::{abi-group}
:::{cpp:function} status_t BBufferProducer::FindLatencyFor(const media_destination& forDestination, bigtime_t* outLatency, media_node_id* outTimeSource) = 0
:::

{hmethod}`FindLatencyFor()` returns the latency introduced by sending data
to the destination {hparam}`forDestination`. On return, the latency will be
stored in {hparam}`outLatency`, and the time source used by
{hparam}`forDestination` will be available in {hparam}`outTimeSource`
(unless an error is returned, in which case these values are undetermined).

The latency of sending a buffer from one time source to another should
always be assumed to be zero, since there may be no relationship between
the progress of time of two different time sources.

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
	- The latency was returned without error.
-
	- {cpp:enumerator}`B_MEDIA_BAD_DESTINATION`.
	- The destination is invalid.
-
	- Port errors.
	- The request couldn't be sent to the destination.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BBufferProducer::FindSeekTag(const media_destination& forDestination, bigtime_t inTargetTime, media_seek_tag* outTag, bigtime_t* outTaggedTime, uint32* outFlags = 0, uint32* inFlags = 0)
:::

In order to improve seek performance, the Media Kit provides the concept
of seek tags. These are special tags that identify easily-located points in
media data (such as key frames in Cinepak video). The
{hmethod}`FindSeekTag()` function asks the consumer specified by
{hparam}`forDestination` for the nearest seek tag to the time specified by
{hparam}`inTargetTime`, and returns the tag in {hparam}`outTag` and the
time corresponding to that tag in {hparam}`outTaggedTime`. On return,
{hparam}`outFlags` (if the pointer isn't {cpp:expr}`NULL`) contains flags
giving further details about the tag.

There are currently no defined values for {hparam}`inFlags` or
{hparam}`outFlags`.

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
	- Port errors.
	- An error occurred communicating with the Media Server.

:::
::::

::::{abi-group}
:::{cpp:function} virtual status_t BBufferProducer::FormatChangeRequested(const media_source& source, const media_destination& destination, media_format* ioFormat, int32* _deprecated_) = 0
:::

Implement {hmethod}`FormatChangeRequested()` to change the format of the
media data flowing from the given {hparam}`source` to the specified
{hparam}`destination` to the format specified by {hparam}`ioFormat`. If
there are wildcards specified in {hparam}`ioFormat`, fill them in to match
the format you prefer before returning from this call. You should ignore
the {hparam}`_deprecated_` argument; it's no longer used.

:::{admonition} Warning
:class: warning
This call is issued synchronously by the destination, so you can't ask it
if the format is acceptable. Fortunately, since the destination issued the
request, you can safely assume that it's fine.
:::

Return {cpp:enumerator}`B_OK` if the change request is processed
successfully; otherwise, return an appropriate error code.

See also: {cpp:func}`FormatSuggestionRequested()
<BBufferProducer::FormatSuggestionRequested>`, {cpp:func}`FormatProposal()
<BBufferProducer::FormatProposal>`
::::

::::{abi-group}
:::{cpp:function} virtual status_t BBufferProducer::FormatProposal(const media_source& output, media_format* format) = 0
:::

Your {hclass}`BBufferProducer` should implement this function to verify
that the proposed {htype}`media_format` is suitable for the specified
{hparam}`output`. If any fields in the {hparam}`format` are wildcards, and
you have a specific requirement, adjust those fields to match your
requirements before returning.

Return {cpp:enumerator}`B_OK` if the proposed format is acceptable; once
you've done so, the Media Kit will assume that any connection request made
on output with the specified format (after any changes you may have made)
will succeed.

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
	- {cpp:enumerator}`B_BAD_SOURCE`
	- {hparam}`output` isn't available.
-
	- {cpp:enumerator}`B_BAD_MEDIA_FORMAT`
	- {hparam}`format` isn't reasonable.

:::
::::

::::{abi-group}
:::{cpp:function} virtual status_t BBufferProducer::FormatSuggestionRequested(media_type type, int32 quality, media_format* format) = 0
:::

You must implement {hmethod}`FormatSuggestionRequested()` to return fill
the buffer pointed to by format that your producer is capable of emitting
that meets the desired type and quality requirements.

If your producer can work with a range of possible formats, let the
quality argument guide your selection. For example, you might choose to use
10 fps for previews, and 60 fps interlaced 640x480 for full-quality video.

If {hparam}`type` is a media class that your producer doesn't want to work
with, return {cpp:enumerator}`B_BAD_MEDIA_FORMAT`. If you're preapared to
accept a wide range of values for some specific field, set that field to
the wildcard value (see media_audio_format::wildcard() and
media_video_format::wildcard() for more information.

Return {cpp:enumerator}`B_OK` if the {hparam}`format` is successfully
returned.
::::

::::{abi-group}
:::{cpp:function} virtual status_t BBufferProducer::GetLatency(bigtime_t* outLatency) = 0
:::

Implement this hook function to store, in {hparam}`outLatency`, the total
amount of latency your {hclass}`BBufferProducer` incurs from receiving a
buffer of data until it reaches its ultimate destination.

Call {cpp:func}`FindLatencyFor() <BBufferProducer::FindLatencyFor>` on
whatever outputs the data is being forwarded to, add your own latency to
the largest of those values, and return that value.

The default implementation of {hmethod}`GetLatency()` finds the maximum
latency of your currently-available outputs by iterating over them, and
returns that value in {hparam}`outLatency`; therefore, your implementation
of this function may simply need to call the inherited version of this
function, then add your own processing latency to the returned value.

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
	- The latency has been returned successfully.
-
	- Other errors.
	- Unable to calculate the latency.

:::
::::

::::{abi-group}
:::{cpp:function} virtual status_t BBufferProducer::GetNextOutput(int32* cookie, media_output* outOutput) = 0
:::

Implement this function to return information about your available
outputs. The first time it's called for a new iteration loop, the value
pointed to by {hparam}`cookie` will be 0. Each time
{hmethod}`GetNextOutput()` is called, you should set it to some value that
makes sense to you so you can keep track of where in the iteration process
the client is, but never set it to 0.

For each call to {hmethod}`GetNextOutput()`, including the first, you
should return one of your outputs that the client hasn't seen during the
iteration loop in {hparam}`outOutput`.

Once all outputs have been reported, you should return
{cpp:enumerator}`B_ERROR`.
::::

::::{abi-group}
:::{cpp:function} virtual status_t BBufferProducer::HandleMessage(int32 message, const void* data, size_t size)
:::

When your node derived from {hclass}`BBufferProducer` receives a message
on its control port, you should handle it yourself if you know how, or
dispatch to each ancestor class in turn (starting with
{hclass}`BBufferProducer`'s {hmethod}`HandleMessage()`) until one of the
{hmethod}`HandleMessage()` implementations returns {cpp:enumerator}`B_OK`.
If none of the inherited implementations of this function returns
{cpp:enumerator}`B_OK`, you should pass the message to
{cpp:func}`BMediaNode::HandleBadMessage` to be dealt with.

Your port-listening thread should call {hmethod}`HandleMessage()` to
dispatch the received data.

See also: "{cpp:func}`About Multiple Virtual Inheritance
<TheMediaKit::AboutMultipleVirtualInheritance>`"
::::

::::{abi-group}
:::{cpp:function} virtual void BBufferProducer::LatencyChanged(const media_source& source, const media_destination& destination, bigtime_t newLatency, uint32 flags)
:::

This hook function is called when a {cpp:class}`BBufferConsumer` that's
receiving data from you determines that its latency has changed. It will
call its {cpp:func}`BBufferConsumer::SendLatencyChange` function, and in
response, the Media Server will call your {hmethod}`LatencyChanged()`
function.

The {hparam}`source` argument indicates your output that's involved in the
connection, and {hparam}`destination` specifies the input on the consumer
to which the connection is linked. {hparam}`newLatency` is the consumer's
new latency. The {hparam}`flags` are currently unused.

Override this function to implement whatever functionality you need to
adjust your own latency calculations to keep the data flowing smoothly.
::::

::::{abi-group}
:::{cpp:function} virtual void BBufferProducer::LateNoticeReceived(const media_source& whichSource, bigtime_t howLate, bigtime_t performanceTime) = 0
:::

This hook function is called when a {cpp:class}`BBufferConsumer` that's
receiving data from you determines that data is arriving late (when the
{cpp:func}`BBufferConsumer::NotifyLateProducer` function is called); the
exact degree to which your buffers are late is specified by the
{hparam}`howLate` argument. Your implementation of this function should
take whatever steps are necessary to correct the problem, either by asking
nodes upstream from you to deliver buffers earlier, dropping buffers, or
other appropriate actions, depending on the current run mode.

The {hparam}`performanceTime` argument specifies the performance time at
which the notification was sent.

See also: {cpp:func}`BMediaNode::RunMode`
::::

::::{abi-group}
:::{cpp:function} virtual status_t BBufferProducer::PrepareToConnect(const media_source& whichSource, const media_destination& whichDestination, media_format* format, media_source* outSource, char* outName) = 0
:::

The {hmethod}`PrepareToConnect()` hook is called before a new connection
between the source {hparam}`whichSource` and the destination
{hparam}`whichDestination` is established, in order to give your producer
one last chance to specialize any wildcards that remain in the format
(although by this point there shouldn't be any, you should check anyway).

Your implementation should, additionally, return in {hparam}`outSource`
the source to be used for the connection, and should fill the
{hparam}`outName` buffer with the name the connection will be given; the
consumer will see this in the `outInput->name` argument specified to
{cpp:func}`BBufferConsumer::Connected`. If your node doesn't care what the
name is, you can leave the {hparam}`outName` untouched.

:::{admonition} Note
:class: note
Your {cpp:func}`Connect() <BBufferProducer::Connect>` function may return
a different {htype}`media_source` value in {hparam}`outOutput`'s source
field than the one specified as the {hparam}`source` argument to this
function. One reason you might do this is if you implement one
{htype}`media_source` to accept connection requests, then create a new
{htype}`media_source` to actually handle each connection.
:::

Return {cpp:enumerator}`B_OK` if the connection process should proceed, or
an appropriate error code if something's wrong.

If you return {cpp:enumerator}`B_OK`, the consumer's
{cpp:func}`Connected() <BBufferConsumer::Connected>` function will be
called, to let it know that a new connection is being established. Finally,
the producer's {hmethod}`Connect()` function is called to complete the
exchange.
::::

::::{abi-group}
:::{cpp:function} media_type BBufferProducer::ProducerType()
:::

Returns the {htype}`media_type` of the media data produced by the node.
::::

::::{abi-group}
:::{cpp:function} status_t BBufferProducer::ProposeFormatChange(media_format* format, const media_destination& forDestination)
:::

Call this function to determine whether or not the destination
{hparam}`forDestination` is prepared to accept buffers in the specified
{hparam}`format`. This function can be especially useful if you want to
test various formats to select the best compatible format during a hookup
request in which the requested format contains wildcards.

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
	- The proposed format is acceptable to the destination.
-
	- Other errors.
	- The proposed format is unacceptable, or an error occurred in querying the
		destination node.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BBufferProducer::SendBuffer(BBuffer* buffer, media_destination& destination)
:::

Call this function to send a buffer of media data to the specified
{hparam}`destination`, which must already be connected to one of your
outputs. This is how your {hclass}`BBufferProducer` object will send data
downstream to {cpp:class}`BBufferConsumer`s to which it's connected.

It's your responsibility to ensure that the buffer's header and the data
contained in the buffer itself are valid, although {hmethod}`SendBuffer()`
will automatically fill out the following header fields for you:

-   {hparam}`buffer`

-   {hparam}`for_id`

-   {hparam}`change_tag`

In particular, be sure that if you're outputting video buffers you set the
{htype}`media_video_buffer` to describe the video properly. If you don't,
things will go badly for you.

You can obtain a buffer to fill and send by calling
{cpp:func}`BBufferConsumer::RequestAdditionalBuffer` on a
{cpp:class}`BBufferConsumer` that you own (and that's okay to use for
buffers going to the specified destination).

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
	- The buffer was sent without error.
-
	- Port errors.
	- An error occurred sending the buffer.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BBufferProducer::SendDataStatus(int32 status, media_destination& destination, bigtime_t atTime)
:::

Call this function to inform the specified {hparam}`destination` whether
or not there's data available from your producer node. Specify the
appropriate status flag as the {hparam}`status` argument, and the time at
which the status takes effect as the atTime argument.

Possible values for the status argument are:

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
	- There aren't any buffers ready for the destination.
-
	- {cpp:enumerator}`B_DATA_AVAILABLE`
	- There are buffers ready for the destination.
-
	- {cpp:enumerator}`B_PRODUCER_STOPPED`
	- The producer has stopped.

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
	- The status update was sent without error.
-
	- Port errors.
	- The status update couldn't be delivered.

:::
::::

::::{abi-group}
:::{cpp:function} virtual status_t BBufferProducer::SetBufferGroup(const media_source& forSource, BBufferGroup* group) = 0
:::

When a client wants a specific {cpp:class}`BBufferGroup` to be used for a
given output {hparam}`forSource`, it will call this function. You should
remember the {hparam}`group` and use it for all requests for buffers to
send on the output forSource (and for no other outputs, unless the client
explicitly requests you do so by calling {hmethod}`SetBufferGroup()` for
another output source).

If your {hclass}`BBufferProducer` goes away, or the connection is broken,
delete the {cpp:class}`BBufferGroup` object.

If {hparam}`group` is {cpp:expr}`NULL`, you should use whatever
{cpp:class}`BBufferGroup` you wish after disposing of the previous group.

It's okay to pass {hparam}`group` on to another node upstream from your
{hclass}`BBufferProducer` if your {hclass}`BBufferProducer` only passes
along buffers it receives in its processing loop; in that case, you're not
really the owner of the {cpp:class}`BBufferGroup`, unless you pass
{cpp:expr}`true` for {hparam}`willReclaim` in the call to
{cpp:func}`BBufferConsumer::SetOutputBuffersFor`.

Return {cpp:enumerator}`B_OK` if the buffer group is set without incident;
otherwise, return an appropriate error code.
::::

::::{abi-group}
:::{cpp:function} void BBufferProducer::SetInitialLatency(bigtime_t initialLatency, uint32 flags) = 0
:::

If your node has additional startup latency imposed by the signal from
which its buffers are constructed, you should call
{hmethod}`SetInitialLatency()` to specify the maximum possible latency that
can be added by this delay. {hparam}`initialLatency` should be the maximum
latency, in microseconds, that might occur.

One situation in which this occurs is for TV capture card nodes. An NTSC
television signal broadcasts a new field about every sixtieth of a second,
which means that if your node is started partway through one field being
received, you might have to wait as long as a sixtieth of a second for the
first complete frame to arrive. So the maximum latency in this situation is
a sixtieth of a second.

Setting the initial latency correctly can prevent consumers from having
problems synchronizing with your node, and can improve performance.

{hparam}`flags` should be 0 for now; there are no values defined yet.
::::

::::{abi-group}
:::{cpp:function} virtual status_t BBufferProducer::SetPlayRate(int32 numerator, int32 denominator)
:::

This function is called to tell the producer to resample the data rate by
the specified factor. Specifying a value of 1 (ie,
{hparam}`numerator`/{hparam}`denominator` = 1) indicates that the data
should be output at the same playback rate that it comes into the node at.
The format of the data should be unchanged.

For example, if you're playing a sound at 48 kHz, and you receive a call
to {hmethod}`SetPlayRate()` with a {hparam}`numerator` of 2 and a
{hparam}`demoninator` of 1 (double speed), you should resample so that you
move twice as fast through the source data while keeping the output rate
constant. You might do this by doing a brute-force resample to 24 kHz
(which would result in twice the data rate) or do time-compression (which
would retain the pitch).

As another example, if you're playing video at 30 frames per second, and
your {hmethod}`SetPlayRate()` function is called with a ratio of 1:2
specified (half speed), you should continue sending 30 frames per second,
but you need to arrange for the playback to look like half-speed. A
reasonable way to do this would be to send each frame twice
(re-time-stamped and buffered internally, if necessary), which would result
in the desired half-speed appearance.

Return {cpp:enumerator}`B_OK` if the sampling rate is changed; otherwise,
return an error. It's okay to return an error if you don't support varying
sampling rates—the Media Kit won't hold that against you.
::::

::::{abi-group}
:::{cpp:function} virtual status_t BBufferProducer::VideoClippingChanged(const media_source& forSource, int16 numShorts, int16* clipData, const media_video_display_info& display, int32* outFromChangeTag) = 0
:::

This hook function is called when a client wants your
{hclass}`BBufferProducer` to output video data clipped to a particular
region. Your producer must remember this clipping region and apply it to
all video data you produce, without altering any bytes outside the region
in any buffers sent through the source {hparam}`forSource`.

Before your implementation of {hmethod}`VideoClippingChanged()` returns,
you should set the value pointed to by {hparam}`outFromChangeTag` to the
change tag value at which the clipping will take effect, so the client will
know what buffers it can expect to have the requested clipping. This can be
done easily by adding the following line to your implementation:

:::{code} cpp
*outFromChangeTag = UpdateChangeTag();
:::

You can use the {cpp:func}`ClipDataToRegion()
<BBufferProducer::ClipDataToRegion>` function to convert the data in
{hparam}`clipData` into an actual {cpp:class}`BRegion` if that's a better
format for you to work with. If you do, keep in mind that
{hparam}`numShorts` is the actual number of {htype}`int16` values in the
array specified by {hparam}`clipData`, while {cpp:func}`ClipDataToRegion()
<BBufferProducer::ClipDataToRegion>` requires the number of bytes of data
in the array; be sure to multiply {hparam}`numShorts` by `sizeof(int16)`.

The {htype}`media_video_display_info` structure referred to by display
indicates the format of the video display onto which the video is being
displayed; this lets you know what color space, screen size, and so forth
is in use on the video display, so your producer can render properly.
{hmethod}`VideoClippingChanged()` is called not only when clipping changes,
but when the configuration of the display changes as well. Your producer
must abide by this starting at the specified change count.

See  "{ref}`Video Clipping`" for information on the format of the clip
data.
::::

## Constants

### Clipping Data Formats

Declared in: media/BufferProducer.h

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
	- {cpp:enumerator}`B_CLIP_SHORT_RUNS`.
	- Clipping is encoded using runs of shorts.

:::

This value defines the only clipping format currently supported by
{hclass}`BBufferProducer`. Note that because this constant is a member of
the {hclass}`BBufferProducer` class, if you need to access it from other
classes, you must code it as `BBufferProducer::B_CLIP_SHORT_RUNS`. See
"{ref}`Video Clipping`" for a description of this format.

### suggestion_quality

Declared in: media/BufferProducer.h

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
	- {cpp:enumerator}`B_ANY_QUALITY`
	- Any quality.
-
	- {cpp:enumerator}`B_LOW_QUALITY`
	- A low quality level (10).
-
	- {cpp:enumerator}`B_MEDIUM_QUALITY`
	- Medium quality level (50).
-
	- {cpp:enumerator}`B_HIGH_QUALITY`
	- High quality level (100).

:::

Quality values you can use when you don't want to have to come up with one
on your own.
