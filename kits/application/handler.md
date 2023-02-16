:::{cpp:class} BHandler
:::

# BHandler

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BHandler::BHandler(const char* name = NULL)
:::

:::{cpp:function} BHandler::BHandler(BMessage* archive)
:::

Initializes the {hclass}`BHandler` by assigning it a {hparam}`name` and
registering it with the messaging system. {hclass}`BHandler`s can also be
reconstructed from a {cpp:class}`BMessage` {hparam}`archive`.
::::

::::{abi-group}
:::{cpp:function} virtual BHandler::~BHandler()
:::

Deletes any {cpp:class}`BMessageFilter`s assigned to the
{hclass}`BHandler`.
::::

## Hook Functions

::::{abi-group}
:::{cpp:function} virtual void BHandler::MessageReceived(BMessage* message)
:::

Implemented by derived classes to respond to messages that are received by
the {hclass}`BHandler`. The default implementation of this function
responds only to scripting requests. It passes all other messages to the
next handler by calling that object's version of
{hmethod}`MessageReceived()`.

A typical {hmethod}`MessageReceived()` implementation distinguishes
between messages by looking at its command constant (i.e. the
{hparam}`what` field). For example:

:::{code} cpp
void MyHandler::MessageReceived(BMessage* message)
{
   switch ( message->what ) {
   case COMMAND_ONE:
      HandleCommandOne();
      break;

   case COMMAND_TWO:
      HandleCommandTwo();
      break;
   ...
   default:
      baseClass::MessageReceived(message);
      break;
   ...
   }
}
:::

:::{list-table}
---
header-rows: 0
align: left
widths: auto
---
-
	- {ref}``

	- It's essential that all unhandled messages are passed to the base class
		implementation of {hmethod}`MessageReceived()`, as shown here. The handler
		chain model depends on it.

:::

If the message comes to the end of the line—if it's not recognized and
there is no next handler—the {hclass}`BHandler` version of this function
sends a {cpp:enumerator}`B_MESSAGE_NOT_UNDERSTOOD` reply to notify the
message source.

:::{admonition} Important
:class: important
Do not delete the argument message when you're done with. It doesn't
belong to you.
:::
::::

## Member Functions

### Archive()

See {cpp:func}`BArchivable::Archive`

::::{abi-group}
:::{cpp:function} virtual status_t BHandler::GetSupportedSuites(BMessage* message)
:::

Implemented by derived classes to report the suites of messages and
specifiers they understand. This function is called in response to either a
{cpp:enumerator}`B_GET_PROPERTIES` scripting message for the "Suites"
property or a {cpp:enumerator}`B_GET_SUPPORTED_SUITES` message.

Each derived class should add the names of the suites it implements to the
{hparam}`suites` array of {hparam}`message`. Each item in the array is a
MIME string with the "suite" supertype. In addition, the class should add
corresponding flattened {cpp:class}`BPropertyInfo` objects in the
{hparam}`messages` array. A typical implementation of
{hmethod}`GetSupportedSuites()` looks like:

:::{code} cpp
status_t MyHandler::GetSupportedSuites(BMessage* message)
{
   message->AddString("suites", "suite/vnd.Me-my_handler"));
   BPropertyInfo prop_info(prop_list);
   message->AddFlat("messages", prop_info);

   return BHandler::GetSupportedSuites(message);
}
:::

The value returned by {hmethod}`GetSupportedSuites()` is added to
{hparam}`message` in the {htype}`int32` {hparam}`be:error` field.

{hclass}`BHandler`'s version of this function adds the universal suite
"suite/vnd.Be-handler" to {hparam}`message` then returns
{cpp:enumerator}`B_OK`.
::::

::::{abi-group}
:::{cpp:function} bool BHandler::LockLooper()
:::

:::{cpp:function} status_t BHandler::LockLooperWithTimeout(bigtime_t timeout)
:::

:::{cpp:function} void BHandler::UnlockLooper()
:::

