# BHandler

A {cpp:class}`BHandler` object responds to messages that are handed to it
by a {cpp:class}`BLooper`. The {cpp:class}`BLooper` tells the
{cpp:class}`BHandler` about a message by invoking the
{cpp:class}`BHandler`'s {cpp:func}`MessageReceived()
<BHandler::MessageReceived>` function.

## The Handler List

To be eligible to get messages from a {cpp:class}`BLooper`, a
{cpp:class}`BHandler` must be in the {cpp:class}`BLooper`'s list of
eligible handlers (as explained in the {cpp:class}`BLooper` class). The
list of eligible handlers is ordered; if the "first" handler doesn't want
to respond to a message that it has received, it simply calls the inherited
version of {cpp:func}`MessageReceived() <BHandler::MessageReceived>` and
the message will automatically be handed to the object's "next" handler.
(System messages are not handed down the list.) The {cpp:class}`BLooper`
that all these {cpp:class}`BHandler`s belong to is always the last the last
handler in the list ({cpp:class}`BLooper` inherits from
{cpp:class}`BHandler`).

A {cpp:class}`BHandler`'s next handler assignment can be changed through
{cpp:func}`SetNextHandler() <BHandler::SetNextHandler>`.

## Targets

You can designate a target {cpp:class}`BHandler` for most messages. The
designation is made when calling {cpp:class}`BLooper`'s
{cpp:func}`PostMessage() <BLooper::PostMessage>` function or when
constructing the {cpp:class}`BMessenger` object that will send the message.
Messages that a user drags and drops are targeted to the object (a
{cpp:class}`BView`) that controls the part of the window where the message
was dropped. The messaging mechanism eventually passes the target
{cpp:class}`BHandler` to {cpp:func}`DispatchMessage()
<BLooper::DispatchMessage>` , so that the message can be delivered to its
designated destination.

## Filtering

Messages can be filtered before they're dispatched; that is, you can
define a function that will look at the message before the target
{cpp:class}`BHandler`'s hook function is called. The filter function is
associated with a {cpp:class}`BMessageFilter` object, which records the
criteria for calling the function.

Filters that should apply only to messages targeted to a particular
{cpp:class}`BHandler` are assigned to the {cpp:class}`BHandler` by
{cpp:func}`SetFilterList() <BHandler::SetFilterList>` or
{cpp:func}`AddFilter() <BHandler::AddFilter>`. Filters that might apply to
any message a {cpp:class}`BLooper` dispatches, regardless of its target,
are assigned by the parallel {cpp:class}`BLooper` functions,
{cpp:func}`SetCommonFilterList() <BLooper::SetCommonFilterList>` and
{cpp:func}`AddCommonFilter() <BLooper::AddCommonFilter>`. See those
functions and the {cpp:class}`BMessageFilter` class for details.

## Notifiers and Observers

A {cpp:class}`BHandler` can be a notifier. A notifier is a handler that
maintains one or more states and notifies interested parties when those
states change. Each state is idenfified by a 32-bit {hparam}`what` code.
Interested parties, called observers, can register to monitor changes in
one or more states by calling {cpp:func}`StartWatching()
<BHandler::StartWatching>` and specifying the {hparam}`what` code of the
state they want to be notified of changes to.

This notification occurs when the {cpp:class}`BHandler` calls
{cpp:func}`SendNotices() <BHandler::SendNotices>`; it's the handler's job
to call {cpp:func}`SendNotices() <BHandler::SendNotices>` whenever a state
changes, to ensure that observers are kept informed of the changes. The
{cpp:class}`BHandler` passes to {cpp:func}`SendNotices()
<BHandler::SendNotices>` a message template to be sent to the observers.

When a notification is sent, observers receive a
{cpp:enumerator}`B_OBSERVER_NOTICE_CHANGE` message with an {htype}`int32`
field {cpp:enumerator}`B_OBSERVER_NOTICE_CHANGE` that contains the
{hparam}`what` code of the state that changed, and a
{cpp:enumerator}`B_OBSERVE_ORIGINAL_WHAT` field that contains the
{hparam}`what` value that was in the template {cpp:class}`BMessage`.
