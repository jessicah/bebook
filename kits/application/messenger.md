:::{cpp:class} BMessenger
:::

# BMessenger

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BMessenger::BMessenger(const BHandler* handler, const BLooper* looper = NULL, status_t* error = NULL)
:::

:::{cpp:function} BMessenger::BMessenger(const char* signature, team_id team = -1, status_t* error = NULL)
:::

:::{cpp:function} BMessenger::BMessenger(const BMessenger& messenger)
:::

:::{cpp:function} BMessenger::BMessenger()
:::

Creates a new {hclass}`BMessenger` and sets its target to a local
{hparam}`looper`/{hparam}`handler`, to the (running) application identified
by {hparam}`signature` or {hparam}`team`, or to the target of some other
{hparam}`messenger`.

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
	- looper/handler.
	- To target a looper, supply a {hparam}`looper` and pass a {cpp:expr}`NULL`
		{hparam}`handler`. When the messenger sends a message, the message will be
		handled by {hparam}`looper`'s preferred handler. If you want the message to
		be sent to a specific handler within a looper, supply a {hparam}`handler`
		and pass a {cpp:expr}`NULL` {hparam}`looper`. The handler must already be
		attached to a looper, and can't switch loopers after this
		{hclass}`BMessenger` is constructed.
-
	- signatureorteam.
	- If you supply a {hparam}`signature` but leave {hparam}`team` as -1, the
		messenger targets an app with that signature. (The app must already be
		running; in the case of multiple instances of a running app, the exact
		instance is indeterminate) If you supply a {hparam}`team` but no
		{hparam}`signature`, you target exactly that {hparam}`team`, regardless of
		{hparam}`signature`. By supplying both a {hparam}`team` and a
		{hparam}`signature`, you can specify a specific instance of an app. In this
		case, {hparam}`team` must be an app that has the proper
		{hparam}`signature`.

:::

Messages sent to a remote target are received and handled by the remote
application's {cpp:class}`BApplication` object.

The {hclass}`BMessenger` doesn't own its target.

The constructor places an error code in {hparam}`error` (if provided).

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
	- The target was properly set.
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- The application identified by {hparam}`signature` couldn't be found, or
		both {hparam}`handler` and {hparam}`looper` are invalid.
-
	- {cpp:enumerator}`B_BAD_TEAM_ID`.
	- Invalid {hparam}`team`.
-
	- {cpp:enumerator}`B_MISMATCHED_VALUES`.
	- {hparam}`team` isn't a {hparam}`signature` app, or {hparam}`handler` is
		associated with a {cpp:class}`BLooper` other than {hparam}`looper`.
-
	- {cpp:enumerator}`B_BAD_HANDLER`.
	- {hparam}`handler` isn't associated with a {ref}`BLooper`

:::
::::

::::{abi-group}
:::{cpp:function} BMessenger::~BMessenger()
:::

Frees the {hclass}`BMessenger`; the target isn't affected.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} bool BMessenger::IsValid() const
:::

Returns {cpp:expr}`true` if the target looper, whether local or remote,
still exists.

:::{admonition} Warning
:class: warning
This function doesn't tell you whether the looper is actually ready to
receive messages, or whether the handler (if it was specified in the
constructor) exists. In other words, a valid {hclass}`BMessenger` is no
guarantee that a message will actually get to the target.
:::
::::

::::{abi-group}
:::{cpp:function} bool BMessenger::LockTarget() const
:::

:::{cpp:function} status_t BMessenger::LockTargetWithTimeout(bigtime_t timeout) const
:::

:::{admonition} Important
:class: important
These functions apply to local targets only.
:::

These functions attempt to lock the target looper in the manner of the
similarly named {cpp:class}`BLooper` functions (see
{cpp:func}`BLooper::Lock` ). In addition to the error codes reported there,
these functions return {cpp:expr}`false` and {cpp:enumerator}`B_BAD_VALUE`
(respectively) if the target isn't local, or if the looper is otherwise
invalid.
::::

::::{abi-group}
:::{cpp:function} status_t BMessenger::SendMessage(BMessage* message, BMessage* reply, bigtime_t deliveryTimeout = B_INFINITE_TIMEOUT, bigtime_t replyTimeout = B_INFINITE_TIMEOUT) const
:::

:::{cpp:function} status_t BMessenger::SendMessage(BMessage* message, BHandler* replyHandler = NULL, bigtime_t deliveryTimeout = B_INFINITE_TIMEOUT) const
:::

