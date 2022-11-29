BMessenger
==========

A BMessenger represents and sends messages to a message target, where the target
is a BLooper and, optionally, a specific BHandler within that looper. The target
can live in the same application as the BMessenger (a local target), or it can
live in some other application (a remote target).

BMessenger's most significant function is SendMessage(), which sends its
argument BMessage to the target.

.. note:: For a local target, SendMessage() is roughly equivalent, in terms of
          efficiency, to posting a message directly to the BMessenger's target
          (i.e BLooper::PostMessage()).

The global be_app_messenger BMessenger pointer, which targets be_app's main
message loop, is automatically initialized for you when you create your
BApplication object. You can use it wherever BMessengers are called for.