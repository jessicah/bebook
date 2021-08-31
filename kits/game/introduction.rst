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
