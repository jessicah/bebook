BHandler
========

A BHandler object responds to messages that are handed to it by a
BLooper. The BLooper tells the BHandler about a message by invoking the
BHandler's MessageReceived() function.

The Handler List
================

To be eligible to get messages from a BLooper, a BHandler must
be in the BLooper's list of eligible handlers (as explained in the BLooper
class). The list of eligible handlers is ordered; if the "first" handler doesn't
want to respond to a message that it has received, it simply calls the inherited
version of MessageReceived() and the message will automatically be handed to the
object's "next" handler. (System messages are not handed down the list.) The
BLooper that all these BHandlers belong to is always the last the last handler
in the list (BLooper inherits from BHandler).

A BHandler's next handler assignment can be changed through SetNextHandler().

Targets
=======

 You can designate a target BHandler for most messages. The designation
is made when calling BLooper's PostMessage() function or when constructing the
BMessenger object that will send the message. Messages that a user drags and
drops are targeted to the object (a BView) that controls the part of the window
where the message was dropped. The messaging mechanism eventually passes the
target BHandler to DispatchMessage() , so that the message can be delivered to
its designated destination.

Filtering
=========

Messages can be filtered before they're dispatched; that is, you can
define a function that will look at the message before the target BHandler's
hook function is called. The filter function is associated with a BMessageFilter
object, which records the criteria for calling the function.

Filters that should apply only to messages targeted to a particular BHandler are
assigned to the BHandler by SetFilterList() or AddFilter(). Filters that might
apply to any message a BLooper dispatches, regardless of its target, are
assigned by the parallel BLooper functions, SetCommonFilterList() and
AddCommonFilter(). See those functions and the BMessageFilter class for details.

Notifiers and Observers
=======================

A BHandler can be a notifier. A notifier is a handler
that maintains one or more states and notifies interested parties when those
states change. Each state is idenfified by a 32-bit what code. Interested
parties, called observers, can register to monitor changes in one or more states
by calling StartWatching() and specifying the what code of the state they want
to be notified of changes to.

This notification occurs when the BHandler calls SendNotices(); it's the
handler's job to call SendNotices() whenever a state changes, to ensure that
observers are kept informed of the changes. The BHandler passes to SendNotices()
a message template to be sent to the observers.

When a notification is sent, observers receive a B_OBSERVER_NOTICE_CHANGE
message with an int32 field B_OBSERVER_NOTICE_CHANGE that contains the what code
of the state that changed, and a B_OBSERVE_ORIGINAL_WHAT field that contains the
what value that was in the template BMessage.