:::{cpp:class} BControllable
:::

# BControllable

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} explicit BControllable::BControllable()
:::

The {hclass}`BControllable` constructor. You should override this in your
derived class to create a {cpp:class}`BParameterWeb` object, configure it
to describe the available parameters, and call {cpp:func}`SetParameterWeb()
<BControllable::SetParameterWeb>` with that object before returning.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} status_t BControllable::BroadcastChangedParameter(int32 parameterID)
:::

When the configuration of a specific parameter changes, you should call
this function with the ID of the changed parameter so that clients know
that they need to check with the node to determine the parameter's new
configuration.

:::{admonition} Note
:class: note
The configuration of a parameter changes only when the range of possible
values for the parameter changes. For example, if the parameter's value is
a CD track number, the configuration would change (thus requiring a call to
{cpp:func}`BroadcastChangedParameter()
<BControllable::BroadcastChangedParameter>`) if the user put in a different
CD with a different number of tracks on it.
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
	- No errors.
-
	- Other errors.
	- See {cpp:func}`BMessenger::SendMessage`

:::
::::

::::{abi-group}
:::{cpp:function} status_t BControllable::BroadcastNewParameterValue(bigtime_t when, int32 id, void* newValue, size_t valueSize)
:::

Call this function when a parameter value change takes effect and you want
people that are interested in knowing about the change to stay in sync with
you. Unlike {cpp:func}`BroadcastChangedParameter()
<BControllable::BroadcastChangedParameter>`, this function actually passes
along the new value of the parameter.

The {hparam}`when` argument indicates the performance time at which the
change took effect. The {hparam}`id` indicates the parameter ID of the
parameter whose value changed. {hparam}`newValue` is a pointer to the
parameter's data, and {hparam}`valueSize` defines the size of that data.

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
	- An error occurred communicating with the Media Server, or with a node in
		the roster.

:::
::::

::::{abi-group}
:::{cpp:function} virtual status_t BControllable::GetParameterValue(int32 parameterID, bigtime_t* lastChangeTime, void* value, size_t* ioSize) = 0
:::

:::{cpp:function} virtual void BControllable::SetParameterValue(int32 parameterID, bigtime_t changeTime, const void* value, size_t size) = 0
:::

You should implement {hmethod}`GetParameterValue()` to store the value of
the parameter with the specified {hparam}`parameterID` in the memory
pointed to by {hparam}`value`. The {htype}`size_t` value pointed to by
{hparam}`ioSize` specifies the size of the value buffer; prior to
returning, your implementation of {hmethod}`GetParameterValue()` should
change {hparam}`ioSize` to the actual size of the returned data.

Also, you should set {hparam}`lastChangeTime` to the time at which the
control's value most recently changed.

{hmethod}`GetParameterValue()` should return {cpp:enumerator}`B_OK` when
done, or an appropriate error code if something goes wrong.

Likewise, you should implement {hmethod}`SetParameterValue()` to change
the value of the parameter; the {hparam}`changeTime` argument is the
performance time at which the change should occur; in other words, you may
need to queue the request so it can be handled at the requested time.
{hparam}`value` points to the value to which the parameter should be set,
and {hparam}`size` is the number of bytes of data in the value.

:::{admonition} Note
:class: note
It's possible that a single parameter may have several channels of values,
if that parameter is a multi-channel parameter. For example, if the
parameter is a two-channel slider (such as a stereo gain control, where the
left and right channels are controlled individually within a single
parameter), the {hparam}`value` argument would point to an array of two
{htype}`float`s, and {hparam}`size` would be 8 (`sizeof(float) * 2`).
:::
::::

::::{abi-group}
:::{cpp:function} virtual status_t BControllable::HandleMessage(int32 message, const void* data, size_t* size_t)
:::

When your node's service loop receives a message, in addition to passing
it to {cpp:class}`BMediaNode` and other superclasses of your node, you
should also pass it to {hmethod}`HandleMessage()`. You should start at the
most-derived class' implementation of {hmethod}`HandleMessage()` and work
your way upward until {cpp:enumerator}`B_OK` is returned.

If it's a message intended for the {cpp:class}`BControllable` interface,
it'll be dispatched and {cpp:enumerator}`B_OK` will be returned; otherwise,
{hmethod}`HandleMessage()` will return an error so you know to try
something else.

:::{code} cpp
/* Message received */

if ((BControllable::HandleMessage(message, data, size) != B_OK) &&
         (BMediaNode::HandleMessage(message, data, size) != B_OK)) {
   BMediaNode::HandleMessage(message, data, size);
}
:::

In this example, the {hclass}`BControllable` implementation of
{hmethod}`HandleMessage()` gets the first crack at handling the request. If
it doesn't know what to do with the message, it's forwarded to
{cpp:class}`BMediaNode`'s implementation. If the message still isn't
handled, it's then sent to {cpp:func}`BMediaNode::HandleBadMessage` to be
dealt with.

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
	- The message was dispatched.
-
	- Other errors.
	- Each message code may respond with various error codes.

:::

