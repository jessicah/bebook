:::{cpp:class} BWindowScreen
:::

# BWindowScreen

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BWindowScreen::BWindowScreen(const char* title, uint32 space, status_t* error, bool debugging = false)
:::

Initializes the {hclass}`BWindowScreen` object by assigning the window a
{hparam}`title` and specifying a {hparam}`space` configuration for the
screen. The window won't have a visible border or a tab in which to display
the title to the user. However, others—such as the Workspaces
application—can use the title to identify the window.

The window is constructed to fill the screen; its frame rectangle contains
every screen pixel when the screen is configured according to the
{hparam}`space` argument. That argument describes the pixel dimensions and
bits-per-pixel depth of the screen that the {hclass}`BWindowScreen` object
should establish when it obtains direct access to the frame buffer. It
should be one of the following constants:

:::{code} sh
B_8_BIT_640x480    B_16_BIT_640x480    B_32_BIT_640x480
B_8_BIT_800x600    B_16_BIT_800x600    B_32_BIT_800x600
B_8_BIT_1024x768   B_16_BIT_1024x768   B_32_BIT_1024x768
B_8_BIT_1152x900   B_16_BIT_1152x900   B_32_BIT_1152x900
B_8_BIT_1280x1024  B_16_BIT_1280x1024  B_32_BIT_1280x1024
B_8_BIT_1600x1200  B_16_BIT_1600x1200  B_32_BIT_1600x1200
:::

These are the same constants that can be passed to
{cpp:func}`set_screen_space()`, the {ref}`Interface Kit` function that
preference applications call to configure the screen.

The {hparam}`space` configuration applies only while the
{hclass}`BWindowScreen` object is in control of the screen. When it gives
up control, the previous configuration is restored.

The constructor assigns the window to the active workspace
({cpp:enumerator}`B_CURRENT_WORKSPACE`). It fails if another
{hclass}`BWindowScreen` object in any application is already assigned to
the same workspace.

To be sure there wasn't an error in constructing the object, check the
{hparam}`error` argument. If all goes well, the constructor sets the
{hparam}`error` variable to {cpp:enumerator}`B_OK`. If not, it sets it to
{cpp:enumerator}`B_ERROR`. If there's an error, it's likely to occur in
this constructor, not the inherited {cpp:class}`BWindow` constructor. Since
the underlying window will probably exist, you'll need to instruct it to
quit. For example:

:::{code} cpp
status_t error;
MyWindowScreen* screen =
            new MyWindowScreen("Glacier", B_8_BIT_1024x768, &error);

if ( error != B_OK )
   screen->PostMessage(B_QUIT_REQUESTED, screen);
:::

If the {hparam}`debugging` flag is {cpp:expr}`true`, the
{hclass}`BWindowScreen` is constructed in debugging mode. This modifies its
behavior and enables three functions, {cpp:func}`RegisterThread()
<BWindowScreen::RegisterThread>`, {cpp:func}`Suspend()
<BWindowScreen::Suspend>`, and {cpp:func}`SuspensionHook()
<BWindowScreen::SuspensionHook>`. The debugging regime is described under
those functions.

See also: the {cpp:class}`BScreen` class in the {ref}`Interface Kit`
::::

::::{abi-group}
:::{cpp:function} virtual BWindowScreen::~BWindowScreen()
:::

Closes the clone of the graphics card driver (through which the
{hclass}`BWindowScreen` object established its connection to the screen),
unloads it from the application, and cleans up after it.
::::

## Hook Functions

::::{abi-group}
:::{cpp:function} virtual void BWindowScreen::ScreenConnected(bool connected)
:::

Implemented by derived classes to take action when the application gains
direct access to the screen and when it's about to lose that access.

This function is called with the {hparam}`connected` flag set to
{cpp:expr}`true` immediately after the {hclass}`BWindowScreen` object
becomes the active window and establishes a direct connection to the
graphics card driver for the screen. At that time, the Application Server's
connection to the screen is suspended; drawing can only be accomplished
through the screen access that the {hclass}`BWindowScreen` object provides.

{hmethod}`ScreenConnected()` is called with a flag of {cpp:expr}`false`
just before the {hclass}`BWindowScreen` object is scheduled to lose its
control over the screen and the Application Server's control is reasserted.
The {hclass}`BWindowScreen`'s connection to the screen will not be broken
until this function returns. It should delay returning until the
application has finished all current drawing and no longer needs direct
screen access.

Note that whenever {hmethod}`ScreenConnected()` is called, the
{hclass}`BWindowScreen` object is guaranteed to be connected to the screen;
if {hparam}`connected` is {cpp:expr}`true`, it just became connected, if
{hparam}`connected` is {cpp:expr}`false`, it's still connected but will be
disconnected when the function returns.

