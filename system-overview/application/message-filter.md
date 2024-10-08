# BMessageFilter

A {cpp:class}`BMessageFilter` is a message-screening function that you
"attach" to a {cpp:class}`BLooper` or {cpp:class}`BHandler`. The message
filter sees messages just before they're dispatched (i.e. just before
{cpp:func}`BLooper::DispatchMessage()`), and can modify or reject the
message, change the message's designated handler, or whatever else it wants
to do—the implementation of the filter function isn't restricted.

To define a message filter, you have to provide a message-filtering
function. You do this by implementing the
{cpp:func}`~BMessageFilter::Filter()` hook function in a
{cpp:class}`BMessageFilter` subclass, or by supplying a
{cpp:func}`filter_hook()` function to the {cpp:class}`BMessageFilter`
constructor. Only one filter function per object is called. If you
implement {cpp:func}`~BMessageFilter::Filter()` and provide a filter_hook
function, the filter_hook will win.

To attach a message filter to a looper, call
{cpp:func}`BLooper::AddCommonFilter()`. To add it to a handler, call
{cpp:func}`BHandler::AddFilter()`. Looper filters see all incoming
messages; handler filters see only those messages that are targetted for
that particular handler.

A {cpp:class}`BLooper` or {cpp:class}`BHandler` can have more than one
message filter. Furthermore, a looper can have two sets of filters: a
looper set and a handler set (keep in mind that {cpp:class}`BLooper` is
derived from {cpp:class}`BHandler`). Looper filters are applied before
handler filters.

A {cpp:class}`BMessageFilter` object can be assigned to only one
{cpp:class}`BHandler` or {cpp:class}`BLooper` at a time.

:::{admonition} Warning
:class: warning
The {cpp:class}`BMessageFilter` class is intended to be used as part of the
system-defined messaging system. If you try to use one outside this system,
your results may not be what you expect.
:::