These are "smart" versions of {cpp:class}`BLooper`'s locking functions
({cpp:func}`BLooper::Lock` et. al.). The difference between the versions is
that these functions retrieve the handler's looper and lock it (or unlock
it) in a pseudo-atomic operation, thus avoiding a race condition. Anytime
you're tempted to write code such as this:

:::{code} cpp
/* DON'T DO THIS */
if (myHandler->Looper()->Lock()) {
   ...
   myHandler->Looper()->Unlock();
}
:::

Don't do it. Instead, do this:

:::{code} cpp
/* DO THIS INSTEAD */
if (myHandler->LockLooper()) {
   ...
   myHandler->UnlockLooper();
}
:::

Except for an additional return value in
{hmethod}`LockLooperWithTimeout()`, these functions are identical to their
{cpp:class}`BLooper` analogues. See {cpp:func}`BLooper::Lock` for details.

{hmethod}`LockLooper()` returns {cpp:expr}`true` if it was able to lock
the looper, or if it's already locked by the calling thread, and
{cpp:expr}`false` otherwise. If the handler changes loopers during the
call, {cpp:expr}`false` is returned.

{hmethod}`LockLooperWithTimeout()` returns:

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
	- This handler's looper is invalid.
-
	- {cpp:enumerator}`B_MISMATCHED_VALUES`.
	- The handler switched loopers during the call.

:::
::::

::::{abi-group}
:::{cpp:function} BLooper* BHandler::Looper() const
:::

Returns the {cpp:class}`BLooper` object that the {hclass}`BHandler` has
been added to. The function returns {cpp:expr}`NULL` if the object hasn't
been added to a {cpp:class}`BLooper`. A {hclass}`BHandler` can be
associated with only one {cpp:class}`BLooper` at a time.

Note that a {cpp:class}`BLooper` object automatically adds itself (as a
handler) to itself (as a looper), and a {cpp:class}`BWindow` automatically
adds its child views. To explicitly add a handler to a looper, you call
{cpp:func}`BLooper::AddHandler`.
::::

::::{abi-group}
:::{cpp:function} virtual BHandler* BHandler::ResolveSpecifier(BMessage* message, int32 index, BMessage* specifier, int32 what, const char* property)
:::

Implemented by derived classes to determine the proper handler for a
scripting message. The message is targeted to the {hclass}`BHandler`, but
the specifiers may indicate that it should be assigned to another object.
It's the job of {hmethod}`ResolveSpecifier()` to examine the current
specifier (or more, if necessary) and return the object that should either
handle the message or look at the next specifier. This function is called
before the message is dispatched and before any filtering functions are
called.

The first argument, {hparam}`message`, points to the scripting message
under consideration. The current specifier is passed in
{hparam}`specifier`; it will be at index {hparam}`index` in the specifier
array of message. Finally, {hparam}`what` contains the what data member of
{hparam}`specifier` while {hparam}`property` contains the name of the
targetted property.

{hmethod}`ResolveSpecifier()` returns a pointer to the next
{hclass}`BHandler` that should look at the message. To identify the
{hclass}`BHandler`, it tries these methods, in order:

#### Method 1:

If the {hparam}`specifier` identifies a {hclass}`BHandler` belonging to
another {cpp:class}`BLooper`, it should send the {hparam}`message` to the
{cpp:class}`BLooper` and return {cpp:expr}`NULL`. The message will be
handled in the message loop of the other {cpp:class}`BLooper`; it won't be
further processed in this one. For example, a {hclass}`BHandler` that kept
a list of proxies might use code like the following:

:::{code} cpp
if ( (strcmp(property, "Proxy") == 0)
      && (what == B_INDEX_SPECIFIER) ) {
   int32 i;
   if ( specifier->FindInt32("index", i) == B_OK ) {
      MyProxy* proxy = (MyProxy*)proxyList->ItemAt(i);
      if ( proxy ) {
            message->PopSpecifier();
            if ( proxy->Looper() != Looper() ) {
               proxy->Looper()->PostMessage(message, proxy);
               return NULL;
            }
      }
      . . .
   }
   . . .
}
:::