Derived classes typically use this function to regulate access to the
screen. For example, they may acquire a semaphore when the
{hparam}`connected` flag is {cpp:expr}`false`, so that application threads
won't attempt direct drawing when the connection isn't in place, and
release the semaphore for drawing threads to acquire when the flag is
{cpp:expr}`true`. For example:

:::{code} cpp
void MyWindowScreen::ScreenConnected(bool connected)
{
   if ( connected == false )
      acquire_sem(directDrawingSemaphore);
   else
      release_sem(directDrawingSemaphore);
}
:::

See also: {cpp:func}`Disconnect() <BWindowScreen::Disconnect>`
::::

## Member Functions

::::{abi-group}
:::{cpp:function} bool BWindowScreen::CanControlFrameBuffer()
:::

Returns {cpp:expr}`true` if the graphics card driver permits applications
to control the configuration of the frame buffer, and {cpp:expr}`false` if
not. Control is exercised through these two functions:

-   {cpp:func}`SetFrameBuffer() <BWindowScreen::SetFrameBuffer>`

-   {cpp:func}`MoveDisplayArea() <BWindowScreen::MoveDisplayArea>`

A return of {cpp:expr}`true` means that these functions can communicate
with the graphics card driver and at least the first will do something
useful. A return of {cpp:expr}`false` means that neither of them will work.
::::

::::{abi-group}
:::{cpp:function} graphics_card_hook BWindowScreen::CardHookAt(int32 index)
:::

Returns a pointer to the graphics card "hook" function that's located at
{hparam}`index` in its list of hook functions. The function returns
{cpp:expr}`NULL` if the graphics card driver doesn't implement a function
at that index or the index is out of range.

The hook functions provide accelerated drawing capabilities. They're
documented under "{ref}`Graphics Card Hook Functions`". The first three
hook functions (indices 0, 1, and 2) are not available through the Game
Kit; if you pass an index of 0, 1, or 2 to {hmethod}`CardHookAt()`, it will
return {cpp:expr}`NULL` even if the function is implemented.

An application can cache the pointers that {hmethod}`CardHookAt()`
returns, but it should ask for a new set each time the depth or dimensions
of the screen changes and each time the {hclass}`BWindowScreen` object
releases or regains control of the screen. You'd typically call
{hmethod}`CardHookAt()` in your implementation of
{cpp:func}`ScreenConnected() <BWindowScreen::ScreenConnected>`.
::::

::::{abi-group}
:::{cpp:function} graphics_card_info* BWindowScreen::CardInfo()
:::

Returns a description of the current configuration of the graphics card,
as kept by the driver for the card. The returned
{htype}`graphics_card_info` structure is defined in
addons/graphics/GraphicsCard.h

:::{admonition} Note
:class: note
The information returned by this function is only valid when the
{hclass}`BWindowScreen` is connected to the display.
:::

See also: {cpp:func}`FrameBufferInfo() <BWindowScreen::FrameBufferInfo>`
::::

::::{abi-group}
:::{cpp:function} void BWindowScreen::Disconnect()
:::

Forces the {hclass}`BWindowScreen` object to disconnect itself from the
screen—to give up its authority over the graphics card driver, allowing the
Application Server to reassert control. Normally, you'd disconnect the
{hclass}`BWindowScreen` only when hiding the game, reducing it to an
ordinary window in the background, or quitting. The {cpp:func}`Hide()
<BWindowScreen::Hide>` and {cpp:func}`Quit() <BWindowScreen::Quit>`
functions automatically disconnect the {hclass}`BWindowScreen` as part of
the process of hiding and quitting. {cpp:func}`Disconnect()
<BWindowScreen::Disconnect>` allows you to sever the connection before
calling those functions.

Before breaking the screen connection, {cpp:func}`Disconnect()
<BWindowScreen::Disconnect>` causes the {hclass}`BWindowScreen` object to
receive a {cpp:func}`ScreenConnected() <BWindowScreen::ScreenConnected>`
notification with a flag of {cpp:expr}`false`. It doesn't return until
{cpp:func}`ScreenConnected() <BWindowScreen::ScreenConnected>` returns and
the connection is broken. {cpp:func}`Hide() <BWindowScreen::Hide>` and
{cpp:func}`Quit() <BWindowScreen::Quit>` share this behavior.
::::

::::{abi-group}
:::{cpp:function} frame_buffer_info* BWindowScreen::FrameBufferInfo()
:::

