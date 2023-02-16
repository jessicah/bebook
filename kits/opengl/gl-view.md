:::{cpp:class} BGLView
:::

# BGLView

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BGLView::BGLView(BRect frame, const char* name, int32 resizingMode, int32 flags, int32 type)
:::

Initializes the view, then creates a new OpenGL drawing context and
attaches it to the view. The {hparam}`type` argument specifies the OpenGL
type specification for the view:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Constant

	- Description

-
	- {cpp:enumerator}`BGL_RGB`
	- Use RGB graphics instead of indexed color (8-bit). This is the default if
		neither {cpp:enumerator}`BGL_RGB` nor {cpp:enumerator}`BGL_INDEX` is
		specified.
-
	- {cpp:enumerator}`BGL_INDEX`
	- Use indexed color (8-bit graphics). Not currently supported.
-
	- {cpp:enumerator}`BGL_SINGLE`
	- Use single-buffering; all rendering is done directly to the display. This
		is not currently supported by the BeOS implementation of OpenGL. This is
		the default if neither {cpp:enumerator}`BGL_SINGLE` nor
		{cpp:enumerator}`BGL_DOUBLE` is specified.
-
	- {cpp:enumerator}`BGL_DOUBLE`
	- Use double-buffered graphics. All rendering is done to an offscreen buffer
		and only becomes visible when the {cpp:func}`SwapBuffers()
		<BGLView::SwapBuffers>` function is called.
-
	- {cpp:enumerator}`BGL_ACCUM`
	- Requests that the view have an accumulation buffer.
-
	- {cpp:enumerator}`BGL_ALPHA`
	- Requests that the view's color buffer include an alpha component.
-
	- {cpp:enumerator}`BGL_DEPTH`
	- Requests that the view have a depth buffer.
-
	- {cpp:enumerator}`BGL_STENCIL`
	- Requests that the view have a stencil buffer.

:::
::::

::::{abi-group}
:::{cpp:function} virtual BGLView::~BGLView()
:::

Disposes of the OpenGL context for the view.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} virtual void BGLView::~BGLView()
:::

Calls the inherited version of {cpp:func}`AttachedToWindow()
<BView::AttachedToWindow>` and sets the view color to
{cpp:enumerator}`B_TRANSPARENT_32_BIT` (this improves performance by
preventing the Application Server from erasing the view, since OpenGL takes
over responsibility for drawing into the view).
::::

::::{abi-group}
:::{cpp:function} status_t BGLView::CopyPixelsIn(BBitmap* source, BPoint dest)
:::

:::{cpp:function} status_t BGLView::CopyPixelsOut(BPoint source, BBitmap* dest)
:::

These functions copy pixel data into and out of the OpenGL draw buffer for
the context.

{hmethod}`CopyPixelsIn()` copies the entire contents of the
{hparam}`source` {cpp:class}`BBitmap` into the OpenGL context, offset such
that the top-left corner of the {cpp:class}`BBitmap` is drawn at the point
dest in the OpenGL buffer.

{hmethod}`CopyPixelsOut()` copies from the OpenGL draw buffer into the
specified {cpp:class}`BBitmap`. The area copied is the size of the dest
bitmap and contains all data from the specified source {hparam}`point` to
the bottom-right corner of the buffer.

:::{admonition} Note
:class: note
If the source is larger than the destination, it's clipped at the bottom
and right edges to fit; no scaling is performed Also, the OpenGL context
and the {cpp:class}`BBitmap` must be in the same color space.
:::

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
	- {cpp:enumerator}`B_OK`
	- The data was copied without error.
-
	- {cpp:enumerator}`B_BAD_VALUE`
	- The current draw buffer is not valid, or the destination buffer's width or
		height is less than or equal to zero.
-
	- {cpp:enumerator}`B_BAD_TYPE`
	- The source and destination are in different color spaces.

:::
::::

::::{abi-group}
:::{cpp:function} void BGLView::DirectConnected(direct_buffer_info* directInfo)
:::

If the {hclass}`BGLView` is in a {cpp:class}`BDirectWindow`, you should
call this from your {cpp:func}`BDirectWindow::DirectConnected` function to
let OpenGL update the window properly.
::::

::::{abi-group}
:::{cpp:function} virtual void BGLView::Draw(BRect updateRect)
:::

Refreshes the contents of the {hclass}`BGLView` by copying the frontbuffer
to the screen.

If the view's color space is eight bits deep and the
{cpp:enumerator}`GL_DITHER` OpenGL option is enabled, the display is
dithered.
::::

::::{abi-group}
:::{cpp:function} BView* BGLView::EmbeddedView()
:::

Returns a pointer to an embedded view that encompasses the current OpenGL
drawing buffer, as defined by OpenGL, for the {hclass}`BGLView`. If the
view is single-buffered, this will be the frontbuffer, and if the view is
double-buffered, the embedded view will encompass the backbuffer.

:::{admonition} Note
:class: note
{hmethod}`EmbeddedView()` returns {cpp:expr}`NULL` if, for any reason,
{cpp:class}`BView` functions can't be used in the GL buffer. Starting with
BeOS R4, this function always returns {cpp:expr}`NULL`, as the new,
high-performance implementation of OpenGL does not support tinkering with
the view.
:::
::::

::::{abi-group}
:::{cpp:function} void BGLView::EnableDirectMode(bool enabled)
:::

Call this function to tell the {hclass}`BGLView` whether or not it should
render in direct mode. If you're using a {cpp:class}`BDirectWindow` and
want video refreshes to be done through the direct window method, pass
{cpp:expr}`true` for {hparam}`enabled`. If you don't want to use the direct
window method, pass {cpp:expr}`false`.
::::

::::{abi-group}
:::{cpp:function} virtual void BGLView::ErrorCallback(GLenum errorCode)
:::

Called when an OpenGL error occurs. By default, this function invokes the
debugger with an error message reading "GL: Error code $xxxx." You can (and
probably should) reimplement this function to cope with errors more
gracefully.
::::

::::{abi-group}
:::{cpp:function} virtual void BGLView::FrameResized(float width, float height)
:::

Calls the inherited version of {cpp:func}`FrameResized()
<BView::FrameResized>`, releases tables that need to be recalculated, and
resizes the OpenGL buffers.

You can augment this function to perform other necessary tasks, such as
adjusting your {hclass}`BGLView`'s coordinate system.
::::

::::{abi-group}
:::{cpp:function} void BGLView::LockGL()
:::

:::{cpp:function} void BGLView::UnlockGL()
:::

These functions lock and unlock the OpenGL context. You must lock the
context before issuing any OpenGL commands, and unlock it when you're
done—this is how OpenGL knows which context the drawing commands are
intended for, since OpenGL itself isn't encapsulated within the
{hclass}`BGLView` class. For example:

:::{code} cpp
LockGL();            /* lock the OpenGL context
glEnable(GL_DITHER); /* turn on dithering support */
UnlockGL();
:::

Failing to lock and unlock the context appropriately will result in
unpredictable behavior and may cause your application to crash.
::::

::::{abi-group}
:::{cpp:function} void BGLView::SwapBuffers()
:::

:::{cpp:function} void BGLView::SwapBuffers(bool vSync)
:::

Swaps the front buffer and back buffer, then redraws the contents of the
{hclass}`BGLView`.

This function has no effect if the view is single-buffered.

If {hparam}`vSync` is specified and is {cpp:expr}`true`, the swap is
synchronized with vertical blanking.
::::
