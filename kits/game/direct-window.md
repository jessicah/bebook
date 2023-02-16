:::{cpp:class} BDirectWindow
:::

# BDirectWindow

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BDirectWindow::BDirectWindow(BRect frame, const char* title, window_type type, uint32 flags, uint32 workspace = B_CURRENT_WORKSPACE)
:::

:::{cpp:function} BDirectWindow::BDirectWindow(BRect frame, const char* title, window_look look, window_feel feel, uint32 flags, uint32 workspace = B_CURRENT_WORKSPACE)
:::

Creates and returns a new {hclass}`BDirectWindow` object. This is
functionally equivalent to the {cpp:class}`BWindow` {cpp:func}`constructor
<BWindow::BWindow()>`, except the resulting {hclass}`BDirectWindow`
supports direct window operations.

You will probably want to set up a flag to keep track of whether or not
the direct window's connection to the screen is viable. In the constructor,
you should set this flag (let's call it {hparam}`fConnectionDisabled` ) to
{cpp:expr}`false`, which indicates to both {cpp:func}`DirectConnected()
<BDirectWindow::DirectConnected>` and your drawing thread that the window
is not in the process of being deconstructed. The destructor would then set
this flag to {cpp:expr}`true` before terminating the connection to avoid
the unlikely possibility of the connection trying to restart while the
{hclass}`BDirectWindow` is being dismantled.

You'll also need other flags or semaphores (or benaphores) to manage the
interaction between the {hclass}`BDirectWindow` and your drawing thread.

See the sample code in "{ref}`Using a Direct Window`" for an example.
::::

::::{abi-group}
:::{cpp:function} BDirectWindow::~BDirectWindow()
:::

Frees all memory the {hclass}`BDirectWindow` object allocated for itself.
You should never delete a {hclass}`BDirectWindow` object; call its
{cpp:func}`Quit() <BWindow::Quit>` function instead (inherited from
{cpp:class}`BWindow`).

Your {hclass}`BDirectWindow` destructor should begin by setting the
{hparam}`fConnectionDisabled` flag to {cpp:expr}`true`, to prevent
{cpp:func}`DirectConnected() <BDirectWindow::DirectConnected>` from
attempting to reconnect to the direct window while it's being
deconstructed.

Then you should call {cpp:func}`Hide() <BWindow::Hide>` and
{cpp:func}`Sync() <BWindow::Sync>` to force the direct window to disconnect
direct access (both inherited from {cpp:class}`BWindow`):

:::{code} cpp
MyDirectWindow::~BDirectWindow
{
   fConnectionDisabled = true;
   Hide();
   Sync();
   /* complete usual destruction here */
}
:::
::::

## Hook Functions

::::{abi-group}
:::{cpp:function} virtual void BDirectWindow::DirectConnected(direct_buffer_info* info)
:::

This hook function is the core of {hclass}`BDirectWindow`. Your
application should override this function to learn about the state of the
graphics display onto which you're drawing, as well as to be informed of
any changes that occur.

This function is also called to suspend and resume your direct access
privileges.

Your code in this function should be as short as possible, because what
your {hmethod}`DirectConnected()` function does can affect the performance
of the entire system. {hmethod}`DirectConnected()` should only handle the
immediate task of dealing with changes in the direct drawing context, and
shouldn't normally do any actual drawing—that's what your drawing thread is
for.

If you have drawing that absolutely has to be done before you can safely
return control to the application server (see the note below), you may do
so, but your code should do the absolute minimum drawing necessary and
leave everything else to the drawing thread.

:::{admonition} Note
:class: note
{hmethod}`DirectConnected()` should only return when it can guarantee to
the application server that the request specified by {hparam}`info` will be
strictly obeyed.
:::

The structure pointed to by {hparam}`info` goes away after
{hmethod}`DirectConnected()` returns, so you should cache the information
that interests you.

:::{admonition} Warning
:class: warning
If your {hmethod}`DirectConnected()` implementation doesn't handle a
request within three seconds, the Application Server will intentionally
crash your application under the assumption that it's deadlocked. Be sure
to handle requests as quickly as possible.
:::

See  "{ref}`Getting Connected (and Staying That Way)`" for more
information about the {htype}`direct_buffer_info` structure.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} status_t BDirectWindow::GetClippingRegion(BRegion* region, BPoint* origin = NULL) const
:::