Returns a pointer to the {htype}`frame_buffer_info` structure that holds
the driver's current conception of the frame buffer. The structure is
defined in addons/graphics/GraphicsCard.h

:::{admonition} Note
:class: note
The information returned by this function is only valid if
{cpp:func}`SetFrameBuffer() <BWindowScreen::SetFrameBuffer>` has been
called.
:::

See also: {cpp:func}`SetSpace() <BWindowScreen::SetSpace>`,
{cpp:func}`SetFrameBuffer() <BWindowScreen::SetFrameBuffer>`,
{cpp:func}`MoveDisplayArea() <BWindowScreen::MoveDisplayArea>`,
{cpp:func}`CardInfo() <BWindowScreen::CardInfo>`
::::

::::{abi-group}
:::{cpp:function} virtual void BWindowScreen::Hide()
:::

:::{cpp:function} virtual void BWindowScreen::Show()
:::

These functions augment their {cpp:class}`BWindow` counterparts to make
sure that the {hclass}`BWindowScreen` is disconnected from the screen
before it's hidden and that it's ready to establish a connection when it
becomes the active window.

{hmethod}`Hide()` calls {cpp:func}`ScreenConnected()
<BWindowScreen::ScreenConnected>` (with an argument of {cpp:expr}`false`)
and breaks the connection to the screen when {cpp:func}`ScreenConnected()
<BWindowScreen::ScreenConnected>` returns. It then hides the window.

{hmethod}`Show()` shows the window on-screen and makes it the active
window, which will cause it to establish a direct connection to the
graphics card driver for the screen. Unlike {hmethod}`Hide()`, it may
return before {cpp:func}`ScreenConnected()
<BWindowScreen::ScreenConnected>` is called (with an argument of
{cpp:expr}`true`).

See also: {cpp:func}`BWindow::Hide`
::::

::::{abi-group}
:::{cpp:function} void* BWindowScreen::IOBase()
:::

Returns a pointer to the base address for the input/output registers on
the graphics card. Registers are addressed by 16-bit offsets from this base
address. (This function may not be supported in future releases.)
::::

::::{abi-group}
:::{cpp:function} status_t BWindowScreen::MoveDisplayArea(int32 x, int32 y)
:::

Relocates the display area, the portion of the frame buffer that's mapped
to the screen. This function moves the area's left-top corner to
({hparam}`x`, {hparam}`y`); by default, the corner lies at (0, 0). The
display area must lie entirely within the frame buffer.

{hmethod}`MoveDisplayArea()` only works if the graphics card driver
permits application control over the frame buffer. It must also permit a
frame buffer with a total area larger than the display area. If successful
in relocating the display area, this function returns
{cpp:enumerator}`B_OK`; if not, it returns {cpp:enumerator}`B_ERROR`.

See also: {cpp:func}`CanControlFrameBuffer()
<BWindowScreen::CanControlFrameBuffer>`
::::

::::{abi-group}
:::{cpp:function} virtual void BWindowScreen::Quit()
:::

Augments the {cpp:class}`BWindow` version of {hmethod}`Quit()` to force
the {hclass}`BWindowScreen` object to disconnect itself from the screen, so
that it doesn't quit while in control of the frame buffer.

Although {hmethod}`Quit()` disconnects the object before quitting, this
may not be soon enough for your application. For example, if you need to
destroy some drawing threads before the {hclass}`BWindowScreen` object is
itself destroyed, you should get rid of them after the screen connection is
severed. You can force the object to disconnect itself by calling
{cpp:func}`Disconnect() <BWindowScreen::Disconnect>`. For example:

:::{code} cpp
void MyWindowScreen::Quit()
{
   Disconnect();
   kill_thread(drawing_thread_a);
   kill_thread(drawing_thread_b);
   BWindowScreen::Quit();
}
:::

