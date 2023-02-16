:::{cpp:class} BMediaRoster
:::

# BMediaRoster

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BMediaRoster::BMediaRoster()
:::

You never construct a {hclass}`BMediaRoster` yourself. Instead, use the
static {cpp:func}`Roster() <BMediaRoster::Roster>` function to obtain an
instance of the {hclass}`BMediaRoster` class that you can use.
::::

::::{abi-group}
:::{cpp:function} virtual BMediaRoster::~BMediaRoster()
:::

You never delete a {hclass}`BMediaRoster` yourself. Just let it go away
automatically when your application shuts down.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} ssize_t BMediaRoster::AudioBufferSizeFor(int32 channelCount, uint32 sampleFormat, float frameRate, bus_type busKind)
:::

{hmethod}`AudioBufferSizeFor()` returns the size, in bytes, that the Media
Kit recommends for audio data with {hparam}`channelCount` channels, with
the specified {hparam}`sampleFormat` and {hparam}`frameRate`.

The {hparam}`busKind` argument is a {htype}`bus_type` value (see
drivers/config_manager.h) indicating the type of bus the data is moving
across. Specify {cpp:enumerator}`B_UNKNOWN_BUS` if you don't know.
::::

::::{abi-group}
:::{cpp:function} status_t BMediaRoster::Connect(const media_source& source, const media_destination& destination, media_format* ioFormat, media_output* outOutput, media_input* outInput)
:::

:::{cpp:function} status_t BMediaRoster::Connect(const media_source& source, const media_destination& destination, media_format* ioFormat, media_output* outOutput, media_input* outInput, uint32 inFlags, void* _reserved = NULL)
:::

:::{cpp:function} status_t BMediaRoster::Disconnect(media_node_id sourceNode, const media_source& source, media_node_id destinationNode, const media_destination& destination)
:::

{hmethod}`Connect()` negotiates a connection from the {hparam}`source` to
the {hparam}`destination`, using the media format specified in
{hparam}`ioFormat` as a basis for the negotiation; {hparam}`ioFormat` is
changed to the negotiated format before this call returns. This describes
the format of media data that will flow across the connection.

The actual connection is returned as an output and an input in
{hparam}`outOutput` and {hparam}`outInput`. These two structures contain
the data format as interpreted by the source and destination. There may be
differences among these formats if wildcard fields were used in the
original format.

The second form of {hmethod}`Connect()` lets you specify connect flags.
Currently the only possible flag is {cpp:enumerator}`B_CONNECT_MUTED`,
which indicates that the connection should be muted on creation.

The actual {cpp:func}`media_source <media::source>` and
{cpp:func}`media_destination <media::destination>` used for the connection
may vary from those passed into {hmethod}`Connect()` if the source or the
destination creates new sources or destinations for each connection
request; the {hparam}`outOutput` and {hparam}`outInput` structures contain
the actual {cpp:func}`media_source <media::source>` and
{cpp:func}`media_destination <media::destination>` values resulting from
the call.

For more detailed information on the use of wildcards in format
negotiation, see media_audio_format::wildcard and
media_video_format::wildcard. A {cpp:func}`media_format <media::format>`
with a type of {cpp:enumerator}`B_MEDIA_UNKNOWN_TYPE` matches any media
class and format, although without specific knowledge of the source and
destination, this will rarely result in a useful connection.

{hmethod}`Disconnect()` breaks the connection established between
{hparam}`source` and {hparam}`destination`, which must belong to the nodes
{hparam}`sourceNode` and {hparam}`destinationNode`, repectively.

The result of breaking a connection that's currently running is undefined,
but is not permitted to crash. Your application should stop both nodes
involved in a connection prior to disconnecting them.

:::{admonition} Note
:class: note
These functions will deadlock if called from a node's control thread or
while the control thread is blocked.
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
	- {cpp:enumerator}`B_OK`
	- No error terminating the connection.
-
	- {cpp:enumerator}`B_NAME_NOT_FOUND`
	- The connection couldn't be made.
-
	- Other errors.
	- The nodes that are being connected may return other error codes as they
		see fit.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaRoster::GetAllInputsFor(const media_node& node, media_input* outInputs, int32 bufNumInputs, int32* outTotalCount)
:::

:::{cpp:function} status_t BMediaRoster::GetAllOutputsFor(const media_node& node, media_output* outOutputs, int32 bufNumOutputs, int32* outTotalCount)
:::

{hmethod}`GetAllInputsFor()` fills the array of {cpp:func}`media_input
<media::input>` structures specified by {hparam}`outInputs` with
information about all inputs belonging to node; the number of elements that
{hparam}`outInputs` can hold is passed in {hparam}`bufNumInputs`.

Similarly, {hmethod}`GetAllOutputsFor()` fills the array
{hparam}`outOutputs` with information about all outputs from the specified
node.

Both functions return the number of elements actually returned in the
buffer in {hparam}`outTotalCount`. If this number is less than the number
you requested, your buffer was too small to receive all the results of the
query. In this case, you might want to resize your array and try again.

:::{admonition} Note
:class: note
These functions will deadlock if called from a node's control thread or
while the control thread is blocked.
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
	- {cpp:enumerator}`B_OK`
	- No error.
-
	- {cpp:enumerator}`B_MEDIA_BAD_NODE`
	- The node isn't of the correct type for the call you issued.
-
	- Other errors.
	- An error occurred communicating with the producer or with the Media
		Server.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaRoster::GetAudioInput(media_node* outNode)
:::

:::{cpp:function} status_t BMediaRoster::GetVideoInput(media_node* outNode)
:::

These functions return the nodes designated by the user as the preferred
nodes for audio and video input. You can then query the returned node, hook
into it, and manipulate it, using the reference returned in
{hparam}`outNode`.

Once your application has finished using these nodes (and they've been
stopped and disconnected), you should release them by calling
{hmethod}`ReleaseNode()`.

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
	- {cpp:enumerator}`B_OK`
	- No error locating the default input node.
-
	- {cpp:enumerator}`B_NAME_NOT_FOUND`
	- The default node couldn't be identified.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaRoster::GetAudioOutput(media_node* outNode)
:::

:::{cpp:function} status_t BMediaRoster::GetAudioOutput(media_node* outNode, int32* outInputID, BString* outInputName)
:::

:::{cpp:function} status_t BMediaRoster::GetVideoOutput(media_node* outNode)
:::

:::{cpp:function} status_t BMediaRoster::GetAudioMixer(media_node* outNode)
:::

These functions return the nodes designated by the user as the preferred
nodes for audio and video output. You can then query the returned node,
hook into it, and manipulate it, using the reference returned in
{hparam}`outNode`.

The second form of {hmethod}`GetAudioOutput()` returns additional
information, including the input ID of the input used for audio output, and
the input's name.

