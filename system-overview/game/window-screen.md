# BWindowScreen

A {cpp:class}`BWindowScreen` object provides exclusive access to the
entire screen, bypassing the Application Server's window system. The object
has direct access to the graphics card driver: It can set up the graphics
environment on the graphics card, call driver-implemented drawing
functions, and directly manipulate the frame buffer.

## Screen Access

Like all windows, a {cpp:class}`BWindowScreen` is hidden (off-screen) when
it's constructed. By calling {cpp:func}`Show() <BWindowScreen::Show>` to
put it on-screen and make it the active window, an application takes over
the whole screen. While the {cpp:class}`BWindowScreen` is active, the
Application Server's graphics operations are suspended—this means that you
can't use any {cpp:class}`BView` functions, nor any functions in classes
derived from {cpp:class}`BView`; you have to draw directly into the
screen's frame buffer, and nothing except what the application draws will
be visible to the user—no other windows and no desktop. When the
{cpp:class}`BWindowScreen` gives up active status, the Application Server
automatically refreshes the screen with its old contents.

Although the {cpp:class}`BWindowScreen` object provides a connection to
the screen, you shouldn't draw from the {cpp:class}`BWindowScreen`'s
thread. Use the thread only to regulate the access of other threads to the
frame buffer.

## Keyboard and Mouse

A {cpp:class}`BWindowScreen` object remains a window while it has control
of the screen; it stays attached to the Application Server and its message
loop continues to function. It gets messages reporting the user's actions
on the keyboard and mouse, just like any other active window. Because it
covers the whole screen, it's notified of all mouse and keyboard events.
You can attach filters to the window to get the messages as they arrive. Or
you can call the Interface Kit's {ref}`get_key_info()` function to poll the
state of the keyboard and construct a nominal {cpp:class}`BView` so that
you can call {cpp:func}`GetMouse() <BView::GetMouse>` to poll the mouse.

## Workspaces

This class respects workspaces. A {cpp:class}`BWindowScreen` object
releases its grip on the screen when the user turns to another workspace
and reestablishes its control when the user returns to the workspace in
which it's the active window.

## Debugging

A {cpp:class}`BWindowScreen` object can be constructed in a debugging mode
that lets you switch back and forth between the workspace in which the game
is running and a workspace where error messages are printed. See the
{cpp:func}`constructor <BWindowScreen::BWindowScreen()>` and the
{cpp:func}`RegisterThread() <BWindowScreen::RegisterThread>` function for
details.