If the screen connection is still in place when {hmethod}`Quit()` is
called, it calls {cpp:func}`ScreenConnected()
<BWindowScreen::ScreenConnected>` with a flag of {cpp:expr}`false`. It
doesn't return until {cpp:func}`ScreenConnected()
<BWindowScreen::ScreenConnected>` returns and the connection is broken.
::::

::::{abi-group}
:::{cpp:function} void BWindowScreen::RegisterThread(thread_id thread)
:::

:::{cpp:function} void BWindowScreen::Suspend(char* label)
:::

:::{cpp:function} virtual void* BWindowScreen::SuspensionHook(bool suspended)
:::

These three functions aid in debugging a game application. They have
relevance only if the {hclass}`BWindowScreen` is running in debugging mode.
To set up the mode, you must:

1.    Construct the {hclass}`BWindowScreen` with the {hparam}`debugging` flag
set to {cpp:expr}`true`. The flag is {cpp:expr}`false` by default.

2.    Register all drawing threads (all threads that can touch the frame buffer
in any way) by passing the {htype}`thread_id` to
{cpp:func}`RegisterThread() <BWindowScreen::RegisterThread>` immediately
after the thread is spawned—before {hmethod}`resume_thread()` is called to
start the thread's execution. The window thread for the
{hclass}`BWindowScreen` object should not draw and should not be
registered.

3.    Launch the application from the command line in a Terminal window. The
window will collect debugging output from the application while the
{hclass}`BWindowScreen` runs in a different workspace, generally the one at
the immediately preceding index. For example, if the Terminal window is in
the fifth workspace ({hkey}`Command`+{hkey}`F5`), the game will run in the
fourth ({hkey}`Command`+{hkey}`F4`); if the Terminal is in the fourth
({hkey}`Command`+{hkey}`F4`), the game runs in the third
({hkey}`Command`+{hkey}`F3`); and so on. However, if the Terminal window is
in the first workspace ({hkey}`Command`+{hkey}`F1`), the game runs in the
second ({hkey}`Command`+{hkey}`F2`).

The Terminal window is the destination for all messages the game writes to
the standard error stream or to the standard output—from printf(), for
example. You can switch back and forth between the game and Terminal
workspaces to check the messages and run your application. When you switch
from the game workspace to the Terminal workspace, all registered threads
are suspended and the graphics context is saved. When you switch back to
the game, the graphics context is restored and the threads are resumed.

Calling {hmethod}`Suspend()` switches to the Terminal workspace
programmatically, just as pressing the correct Command—function key
combination would. Registered threads are suspended, the Terminal workspace
is activated, and the {hparam}`label` passed as an argument is displayed in
a message in the Terminal window. You can resume the game by manually
switching back to its workspace.

{hmethod}`SuspensionHook()` is called whenever the game is suspended or
resumed—whether by the user switching workspaces or by
{hmethod}`Suspend()`. It gives you an opportunity to save and restore any
state that would otherwise be lost. {hmethod}`SuspensionHook()` is called
with a {hparam}`suspended` flag of {cpp:expr}`true` just after the
application is suspended and with a flag of {cpp:expr}`false` just before
it's about to be resumed.

{hmethod}`ScreenConnected()` is not called when you switch between the
Terminal and game workspaces while in debugging mode. However, it is called
for all normal game activities—when the {hclass}`BWindowScreen` is first
activated and when it hides or quits, for example.

Debugging mode can also preserve some information in case of a crash. Hold
down all the left modifier keys ({hkey}`Shift`, {hkey}`Control`,
{hkey}`Option`, {hkey}`Command`, {hkey}`Alt`, or whatever the keys may
happen to be on your keyboard), and press the {hkey}`F12` key. This
restarts the screen with a 640 * 480 resolution and displays a debugger
window. You should then be able to switch to the Terminal workspace to
check the last set of messages before the crash, modify your code, and
start again.
::::

::::{abi-group}
:::{cpp:function} virtual void BWindowScreen::ScreenChanged(BRect frame, color_space mode)
:::

Overrides the {cpp:class}`BWindow` version of {cpp:func}`ScreenChanged()
<BWindow::ScreenChanged>` so that it does nothing. This function is called
automatically when the screen configuration changes. It's not one that you
should call in application code or reimplement for the game.

See also: {cpp:func}`BWindow::ScreenChanged`
::::

::::{abi-group}
:::{cpp:function} void BWindowScreen::SetColorList(rgb_color* colors, int32 first = 0, int32 last = 255)
:::

:::{cpp:function} rgb_color* BWindowScreen::ColorList()
:::

These functions set and return the list of 256 colors that can be
displayed when the frame buffer has a depth of 8 bits per pixel (the
{cpp:enumerator}`B_CMAP8` color space). {hmethod}`SetColorList()` is passed
an array of one or more colors to replace the colors currently in the list.
The first color in the array replaces the color in the list at the
specified {hparam}`first` index; all colors up through the {hparam}`last`
specified index are modified. It fails if either index is out of range.

{hmethod}`SetColorList()` alters the list of colors kept on the graphics
card. If the {hclass}`BWindowScreen` isn't connected to the screen, the new
list takes effect when it becomes connected.

{hmethod}`ColorList()` returns a pointer to the entire list of 256 colors.
This is not the list kept by the graphics card driver, but a local copy. It
belongs to the {hclass}`BWindowScreen` object and should be altered only by
calling {hmethod}`SetColorList()`.

See also: {cpp:func}`BScreen::ColorMap` in the {ref}`Interface Kit`
::::

::::{abi-group}
:::{cpp:function} status_t BWindowScreen::SetFrameBuffer(int32 width, int32 height)
:::

Configures the frame buffer on the graphics card so that it's
{hparam}`width` pixel columns wide and {hparam}`height` pixel rows high.
This function works only if the driver for the graphics card allows custom
configurations (as reported by {cpp:func}`CanControlFrameBuffer()
<BWindowScreen::CanControlFrameBuffer>`) and the {hclass}`BWindowScreen`
object is currently connected to the screen.

The new dimensions of the frame buffer must be large enough to hold all
the pixels displayed on-screen—that is, they must be at least as large as
the dimensions of the display area. If the driver can't accommodate the
proposed width and height, {cpp:func}`SetFrameBuffer()
<BWindowScreen::SetFrameBuffer>` returns {cpp:enumerator}`B_ERROR`. If the
change is made, it returns {cpp:enumerator}`B_OK`.

This function doesn't alter the depth of the frame buffer or the size or
location of the display area.

See also: {cpp:func}`MoveDisplayArea() <BWindowScreen::MoveDisplayArea>`,
{cpp:func}`SetSpace() <BWindowScreen::MoveDisplayArea>`
::::

::::{abi-group}
:::{cpp:function} status_t BWindowScreen::SetSpace(uint32 space)
:::

Configures the screen space to one of the standard combinations of width,
height, and depth. The configuration is first set by the class
constructor—permitted {hparam}`space` constants are documented there—and it
may be altered after construction only by this function.

Setting the screen space sets the dimensions of the frame buffer and
display area. For example, if {hparam}`space` is
{cpp:enumerator}`B_32_BIT_800x600`, the frame buffer will be 32 bits deep
and at least 800 pixel columns wide and 600 pixel rows high. The display
area (the area of the frame buffer mapped to the screen) will also be 800
pixels * 600 pixels. After setting the screen space, you can enlarge the
frame buffer by calling {cpp:func}`SetFrameBuffer()
<BWindowScreen::SetFrameBuffer>` and relocate the display area in the
larger buffer by calling {cpp:func}`MoveDisplayArea()
<BWindowScreen::MoveDisplayArea>`.

If the requested configuration is refused by the graphics card driver,
{cpp:enumerator}`SetSpace()` returns {cpp:enumerator}`B_ERROR`. If all goes
well, it returns {cpp:enumerator}`B_OK`.

See also: the {hclass}`BWindowScreen` {cpp:func}`constructor
<BWindowScreen::BWindowScreen()>`, {cpp:func}`SetFrameBuffer()
<BWindowScreen::SetFrameBuffer>`, {cpp:func}`MoveDisplayArea()
<BWindowScreen::MoveDisplayArea>`
::::

::::{abi-group}
:::{cpp:function} virtual void BWindowScreen::WindowActivated(bool active)
:::

Overrides the {cpp:class}`BWindow` version of {cpp:func}`WindowActivated()
<BWindow::WindowActivated>` to connect the {hclass}`BWindowScreen` object
to the screen (give it control over the graphics card driver) when the
{hparam}`active` flag is {cpp:expr}`true`.

This function doesn't disconnect the {hclass}`BWindowScreen` when the flag
is {cpp:expr}`false`, because there's no way for the window to cease being
the active window without the connection already having been lost.

Don't reimplement this function in your application, even if you call the
inherited version; rely instead on {cpp:func}`ScreenConnected()
<BWindowScreen::ScreenConnected>` for accurate notifications of when the
{hclass}`BWindowScreen` gains and loses control of the screen.

See also: {cpp:func}`BWindow::WindowActivated`,
{cpp:func}`ScreenConnected() <BWindowScreen::ScreenConnected>`
::::

::::{abi-group}
:::{cpp:function} virtual void BWindowScreen::WorkspaceActivated(int32 workspace, bool active)
:::

Overrides the {cpp:class}`BWindow` version of
{cpp:func}`WorkspaceActivated() <BWindow::WorkspaceActivated>` to connect
the {hclass}`BWindowScreen` object to the screen when the {hparam}`active`
flag is {cpp:expr}`true` and to disconnect it when the flag is
{cpp:expr}`false`. User's typically activate the game by activating the
workspace in which it's running, and deactivate it by moving to another
workspace.

Don't override this function in your application; implement
{cpp:func}`ScreenConnected() <BWindowScreen::ScreenConnected>` instead.

See also: {cpp:func}`BWindow::WorkspaceActivated`,
{cpp:func}`ScreenConnected() <BWindowScreen::ScreenConnected>`
::::