:::{cpp:function} status_t BMessenger::SendMessage(BMessage* message, BMessenger* replyMessenger, bigtime_t deliveryTimeout = B_INFINITE_TIMEOUT) const
:::

:::{cpp:function} status_t BMessenger::SendMessage(uint32 command, BMessage* reply) const
:::

:::{cpp:function} status_t BMessenger::SendMessage(uint32 command, BHandler* replyHandler = NULL) const
:::

Sends a copy of {hparam}`message` (or a {cpp:class}`BMessage` based on a
{hparam}`command` constant) to the object's target. The caller retains
ownership of {hparam}`message`. The function doesn't return until the
message has been delivered; if you're sending a {hparam}`message` (as
opposed to a {hparam}`command` constant) you can set a microsecond delivery
timeout through {hparam}`deliveryTimeout`.

The target can respond to the message:

-   If you supply a {hparam}`reply` {cpp:class}`BMessage`, the response is
synchronous, with an optional timeout ({hparam}`replyTimeout`) that starts
ticking after the original message has been delivered. If the response
times out, or the target deletes the original message without responding,
the {hparam}`reply`->{hparam}`what` is set to {cpp:enumerator}`B_NO_REPLY`.
The caller is responsible for allocating and freeing {hparam}`reply`.
{hparam}`message` and {hparam}`reply` can be the same object.

  :::{admonition} Warning
:class: warning
  Use caution when requesting a synchronous reply: If you call
{hmethod}`SendMessage()` from the target looper's thread, you'll deadlock
(or, at best, time out).
:::

-   If you supply a reply target ({hparam}`replyMessenger` or
{hparam}`replyHandler`), the response is asynchronous, and is sent to the
reply target.

-   If you supply neither a reply message nor a reply target, the target's
response is sent to {hparam}`be_app_messenger`.

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
	- The message was delivered (and the synchronous reply was received, if
		applicable).
-
	- {cpp:enumerator}`B_TIMED_OUT`.
	- {hparam}`deliveryTimeout` expired; the message never made it to the
		target.
-
	- {cpp:enumerator}`B_WOULD_BLOCK`.
	- You requested a 0 {hparam}`deliveryTimeout`, and the target's message
		queue is full.
-
	- {cpp:enumerator}`B_BAD_PORT_ID`.
	- The messenger's target is invalid, or the reply port was deleted while
		waiting for a reply (synchronous response requests only).
-
	- {cpp:enumerator}`B_NO_MORE_PORTS`.
	- You asked for a synchronous reply, but there are no more reply ports.

:::

:::{admonition} Warning
:class: warning
If you specified a {hparam}`handler` when you constructed your
{hclass}`BMessenger`, and if that handler has since changed loopers,
{hmethod}`SendMessage()` won't deliver its message, but it doesn't complain
(it returns {cpp:enumerator}`B_OK`).
:::
::::

::::{abi-group}
:::{cpp:function} BHandler BMessenger::Target(BLooper** looper) const
:::

:::{cpp:function} bool BMessenger::IsTargetLocal() const
:::

:::{cpp:function} inline team_id BMessenger::Team() const
:::

{hmethod}`Target()` returns the {hclass}`BMessenger`'s handler (directly)
and looper (by reference in {hparam}`looper`). This function only works for
local targets. If {hmethod}`Target()` returns {cpp:expr}`NULL`, it can mean
one of four things:

1.    The target is remote; {hparam}`looper` is set to {cpp:expr}`NULL`.

2.    The {hclass}`BMessenger` hasn't been initialized; {hparam}`looper` is set
to {cpp:expr}`NULL`.

3.    The handler is the looper's preferred handler; {hparam}`looper` will be
valid.

4.    The handler has been deleted; {hparam}`looper` will be valid given that it
hasn't been deleted as well.

{hmethod}`IsTargetLocal()` returns {cpp:expr}`true` if the target is
local. {hmethod}`Team()` returns a target's team.
::::

## Operators

::::{abi-group}
:::{cpp:function} BMessenger& BMessenger::operator=(const BMessenger& from)
:::

Sets the left-side {hclass}`BMessenger`'s target to that of the right-side
object.
::::

::::{abi-group}
:::{cpp:function} bool BMessenger::operator==(const BMessenger& other) const
:::

Two {hclass}`BMessenger`s are equal if they have the same target.
::::