See also: "{cpp:func}`About Multiple Virtual Inheritance
<TheMediaKit::AboutMultipleVirtualInheritance>`"
::::

::::{abi-group}
:::{cpp:function} bool BControllable::LockParameterWeb()
:::

:::{cpp:function} void BControllable::UnlockParameterWeb()
:::

{hmethod}`LockParameterWeb()` locks the web to prevent access to it while
you're working on it, and {hmethod}`UnlockParameterWeb()` releases it when
you're done. You should surround your accesses to the web with these calls:

:::{code} cpp
LockParameterWeb();
Web()->MakeGroup("EqualizerControls");
...
UnlockParameterWeb();
:::
::::

::::{abi-group}
:::{cpp:function} status_t BControllable::MakeParameterData(const int32* parameterList, int32 numParameters, void* buffer, size_t* ioSize)
:::

:::{cpp:function} status_t BControllable::ApplyParameterData(const void* value, size_t ioSize)
:::

The {hmethod}`MakeParameterData()` utility function takes a list of
parameter IDs from {hparam}`parameterList` and calls
{cpp:func}`GetParameterValue() <BControllable::GetParameterValue>` for each
of them, storing the values in the specified {hparam}`buffer` until the
size specified in {hparam}`ioSize` is filled, or all the parameters are
read. The number of bytes of the buffer used will be returned in
{hparam}`ioSize`.

If your {hclass}`BControllable` is also a {cpp:class}`BBufferConsumer`
that accepts {cpp:enumerator}`B_MEDIA_PARAMETERS` type data on some input,
call {hmethod}`ApplyParameterData()` with {hparam}`value` set to the result
of {cpp:func}`BBuffer::Data` and {hparam}`size` set to
{cpp:func}`BBuffer::SizeUsed`. This function will then parse the parameter
change requests in the buffer and dispatch them to your
{hmethod}`SetParameterValue()` function to fulfill the requests.

This lets your node support easy automation of parameter information. Even
more benefit can be obtained by also deriving from
{cpp:class}`BBufferProducer`, and providing an output for the
{cpp:enumerator}`B_MEDIA_PARAMETERS` data format, so that changes can be
recorded as they occur. This provides a mechanism for automating the
parameters by recording a user's changes to them, then playing back the
changes later.

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
	- No errors.
-
	- {cpp:enumerator}`B_NO_MEMORY`.
	- The output buffer is too small.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BControllable::SetParameterWeb(BParameterWeb* web)
:::

:::{cpp:function} BParameterWeb* BControllable::SetParameterWeb()
:::

Your constructor should create a {cpp:class}`BParameterWeb` object and
call {hmethod}`SetParameterWeb()` with it as an argument. This will
describe to the outside world what parameters are available and how they
relate to each other; in other words, this describes your internal signal
path, and how it can be manipulated.

If the {hparam}`web` argument isn't {cpp:expr}`NULL`, and is different
from the previously-established web for the {hclass}`BControllable` node, a
{cpp:enumerator}`B_MEDIA_WEB_CHANGED` message is sent to everyone watching
for media notifications. See {cpp:func}`StartWatching()
<BMediaRoster::StartWatching>` for more information.

{hmethod}`SetParameterWeb()` will return {cpp:enumerator}`B_OK` if the web
was set without errors; otherwise an error code will be returned.

The {hmethod}`Web()` function returns the {cpp:class}`BParameterWeb`
assigned to the {hclass}`BControllable`.
::::

::::{abi-group}
:::{cpp:function} virtual status_t BControllable::StartControlPanel(BMessenger* outMessenger)
:::

This hook function is called whenever a client application wants the node
to present its own control panel user interface (so that the user can
configure the node).

On return, {hparam}`outMessenger` is a {cpp:class}`BMessenger` that you
can use to communicate with the control panel.

Because the add-on lives in the Media Server, and a problem in the user
interface could bring down the entire system, it's recommended that the
control panel run as its own team. This can be done easily by writing your
node as both a Media Server add-on (by exporting make_media_addon()) and an
application (by implementing main() and including start_dyn.o among the
link libraries). Be sure you have the multi-launch application flags set on
your add-on, or this won't work right.

Then your {hmethod}`StartControlPanel()` implementation can simply launch
the add-on as an application, and if the user double-clicks the add-on,
they'll be presented with the control panel. In addition, the user benefits
by only having to install a single file for your add-on to work properly.

The first argv argument to your main() function will be a string of the
format "node=%d" with the node ID in question as "%d".

:::{admonition} Note
:class: note
The above implementation suggestion (providing your control panel by
launching the add-on as an application) is the default behavior of
{hmethod}`StartControlPanel()`, so if that's how you implement your
{hclass}`BControllable`, you don't have to override
{hmethod}`StartControlPanel()` at all. In this case, the returned
{cpp:class}`BMessenger` is for the control panel application, and not for a
particular {cpp:class}`BWindow` or {cpp:class}`BView` therein.
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
	- No errors occurred.
-
	- {cpp:enumerator}`B_ERROR`.
	- Node wasn't loaded from an add-on.
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- An error occurred locating the image from which the node was loaded, or
		the add-on can't be launched as an application.
-
	- {cpp:enumerator}`B_LAUNCH_FAILED`.
	- The control panel couldn't be launched for some other reason, such as
		insufficient memory.

:::
::::
