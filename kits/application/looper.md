:::{cpp:class} BLooper
:::

# BLooper

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BLooper::BLooper(const char* name = NULL, int32 priority = B_NORMAL_PRIORITY, int32 portCapacity = B_LOOPER_PORT_DEFAULT_CAPACITY)
:::

:::{cpp:function} BLooper::BLooper(BMessage* archive)
:::

Assigns the {hclass}`BLooper` object a {hparam}`name` and then locks it
(by calling {cpp:func}`Lock() <BLooper::Lock>`). {hparam}`priority` is a
value that describes the amount of CPU attention the message loop will
receive once it starts running, and {hparam}`portCapacity` is the number of
messages the {hclass}`BLooper` can hold in its "message port" (this is
__not__ the message queue, as explained below).

After you construct the {hclass}`BLooper`, you have to tell it to
{cpp:func}`Run() <BLooper::Run>`. Because the object is locked,
{cpp:func}`Run() <BLooper::Run>` can only be called from the thread that
constructed the object. It's legal to invoke {cpp:func}`Run()
<BLooper::Run>` from within a subclass implementation of the constructor.

#### Priority

A set of priority values are defined in kernel/OS.h; from lowest to
highest, they are:

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
	- {cpp:enumerator}`B_LOW_PRIORITY`
	- For threads running in the background that shouldn't interrupt other
		threads.
-
	- {cpp:enumerator}`B_NORMAL_PRIORITY`
	- For all ordinary threads, including the main thread.
-
	- {cpp:enumerator}`B_DISPLAY_PRIORITY`
	- For threads associated with objects in the user interface, including
		window threads.
-
	- {cpp:enumerator}`B_URGENT_DISPLAY_PRIORITY`
	- For interface threads that deserve more attention than ordinary windows.
-
	- {cpp:enumerator}`B_REAL_TIME_DISPLAY_PRIORITY`
	- For threads that animate the on-screen display.
-
	- {cpp:enumerator}`B_URGENT_PRIORITY`
	- For threads performing time-critical computations.
-
	- {cpp:enumerator}`B_REAL_TIME_PRIORITY`
	- For threads controlling real-time processes that need unfettered access to
		the CPUs.

:::

#### Port Capacity

Messages that are sent to a {hclass}`BLooper` first show up in a port (as
the term is defined by the {ref}`Kernel Kit`), and then are moved to the
{cpp:class}`BMessageQueue`. The capacity of the {cpp:class}`BMessageQueue`
is virtually unlimited; the capacity of the port is not. Although messages
are moved from the port to the queue as quickly as possible, the port can
fill up. A full port will block subsequent message senders.

The default port capacity (100), should be sufficient for most apps, but
you can fiddle with it through the {hparam}`portCapacity` argument.
::::

::::{abi-group}
:::{cpp:function} virtual BLooper::~BLooper()
:::

Frees the message queue and all pending messages and deletes the message
loop. {cpp:class}`BHandler`s that have been added to the {hclass}`BLooper`
are not deleted, but {cpp:class}`BMessageFilter` objects added as common
filters are.

In general, you should never delete your {hclass}`BLooper` objects: With
the exception of the {cpp:class}`BApplication` object, {hclass}`BLooper`s
are destroyed by the {cpp:func}`Quit() <BLooper::Quit>` function.

:::{admonition} Warning
:class: warning
If you create a {hclass}`BLooper`-derived class that uses multiple
inheritance, make sure the first class your mixin class inherits from is
{hclass}`BLooper`; otherwise, you'll crash when you try to close the
window. This happens because of an interaction between the window thread
how C++ deletes objects of a multiply-inherited class. In other words:

is safe, whilst

is not.
:::
::::

## Hook Functions

::::{abi-group}
:::{cpp:function} virtual void BLooper::DispatchMessage(BMessage* message, BHandler* target)
:::

{hmethod}`DispatchMessage()` is the {hclass}`BLooper`'s central
message-processing function. It's called automatically as messages arrive
in the looper's queue, one invocation per message. You never invoke
{hmethod}`DispatchMessage()` yourself.

The default implementation passes {hparam}`message` to {hparam}`handler`
by invoking the latter's {cpp:func}`MessageReceived()
<BHandler::MessageReceived>`:

:::{code} cpp
target->MessageReceived(message);
:::

The only exception is where {hparam}`message`.what is
{cpp:enumerator}`B_QUIT_REQUESTED` and {hparam}`handler` is the looper
itself; in this case, the object invokes its own {cpp:func}`QuitRequested()
<BLooper::QuitRequested>` function.

You can override this function to dispatch the messages that your own
application defines or recognizes. All unhandled messages should be passed
to the base class version, as demonstrated below:

:::{code} cpp
void MyLooper::DispatchMessage(BMessage *msg,
                               BHandler *target)
{
   switch ( msg->what ) {
   case MY_MESSAGE1:
      ...
      break;
   case MY_MESSAGE2:
      ...
      break;
   default:
      baseClass::DispatchMessage(msg, target);
      break;
   }
}
:::

Also, note that you mustn't delete {hparam}`message`; it's deleted for
you..

The system locks the {hclass}`BLooper` before calling
{hmethod}`DispatchMessage()` and keeps it locked for the duration of the
function.
::::

::::{abi-group}
:::{cpp:function} virtual bool BLooper::QuitRequested()
:::

Hook function that's invoked when the {hclass}`BLooper` receives a
{cpp:enumerator}`B_QUIT_REQUESTED` message. You never invoke this function
directly. Derived classes implement this function to return
{cpp:expr}`true` if it's okay to quit this {hclass}`BLooper`, and
{cpp:expr}`false` if not. Note that this function does not actually quit
the object—the code that handles the {cpp:enumerator}`B_QUIT_REQUESTED`
message does that.

{hclass}`BLooper`'s default implementation of {hmethod}`QuitRequested()`
always returns {cpp:expr}`true`.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} virtual void BLooper::AddCommonFilter(BMessageFilter* filter)
:::

:::{cpp:function} virtual bool BLooper::RemoveCommonFilter(BMessageFilter* filter)
:::

:::{cpp:function} virtual void BLooper::SetCommonFilterList(BList* filters)
:::

:::{cpp:function} BList* BLooper::CommonFilterList() const
:::

These functions manage the {hclass}`BLooper`'s list of
{cpp:class}`BMessageFilter`s. Message filters are objects that screen
in-coming messages. In the case of {hclass}`BLooper`, each message is
passed through all filters in the list before it's passed on to
{cpp:func}`DispatchMessage() <BLooper::DispatchMessage>`. The order of the
filters in the list is determinate. See the {cpp:class}`BMessageFilter`
class for details on how message filters work.

{hmethod}`AddCommonFilter()` adds {hparam}`filter` to the end of the
filter list (creating a {cpp:class}`BList` container if necessary).

{hmethod}`RemoveCommonFilter()` removes {hparam}`filter` from the list,
but doesn't free the filter. It returns {cpp:expr}`true` if successful, and
{cpp:expr}`false` if it can't find the specified filter.

{hmethod}`SetCommonFilterList()` deletes the current filter list and its
contents, and replaces it with {hparam}`filters`. All elements in
{hparam}`filters` must be {cpp:class}`BMessageFilter` pointers. The
{hclass}`BLooper` takes ownership of all objects in {hparam}`filters`, as
well as {hparam}`filters` itself. If {hparam}`filters` is {cpp:expr}`NULL`,
the current list is deleted without a replacement.

{hmethod}`CommonFilterList()` returns a pointer to the current list. You
can examine the list but you shouldn't modify or delete it.

:::{admonition} Warning
:class: warning
For all but {hmethod}`CommonFilterList()`, the {hclass}`BLooper` must be
locked.
:::
::::

::::{abi-group}
:::{cpp:function} void BLooper::AddHandler(BHandler* handler)
:::

:::{cpp:function} bool BLooper::RemoveHandler(BHandler* handler)
:::

:::{cpp:function} BHandler* BLooper::HandlerAt(int32 index) const
:::

:::{cpp:function} int32 BLooper::CountHandlers() const
:::

:::{cpp:function} int32 BLooper::IndexOf(BHandler* handler) const
:::

{hmethod}`AddHandler()` adds {hparam}`handler` to the {hclass}`BLooper`'s
list of {cpp:class}`BHandler` objects, and {hmethod}`RemoveHandler()`
removes it. Only {cpp:class}`BHandler` that have been added to the list are
eligible to respond to the messages the {hclass}`BLooper` dispatches.

{hmethod}`AddHandler()` fails if the handler already belongs to a
{hclass}`BLooper`; a {cpp:class}`BHandler` can belong to no more than one
{hclass}`BLooper` at a time. It can change its affiliation from time to
time, but must be removed from one {hclass}`BLooper` before it can be added
to another. {hmethod}`RemoveHandler()` returns {cpp:expr}`true` if it
succeeds in removing the {cpp:class}`BHandler` from the {hclass}`BLooper`,
and {cpp:expr}`false` if not or if the handler doesn't belong to the
{hclass}`BLooper` in the first place.

{hmethod}`AddHandler()` also calls the handler's
{cpp:func}`SetNextHandler() <BHandler::SetNextHandler>` function to assign
it the {hclass}`BLooper` as its default next handler.
{hmethod}`RemoveHandler()` calls the same function to set the handler's
next handler to {cpp:expr}`NULL`.

{hmethod}`HandlerAt()` returns the {cpp:class}`BHandler` object currently
located at {hparam}`index` in the {hclass}`BLooper`'s list of eligible
handlers, or {cpp:expr}`NULL` if the index is out of range. Indices begin
at 0 and there are no gaps in the list. {hmethod}`CountHandlers()` returns
the number of objects currently in the list; the count should always be at
least 1, since the list automatically includes the {hclass}`BLooper`
itself. {hmethod}`IndexOf()` returns the index of the specified
{hparam}`handler`, or {cpp:enumerator}`B_ERROR` if that object isn't in the
list.

For any of these functions to work, the {hclass}`BLooper` must be locked.

See also: {cpp:func}`BHandler::Looper`, {cpp:func}`SetNextHandler()
<BHandler::SetNextHandler>`, {cpp:func}`PostMessage()
<BLooper::PostMessage>`, the {cpp:class}`BMessenger` class
::::

::::{abi-group}
:::{cpp:function} BMessage* BLooper::CurrentMessage() const
:::

:::{cpp:function} BMessage* BLooper::DetachCurrentMessage()
:::

The message that a {hclass}`BLooper` passes to its handler(s) is called
the "current message." These functions access the current message; they're
meaningless (they return {cpp:expr}`NULL`) when called from outside the
message processing loop.

{hmethod}`CurrentMessage()` simply returns a pointer to the current
message without affecting the {cpp:class}`BMessage` object itself. This is
particularly useful to functions that respond to system messages (such as
{hmethod}`MouseDown()` and {hmethod}`ScreenChanged()`), but that aren't
sent the full {cpp:class}`BMessage` object that initiated the response.

{hmethod}`DetachCurrentMessage()` removes the current message from the
message queue and passes ownership of it to the caller; deleting the
message is the caller's responsibility. This is useful if you want to delay
the response to the message without tying up the {hclass}`BLooper`. But be
careful—if the message sender is waiting for a synchronous reply, detaching
the message and holding on to it will block the sender.
::::

::::{abi-group}
:::{cpp:function} bool BLooper::Lock()
:::

:::{cpp:function} status_t BLooper::LockWithTimeout(bigtime_t timeout)
:::

:::{cpp:function} void BLooper::Unlock()
:::

{hmethod}`Lock()` locks the {hclass}`BLooper`. Locks are held within the
context of a thread; while a {hclass}`BLooper` is locked, no other thread
can invoke its most important functions ( {cpp:func}`AddHandler()
<BLooper::AddHandler>`, {cpp:func}`DispatchMessage()
<BLooper::DispatchMessage>`, etc.)

If the looper is already locked (by some other thread), {hmethod}`Lock()`
blocks until the looper is unlocked. To set a timeout for the block, use
{hmethod}`LockWithTimeout()` instead. {hparam}`timeout` is measured in
microseconds; if it's 0, the function returns immediately (with or without
the lock); if it's {cpp:enumerator}`B_INFINITE_TIMEOUT`, it blocks without
limit.

{hmethod}`Unlock()` unlocks a locked looper. It can only be called by the
thread that currently holds the lock.

Calls to {hmethod}`Lock()`/{hmethod}`LockWithTimeout()` and
{hmethod}`Unlock()` can be nested, but locking and unlocking must always be
balanced. A single {hmethod}`Unlock()` will not undo a series of
{hmethod}`Lock()`'s.

{cpp:class}`BHandler` defines "smart" versions of these functions that
find the handler's looper and then locks it (or unlocks it) in a
pseudo-atomic operation (see {cpp:func}`BHandler::LockLooper`). You should
always use the {cpp:class}`BHandler` versions, if possible, rather than
retrieving the handler's looper and locking it yourself.

{hmethod}`Lock()` returns {cpp:expr}`true` if it was able to lock the
looper, or if it's already locked by the calling thread, and
{cpp:expr}`false` otherwise.

{hmethod}`LockWithTimeout()` returns:

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
	- The looper was successfully locked.
-
	- {cpp:enumerator}`B_TIMED_OUT`.
	- The call timed out without locking the looper.
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- This looper was deleted while the function was blocked.

:::
::::

::::{abi-group}
:::{cpp:function} thread_id BLooper::LockingThread() const
:::

:::{cpp:function} bool BLooper::IsLocked() const
:::

:::{cpp:function} int32 BLooper::CountLocks() const
:::

:::{cpp:function} int32 BLooper::CountLockRequests() const
:::

:::{cpp:function} sem_id BLooper::Sem() const
:::

These functions may be useful while debugging a {hclass}`BLooper`.

{hmethod}`LockingThread()` returns the thread that currently has the
{hclass}`BLooper` locked, or 1 if the {hclass}`BLooper` isn't locked.

{hmethod}`IsLocked()` returns {cpp:expr}`true` if the calling thread
currently has the {hclass}`BLooper` locked (if it's the locking thread) and
{cpp:expr}`false` if not (if some other thread is the locking thread or the
{hclass}`BLooper` isn't locked).

{hmethod}`CountLocks()` returns the number of times the locking thread has
locked the {hclass}`BLooper`the number of {cpp:func}`Lock()
<BLooper::Lock>` (or {cpp:func}`LockWithTimeout() <BLooper::Lock>`) calls
that have not yet been balanced by matching {cpp:func}`Unlock()
<BLooper::Lock>` calls.

{hmethod}`CountLockRequests()` returns the number of threads currently
trying to lock the {hclass}`BLooper`. The count includes the thread that
currently has the lock plus all threads currently waiting to acquire it.

{hmethod}`Sem()` returns the {htype}`sem_id` for the semaphore that the
{hclass}`BLooper` uses to implement the locking mechanism.

See also: {cpp:func}`Lock() <BLooper::Lock>`
::::

::::{abi-group}
:::{cpp:function} virtual void BLooper::MessageReceived(BMessage* message)
:::

Simply calls the inherited function. For the current release, the
{hclass}`BLooper` implementation of this function does nothing of
importance.

See also: {cpp:func}`BHandler::MessageReceived`
::::

::::{abi-group}
:::{cpp:function} BMessageQueue* BLooper::MessageQueue() const
:::

Returns the queue that holds messages delivered to the {hclass}`BLooper`'s
thread. You rarely need to examine the message queue directly; it's made
available so you can cheat fate by looking ahead.

See also: the {cpp:class}`BMessageQueue` class
::::

::::{abi-group}
:::{cpp:function} status_t BLooper::PostMessage(BMessage* message)
:::

:::{cpp:function} status_t BLooper::PostMessage(uint32 command)
:::

:::{cpp:function} status_t BLooper::PostMessage(BMessage* message, BHandler* handler, BHandler* replyHandler = NULL)
:::

:::{cpp:function} status_t BLooper::PostMessage(uint32 command, BHandler* handler, BHandler* replyHandler = NULL)
:::

{hmethod}`PostMessage()` is similar to
{cpp:func}`BMessenger::SendMessage`. The {cpp:func}`BMessenger` version is
preferred (it's a bit safer than {hmethod}`PostMessage()`).

Places a message at the far end of the {hclass}`BLooper`'s message queue.
The message will be processed by {cpp:func}`DispatchMessage()
<BLooper::DispatchMessage>` when it comes to the head of the queue.

The message can be a full {cpp:class}`BMessage` object
({hparam}`message`), or just a command constant ({hparam}`command`). In the
former case, the message is copied and the caller retains ownership of the
argument, which can be deleted as soon as {hmethod}`PostMessage()` returns.
In the latter case, a {cpp:class}`BMessage` is created (and deleted) for
you.

{hparam}`handler` is the designated handler for the message, and must be
part of this {hclass}`BLooper`'s handler chain. If handler is (literally)
{cpp:expr}`NULL`, the designated handler is the {hclass}`BLooper`'s
preferred handler at the time {cpp:func}`DispatchMessage()
<BLooper::DispatchMessage>` is called. In the versions of
{hmethod}`PostMessage()` that don't have a handler argument, the designated
handler is the {hclass}`BLooper` object itself.

Replies to the message are delivered to {hparam}`replyHandler`. If a
{hparam}`replyHandler` isn't specified, replies are sent to
{hparam}`be_app_messenger`.

A {hclass}`BLooper` should never post a message to itself from within its
own message loop thread.

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
	- The message was successfully posted.
-
	- {cpp:enumerator}`B_MISMATCHED_VALUES`.
	- {hparam}`handler` doesn't belong to this {hclass}`BLooper`.
-
	- Other errors.
	- See the return values for {cpp:func}`BMessenger::SendMessage`.

:::
::::

::::{abi-group}
:::{cpp:function} virtual void BLooper::Quit()
:::

Shuts down the message loop (if it's running), and deletes the
{hclass}`BLooper`. The object must be locked.

When {hmethod}`Quit()` is called from the {hclass}`BLooper`'s thread, the
message loop is immediately stopped and any messages in the message queue
are deleted (without being processed). Note that, in this case,
{hmethod}`Quit()` doesn't return since the calling thread is dead.

When called from another thread, {hmethod}`Quit()` waits until all
messages currently in the queue have been handled before it kills the
message loop. It returns after the {hclass}`BLooper` has been deleted.

If you're quitting a {hclass}`BLooper` from some other thread, you should
send the object a {cpp:enumerator}`B_QUIT_REQUESTED` message rather than
calling {hmethod}`Quit()` directly.
::::

::::{abi-group}
:::{cpp:function} virtual thread_id BLooper::Run()
:::

Spawns the message loop thread and starts it running. {hmethod}`Run()`
expects the {hclass}`BLooper` to be locked (once only!) when it's called;
it unlocks the object before it returns. Keep in mind that a
{hclass}`BLooper` is locked when it's constructed.

:::{admonition} Caution
:class: caution
Calling {hmethod}`Run()` on a {hclass}`BLooper` that's already running
will dump you into the debugger.
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
	- Positive values.
	- The thread was successfully spawned and started; this is the
		{htype}`thread_id` for the thread.
-
	- Thread errors.
	- See {cpp:func}`spawn_thread() <spawn::thread>` and
		{cpp:func}`resume_thread() <resume::thread>`.
-
	- Port errors.
	- See {cpp:func}`create_port() <create::port>`.

:::
::::

::::{abi-group}
:::{cpp:function} void BLooper::SetPreferredHandler(BHandler* handler) const
:::

:::{cpp:function} BHandler* BLooper::PreferredHandler()
:::

These functions set and return the {hclass}`BLooper`'s preferred
handler—the {cpp:class}`BHandler` object that should handle messages not
specifically targetted to another {cpp:class}`BHandler`.

To designate the current preferred handler, whatever object that may be,
as the target of a message, pass {cpp:expr}`NULL` for the target handler to
{cpp:func}`PostMessage() <BLooper::PostMessage>` or to the
{cpp:func}`BMessenger constructor <BMessenger::BMessenger()>`.

Posting or sending messages to the preferred handler can be useful. For
example, in the {ref}`Interface Kit`, {cpp:class}`BWindow` objects name the
current focus view as the preferred handler. This makes it possible for
other objects, such as {cpp:class}`BMenuItem`s and {cpp:class}`BButtons`,
to target messages to the {cpp:class}`BView` that's currently in focus,
without knowing what view that might be. For example, by posting its
messages to the window's preferred handler, a Cut menu item can make sure
that it always acts on whatever view contains the current selection. See
the chapter on the {ref}`Interface Kit` for information on windows, views,
and the role of the focus view.

By default, {hclass}`BLooper`s don't have a preferred handler; until one
is set, {hmethod}`PreferredHandler()` returns {cpp:expr}`NULL`. Note
however, that messages targeted to the preferred handler are dispatched to
the {hclass}`BLooper` whenever the preferred handler is {cpp:expr}`NULL`.
In other words, the {hclass}`BLooper` acts as default preferred handler,
even though the default is formally {cpp:expr}`NULL`.

See also: {cpp:func}`BInvoker::SetTarget`, {cpp:func}`PostMessage()
<BLooper::PostMessage>`
::::

::::{abi-group}
:::{cpp:function} thread_id BLooper::Thread() const
:::

:::{cpp:function} team_id BLooper::Team() const
:::

These functions identify the thread that runs the message loop and the
team to which it belongs. {hmethod}`Thread()` returns
{cpp:enumerator}`B_ERROR` if {cpp:func}`Run() <BLooper::Run>` hasn't yet
been called to spawn the thread and begin the loop. {hmethod}`Team()`
always returns the application's {htype}`team_id`.
::::

## Static Functions

::::{abi-group}
:::{cpp:function} static BLooper* BLooper::LooperForThread(thread_id thread)
:::

Returns the {hclass}`BLooper` object that spawned the specified thread, or
{cpp:expr}`NULL` if the thread doesn't belong to a {hclass}`BLooper`.
::::

## Constants

::::{abi-group}
:::{cpp:enumerator} B_LOOPER_PORT_DEFAULT_CAPACITY
:::

:::{code} c
#define B_LOOPER_PORT_DEFAULT_CAPACITY 100
:::

The default capacity of the port that holds incoming messages before
they're placed in the {hclass}`BLooper`'s {cpp:class}`BMessageQueue`. The
capacity is set in the {hclass}`BLooper` {cpp:func}`constructor
<BLooper::BLooper()>`.
::::
