# BWindow

A {cpp:class}`BWindow` object represents a window that can be displayed on
the screen, and that can be the target of user events. You almost always
create your own {cpp:class}`BWindow` subclass(es) rather than use direct
instances of {cpp:class}`BWindow`.

{cpp:class}`BWindow` objects draw windows by talking to the App Server. If
you want to take over the entire screen or draw directly into the graphics
card's frame buffer (by-passing the App Server), you should use a
{cpp:class}`BDirectWindow` or {cpp:class}`BWindowScreen` object (both
classes are defined in the Game Kit).

## Creating and Using a BWindow

You must create your {cpp:class}`BApplication` object ({hparam}`be_app`)
before you create any windows. be_app needn't be running to construct—or
even show—a window, but it must be running for the window to receive
notifications of user events (mouse clicks, key presses, etc.).

Typically, the first thing you do with your {cpp:class}`BWindow` is add
{cpp:class}`BView`s to it, through the {cpp:func}`AddChild()
<BWindow::AddChild>` function. Again, {hparam}`be_app` needn't be running
at this point, nor must the window be showing.

Even though it inherits from {cpp:class}`BLooper`, you never invoke
{cpp:func}`AddChild() <BWindow::AddChild>`Run() on a {cpp:class}`BWindow`.
Instead, you call {cpp:func}`Show() <BWindow::Show>`. In addition to
putting the window on-screen, the first (and only the first)
{cpp:func}`Show() <BWindow::Show>` invocation starts the
{cpp:class}`BWindow`'s message loop. To remove a window from the screen
without interrupting the object's message loop, use {cpp:func}`Hide()
<BWindow::Hide>`. Other message loop details (locking and quitting in
particular) are handled as described in the {cpp:class}`BLooper` class.

:::{admonition} Warning
:class: warning
If you create a {cpp:class}`BWindow`-derived class that uses multiple
inheritance, make sure the first class your mixin class inherits from is
{cpp:class}`BWindow`; otherwise, you'll crash when you try to close the
window. This happens because of an interaction between the window thread
how C++ deletes objects of a multiply-inherited class. In other words:

is safe, while

is not.
:::