You should usually use {hmethod}`GetAudioMixer()` when getting a node for
playing audio instead of using the {hmethod}`GetAudioOutput()` function.
{hmethod}`GetAudioOutput()` returns the lower-level node for audio output,
which you would typically only need access to if you wanted to do some form
of processing on all audio data being played in the system (such as a level
meter).

The {hmethod}`GetAudioMixer()` function returns a reference to the audio
mixer, which will perform audio mixing, format conversion, and sample rate
conversion for you, then pass along the audio to the output node.

Once your application has finished using these nodes (and they've been
stopped and disconnected), you should release them by calling
{cpp:func}`ReleaseNode() <BMediaRoster::ReleaseNode>`.

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
	- {cpp:enumerator}`B_OK`
	- No error locating the default input node.
-
	- {cpp:enumerator}`B_NAME_NOT_FOUND`
	- The default node couldn't be identified.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaRoster::GetConnectedInputsFor(const media_node& node, media_input* outActiveInputsList, int32 numListInputs, int32* outNumInputs)
:::

:::{cpp:function} status_t BMediaRoster::GetFreeInputsFor(const media_node& node, media_input* outFreeInputsList, int32 numListInputs, int32* outNumInputs, media_type filterType = B_MEDIA_UNKNOWN_TYPE)
:::

{hmethod}`GetConnectedInputsFor()` fills the array of
{cpp:func}`media_input <media::input>` structures specified by
{hparam}`outActiveInputsList` with information about all inputs belonging
to node that are currently connected to some output; the number of elements
that {hparam}`outActiveInputsList` can hold is passed in
{hparam}`numListInputs`.

Similarly, {hmethod}`GetFreeInputsFor()` fills the array
{hparam}`outFreeInputsList` with information about all inputs that are
still available in the specified node. Specifying a {hparam}`filterType`
other than {cpp:enumerator}`B_MEDIA_NO_TYPE` lets you obtain a list of
inputs for a specific media type (or for inputs that can handle any media
type). This is especially useful if you're only interested in a list of
accepted media types your application supports.

:::{admonition} Note
:class: note
Even though a node may report that a specific number of free inputs are
available, it is possible that a node might create more inputs on demand.
There is no way to know if this might happen, so
{hmethod}`GetFreeInputsFor()` may not tell you whether or not a node can
accept all the connections you'd like to make.
:::

Both functions return the number of elements actually returned in the
buffer in {hparam}`outNumInputs`. If this number is less than
{hparam}`numListInputs`, your buffer was too small to receive all the
results of the query. In this case, you might want to resize your array and
try again.

These functions will deadlock if called from a node's control thread or
while the control thread is blocked.

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
	- {cpp:enumerator}`B_OK`
	- No error cloning the node.
-
	- {cpp:enumerator}`B_NAME_NOT_FOUND`
	- The requested node couldn't be cloned.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaRoster::GetConnectedOutputsFor(const media_node& node, media_output* outActiveOutputsList, int32 numListOutputs, int32* outNumOutputs)
:::

:::{cpp:function} status_t BMediaRoster::GetFreeOutputsFor(const media_node& node, media_output* outFreeOutputsList, int32 numListOutputs, int32* outNumOutputs, media_type filterType = B_MEDIA_UNKNOWN_TYPE)
:::

{hmethod}`GetConnectedOutputsFor()` fills the array of
{cpp:func}`media_output <media::output>` structures specified by
{hparam}`outActiveOutputsList` with information about all outputs belonging
to node that are currently connected to some input; the number of elements
that {hparam}`outActiveOutputsList` can hold is passed in
{hparam}`numListOutputs`.

Similarly, {hmethod}`GetFreeOutputsFor()` fills the array
{hparam}`outFreeOutputsList` with information about all outputs that are
still available in the specified node. Specifying a {hparam}`filterType`
other than {cpp:enumerator}`B_MEDIA_UNKNOWN_TYPE` lets you obtain a list of
outputs for a specific media type (or for outputs that can handle any media
type). This is especially useful if you're only interested in a list of
accepted media types your application supports.

:::{admonition} Note
:class: note
Even though a node may report that a specific number of free outputs are
available, it is possible that a node might create more outputs on demand.
There is no way to know if this might happen, so
{hmethod}`GetFreeOutputsFor()` may not tell you whether or not a node can
accept all the connections you'd like to make.
:::

Both functions return the number of elements actually returned in the
buffer in {hparam}`outNumOutputs`. If this number is less than
{hparam}`numListOutputs`, your buffer was too small to receive all the
results of the query. In this case, you might want to resize your array and
try again.

:::{admonition} Note
:class: note
These functions will deadlock if called from a node's control thread or
while the control thread is blocked.
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
	- {cpp:enumerator}`B_OK`
	- No error.
-
	- {cpp:enumerator}`B_MEDIA_BAD_NODE`
	- The node isn't a buffer producer.
-
	- Other errors.
	- An error occurred communicating with the producer or with the Media
		Server.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaRoster::GetDormantFlavorInfoFor(const dormant_node_info& inDormantNode, dormant_flavor_info* outFlavor)
:::

This function returns, in {hparam}`outFlavor`, information describing the
dormant flavors supported by the dormant node {hparam}`inDormantNode`.

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
	- {cpp:enumerator}`B_OK`
	- No error.
-
	- Messaging errors.
	- An error occurred communicating with the Media Server.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaRoster::GetDormantNodes(dormant_node_info* outDormantNodeList, int32* inOutNumNodes, const media_format* hasInputFormat = NULL, const media_format* hasOutputFormat = NULL, char* name = NULL, uint64 requireKinds = 0, uint64 denyKinds = 0)
:::

Queries dormant nodes (those nodes that live in add-ons, rather than in
the application) and returns those who match the specified inputs. If
{hparam}`hasInputFormat` isn't {cpp:expr}`NULL`, the node has to be a
{cpp:class}`BBufferConsumer` and have an input format compatible with the
format described in {hparam}`hasInputFormat`. Likewise, if
{hparam}`hasOutputFormat` isn't {cpp:expr}`NULL`, the node has to be a
{cpp:class}`BBufferProducer` that's compatible with the format described in
{hparam}`hasOutputFormat.`

If name isn't {cpp:expr}`NULL`, the node has to have a name that equals
{hparam}`name`, or, if the last character of name is an asterisk ("*"), a
name whose initial characters match name up to, but not including, the
asterisk.

The {hparam}`requireKinds` and {hparam}`denyKinds` arguments specifiy,
respectively, the kinds that must be supported, and the kinds that must not
be supported by the returned nodes.

Matching nodes are returned in {hparam}`outDormantNodeList`. You should
pass the size of the {hparam}`outDormantNodeList` array (the number of
elements that the array can hold) in {hparam}`inOutNumNodes`; when this
function returns, the value in {hparam}`inOutNumNodes` will be changed to
the actual number of matching nodes found, unless an error occurs.

