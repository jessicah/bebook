# BPicture

A {cpp:class}`BPicture` object represents a set of drawing instructions
that are executed when the object is passed to {cpp:class}`BView`'s
{cpp:func}`DrawPicture() <BView::DrawPicture>` function. Because it
contains drawing instructions rather than an actual image, a
{cpp:class}`BPicture`BPicture (unlike a {cpp:class}`BBitmap`) is
independent of the resolution of the display device.

## Recording a Picture

To start recording into a {cpp:class}`BPicture`, you pass a
{cpp:class}`BPicture` object to {cpp:func}`BView::BeginPicture`. All
drawing instructions that are executed by the {cpp:class}`BView` are
recorded into the {cpp:class}`BPicture` object. When you're done recording,
you call {cpp:func}`BView::EndPicture`, which passes back a pointer to the
recorded object. For example:

:::{code} cpp
BPicture *myPict;
someView->BeginPicture(new BPicture);
/* drawing code goes here*/
myPict = someView->EndPicture();
:::

Only drawing that the {cpp:class}`BView` does is recorded; drawing done by
children and other views attached to the window is ignored, as is
everything except drawing code.

Drawing instructions that are captured between {cpp:func}`BeginPicture()
<BView::BeginPicture>` and {cpp:func}`EndPicture() <BView::EndPicture>` are
not renedered on-screen; ignored instructions may be rendered if they draw
into the visible region of an on-screen window.

Any picture data in the {cpp:class}`BPicture` passed to
{cpp:func}`BeginPicture() <BView::BeginPicture>` is cleared; if you'd
instead like to append to the {cpp:class}`BPicture`, begin the picture
recording with {cpp:func}`AppendPicture() <BView::AppendToPicture>`
instead. As with {cpp:func}`BeginPicture() <BView::BeginPicture>`, each
{cpp:func}`AppendToPicture() <BView::AppendToPicture>` must have a
corresponding EndPicture().

## The Picture Definition

The picture captures everything that affects the image that's drawn. It
takes a snapshot of the {cpp:class}`BView`'s graphics state—the pen size,
high and low colors, font size, and so on—when {cpp:func}`BeginPicture()
<BView::BeginPicture>` is called. It then captures all subsequent
modifications to those parameters, such as calls to {cpp:func}`MovePenTo()
<BView::MovePenTo>`, {cpp:func}`SetLowColor() <BView::SetLowColor>`, an
{cpp:func}`SetFontSize() <BView::SetFontSize>`. The recorded graphics state
is used when the picture is drawn (through {cpp:func}`BView::DrawPicture`).

The picture records all primitive drawing instruction (
{cpp:func}`DrawBitmap() <BView::DrawBitmap>`, {cpp:func}`StrokeEllipse()
<BView::StrokeEllipse>`, {cpp:func}`FillRect() <BView::FillRect>`, etc.)
and will even record calls to {cpp:func}`DrawPicture()
<BView::DrawPicture>`.

The picture makes its own copy of any data that's passed during the
recording session, including bitmaps passed to {cpp:func}`DrawBitmap()
<BView::DrawBitmap>` and picture data passed to {cpp:func}`DrawPicture()
<BView::DrawPicture>`.
