BLooper
=======

A BLooper object creates a "message loop" that receives messages that are sent
or posted to the BLooper. The message loop runs in a separate thread that's
spawned (and told to run) when the BLooper receives a Run() call. If you're
creating your own BLooper, you can invoke Run() from within the constructor.

You tell the loop to stop by sending the BLooper a B_QUIT_REQUESTED message,
which invokes the object's Quit() function. You can also call Quit() directly,
but you have to Lock() the object first (BLooper locking is explained later).
Quit() deletes the BLooper for you.

.. note:: The BApplication class, the most important BLooper subclass, bends the
          above description in one of two ways:

          #. A BApplication takes over the main thread, it doesn't spawn a new one.
          #. You do have to delete be_app; you can't just Quit() it.

Messages and Handlers
=====================

You can deliver messages to a BLooper's thread by…

* Posting them directly by calling BLooper's PostMessage() function.
* Sending them through BMessenger's SendMessage() or BMessage's SendReply()
  function.

As messages arrive, they're added to the BLooper's BMessageQueue object. The
BLooper takes messages from the queue in the order that they arrived, and calls
DispatchMessage() for each one. DispatchMessage() locks the BLooper and then
hands the message to a BHandler object by invoking the handler's
MessageReceived() function. But which BHandler does the BLooper hand the message
to? Here's the path:

* If an incoming message targets a specific BHandler, and if that BHandler is one
  of the BLooper's eligible handlers (as set through the AddHandler() function),
  the BLooper uses that BHandler. (See the BMessage and BMessenger classes for
  instructions on how to target a BHandler.)
* Otherwise it hands the message to its preferred handler, as set through
  SetPreferredHandler().
* If no preferred handler is set, the BLooper itself handles the message (its own
  implementation of MessageReceived() is invoked).

After the handler is finished (when its MessageReceived() returns), the BMessage
is automatically deleted and the BLooper is unlocked.

Locking
=======

 Access to many BLooper functions (and some BHandler functions) is
proteced by a lock. To invoke a lock-protected functions (or groups of
functions), you must first call Lock(), and then call Unlock() when you're done.
The lock is scoped to the calling thread: Lock()/Unlock() calls can be nested
within the thread. Keep in mind that each Lock() must balanced by an Unlock().

The BLooper constructor automatically locks the object. It's unlocked when Run()
is invoked. This means that the Run() function and any other lock-protected
functions that you call before you call Run() must be called from the thread
that constructed the BLooper.

Allocation
==========

Because they delete themselves when told to quit, BLoopers can't be
allocated on the stack; you have to construct them with new.