Nodes you obtain using {hmethod}`GetDormantNodes()` must be released when
you're done using them. To do this, be sure they're stopped and
disconnected, then call {cpp:func}`ReleaseNode()
<BMediaRoster::ReleaseNode>`.

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
	- {cpp:enumerator}`B_OK`
	- No error cloning the node.
-
	- {cpp:enumerator}`B_NAME_NOT_FOUND`
	- The requested node couldn't be cloned.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaRoster::GetFileFormatsFor(const media_node& fileInterface, media_file_format* outFormatList, int32* inOutFormatCount = 0)
:::

Given a {cpp:class}`BFileInterface` node in {hparam}`fileInterface`,
returns information about the file formats the file interface can deal with
in the array {hparam}`outFormatList`. On entry, {hparam}`inOutFormatCount`
points to the number of {ref}`media_file_format` structures that can fit in
the array specified by {hparam}`outFormatList`. Upon return, it will
contain the actual number of formats returned, unless
{hmethod}`GetFileFormatsFor()` returns an error.

:::{admonition} Note
:class: note
This function will deadlock if called from a node's control thread or
while the control thread is blocked.
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
	- {cpp:enumerator}`B_OK`
	- No error sending the set mode request.
-
	- {cpp:enumerator}`B_NAME_NOT_FOUND`
	- The requested node couldn't be cloned.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaRoster::GetFormatFor(const media_output& output, media_format* ioFormat, uint32 flags = 0)
:::

:::{cpp:function} status_t BMediaRoster::GetFormatFor(const media_input& input, media_format* ioFormat, uint32 flags = 0)
:::

:::{cpp:function} status_t BMediaRoster::GetFormatFor(const media_node& input, media_format* ioFormat, float quality = B_MEDIA_ANY_QUALITY)
:::

{hmethod}`GetFormatFor()` returns the {cpp:func}`media_format
<media::format>` being used by the given object, which may be a
{cpp:func}`media_output <media::output>`, a {cpp:func}`media_input
<media::input>`, or a {cpp:func}`media_node <media::node>`. Pass in
{hparam}`ioFormat` a pointer to a {cpp:func}`media_format <media::format>`
object to be filled out with the object's format.

The {hparam}`flags` currently must be zero.

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
	- {cpp:enumerator}`B_OK`
	- No error.
-
	- {cpp:enumerator}`B_BAD_VALUE`
	- You can't pass {cpp:expr}`NULL` for {hparam}`ioFormat`.
-
	- {cpp:enumerator}`B_MEDIA_BAD_NODE`
	- The node isn't of the correct type for the given request.
-
	- {cpp:enumerator}`B_MEDIA_BAD_SOURCE`
	- The node's {cpp:func}`media_source <media::source>` is invalid.
-
	- Messaging errors.
	- An error occurred communicating with the Media Server.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaRoster::GetInitialLatencyFor(media_node& producer, bigtime_t* outLatency, uint32* outFlags = NULL)
:::

Returns, in {hparam}`outLatency`, the additional amount of time in
microseconds the specified producer node requires in order to synchronize
to a signal. For example, a TV capture card that's started while the
capture is in the middle of a field will have to wait until the next field
begins before actually starting to produce buffers.

{hparam}`outFlags` is set to the flags returned by the producer. Currently
there aren't any flags defined, so this will be returned as zero for now.

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
	- {cpp:enumerator}`B_OK`
	- No error.
-
	- {cpp:enumerator}`B_BAD_VALUE`
	- {hparam}`outLatency` was specified as {cpp:expr}`NULL`.
-
	- {cpp:enumerator}`B_MEDIA_BAD_NODE`
	- {hparam}`producer` isn't a valid node.
-
	- Port errors.
	- An error occurred communicating with the producer.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaRoster::GetInstancesFor(media_addon_id addon, int32 flavor, media_node_id* outID, int32* ioCount = 0)
:::

Given the specified {hparam}`addon` ID and {hparam}`flavor`, this function
fills the {hparam}`outID` list with up to {hparam}`ioCount` node IDs that
were derived from the specified add-on. If you specify zero for
{hparam}`ioCount`, one node ID will be returned. On return,
{hparam}`ioCount` is changed to indicate how many nodes have been returned
in the list.

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
	- {cpp:enumerator}`B_OK`
	- No error.
-
	- Port errors.
	- Communication with the Media Server failed.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaRoster::GetLatencyFor(const media_node& producer, bigtime_t* outLatency)
:::

Reports in {hparam}`outLatency` the maximum latency found downstream from
the specified {cpp:class}`BBufferProducer`, {hparam}`producer`, given the
current connections.

If an error occurs, the value in {hparam}`outLatency` is unreliable.

:::{admonition} Note
:class: note
This function will deadlock if called from a node's control thread or
while the control thread is blocked.
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
	- {cpp:enumerator}`B_OK`
	- No error.
-
	- Other errors.
	- Unable to get the latency.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaRoster::GetLiveNodes(live_node_info* outLiveNodeList, int32* ioTotalCount, const media_format* hasInput = NULL, const media_format* hasOutput = NULL, const char* name = NULL, uint64 nodeKinds = 0)
:::

