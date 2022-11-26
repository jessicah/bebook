BMessageQueue
=============

The BMessageQueue class completes the implementation of BLooper by providing a
first-in/first-out stack in which the looper can place in-coming BMessages. In
general, the message dispatching mechanism of BLooper should suffice. However,
if you ever need to manipulate a BMessage queue directly, you can do so.