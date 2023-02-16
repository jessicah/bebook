:::{cpp:class} BInvoker
:::

# BInvoker

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BInvoker::BInvoker(BMessage* message, BMessenger messenger)
:::

:::{cpp:function} BInvoker::BInvoker(BMessage* message, const BHandler* handler, const BLooper* looper = NULL)
:::

:::{cpp:function} BInvoker::BInvoker()
:::

Initializes the {hclass}`BInvoker` by setting its message and its
messenger.

-   The object's {cpp:class}`BMessage` is taken directly as
{hparam}`message`—the object is __not__ copied. The {hclass}`BInvoker`
takes over ownership of the {cpp:class}`BMessage` that you pass in.

-   The object's {cpp:class}`BMessenger` is copied from {hparam}`messenger`,
or initialized with {hparam}`looper` and {hparam}`handler`. See the
{cpp:class}`BMessenger` class for details on how a {cpp:class}`BMessenger`
identifies a target.

If you want a reply handler, you have to call
{cpp:func}`SetHandlerForReply() <BInvoker::SetHandlerForReply>` after the
constructor returns. You can reset the message and messenger through
{cpp:func}`SetMessage() <BInvoker::SetMessage>` and {cpp:func}`SetTarget()
<BInvoker::SetTarget>`.
::::

::::{abi-group}
:::{cpp:function} virtual BInvoker::~BInvoker()
:::

Deletes the object's {cpp:class}`BMessage`.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} void BInvoker::BeginInvokeNotify(uint32 kind = B_CONTROL_INVOKED)
:::

:::{cpp:function} void BInvoker::EndInvokeNotify()
:::

If for some reason you need to implement a method that emulates an
{cpp:func}`InvokeNotify() <BInvoker::Invoke>` call inside an
{cpp:func}`Invoke() <BInvoker::Invoke>` implementation, you should wrap the
invocation code in these functions. They set up and tear down an
{cpp:func}`InvokeNotify() <BInvoker::Invoke>` context.
::::

::::{abi-group}
:::{cpp:function} virtual status_t BInvoker::Invoke(BMessage* message = NULL)
:::

:::{cpp:function} status_t BInvoker::InvokeNotify(BMessage* message, uint32 kind = B_CONTROL_INVOKED)
:::

{hmethod}`Invoke()` tells the {hclass}`BInvoker`'s messenger to send a
message. If {hparam}`message` is non-{cpp:expr}`NULL`, that message is
sent, otherwise the object sends its default message (i.e. the
{cpp:class}`BMessage` that was passed in the constructor or in
{cpp:func}`SetMessage() <BInvoker::SetMessage>`). The message is sent
asynchronously with no time limit on the reply.

:::{admonition} Note
:class: note
Regarding the use of the default message vs the argument, a common
practice is to reserve the default message as a template, and pass a
fine-tuned copy to {hmethod}`Invoke()`
:::

The {hmethod}`InvokeNotify()` function sends the {hparam}`message` to the
target, using the notification change code specified by {hparam}`kind`. If
{hparam}`message` is {cpp:expr}`NULL`, nothing gets sent to the target, but
any watchers of the invoker's handler will receive their expected
notifications. By default, the {hparam}`kind` is
{cpp:enumerator}`B_CONTROL_INVOKED`, the same kind sent by a straight
{hmethod}`Invoke()`.

