# BLooper

A {cpp:class}`BLooper` object creates a "message loop" that receives
messages that are sent or posted to the {cpp:class}`BLooper`. The message
loop runs in a separate thread that's spawned (and told to run) when the
{cpp:class}`BLooper` receives a {cpp:func}`Run() <BLooper::Run>` call. If
you're creating your own {cpp:class}`BLooper`, you can invoke
{cpp:func}`Run() <BLooper::Run>` from within the {cpp:func}`constructor
<BLooper::BLooper()>`.

You tell the loop to stop by sending the {cpp:class}`BLooper` a
{cpp:enumerator}`B_QUIT_REQUESTED` message, which invokes the object's
{cpp:func}`Quit() <BLooper::Quit>` function. You can also call
{cpp:func}`Quit() <BLooper::Quit>` directly, but you have to
{cpp:func}`Lock() <BLooper::Lock>` the object first ({cpp:class}`BLooper`
locking is explained later). {cpp:func}`Quit() <BLooper::Quit>` deletes the
{cpp:class}`BLooper` for you.

:::{admonition} Note
:class: note
The {cpp:class}`BApplication` class, the most important
{cpp:class}`BLooper` subclass, bends the above description in one of two
ways:

A {cpp:class}`BApplication` takes over the main thread, it doesn't spawn a
new one.

You do have to delete {hparam}`be_app`; you can't just {cpp:func}`Quit()
<BLooper::Quit>` it.
:::

## Messages and Handlers

You can deliver messages to a {cpp:class}`BLooper`'s thread by…

-   Posting them directly by calling {cpp:class}`BLooper`'s
{cpp:func}`PostMessage() <BLooper::PostMessage>` function.

-   Sending them through {cpp:class}`BMessenger`'s {cpp:func}`SendMessage()
<BMessenger::SendMessage>` or {cpp:class}`BMessage`'s
{cpp:func}`SendReply() <BMessage::SendReply>` function.

As messages arrive, they're added to the {cpp:class}`BLooper`'s
{cpp:class}`BMessageQueue` object. The {cpp:class}`BLooper` takes messages
from the queue in the order that they arrived, and calls
{cpp:func}`DispatchMessage() <BLooper::DispatchMessage>` for each one.
{cpp:func}`DispatchMessage() <BLooper::DispatchMessage>` locks the
{cpp:class}`BLooper` and then hands the message to a {cpp:class}`BHandler`
object by invoking the handler's {cpp:func}`MessageReceived()
<BHandler::MessageReceived>` function. But which {cpp:class}`BHandler` does
the {cpp:class}`BLooper` hand the message to? Here's the path:

-   If an incoming message targets a specific {cpp:class}`BHandler`, and if
that {cpp:class}`BHandler` is one of the {cpp:class}`BLooper`'s eligible
handlers (as set through the {cpp:func}`AddHandler() <BLooper::AddHandler>`
function), the {cpp:class}`BLooper` uses that {cpp:class}`BHandler`. (See
the {cpp:class}`BMessage` and {cpp:class}`BMessenger` classes for
instructions on how to target a {cpp:class}`BHandler`.)

-   Otherwise it hands the message to its _preferred handler_, as set through
{cpp:func}`SetPreferredHandler() <BLooper::SetPreferredHandler>`.

-   If no preferred handler is set, the {cpp:class}`BLooper` itself handles
the message (its own implementation of {cpp:func}`MessageReceived()
<BLooper::MessageReceived>` is invoked).

After the handler is finished (when its {cpp:func}`MessageReceived()
<BLooper::MessageReceived>` returns), the {cpp:class}`BMessage` is
automatically deleted and the {cpp:class}`BLooper` is unlocked.

## Locking

Access to many {cpp:class}`BLooper` functions (and some
{cpp:class}`BHandler` functions) is proteced by a lock. To invoke a
lock-protected functions (or groups of functions), you must first call
{cpp:func}`Lock() <BLooper::Lock>`, and then call {cpp:func}`Unlock()
<BLooper::Lock>` when you're done. The lock is scoped to the calling
thread: {cpp:func}`Lock() <BLooper::Lock>`/{cpp:func}`Unlock()
<BLooper::Lock>` calls can be nested within the thread. Keep in mind that
each {cpp:func}`Lock() <BLooper::Lock>` must balanced by an
{cpp:func}`Unlock() <BLooper::Lock>`.

The {cpp:class}`BLooper` {cpp:func}`constructor <BLooper::BLooper()>`
automatically locks the object. It's unlocked when {cpp:func}`Run()
<BLooper::Run>` is invoked. This means that the {cpp:func}`Run()
<BLooper::Run>` function and any other lock-protected functions that you
call before you call {cpp:func}`Run() <BLooper::Run>` must be called from
the thread that constructed the {cpp:class}`BLooper`.

## Allocation

Because they delete themselves when told to quit, {cpp:class}`BLooper`s
can't be allocated on the stack; you have to construct them with
{hmethod}`new`.