Since this function resolved the specifier at {hparam}`index`, it calls
{cpp:func}`PopSpecifier() <BMessage::PopSpecifier>` to decrement the index
before forwarding the message. Otherwise, the next handler would try to
resolve the same specifier.

#### Method 2:

If the {hparam}`specifier` picks out another {hclass}`BHandler` object
belonging to the same {cpp:class}`BLooper`, {hmethod}`ResolveSpecifier()`
can return that {hclass}`BHandler`. For example:

:::{code} cpp
if ( proxy ) {
   message->PopSpecifier();
   if ( proxy->Looper() != Looper() ) {
      proxy->Looper()->PostMessage(message, proxy);
      return NULL;
   }
   else {
      return proxy;
   }
}
:::

This, in effect, puts the returned object in the {hclass}`BHandler`'s
place as the designated handler for the message. The {cpp:class}`BLooper`
will give the returned handler a chance to respond to the message or
resolve the next specifier.

Again, {cpp:func}`PopSpecifier() <BMessage::PopSpecifier>` should be
called so that an attempt isn't made to resolve the same specifier twice.

#### Method 3:

If it can resolve all remaining specifiers and recognizes the message as
one that the {hclass}`BHandler` itself can handle, it should return the
{hclass}`BHandler` ({hparam}`this`). For example:

:::{code} cpp
if ( (strcmp(property, "Value") == 0) &&
     (message->what == B_GET_PROPERTY) )
   return this;
:::

This confirms the {hclass}`BHandler` as the message target.
{hmethod}`ResolveSpecifier()` won't be called again, so it's not necessary
to call {cpp:func}`PopSpecifier() <BMessage::PopSpecifier>` before
returning.

#### Method 4:

If it doesn't recognize the property or can't resolve the specifier, it
should call (and return the value returned by) the inherited version of
{hmethod}`ResolveSpecifier()`.

#### Examples

The {cpp:class}`BApplication` object takes the first path when it resolves
a specifier for a "Window" property; it sends the message to the specified
{cpp:class}`BWindow` and returns {cpp:expr}`NULL`. A {cpp:class}`BWindow`
follows the second path when it resolves a specifier for a "View" property;
it returns the specified {cpp:class}`BView`. Thus, a message initially
targeted to the {cpp:class}`BApplication` object can find its way to a
{cpp:class}`BView`.

{hclass}`BHandler`'s version of {hmethod}`ResolveSpecifier()` recognizes a
{cpp:enumerator}`B_GET_PROPERTY` {hparam}`message` with a direct
{hparam}`specifier` requesting a "Suite" for the supported suites,
"Messenger" for the {hclass}`BHandler`, or the {hclass}`BHandler`'s
"InternalName" (the same name that its {hmethod}`Name()` function returns).
In all three cases, it assigns the {hclass}`BHandler`({hparam}`this`) as
the object responsible for the message.

For all other specifiers and messages, it sends a
{cpp:enumerator}`B_MESSAGE_NOT_UNDERSTOOD` reply and returns
{cpp:expr}`NULL`. The reply message has an {hparam}`error` field with
{cpp:enumerator}`B_SCRIPT_SYNTAX` as the error and a {hparam}`message`
field with a longer textual explanation of the error.
::::

::::{abi-group}
:::{cpp:function} virtual void BHandler::SetFilterList(BList* list)
:::

:::{cpp:function} BList* BHandler::FilterList() const
:::

:::{cpp:function} virtual void BHandler::AddFilter(BMessageFilter* filter)
:::

:::{cpp:function} virtual bool BHandler::RemoveFilter(BMessageFilter* filter)
:::

These functions manage a list of {cpp:class}`BMessageFilter` objects
associated with the {hclass}`BHandler`.