Queries the Media Server for a list of all currently active nodes (whether
they're running or not), and fills the array specified by
{hparam}`outLiveNodeList` with information about the nodes. The size of the
array should be specified—in terms of how many elements it can contain—by
the {hparam}`ioTotalCount` argument; the actual number of entries in the
returned list will be stored in {hparam}`ioTotalCount` before the call
returns.

An active node is a node that is preloaded by the system and is always
available for use, as opposed to a dormant node, which resides in an add-on
and is only loaded when instantiated using
{cpp:func}`InstantiateDormantNode()
<BMediaRoster::InstantiateDormantNode>`.

You can obtain a more specific result list by specifying one or more of
the {hparam}`hasInput`, {hparam}`hasOutput`, {hparam}`name`, and
{hparam}`nodeKinds` arguments. {hparam}`hasInput` and {hparam}`hasOutput`
let you restrict the resulting list to containing nodes that accept as
input (or output) the specified format.

You should always specify 0 for {hparam}`nodeKinds`; this parameter is
currently not used.

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
	- {cpp:enumerator}`B_OK`
	- No error.
-
	- Other errors.
	- Unable to get the list of live nodes.

:::
::::

::::{abi-group}
:::{cpp:function} ssize_t BMediaRoster::GetNodeAttributesFor(const media_node& node, media_node_attributes* outArray, size_t inMaxCount)
:::

Fills the array {hparam}`outArray` with up to {hparam}`inMaxCount`
attributes of the given node. Returns the number of attributes returned. If
the result is less than zero, an error occurred.
::::

::::{abi-group}
:::{cpp:function} status_t BMediaRoster::GetNodeFor(media_node_id nodeID, media_node* clonedNode)
:::

Given a node specified by {hparam}`node_id`, {hmethod}`GetNodeFor()`
returns in {hparam}`clonedNode` a {cpp:func}`media_node <media::node>`
reference to a clone of the node. You can then use the {hparam}`clonedNode`
to query the node for available inputs, outputs, and so forth.

Once your application has finished using the returned node (and it's been
stopped and disconnected), you should release it by calling
{cpp:func}`ReleaseNode() <BMediaRoster::ReleaseNode>`.

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
	- {cpp:enumerator}`B_OK`
	- No error cloning the node.
-
	- BMessageerrors.
	- Unable to get the list of live nodes.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaRoster::GetParameterWebFor(const media_node& node, BParameterWeb** outWeb)
:::

Instantiates a {cpp:class}`BParameterWeb` that describes the internal
layout of a specific controllable node and stores a pointer to the
{cpp:class}`BParameterWeb` in {hparam}`outWeb`. You can then walk the
various {cpp:class}`BParameter`s within the web to figure out what there is
to control, and to present a user interface to the node's parameters.
Delete the web pointed to by {hparam}`outWeb` when you're done with it.

Note that the {cpp:func}`StartControlPanel()
<BMediaRoster::StartControlPanel>` function provides an easy, painless way
to automatically present user interface for configuring nodes.

:::{admonition} Note
:class: note
This function will deadlock if called from a node's control thread or
while the control thread is blocked.
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
	- {cpp:enumerator}`B_OK`
	- No error obtaining the {cpp:class}`BParameterWeb`.
-
	- {cpp:enumerator}`B_MEDIA_BAD_NODE`
	- The requested node is invalid.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaRoster::GetReadFileFormatList(const dormant_node_info& inNode, media_file_format* outReadFormats, int32 inReadCount, int32* outReadCount)
:::

:::{cpp:function} status_t BMediaRoster::GetWriteFileFormatList(const dormant_node_info& inNode, media_file_format* outWriteFormats, int32 inWriteCount, int32* outWriteCount)
:::

These two functions return lists of file formats that the dormant node
described by {hparam}`inNode` can read or write.

{hmethod}`GetReadFileFormatList()` returns in the array specified by
{hparam}`outReadFormats` a list of file formats the node can read. Specify
in {hparam}`inReadCount` the number of formats that can be held by the
{hparam}`outReadFormats` array. On exit, {hparam}`outReadCount` indicates
how many formats are being returned in the array.

{hmethod}`GetWriteFileFormatList()` returns in the array specified by
{hparam}`outWriteFormats` a list of file formats the node can write.
Specify in {hparam}`inWriteCount` the number of formats that can be held by
the {hparam}`outWriteFormats` array. On exit, {hparam}`outWriteCount`
indicates how many formats are being returned in the array.

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
	- {cpp:enumerator}`B_OK`
	- The list was returned without error.
-
	- {cpp:enumerator}`B_BAD_VALUE`
	- {hparam}`outReadFormats` or {hparam}`outWriteFormats` is {cpp:expr}`NULL`.
-
	- BMessageerrors.
	- An error occurred communicating with the Media Server.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaRoster::GetRealtimeFlags(uint32* outEnabled)
:::

:::{cpp:function} status_t BMediaRoster::SetRealtimeFlags(uint32 inEnabled)
:::

{hmethod}`GetRealtimeFlags()` returns flags that the Media Server uses to
determine whether or not memory needs to be locked down.
{hmethod}`SetRealtimeFlags()` sets these flags, and is generally only
called by the Media preference application.

Any or all of these flags can be set, in combination.

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
	- {cpp:enumerator}`B_MEDIA_REALTIME_ALLOCATOR`
	- When set, {cpp:func}`rtm_alloc() <rtm::alloc>` will return locked memory.
-
	- {cpp:enumerator}`B_MEDIA_REALTIME_AUDIO`
	- Audio add-ons in the Media Server are locked in memory, and should lock
		their thread stacks using {ref}`media_realtime_init_thread()`.
-
	- {cpp:enumerator}`B_MEDIA_REALTIME_VIDEO`
	- Video add-ons are locked in memory, and should lock their thread stacks
		using {ref}`media_realtime_init_thread()`.
-
	- {cpp:enumerator}`B_MEDIA_REALTIME_ANYKIND`
	- All Media add-ons are locked in memory, and should lock their thread
		stacks using {ref}`media_realtime_init_thread()`.

:::

See the {cpp:class}`BMediaNode overview` for a discussion of realtime
allocation and thread stack locking.

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
	- {cpp:enumerator}`B_OK`
	- No error.
-
	- Other errors.
	- Unable to set or retrieve the realtime flags.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaRoster::GetStartLatencyFor(const media_node& timeSource, bigtime_t* outLatency)
:::

Reports in {hparam}`outLatency` the maximum latency found downstream from
the time source specified by {hparam}`timeSource`, given the current
connections.

If an error occurs, the value in {hparam}`outLatency` is unreliable.

:::{admonition} Note
:class: note
This function will deadlock if called from a node's control thread or
while the control thread is blocked.
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
	- {cpp:enumerator}`B_OK`
	- No errors.
-
	- Other errors.
	- Unable to get the latency.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaRoster::GetSystemTimeSource(media_node* clonedTimeSource)
:::

This function returns, in {hparam}`clonedTimeSource`, a reference to a
clone of the system time source. The system time source is the fallback
time source used when no other source is available; its time is derived
from the {cpp:func}`system_time() <system::time>` real-time clock. As such,
it's quite accurate, but has no relevant relationship to the timing of the
hardware devices being used for media input and output. Thus it's not a
good choice for a master clock—but it's there if nothing else is available.

By default, new nodes are slaved to the system time source.

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
	- {cpp:enumerator}`B_OK`
	- No error cloning the node.
-
	- {cpp:enumerator}`B_NAME_NOT_FOUND`
	- The time source couldn't be cloned.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaRoster::GetTimeSource(media_node* outNode)
:::

:::{cpp:function} BTimeSource* BMediaRoster::MakeTimeSourceFor(media_node& node)
:::

{hmethod}`GetTimeSource()` returns, in {hparam}`outNode`, the preferred
master clock to which other nodes can be slaved. By slaving all nodes to a
single master clock, good synchronization can be ensured.

Typically, the preferred master clock will be the same node as the default
audio output (assuming that the audio output node is also a
{cpp:class}`BTimeSource`, which should be the case). The sound circuitry's
DAC is then used as a timing reference. Although this may be less accurate
than the system clock (as defined by the global {cpp:func}`system_time()
<system::time>` function), glitch-free audio performance is best ensured by
using the audio output to synchronize media operations.

By default, nodes are slaved to the system time source (see
{cpp:func}`GetSystemTimeSource() <BMediaRoster::GetSystemTimeSource>`
above). Usually you'll want to use this function to obtain a more accurate
time source, then slave your nodes to it:

:::{code} cpp
media_node timeSource;
roster->GetTimeSource(&media_node);
roster->SetTimeSourceFor(myNode, timeSource.node);
:::

This will slave the previously-created node myNode to the preferred time
source.

{hmethod}`MakeTimeSourceFor()` returns a {cpp:class}`BTimeSource` object
corresponding to the specified node's time source. This object can then be
used to issue {cpp:class}`BTimeSource` calls to determine and adjust timing
issues (for instance, to determine the current performance time). When
you're done with the {cpp:class}`BTimeSource`, you should call
{cpp:func}`ReleaseNode() <BMediaRoster::ReleaseNode>` on it.

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
	- {cpp:enumerator}`B_OK`
	- No error locating the default input node.
-
	- {cpp:enumerator}`B_NAME_NOT_FOUND`
	- The default node couldn't be identified.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaRoster::InstantiateDormantNode(const dormant_node_info& inInfo, media_node* outNode)
:::

:::{cpp:function} status_t BMediaRoster::InstantiateDormantNode(const dormant_node_info& inInfo, media_node* outNode, uint32 flags)
:::

These functions instantiate a node from an add-on, given the information
specified in the {htype}`dormant_node_info` structure.

The {hparam}`addon` field should be filled out to contain the add-on ID of
the add-on from which the node should be instantiated, and the
{hparam}`flavor_id` should be the flavor ID number the node should be
instantiated to process. Typically you'll use a function such as
{cpp:func}`GetDormantNodes() <BMediaRoster::GetDormantNodes>` to find a
{htype}`dormant_node_info` structure that describes a suitable node.

When you're done using the node, and have stopped and disconnected it, you
should always call {cpp:func}`ReleaseNode() <BMediaRoster::ReleaseNode>` to
let the Media Server know you're finished with it. This lets the Media
Server track whether or not the node's add-on can be unloaded, based on the
number of applications still using it.

The difference between these two functions is that the second form lets
you specify flags controlling how the node is instantiated. The
{cpp:enumerator}`B_FLAVOR_IS_GLOBAL` flag instantiates the node in the
Media Add-on Server's memory space, while the
{cpp:enumerator}`B_FLAVOR_IS_LOCAL` flag instantiates the node in your
application's memory. Using {cpp:enumerator}`B_FLAVOR_IS_LOCAL` protects
other applications—not to mention the Media Server—from being derailed if
the node crashes. Whenever possible, you should instantiate nodes locally.
You should only use {cpp:enumerator}`B_FLAVOR_IS_GLOBAL` if you need the
node to stay around after your application exits.

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
	- {cpp:enumerator}`B_OK`
	- No error instantiating the node.
-
	- {cpp:enumerator}`B_NAME_NOT_FOUND`
	- The requested node couldn't be instantiated.

:::
::::

::::{abi-group}
:::{cpp:function} static ssize_t BMediaRoster::MediaFlags(media_flags flag, void* buffer, size_t bufferSize)
:::

Asks the Media Server about its support for specific features and
capabilities.

The specified buffer will be filled with the data indicating the value of
the specified {hparam}`flag`. If the buffer is too small (as indicated by
{hparam}`bufferSize`), only the first {hparam}`bufferSize` bytes of the
result data will be stored in the buffer, but no error will occur.

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
	- {cpp:enumerator}`B_MEDIA_FLAGS_VERSION`
	- Returns the Media Kit version as an {htype}`int32` value.

:::

If the result is negative, an error occurred, or the Media Server isn't
running.
::::

::::{abi-group}
:::{cpp:function} media_node_id BMediaRoster::NodeIDFor(port_id sourceOrDestinationPort)
:::

Given a source or destination port, this function returns the
corresponding node's ID number.
::::

::::{abi-group}
:::{cpp:function} status_t BMediaRoster::PrerollNode(const media_node& node)
:::

Calling {hmethod}`PrerollNode()` sends a preroll message to the specified
{hparam}`node`; the node's {cpp:func}`Preroll() <BMediaNode::Preroll>` hook
function will be called. When that hook returns, {hmethod}`PrerollNode()`
will also return. A node that's been prerolled should respond very quickly
to a {cpp:func}`StartNode() <BMediaRoster::StartNode>` call, because the
time-consuming setup operations should have been done already by the
{cpp:func}`Preroll() <BMediaNode::Preroll>` hook.

While it's not mandatory for an application to call
{hmethod}`PrerollNode()` before calling {cpp:func}`StartNode()
<BMediaRoster::StartNode>`, it's recommended, because doing so may improve
real-time performance once the node is started.

:::{admonition} Note
:class: note
This function will deadlock if called from a node's control thread or
while the control thread is blocked.
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
	- {cpp:enumerator}`B_OK`
	- No error sending the set mode request.
-
	- {cpp:enumerator}`B_NAME_NOT_FOUND`
	- The requested node couldn't be cloned.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaRoster::RegisterNode(BMediaNode* node)
:::

:::{cpp:function} status_t BMediaRoster::UnregisterNode(BMediaNode* node)
:::

{hmethod}`RegisterNode()` registers an object of a class derived from
{cpp:class}`BMediaNode` with the media roster and assigns it a node_id.
This function should be called once a {hclass}`BMediaNode`-derived object
is fully-constructed and before any attempt is made to connect the node to
some other participant in the Media Server.

{hmethod}`RegisterNode()` is called automatically for nodes instantiated
from add-ons, but your application will have to call it for any nodes it
creates itself.

If you create your own subclass of {cpp:class}`BMediaNode`, its
constructor can call {hmethod}`RegisterNode()` itself just before returning
(it must be the last thing the constructor does).

{hmethod}`UnregisterNode()` unregisters a node from the Media Server. It's
called automatically by the {cpp:class}`BMediaNode` destructor, but it
might be convenient to call it sometime before you delete your node
instance, depending on your implementation and circumstances.

These functions are generally only used if you're creating your own node
class.

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
	- {cpp:enumerator}`B_OK`
	- No error sending the seek request.
-
	- {cpp:enumerator}`B_BAD_VALUE`
	- Invalid {cpp:class}`BMediaNode` specified.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaRoster::ReleaseNode(const media_node& node)
:::

Releases the specified node, which has previously been obtained by using
the {cpp:func}`InstantiateDormantNode()
<BMediaRoster::InstantiateDormantNode>`, {cpp:func}`GetNodeFor()
<BMediaRoster::GetNodeFor>`, or default node functions (such as
{cpp:func}`GetVideoOutput() <BMediaRoster::GetVideoOutput>` or
{cpp:func}`GetAudioMixer() <BMediaRoster::GetAudioMixer>`).

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
	- {cpp:enumerator}`B_OK`
	- No error releasing the node.
-
	- BMessageerrors.
	- The node couldn't be released.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaRoster::RollNode(const media_node& node, bigtime_t startPerformanceTime, bigtime_t stopPerformanceTime, bigtime_t atMediaTime = -B_INFINITE_TIMEOUT)
:::

Atomically queues a start and stop for the given node. The node will start
playing at the performance time indicated by
{hparam}`startPerformanceTime`, and will stop playing at the performance
time indicated by {hparam}`stopPerformanceTime`.

If the {hparam}`atMediaTime` argument is given, a seek to that media time
is also queued.

This function is especially useful for the offline rendering case (the
{cpp:enumerator}`B_OFFLINE` run mode). It lets you render a certain time
range without accidentally going too far; if you queue up a start and stop
using {cpp:func}`Start() <BMediaNode::Start>` and {cpp:func}`Stop()
<BMediaNode::Stop>`, the node may have already rendered past your desired
stop time before your {cpp:func}`Stop() <BMediaNode::Stop>` call occurs.
{cpp:func}`RollNode() <BMediaRoster::RollNode>` avoids that problem.

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
	- {cpp:enumerator}`B_OK`
	- No error.
-
	- {cpp:enumerator}`B_MEDIA_BAD_NODE`
	- The node isn't valid.

:::
::::

::::{abi-group}
:::{cpp:function} static BMediaRoster* BMediaRoster::Roster(status_t* outError = NULL)
:::

:::{cpp:function} static BMediaRoster* BMediaRoster::CurrentRoster()
:::

{hmethod}`Roster()` returns a pointer to the default
{hclass}`BMediaRoster` instance, or creates the {hclass}`BMediaRoster`
instance if it doesn't exist yet, then returns a pointer to it. If you
don't want to create the roster if it doesn't already exist, use the
{hmethod}`CurrentRoster()` function (it returns {cpp:expr}`NULL` if there's
no roster).

Since {hmethod}`CurrentRoster()` doesn't create a media roster, you
obviously must use {hmethod}`Roster()` at least once in your application to
create one.

These static member functions should be called by explicit scope, and
never by dereference; this is how you get the {hclass}`BMediaRoster`
through which all other media roster functions are called. For example:

:::{code} cpp
BMediaRoster* r = BMediaRoster::Roster();
status_t err = r->GetFreeOutputsFor(some_node, some_array, 3, &n);
:::

On return, {hparam}`outError` is set to {cpp:enumerator}`B_OK` if the
default {hclass}`BMediaRoster` was successfully returned, or a negative
error code if something went wrong (for example, if the Media Server isn't
running). If {hparam}`outError` is {cpp:expr}`NULL`, no error code is
returned.

In any case, {hmethod}`Roster()` returns {cpp:expr}`NULL` if an error
occurs.
::::

::::{abi-group}
:::{cpp:function} status_t BMediaRoster::SeekNode(const media_node& node, bigtime_t newMediaTime, bigtime_t atPerformanceTime = 0)
:::

Sends the specified {hparam}`node` a request that it change its playing
location to the media time {hparam}`newMediaTime` once the performance time
{hparam}`atPerformanceTime` is reached.

If the node isn't running, the seek request is processed immediately, and
the {hparam}`atPerformanceTime` argument is ignored.

The error returned by this function only indicates whether or not the
request was sent successfully; the node may later run into problems trying
to perform the seek operation.

:::{admonition} Note
:class: note
If the node is a time source, and you want to operate on the time source
aspect of the node (to seek all slaved nodes), you should call
{cpp:func}`SeekTimeSource() <BMediaRoster::SeekTimeSource>` instead.
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
	- {cpp:enumerator}`B_OK`
	- No error sending the seek request.
-
	- Other errors
	- Are node specific

:::

See also: {cpp:func}`StartNode() <BMediaRoster::StartNode>`,
{cpp:func}`StopNode() <BMediaRoster::StopNode>`
::::

::::{abi-group}
:::{cpp:function} status_t BMediaRoster::SeekTimeSource(const media_node& timeSource, bigtime_t newPerformanceTime, bigtime_t atRealTime)
:::

Sends the specified timeSource a request that it change the performance
time it outputs to its slaved nodes to the time
{hparam}`newPerformanceTime` once the performance time {hparam}`atRealTime`
is reached.

If the {hparam}`timeSource` isn't running, the seek request is processed
immediately, and the atRealTime argument is ignored.

The error returned by this function only indicates whether or not the
request was sent successfully; the node may later run into problems trying
to perform the seek operation.

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
	- {cpp:enumerator}`B_OK`
	- No error sending the seek request.
-
	- Other errors
	- Are node specific

:::

See also: {cpp:func}`StartTimeSource() <BMediaRoster::StartTimeSource>`,
{cpp:func}`StopTimeSource() <BMediaRoster::StopTimeSource>`
::::

::::{abi-group}
:::{cpp:function} status_t BMediaRoster::SetAudioInput(const media_node& defaultNode)
:::

:::{cpp:function} status_t BMediaRoster::SetAudioInput(const dormant_node_info& defaultNodeInfo)
:::

:::{cpp:function} status_t BMediaRoster::SetVideoInput(const media_node& defaultNode)
:::

:::{cpp:function} status_t BMediaRoster::SetVideoInput(const dormant_node_info& defaultNodeInfo)
:::

These functions set the preferred nodes for audio and video input. If the
specified node isn't capable of being the system default, an error will be
returned (for example, nodes defined by an application can't be the system
default—only nodes defined by Media Kit add-ons can be system defaults).

:::{admonition} Note
:class: note
In general, you shouldn't call these functions unless you're writing
software that reimplements the functionality of the BeOS Audio or Video
preference panels.
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
	- {cpp:enumerator}`B_OK`
	- No error setting the default input node.
-
	- {cpp:enumerator}`B_NAME_NOT_FOUND`
	- The default node couldn't be changed.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaRoster::SetAudioOutput(const media_node& defaultNode)
:::

:::{cpp:function} status_t BMediaRoster::SetAudioOutput(const dormant_node_info& defaultNodeInfo)
:::

:::{cpp:function} status_t BMediaRoster::SetAudioOutput(const media_input& inputToOutput)
:::

:::{cpp:function} status_t BMediaRoster::SetVideoOutput(const media_node& defaultNode)
:::

:::{cpp:function} status_t BMediaRoster::SetVideoOutput(const dormant_node_info& defaultNodeInfo)
:::

These functions set the preferred nodes for audio and video output. If the
specified node isn't capable of being the system default, an error will be
returned (for example, nodes defined by an application can't be the system
default—only nodes defined by Media Kit add-ons can be system defaults).

:::{admonition} Note
:class: note
In general, you shouldn't call these functions unless you're writing
software that reimplements the functionality of the BeOS Audio or Video
preference panels.
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
	- {cpp:enumerator}`B_OK`
	- No error setting the default output node.
-
	- {cpp:enumerator}`B_NAME_NOT_FOUND`
	- The default node couldn't be changed.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaRoster::SetProducerRate(const media_node& node, int32 numerator, int32 demominator)
:::

This function is called to tell the producer to resample the data rate by
the specified factor. Specifying a value of 1 (ie,
{hparam}`numerator`/{hparam}`denominator` = 1) indicates that the data
should be output at the same playback rate that it comes into the node at.
The format of the data should be unchanged.

:::{admonition} Note
:class: note
Nodes are not required to support this mechanism for controlling their
data rate, so this call may have no effect.
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
	- {cpp:enumerator}`B_OK`
	- No error.
-
	- Other errors.
	- Returned by {cpp:func}`BBufferProducer::SetPlayRate`.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaRoster::SetProducerRunModeDelay(const media_node& node, bigtime_t delay, BMediaNode::run_mode mode = B_RECORDING)
:::

Sets the run mode for the given producer node to {hparam}`mode`. Also sets
the specified {hparam}`delay` to be added to each buffer sent by the
producer node. This function should only be called for
{cpp:enumerator}`B_RECORDING` mode; it's provided to compensate when you
connect a node that's in recording mode to a node that isn't.

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
	- {cpp:enumerator}`B_OK`
	- No error.
-
	- {cpp:enumerator}`B_MEDIA_BAD_NODE`
	- The node is invalid.
-
	- Port errors.
	- An error occurred communicating with the Media Server.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaRoster::SetRefFor(const media_node& fileInterface, entry_ref& file, bool createAndTruncate, bigtime_t* outDuration)
:::

:::{cpp:function} status_t BMediaRoster::GetRefFor(const media_node& fileInterface, entry_ref* outFile, BMimeType* outMimeType = NULL)
:::

{hmethod}`SetRefFor()` tells the {cpp:class}`BFileInterface`
{hparam}`fileInterface` to work on the file whose {htype}`entry_ref` is
specified by {hparam}`file`. If {hparam}`createAndTruncate` is
{cpp:expr}`true`, any previous file with that reference is deleted and the
file will be prepared for new output. If {hparam}`createAndTruncate` is
{cpp:expr}`false`, {hparam}`outDuration` will, on return, contain the
duration of the performance data found in the file.

{hmethod}`GetRefFor()` fills out the specified {htype}`entry_ref`,
{hparam}`outFile`, to reference the file with which the specified
{hparam}`fileInterface` node is working. If {hparam}`outMimeType` isn't
{cpp:expr}`NULL`, it'll contain a {cpp:class}`BMimeType` object describing
the file's type, unless an error occurs.

:::{admonition} Note
:class: note
These functions will deadlock if called from a node's control thread or
while the control thread is blocked.
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
	- {cpp:enumerator}`B_OK`
	- No error.
-
	- {cpp:enumerator}`B_MEDIA_BAD_NODE`
	- The specified node doesn't exist, or isn't a file interface.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaRoster::SetRunModeNode(const media_node& node, bigtime_t delay, BMediaNode::run_mode newMode)
:::

Sends the specified {hparam}`node` a request that it change its policy for
handling situations where it falls behind during real-time processing.

The error returned by this function only indicates whether or not the
request was sent successfully.

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
	- {cpp:enumerator}`B_OK`
	- No error sending the set mode request.
-
	- {cpp:enumerator}`B_BAD_NODE`
	- The specified node is invalid.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaRoster::SetTimeSourceFor(media_node_id node, media_node_id timeSource)
:::

Tells the specified {hparam}`node` to slave its timing to
{hparam}`timeSource`. Once this is done, the node will receive its notion
of the passage of time from {hparam}`timeSource`. As such, it will pause
whenever timeSource is stopped, and so forth.

:::{admonition} Note
:class: note
By default, nodes are slaved to the system time source, so you only need
to call this function if you need to slave a node to a different time
source.
:::

The node will take whatever precautions are necessary to remain faithful
to the notion of time presented by {hparam}`timeSource` without causing
glitches in the presentation of its media. For example, if a sound card
node has a DAC that drifts from {hparam}`timeSource`, it might try to fix
the problem by varying the sampling rate slightly, or by dropping or
doubling buffers occasionally. This is why you should usually use the
preferred time source—rather than the system time source—as your master
time source. The preferred time source will usually be derived directly
from the DAC being used to produce the media output.

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
	- {cpp:enumerator}`B_OK`
	- No error.
-
	- BMessageerrors.
	- Unable to set the time source.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaRoster::SniffRef(const entry_ref& node, uint64 requireNodeKinds, dormant_node_info* outNode, BMimeType* outMimeType = NULL)
:::

:::{cpp:function} status_t BMediaRoster::SniffRefFor(const media_node& fileInterface, const entry_ref& node, uint64 requireNodeKinds, dormant_node_info* outNode, BMimeType* outMimeType = NULL)
:::

{hmethod}`SniffRef()` asks all {cpp:class}`BMediaAddOn` instances that
satisfy the {hparam}`requireNodeKinds` restraint to identify the file. The
{hparam}`requireNodeKinds` argument should contain flags composited from
the {ref}`node_kind` constants.

The node that returns the greatest {hparam}`outCapability` value will be
chosen, and a reference to it put in {hparam}`outNode`. The MIME type of
the file will be put into {hparam}`outMimeType`.

In simpler terms: {hmethod}`SniffRef()` returns the node that can best
handle the media data in the specified file.

{hmethod}`SniffRefFor()`, on the other hand, asks the specified
{hparam}`fileInterface` node to examine the file. If the node recognizes
the file, the MIME type of the file is stored in the buffer
{hparam}`outMimeType`, and the node's capability to handle the file is
returned in {hparam}`outCapability`.

If the node doesn't recognize the file, an error is returned. If the node
recognizes the file format but finds no recognizable data within the file,
{hparam}`outCapability` is set to 0.0 and no error is returned.

In either case, the higher the {hparam}`outCapability` value returned, the
more appropriate the node is for handling the media data in the file.

:::{admonition} Note
:class: note
These functions will deadlock if called from a node's control thread or
while the control thread is blocked.
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
	- {cpp:enumerator}`B_OK`
	- No errors.
-
	- {cpp:enumerator}`B_MEDIA_BAD_NODE`
	- The specified node is invalid, or isn't a file interface.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaRoster::StartControlPanel(const media_node node, Messenger* outMessenger = NULL)
:::

Tells the specified node to start its custom control panel, which is
started outside your application. There's no way to tell when the user has
closed the control panel, other than by indirectly detecting possible
changes to the node, such as a renegotiation of the format of data being
output by the node.

If a {cpp:class}`BMessenger` is provided as input to
{hmethod}`StartControlPanel()`, the function returns in
{hparam}`outMessenger` a {cpp:class}`Messenger` that can be used to
communicate with the control panel.

:::{admonition} Note
:class: note
These functions will deadlock if called from a node's control thread or
while the control thread is blocked.
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
	- {cpp:enumerator}`B_OK`
	- No error starting the control panel.
-
	- {cpp:enumerator}`B_MEDIA_BAD_NODE`
	- The specified node is invalid.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaRoster::StartNode(const media_node node, bigtime_t atPerformanceTime)
:::

:::{cpp:function} status_t BMediaRoster::StartNode(const media_node node, bigtime_t atPerformanceTime, bool immediate = false)
:::

{hmethod}`StartNode()` sends the specified node a request to start
streaming data at the performance time specified by the
{hparam}`atPerformanceTime` argument, according to that node's time source.

By default, nodes are in a stopped state upon creation, so you have to
call {hmethod}`StartNode()` once you have a reference to it before anything
will happen. Starting a node that's already running has no effect.

{hmethod}`StopNode()` sends node a request to stop streaming data once the
specified performance time {hparam}`atPerformanceTime` is reached,
according to that node's time source. Stopping a node that's already
stopped has no effect. If {hparam}`immediate` is {cpp:expr}`true`, the node
is instructed to stop immediately and the {hparam}`atPerformanceTime`
argument is ignored; if {hparam}`immediate` is {cpp:expr}`false`, the node
is stopped at the specified performance time.

In either case, the requested change will occur at the time specified by
{hparam}`atPerformanceTime`.

:::{admonition} Note
:class: note
If the node is a time source, and you want to operate on the time source
aspect of the node (to start or stop all slaved nodes), you should call
{cpp:func}`SeekTimeSource() <BMediaRoster::SeekTimeSource>` instead.
:::

The error returned by these functions only indicates whether or not the
request was sent successfully; the node may later run into problems trying
to start or stop its media and you won't know it based on the result of
these functions.

:::{admonition} Note
:class: note
{hmethod}`StopNode()` will deadlock if called from a node's control thread
or while the control thread is blocked.
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
	- {cpp:enumerator}`B_OK`
	- No error sending the start or stop request.
-
	- Other errors.
	- Are node specific.

:::

See also: {cpp:func}`SeekNode() <BMediaRoster::SeekNode>`
::::

::::{abi-group}
:::{cpp:function} status_t BMediaRoster::StartTimeSource(const media_node timeSource, bigtime_t atRealTime)
:::

:::{cpp:function} status_t BMediaRoster::StopTimeSource(const media_node timeSource, bigtime_t atRealTime, bool immediate = false)
:::

{hmethod}`StartTimeSource()` sends the specified {hparam}`timeSource` a
request to start running at the real time specified by the
{hparam}`atRealTime` argument.

{hmethod}`StopTimeSource()` sends node a request to stop the specified
{hparam}`timeSource` once the specified real time {hparam}`atRealTime` is
reached. Stopping a time source that's already stopped has no effect. If
{hparam}`immediate` is {cpp:expr}`true`, the time source is instructed to
stop immediately and the {hparam}`atRealTime` argument is ignored; if
{hparam}`immediate` is {cpp:expr}`false`, the time source is stopped at the
specified real time.

In either case, the requested change will occur at the time specified by
{hparam}`atRealTime`.

The error returned by these functions only indicates whether or not the
request was sent successfully; the node may later run into problems trying
to start or stop and you won't know it based on the result of these
functions.

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
	- {cpp:enumerator}`B_OK`
	- No error sending the start or stop request.
-
	- Other errors.
	- Are node specific.

:::

See also: {cpp:func}`SeekTimeSource() <BMediaRoster::SeekTimeSource>`
::::

::::{abi-group}
:::{cpp:function} status_t BMediaRoster::StartWatching(const BMessenger& notifyHandler)
:::

:::{cpp:function} status_t BMediaRoster::StartWatching(const BMessenger& notifyHandler, int32 notificationType)
:::

:::{cpp:function} status_t BMediaRoster::StartWatching(const BMessenger& notifyHandler, const media_node& node, int32 notificationType)
:::

:::{cpp:function} status_t BMediaRoster::StopWatching(const BMessenger& notifyHandler)
:::

:::{cpp:function} status_t BMediaRoster::StopWatching(const BMessenger& notifyHandler, int32 notificationType)
:::

:::{cpp:function} status_t BMediaRoster::StopWatching(const BMessenger& notifyHandler, const media_node& node, int32 notificationType)
:::

{hmethod}`StartWatching()` registers the specified {cpp:class}`BHandler`
or {cpp:class}`BLooper` as a recipient of notification messages from the
Media Server. {hmethod}`StopWatching()` cancels this registration so that
no further notifications will be sent.

If you're only interested in a particular notification type, you can
specify that code in the {hparam}`notificationType` argument. If you don't
specify a notification type, {cpp:enumerator}`B_MEDIA_WILDCARD` is assumed;
this matches all notification types. You can also specify that you want to
watch a specific node; if you don't specify a node, you'll receive
notifications for all nodes.

Events are sent to registered {cpp:class}`BHandler`s and
{cpp:class}`BLooper`s when certain events happen, such as nodes being
created or deleted, or connections being made or broken.

See "{ref}`Notification Messages`" for a list of the notifications you can
receive, and the formats of the corresponding messages.

Although the Media Server will automatically cancel notifications to
{cpp:class}`BHandler`s and {cpp:class}`BLooper`s that go away without
explicitly calling {hmethod}`StopWatching()`, this detection is expensive
and may briefly interrupt the media system, so you should always call
{hmethod}`StopWatching()` before allowing a {cpp:class}`BHandler` or
{cpp:class}`BLooper` to go away.

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
	- {cpp:enumerator}`B_OK`
	- No error cloning the node.
-
	- {cpp:enumerator}`B_NAME_NOT_FOUND`
	- The requested node couldn't be cloned.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BMediaRoster::SyncToNode(const media_node node, bigtime_t atPerformanceTime, bigtime_t timeout = B_INFINITE_TIMEOUT)
:::

If you want to detect the arrival of a specific performance time on a
given node, you can do that by calling {hmethod}`SyncToNode()`. Specify the
node you want to monitor in {hparam}`node`, and the time you want to be
notified of in {hparam}`atPerformanceTime`. You can, optionally, specify a
{hparam}`timeout`; if the sync hasn't occurred in {hparam}`timeout`
microseconds, the request will time out.

This function doesn't return until either the specified performance time
arrives, or the sync operation times out.

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
	- {cpp:enumerator}`B_OK`
	- All's well.
-
	- {cpp:enumerator}`B_MEDIA_BAD_NODE`
	- The specified node is invalid.
-
	- {cpp:enumerator}`B_TIMED_OUT`
	- The request timed out.
-
	- Port errors.
	- An error occurred communicating with the Media Server.

:::
::::

## Constants

### connect_flags

Declared in: media/MediaRoster.h

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
	- {cpp:enumerator}`B_CONNECT_MUTED`
	- The connection should be muted on creation.

:::
