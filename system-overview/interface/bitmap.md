# BBitmap

A {cpp:class}`BBitmap` describes a rectangular image as a two-dimensional
array of pixel data (or bitmap). The {cpp:class}`BBitmap` class lets you
create a bitmap by specifying raw pixel data (through the {cpp:func}`Bits()
<BBitmap::Bits>` and {cpp:func}`SetBits() <BBitmap::SetBits>` functions),
or you can add a {cpp:class}`BView` to your {cpp:class}`BBitmap` and use
the view's drawing operations ( {cpp:func}`FillRect() <BView::FillRect>`,
{cpp:func}`StrokeLine() <BView::StrokeLine>`, etc) to draw into the
{cpp:class}`BBitmap` object (see "{ref}`Using a View to Draw into a
Bitmap`", below).

The {cpp:class}`BBitmap` class doesn't provide a way to actually display
bitmap data. Displaying a bitmap is the task of {cpp:class}`BView`
functions such as {cpp:func}`DrawBitmap() <BView::DrawBitmap>`.

## Bitmap Data

A bitmap records the color values of every pixel within a rectangular
area. The data is specified in rows, beginning with the top row of pixels
in the image and working downward to the bottom row. Each row is aligned on
a long word boundary.

When you construct a {cpp:class}`BBitmap` object, you give it a bounds
rectangle (integer coordinates only!) and a color space. For example, this
code

:::{code} cpp
BBitmap* image = new BBitmap(BRect(0.0, 0.0, 79.0, 39.0),
                             B_CMAP8);
:::

constructs a 40 x 80 bitmap of 8-bit color data.

The data in a {cpp:class}`BBitmap` object isn't initialized—a
{cpp:class}`BBitmap` has no default background color. When you set the
bitmap's data (however you set it) you must "paint" every pixel within the
bitmap's bounds rectangle.

## Using a View to Draw into a Bitmap

If you're going to use a view to draw into your bitmap, you must tell the
{cpp:class}`BBitmap` constructor by setting the third argument to
{cpp:expr}`true`:

:::{code} cpp
BBitmap *image = new BBitmap(BRect(...), B_CMAP8, true);
:::

You then add the view to the bitmap (you don't have to do anything special
when constructing the {cpp:class}`BView`):

:::{code} cpp
bitmap->AddChild(view);
:::

When the view draws, the drawing operations are rendered into the bitmap.
Note that you must explicitly tell the {cpp:class}`BView`): to draw—the
{cpp:class}`BView`s that you use to draw into a {cpp:class}`BBitmap` aren't
part of the user interface, so they won't receive user event messages. When
you're done drawing, you should call {cpp:class}`BView`'s {cpp:func}`Sync()
<BView::Sync>` function to make sure the drawing has all been performed. If
the bitmap that you've created is static—if it doesn't need to change after
you've drawn into it—you can throw away the {cpp:class}`BView` that you
used create the bitmap data.

A {cpp:class}`BBitmap` can contain more than one {cpp:class}`BView`—it can
act as the root of an entire view hierarchy. The {cpp:class}`BBitmap` class
defines a number of {cpp:class}`BWindow`-like
functions—{cpp:func}`AddChild() <BBitmap::AddChild>`, {cpp:func}`FindView()
<BBitmap::FindView>`, {cpp:func}`ChildAt() <BBitmap::ChildAt>`, and so
on—to help you create and manage the hierarchy.

## Transparency

Color bitmaps can have transparent pixels. When the bitmap is imaged in a
drawing mode other than {cpp:enumerator}`B_OP_COPY`, its transparent pixels
won't be transferred to the destination view. The destination image will
show through wherever the bitmap is transparent.

To introduce transparency into a {cpp:enumerator}`B_CMAP8` bitmap, a pixel
can be assigned one of the following values, as appropriate for the
bitmap's color space.

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
	- {cpp:enumerator}`B_TRANSPARENT_MAGIC_CMAP8`
	- 8-bit indexed color transparent pixel.
-
	- {cpp:enumerator}`B_TRANSPARENT_MAGIC_RGBA15`
	- 15-bit transparent pixel.
-
	- {cpp:enumerator}`B_TRANSPARENT_MAGIC_RGBA15_BIG`
	- 15-bit transparent pixel, big-endian.
-
	- {cpp:enumerator}`B_TRANSPARENT_MAGIC_RGBA32`
	- 32-bit transparent pixel.
-
	- {cpp:enumerator}`B_TRANSPARENT_MAGIC_RGBA32_BIG`
	- 32-bit transparent pixel, big-endian.

:::

Opaque pixels should have an alpha value of 255 for 8-bit alpha channels
or 1 for 1-bit alpha channels; values of 0 indicate 100% transparent
pixels. Values in between (for 8-bit alpha channels) represent varying
degrees of transparency.

Transparency is covered in more detail under "{ref}`Drawing Modes`".

See also: {cpp:func}`system_colors() <system::colors>`