Sets the specified {hparam}`region` to match the current clipping region
of the direct window. If {hparam}`origin` is specified, each point in the
region is offset by the {hparam}`origin`, resulting in a
{cpp:class}`BRegion` that's localized to your application's vision of where
in space the origin is (relative to the origin of the screen's frame
buffer).

Although the {htype}`direct_buffer_info` structure contains the clipping
region of a direct window, it's not in standard {cpp:class}`BRegion` form.
This function is provided so you can obtain a standard {cpp:class}`BRegion`
if you need one.

:::{admonition} Warning
:class: warning
The {hmethod}`GetClippingRegion()` function can only be called from the
{cpp:func}`DirectConnected() <BDirectWindow::DirectConnected>` function;
calling it from outside {cpp:func}`DirectConnected()
<BDirectWindow::DirectConnected>` will return invalid results.
:::

If you need to cache the clipping region of your window and need a
{cpp:class}`BRegion` for clipping purposes, you could use the following
code inside your {cpp:func}`DirectConnected()
<BDirectWindow::DirectConnected>` function:

:::{code} cpp
BRegion rgn;
GetClippingRegion(&rgn);
:::

This serves a double purpose: it obtains the clipping region in
{cpp:class}`BRegion` form, and it returns a copy of the region that you can
maintain locally. However, it may be more efficient to copy the clipping
region by hand, since the clipping rectangle list used by
{hclass}`BDirectWindow` uses integer numbers, while {cpp:class}`BRegion`
uses floating-point.

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`B_OK`.
	- The clipping region was successfully returned.
-
	- {cpp:enumerator}`B_ERROR`.
	- An error occurred while trying to obtain the clipping region.

:::
::::

::::{abi-group}
:::{cpp:function} bool BDirectWindow::IsFullScreen() const
:::

:::{cpp:function} status_t BDirectWindow::SetFullScreen(bool enable)
:::

{hmethod}`IsFullScreen()` returns {cpp:expr}`true` if the direct window is
in full-screen exclusive mode, or {cpp:expr}`false` if it's in window mode.

The value returned by {hmethod}`IsFullScreen()` is indeterminate if a call
to {hmethod}`SetFullScreen()` is in progress—if this is the case, you
shouldn't rely on the resulting value. Instead, it would be safer to
maintain a state setting of your own and use that value.

{hmethod}`SetFullScreen()` enables full-screen exclusive mode if the
{hparam}`enable` flag is {cpp:expr}`true`. To switch to window mode, pass
{cpp:expr}`false`. The {cpp:func}`SupportsWindowMode()
<BDirectWindow::SupportsWindowMode>` function can be used to determine
whether or not the video card is capable of supporting window mode. See
"{ref}`Window Mode vs. Full Screen Mode`" for a detailed explanation of the
differences between these modes.

When your window is in full screen mode, it will always have the focus,
and no other window can come in front of it.

{hmethod}`SetFullScreen()` can return any of the following result codes.

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`B_OK`.
	- The mode was successfully changed.
-
	- {cpp:enumerator}`B_ERROR`.
	- An error occurred while trying to switch between full screen and window
		modes  (for example, another window may already be in full-screen exclusive
		mode in the same workspace).

:::
::::

::::{abi-group}
:::{cpp:function} static bool BDirectWindow::SupportsWindowMode(screen_id id = B_MAIN_SCREEN_ID)
:::

Returns {cpp:expr}`true` if the specified screen supports window mode; if
you require the ability to directly access the frame buffer of a window
(rather than occupying the whole screen), you should call this function to
be sure that the graphics hardware in the computer running your application
supports it. Because this is a static function, you don't have to construct
a {hclass}`BDirectWindow` object to call it:

:::{code} cpp
if (BDirectWindow::SupportsWindowMode()) {
   /* do stuff here */
}
:::

In particular, window mode requires a graphics card with DMA support and a
hardware cursor; older video cards may not be capable of supporting window
mode.

If window mode isn't supported, but you still select window mode,
{cpp:func}`DirectConnected() <BDirectWindow::DirectConnected>` will never
be called (so you'll never be authorized for direct frame buffer access).

Even if window mode isn't supported, you can still use
{hclass}`BDirectWindow` objects for full-screen direct access to the frame
buffer, but it's recommended that you avoid direct video DMA or the use of
parallel drawing threads that use both direct frame buffer access and
{cpp:class}`BView` calls (because it's likely that such a graphics card
won't handle the parallel access and freeze the PCI bus—and that would be
bad).
::::
