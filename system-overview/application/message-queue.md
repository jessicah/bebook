# BMessageQueue

The {cpp:class}`BMessageQueue` class completes the implementation of
{cpp:class}`BLooper` by providing a first-in/first-out stack in which the
looper can place in-coming {cpp:class}`BMessage`s. In general, the message
dispatching mechanism of {cpp:class}`BLooper` should suffice. However, if
you ever need to manipulate a {cpp:class}`BMessage` queue directly, you can
do so.
