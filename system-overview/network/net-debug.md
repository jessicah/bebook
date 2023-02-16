# BNetDebug

{cpp:class}`BNetDebug` provides a few functions that let you turn on and
off debug output, and dump raw data to stderr in a clean format.

All the member functions are static; instead of creating a
{cpp:class}`BNetDebug` object, call them like this:

:::{code} cpp
BNetDebug::Print("Starting server...");
:::

Debug output is off by default; call {cpp:func}`BNetDebug::Enable` to
enable it.
