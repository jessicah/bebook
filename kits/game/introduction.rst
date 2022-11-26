.. title:: The Game Kit

Introduction
============

The Game Kit provides features that game developers will find particularly
useful.

There are two types of functionality provided by the Game Kit:

* Low-level graphics access
* High-performance and convenient sound playback
  
There's also one global function, :cpp:func:`set_mouse_position()`, which lets
you move the mouse cursor programmatically.

Although designed with games in mind, nothing in the Game Kit is restricted to
game applications, except that the user will have to deposit another 50 cents
every three minutes.

Low-Level Graphics Access
=========================

There are two classes provided for direct access to the underlying graphics
hardware: :cpp:class:`BWindowScreen` and :cpp:class:`BDirectWindow`. These two
classes both give you direct access to the graphics card's frame buffer; the
difference between them is that :cpp:class:`BWindowScreen` always takes over the
entire screen, bypassing the Application Server, while
:cpp:class:`BDirectWindow` can draw directly into a window on most graphics
hardware.

Although :cpp:class:`BDirectWindow` can do everything :cpp:class:`BWindowScreen`
can do, :cpp:class:`BWindowScreen` can be a little easier to use.

High-Performance Audio
======================

Several classes are provided for high-performance audio playback:

:cpp:class:`BGameSound`
	Is a base class and isn't used directly; it's the foundation for all the
	other audio classes in the Game Kit

:cpp:class:`BFileGameSound`
	Is used to represent a sound effect stored in a disk file, and provides
	functions for playing the sound. It can be used for playing music loops from
	audio files, or for playing the occasional large sound effect.

:cpp:class:`BSimpleGameSdoun`
	On the other hand, preloads the sound into memory, so that it can be played
	back with extremely low latency and low overhead (at the expensive of memory
	space).

:cpp:class:`BPushGameSound`
	These are used to let you fill buffers flowing to the speakers (or
	headphones, or whatever audio output device is being used). Their mission is
	the same, but their methods are different; :cpp:class:`BPushGameSound` also
	provides a way to play sound in a cyclic loop, keeping ahead of the playback
	point in the buffer. This is the extreme in high-performance, low-latency
	audio, but does require some extra work on the programmer's part.

:cpp:class:`BStreamingGameSound`
	Requires magic powers to use; it's functionality is closely tied to the
	implementation of the Kit, especially when hardware sound acceleration is
	involved. So don't touch it, we beg you.
