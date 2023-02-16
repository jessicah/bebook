# BFont

A {cpp:class}`BFont` object records a set of font attributes, such as the
font's family, style, size, and so on. You can set most of these attributes
to modify the font and then use the object to set the font of a
{cpp:class}`BView`. A {cpp:class}`BView`'s font determines how the
characters that it draws (with the {cpp:func}`DrawString()
<BView::DrawString>` and {cpp:func}`DrawChar() <BView::DrawChar>`
functions) will be rendered.

A {cpp:class}`BFont` object can perform calculations based on the metrics
of the particular font it represents. For example, it can tell you how much
screen real estate it needs to display a given line of text.

To find which fonts are currently installed on the system, call
{ref}`get_font_family()` and {ref}`get_font_style()`.

## Using a BFont Object

A {cpp:class}`BFont` object by itself doesn't do anything. To be able to
draw characters in the font, the object must be passed to
{cpp:class}`BView`'s {cpp:func}`SetFont() <BView::SetFont>` function (or
{cpp:class}`BTextView`'s {cpp:func}`SetFontAndColor()
<BTextView::SetFontAndColor>`).

A {cpp:class}`BFont` object is always a full representation of a font; all
attributes are always set. However, you can choose which of these
attributes will modify a {cpp:class}`BView`'s current font by passing a
mask to {cpp:func}`SetFont() <BView::SetFont>` (or {cpp:class}`BTextView`'s
{cpp:func}`SetFontAndColor() <BTextView::SetFontAndColor>`). For example,
this code sets only the font shear and spacing:

:::{code} cpp
BFont font;
font.SetShear(60.0);
font.SetSpacing(B_CHAR_SPACING);
myView->SetFont(&font, B_FONT_SHEAR | B_FONT_SPACING);
:::

Alternatively, the {hclass}`BView`'s font could have been modified and
reset as follows:

:::{code} cpp
BFont font;
myView->GetFont(&font);
font.SetShear(60.0);
font.SetSpacing(B_CHAR_SPACING);
myView->SetFont(&font);
:::

Notice that we had to explicitly reset the view's font (through
{cpp:func}`SetFont() <BView::SetFont>`) after changing the font's
attributes.

## System Fonts

The Interface Kit constructs three {cpp:class}`BFont` objects (plain,
bold, and fixed)for each application when the application starts up. The
values of these fonts are set by the user through the FontPanel preferences
application. You can get to these objects through global pointers :

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
	- constBFont*be_plain_font
	- The font that's used to display most gadgets in the user interface, such
		as check box labels and menu items. All {cpp:class}`BControl` objects use
		this font.
-
	- constBFont*be_bold_font
	- The font that's used to display window titles and {cpp:class}`BBox`
		labels.
-
	- constBFont*be_fixed_font
	- The font that's used to display fixed-width characters.

:::

The global fonts are const objects that can't be modified by your
application, and aren't updated by the system, even if the user changes
their definitions while your app is running. The new values take effect the
next time your application is launched.

To use a system font in a view, simply call {cpp:func}`SetFont()
<BView::SetFont>`:

:::{code} cpp
myView->SetFont(be_bold_font);
:::

If you want to modify some attributes of a system font, you have to make a
copy of it first (and modify the copy):

:::{code} cpp
BFont font(be_bold_font);
font.SetSize(13.0);
myView->SetFont(&font);
:::

Applications should respect the user's choices and base all font choices
on these three system fonts, rather than hard-code font names into the
application. You should not try to predict the fonts that will be installed
on the user's machine.