{hmethod}`SetFilterList()` assigns the {hclass}`BHandler` a new
{hparam}`list` of filters; the list must contain pointers to instances of
the {cpp:class}`BMessageFilter` class or to instances of classes that
derive from {cpp:class}`BMessageFilter`. The new list replaces any list of
filters previously assigned. All objects in the previous list are deleted,
as is the {cpp:class}`BList` that contains them. If list is
{cpp:expr}`NULL`, the current list is removed without a replacement.
{hmethod}`FilterList()` returns the current list of filters.

{hmethod}`AddFilter()` adds a {hparam}`filter` to the end of the
{hclass}`BHandler`'s list of filters. It creates the {cpp:class}`BList`
object if it doesn't already exist. By default, BHandlers don't maintain a
{cpp:class}`BList` of filters until one is assigned or the first
{cpp:class}`BMessageFilter` is added. {hmethod}`RemoveFilter()` removes a
{hparam}`filter` from the list without deleting it. It returns
{cpp:expr}`true` if successful, and {cpp:expr}`false` if it can't find the
specified filter in the list (or the list doesn't exist). It leaves the
{cpp:class}`BList` in place even after removing the last filter.

For {hmethod}`SetFilterList()`, {hmethod}`AddFilter()` and
{hmethod}`RemoveFilter()` to work, the {hclass}`BHandler` must be assigned
to a {cpp:class}`BLooper` object and the {cpp:class}`BLooper` must be
locked.

See also: {cpp:func}`BLooper::SetCommonFilterList`,
{cpp:func}`BLooper::Lock`, the {cpp:class}`BMessageFilter` class
::::

::::{abi-group}
:::{cpp:function} void BHandler::SetName(const char* string)
:::

:::{cpp:function} const char* BHandler::Name() const
:::

These functions set and return the name that identifies the
{hclass}`BHandler`. The name is originally set by the constructor.
{hmethod}`SetName()` assigns the {hclass}`BHandler` a new name, and
{hmethod}`Name()` returns the current name. The string returned by
{hmethod}`Name()` belongs to the {hclass}`BHandler` object; it shouldn't be
altered or freed.

See also: The {hclass}`BHandler` {cpp:func}`constructor
<BHandler::BHandler()>`, {cpp:func}`BView::FindView` in th {ref}`Interface
Kit`
::::

::::{abi-group}
:::{cpp:function} void BHandler::SetNextHandler(BHandler* handler)
:::

:::{cpp:function} BHandler* BHandler::NextHandler() const
:::

{hmethod}`SetNextHandler()` reorders the objects in the handler chain so
that {hparam}`handler` follows this {hclass}`BHandler`. This
{hclass}`BHandler` and {hparam}`handler` must already be part of the same
chain, and the {cpp:class}`BLooper` they belong to must be locked. The
order of objects in the handler chain affects the way in-coming messages
are handled (as explained in "{ref}`Inheritance and the Handler Chain`". By
default handlers are placed in the order that they're added (through
{cpp:func}`BLooper::AddHandler`).

{hmethod}`NextHandler()` returns this object's next handler. If this
object is at the end of the chain, it returns {cpp:expr}`NULL`.
::::

::::{abi-group}
:::{cpp:function} virtual void BHandler::SendNotices(uint32 what, const BMessage* msg = 0)
:::

Sends a {cpp:enumerator}`B_OBSERVER_NOTICE_CHANGE` message to each
{hclass}`BHandler` object (or "observer") that's observing this handler
(the "notifier"). To observe a notifier, the observer calls
{cpp:func}`StartWatching() <BHandler::StartWatching>`. The {hparam}`what`
argument describes the type of change that's prompting this notification;
only those observers that have registered to be notified about what (or
that are watching all changes) are sent notifications.

The {cpp:enumerator}`B_OBSERVER_NOTICE_CHANGE` messages that are sent are
copied from {hparam}`msg` with the what argument added as the
{hparam}`be:old_what` field. Note that {hparam}`msg`'s original
{hparam}`what` field is clobbered.
::::

::::{abi-group}
:::{cpp:function} status_t BHandler::StartWatching(BMessenger watcher, uint32 what)
:::

:::{cpp:function} status_t BHandler::StartWatching(BHandler* watcher, uint32 what)
:::

:::{cpp:function} status_t BHandler::StartWatchingAll(BMessenger watcher)
:::

:::{cpp:function} status_t BHandler::StartWatchingAll(BHandler* watcher)
:::

:::{cpp:function} status_t BHandler::StopWatching(BMessenger watcher, uint32 what)
:::

:::{cpp:function} status_t BHandler::StopWatching(BHandler* watcher, uint32 what)
:::

:::{cpp:function} status_t BHandler::StopWatchingAll(BMessenger watcher)
:::

:::{cpp:function} status_t BHandler::StopWatchingAll(BHandler* watcher)
:::

The {hclass}`BHandler` class provides the concept of a notifier. Notifiers
maintain one or more states that other entities might want to monitor
changes to. These states are identified by a 32-bit {hparam}`what` code.
Another entity a {hclass}`BHandler` or a {cpp:class}`BMessenger` can watch
for changes notifiers' states. These are called observers.

{hmethod}`StartWatching()` registers the {cpp:class}`BMessenger` or
{hclass}`BHandler` specified by {hparam}`watcher` to be notified whenever
the state specified by {hparam}`what` changes.
{hmethod}`StartWatchingAll()` registers the specified
{cpp:class}`BMessenger` or {hclass}`BHandler` to be notified when any of
the notifer's states change.

{hmethod}`StartWatching()` works by sending a message to the
{hclass}`BHandler` you want to observe, with a {cpp:class}`BMessenger` back
to the observer, so both must be attached to a looper at the time
{hmethod}`StartWatching()` is called.

:::{admonition} Note
:class: note
The forms of {hmethod}`StartWatching()` and {hmethod}`StartWatchingAll()`
that accept a {hclass}`BHandler` can be used to observe a handler that's
not yet attached to a looper. However, these only work if the observer and
notifier are both in the same looper.
:::

{hmethod}`StopWatching()` ceases monitoring of the state {hparam}`what`.
{hmethod}`StopWatchingAll()`, by some odd coincidence, stops all monitoring
by the {hclass}`BHandler` or {cpp:class}`BMessenger` specified by
{hparam}`watcher`.

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
	- {cpp:enumerator}`B_BAD_HANDLER`.
	- The specified {hclass}`BHandler` isn't valid.

:::
::::

## Static Functions

### Instantiate()

See {cpp:func}`BArchivable::Instantiate`

## Archived Fields

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Field

	- Type code

	- Description

-
	- {hparam}`_name`

	- {cpp:enumerator}`B_STRING_TYPE`

	- The object's name (see {cpp:func}`SetName() <BHandler::SetName>`).


:::

{hclass}`BHandler` records its own name.

## Scripting Suites and Properties

### Suite: "suite/vnd.Be-handler"

#### "InternalName"

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Message

	- Specifiers

	- Reply Type

-
	- {cpp:enumerator}`B_GET_PROPERTY`

	- {cpp:enumerator}`B_DIRECT_SPECIFIER`

	- {cpp:enumerator}`B_STRING_TYPE`


:::

Returns the handler's name.

#### "Messenger"

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Message

	- Specifiers

	- Reply Type

-
	- {cpp:enumerator}`B_GET_PROPERTY`

	- {cpp:enumerator}`B_DIRECT_SPECIFIER`

	- {cpp:enumerator}`B_MESSENGER_TYPE`


:::

Returns a {cpp:class}`BMessenger` for the handler.

#### "Suites"

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Message

	- Specifiers

	- Reply Type

-
	- {cpp:enumerator}`B_GET_PROPERTY`

	- {cpp:enumerator}`B_DIRECT_SPECIFIER`

	- B_STRING_TYPE array


:::

Returns an array of suites that the target supports, identified by name
(e.g. "suite/vnd.Be-handler").