{hmethod}`Invoke()` doesn't call {cpp:func}`SendNotices()
<BHandler::SendNotices>` by default; you'll have to implement code to do it
yourself. Here's how:

:::{code} cpp
status_t BControl::Invoke(BMessage* msg) {
   bool notify = false;
   uint32 kind = InvokeKind(notify);

   BMessage clone(kind);
   status_t err = B_BAD_VALUE;

   if (!msg && !notify) {
      // If no message is supplied, pull it from the BInvoker.
      // However, ONLY do so if this is not an InvokeNotify()
      // context -- otherwise, this is not the default invocation
      // message, so we don't want it to get in the way here.
      // For example, a control may call InvokeNotify() with their
      // "modification" message... if that message isn't set,
      // we still want to send notification to any watchers, but
      // -don't- want to send a message through the invoker.
      msg = Message();
   }

   if (!msg) {
      // If not being watched, there is nothing to do.
      if( !IsWatched() ) return err;
   } else {
      clone = *msg;
   }

   clone.AddInt64("when", system_time());
   clone.AddPointer("source", this);
   clone.AddInt32("be:value",fValue);
   clone.AddMessenger(B_NOTIFICATION_SENDER, BMessenger(this));

   if( msg ) err = BInvoker::Invoke(&clone);

   // Also send invocation to any observers of this handler.
   SendNotices(kind, clone);

   return err;
}
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
	- The message was sent.
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- No default message, and no message argument.
-
	- Other errors.
	- Forwarded from {cpp:func}`BMessenger::SendMessage`.

:::
::::

::::{abi-group}
:::{cpp:function} uint32 BInvoker::InvokeKind(bool* notify = NULL)
:::

Returns the kind passed to {cpp:func}`InvokeNotify() <BInvoker::Invoke>`.
This should be called from within your implementation of
{cpp:func}`Invoke() <BInvoker::Invoke>` if you need to determine what kind
was specified when {cpp:func}`InvokeNotify() <BInvoker::Invoke>` was
called. If you care whether {cpp:func}`Invoke() <BInvoker::Invoke>` or
{cpp:func}`InvokeNotify() <BInvoker::Invoke>` was originally called, you
can specify a pointer to a {htype}`bool`, {hparam}`notify`, which is set to
{cpp:expr}`true` if {cpp:func}`InvokeNotify() <BInvoker::Invoke>` was
called, or {cpp:expr}`false` if {cpp:func}`Invoke() <BInvoker::Invoke>` was
called. This lets you fetch the {cpp:func}`InvokeNotify()
<BInvoker::Invoke>` arguments from your {cpp:func}`Invoke()
<BInvoker::Invoke>` code without breaking compatibility with older
applications by adding arguments to {cpp:func}`Invoke()
<BInvoker::Invoke>`.
::::

::::{abi-group}
:::{cpp:function} virtual status_t BInvoker::SetHandlerForReply(BHandler* replyHandler)
:::

:::{cpp:function} BHandler* BInvoker::HandlerForReply() const
:::

{hmethod}`SetHandlerForReply()` sets the {cpp:class}`BHandler` object that
handles replies that are sent back by the target. By default (or if
{hparam}`replyHandler` is {cpp:expr}`NULL`), replies are sent to the
{cpp:class}`BApplication` object.

{hmethod}`HandlerForReply()` returns the object set through
{hmethod}`SetHandlerForReply()`. If the reply handler isn't set, this
function returns {cpp:expr}`NULL`, it doesn't return {cpp:var}`be_app`
(even though {cpp:var}`be_app` will be handling the reply).

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
	- {hmethod}`SetHandlerForReply()` always returns {cpp:enumerator}`B_OK` it
		doesn't check for validity.

:::
::::

::::{abi-group}
:::{cpp:function} virtual status_t BInvoker::SetMessage(BMessage* message)
:::

:::{cpp:function} BMessage* BInvoker::Message() const
:::

:::{cpp:function} uint32 BInvoker::Command() const
:::

{hmethod}`SetMessage()` sets the {hclass}`BInvoker`'s default message to
point to {hparam}`message` (the message is __not__ copied). The previous
default message (if any) is deleted; a {cpp:expr}`NULL` {hparam}`message`
deletes the previous message without setting a new one. The
{hclass}`BInvoker` owns the {cpp:class}`BMessage` that you pass in; you
mustn't delete it yourself.

{hmethod}`Message()` returns a pointer to the default message, and
{hmethod}`Command()` returns its {hparam}`what` data member. Lacking a
default message, the functions return {cpp:expr}`NULL`.

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
	- {hmethod}`SetMessage()` always returns {cpp:enumerator}`B_OK`.

:::
::::

::::{abi-group}
:::{cpp:function} virtual status_t BInvoker::SetTarget(BMessenger messenger)
:::

:::{cpp:function} virtual status_t BInvoker::SetTarget(const BHandler* handler, const BLooper* looper = NULL)
:::

:::{cpp:function} BHandler* BInvoker::Target(BLooper** looper = NULL) const
:::

:::{cpp:function} bool BInvoker::IsTargetLocal() const
:::

:::{cpp:function} BMessenger BInvoker::Messenger() const
:::

These functions set and query the {hclass}`BInvoker`'s target. This is the
{cpp:class}`BHandler` to which the object sends a message when
{cpp:func}`Invoke() <BInvoker::Invoke>` is called. The target is
represented by a {cpp:class}`BMessenger` object; you can set the
{cpp:class}`BMessenger` as a copy of {hparam}`messenger`, or initialize it
with {hparam}`looper` and {hparam}`handler`. See the
{cpp:class}`BMessenger` class for details on how a {cpp:class}`BMessenger`
identifies a target.

{hmethod}`Target()` returns the {cpp:class}`BHandler` that's targeted by
the object's messenger. If {hparam}`looper` is non-{cpp:expr}`NULL`, the
{cpp:class}`BLooper` that owns the {cpp:class}`BHandler` is returned by
reference. If the target was set as a looper's preferred handler (i.e.
`SetTarget(NULL, looper)`), or if the target hasn't been set yet,
{hmethod}`Target()` returns {cpp:expr}`NULL`. The function returns
{cpp:expr}`NULL` for both objects if the target is remote.

{hmethod}`IsTargetLocal()` returns {cpp:expr}`true` if the target lives
within the {hclass}`BInvoker`'s application, and {cpp:expr}`false` if it
belongs to some other application.

{hmethod}`Messenger()` returns a copy of the {cpp:class}`BMessenger`
object the {hclass}`BInvoker` uses to send messages. If a target hasn't
been set yet, the return will be invalid.

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
	- The target was successfully set.
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- The proposed {hparam}`handler` doesn't belong to a {cpp:class}`BLooper`.
-
	- {cpp:enumerator}`B_MISMATCHED_VALUES`.
	- {hparam}`handler` doesn't belong to {hparam}`looper`.

:::

:::{admonition} Warning
:class: warning
{hmethod}`SetTarget()` doesn't detect invalid {cpp:class}`BLooper`s and
{cpp:class}`BMessenger`s.
:::
::::

::::{abi-group}
:::{cpp:function} status_t BInvoker::SetTimeout(bigtime_t timeout)
:::

:::{cpp:function} bigtime_t BInvoker::Timeout() const
:::

{hmethod}`SetTimeout()` sets the timeout that will be used when sending
the invocation message to the invoker's target. By default this is
{cpp:enumerator}`B_INFINITE_TIMEOUT`.

{hmethod}`Timeout()` returns the current setting for this value.

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

:::
::::
