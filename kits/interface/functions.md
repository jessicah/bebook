# Functions

This section describes the global C functions defined in the Interface
Kit. All these functions deal with aspects of the system-wide environment
for the user interface—the screen, workspaces, installed fonts, the list of
possible colors, and various user preferences. For mouse and keyboard
functions, see "{ref}`Input Functions`" in {ref}`The Input Server`.

In almost all cases, you need a valid (but not necessarily running)
{hparam}`be_app` object in order to call these functions.

## activate_workspace(), current_workspace()









Declared in: interface/InterfaceDefs.h

These functions set and return the active workspace, the one that's
currently displayed on-screen. The workspace is identified by an index,
0-based.

See also: {cpp:func}`BWindow::WorkspaceActivated`

## bitmaps_support_space()





Declared in:  interface/InterfaceDefs.h

Returns {cpp:expr}`true` if {cpp:class}`BBitmap`s can contain graphics in
the specified color space, or {cpp:expr}`false` if not.

The {htype}`uint32` pointed to by {hparam}`supportFlags` will be set to a
bit field of flags, further describing the support for the specified color
space by the {cpp:class}`BBitmap`s class. The flags are:

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
	- {cpp:enumerator}`B_VIEWS_SUPPORT_DRAW_BITMAP`
	- {cpp:func}`BView::DrawBitmap` supports drawing {cpp:class}`BBitmap`s of
		the specified color space.
-
	- {cpp:enumerator}`B_BITMAPS_SUPPORT_ATTACHED_VIEWS`
	- Indicates that {cpp:class}`BBitmap`s in the specified color space support
		attached {cpp:class}`BView`s.

:::

## get_deskbar_frame()





Declared in:  interface/InterfaceDefs.h

Writes the screen coordinates of the current frame of the Deskbar window
into {hparam}`frame`. Returns {cpp:enumerator}`B_OK` on success or an
appropriate error code on failure.

## get_font_family(), count_font_families(), get_font_style(), count_font_styles()

















Declared in:  interface/Font.h

These functions are used in combination to get the names of the families
and styles of all installed fonts. For example:

:::{code} cpp
int32 numFamilies = count_font_families();
for ( int32 i = 0; i < numFamilies; i++ ) {
   font_family family;
   uint32 flags;
   if ( get_font_family(i, &family, &flags) == B_OK ) {
      . . .
      int32 numStyles = count_font_styles(family);
      for ( int32 j = 0; j < numStyles; j++ ) {
         font_style style;
         if ( get_font_style(family, j, &style, &flags) == B_OK ) {
            . . .
         }
      }
   }
}
:::

get_font_family() reads one family name from the list of installed fonts,
the name at {hparam}`index`, and copies it into the {hparam}`family`
buffer; count_font_families() returns the number of font families currently
installed. Similarly, get_font_style() reads the name of the style at
{hparam}`index` and copies into the {hparam}`style` buffer. Since each
family can have a different set of styles, a family name must be passed to
get_font_style(); count_font_styles() returns the number of styles for the
particular {hparam}`family`. Family and style names can be up to 64 bytes
long including a null terminator. Indices begin at 0.

The names of installed font families and styles are not indexed in any
particular order. You might want to alphabetize them before displaying them
to the user in a menu or list.

If you pass a {hparam}`flags` argument to get_font_family() and
get_font_style(), they will place a mask with useful information about the
particular family or style in the variable that the argument refers to.
Currently there are just two flags:

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
	- {cpp:enumerator}`B_IS_FIXED`
	- Indicates that the font is a nonproportional, or fixed-width, font—one for
		which all characters have the same width.
-
	- {cpp:enumerator}`B_HAS_TUNED_FONT`
	- Indicates that the family or style has versions of the font especially
		adapted or "tuned" for on-screen display.

:::

If neither flag applies, the variable that {hparam}`flags` points to will
be set to 0.

If you find a family and style that has a tuned font, you can set a
{cpp:class}`BFont` object to that family and style, then call the object's
{cpp:func}`GetTunedInfo() <BFont::GetTunedInfo>` function to get details
about exactly which combination of font properties (for example, which font
sizes) have tuned counterparts. If you set a {cpp:class}`BFont` so that it
has those properties and make it a {cpp:class}`BView`'s current font, the
tuned version will be used when the {cpp:class}`BView` draws to the screen.

It's possible for the user to install or remove fonts while the
application is running. However, unless {ref}`update_font_families()` has
been called to get the updated list, {hmethod}`get_font_family()` will
provide information on the same set of fonts each time it's called. The
list isn't automatically updated.

See also: {ref}`update_font_families()`, {cpp:func}`BView::SetFont`,
{cpp:func}`BFont::SetFamilyAndStyle`

## get_pixel_size_for()





Declared in:  interface/GraphicsDefs.h

Given the specified color space, returns information about pixel and row
alignment for that color space.

## idle_time()





Declared in:  interface/InterfaceDefs.h

Returns the number of microseconds since the user last manipulated the
mouse or keyboard. This information isn't specific to a particular
application; idle_time() tells you when the user last directed an action at
any application, not just yours.

## keyboard_navigation_color()



Declared in: interface/InterfaceDefs.h



Returns the color that should be used to mark the {cpp:class}`BView`
that's currently in focus, when the user can change the focus from the
keyboard. The keyboard navigation color is typically used to underline the
labels of control devices and to outline text fields where the user can
type.

## run_add_printer_panel(), run_select_printer_panel()









Declared in: interface/InterfaceDefs.h

These two functions have the Print Server place panels on-screen where the
user can set up a printer and choose which printer to use.
run_add_printer_panel() displays a panel that informs the server about a
new printer. run_select_printer_panel() displays a panel that lists all
known printers and lets the user select one.

See also: The {cpp:class}`BPrintJob` class

## set_menu_info(), get_menu_info()









Declared in: interface/Menu.h

These functions set and get the user's preferences for how menus should
look and work. User's express their preferences with the Menu application,
which calls set_menu_info(). get_menu_info() writes the current preferences
into the {htype}`menu_info` structure that into refers to. This structure
contains the following fields:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Field

	- Description

-
	- floatfont_size
	- The size of the font that will be used to display menu items.
-
	- font_namefont
	- The name of the font that's used to display menu items.
-
	- rgb_colorbackground_color
	- The background color of the menu.
-
	- int32separator
	- The style of horizontal line that separates groups of items in a menu. The
		value is an index ranging from 0 through 2; there are three possible
		separators.
-
	- boolclick_to_open
	- Whether it's possible to open a menu by clicking in the item that controls
		it. The default value is true.
-
	- booltriggers_always_shown
	- Whether trigger characters are always marked in menus and menu bars,
		regardless of whether the menu hierarchy is the target for keyboard
		actions. The default value is false.

:::

(At present, both functions always return {cpp:enumerator}`B_OK`.)

See also: The {cpp:class}`BMenu` class

## set_screen_space()





Declared in: interface/InterfaceDefs.h

Changes the configuration of the screen—its depth and dimensions—to match
the values specified in the {hparam}`space` constant, which can be any of
the following:

-   {cpp:enumerator}`B_8_BIT_640x400`

-   {cpp:enumerator}`B_8_BIT_640x480`

-   {cpp:enumerator}`B_8_BIT_800x600`

-   {cpp:enumerator}`B_8_BIT_1024x768`

-   {cpp:enumerator}`B_8_BIT_1152x900`

-   {cpp:enumerator}`B_8_BIT_1280x1024`

-   {cpp:enumerator}`B_8_BIT_1600x1200`

-   {cpp:enumerator}`B_15_BIT_640x480`

-   {cpp:enumerator}`B_15_BIT_800x600`

-   {cpp:enumerator}`B_15_BIT_1024x768`

-   {cpp:enumerator}`B_15_BIT_1152x900`

-   {cpp:enumerator}`B_15_BIT_1280x1024`

-   {cpp:enumerator}`B_15_BIT_1600x1200`

-   {cpp:enumerator}`B_16_BIT_640x480`

-   {cpp:enumerator}`B_16_BIT_800x600`

-   {cpp:enumerator}`B_16_BIT_1024x768`

-   {cpp:enumerator}`B_16_BIT_1152x900`

-   {cpp:enumerator}`B_16_BIT_1280x1024`

-   {cpp:enumerator}`B_16_BIT_1600x1200`

-   {cpp:enumerator}`B_32_BIT_640x480`

-   {cpp:enumerator}`B_32_BIT_800x600`

-   {cpp:enumerator}`B_32_BIT_1024x768`

-   {cpp:enumerator}`B_32_BIT_1152x900`

-   {cpp:enumerator}`B_32_BIT_1280x1024`

-   {cpp:enumerator}`B_32_BIT_1600x1200`

The first part of the constant designates the screen depth and color
space. {cpp:enumerator}`B_8_BIT…` refers to the {cpp:enumerator}`B_CMAP8`
color space. The other values correspond to the {cpp:enumerator}`B_RGB15`,
{cpp:enumerator}`B_RGB16`, and {cpp:enumerator}`B_RGB32` color spaces, as
appropriate. Although constants are defined for 15-bit screen depths, the
operating system currently doesn't support them. The second part of the
constant designates the pixel resolution of the screen. For example,
{cpp:enumerator}`B_32_BIT_1280x1024` means that the frame buffer is 32 bits
deep ({cpp:enumerator}`B_RGB32`) while the screen grid is 1,280 pixels wide
and 1,024 pixels high.

This function affects the screen at {hparam}`index`. Since the BeOS
currently doesn't support more than one screen, the only index that makes
sense is 0.

The change to the screen takes effect immediately. If the
{hparam}`makeDefault` flag is {cpp:expr}`true`, the new configuration also
becomes the default and will be used the next time the machine is turned
on. If {hparam}`makeDefault` is {cpp:expr}`false`, the configuration is in
effect for the current session only.

Since not all configurations are possible for all graphics cards,
set_screen_space() can fail. It returns {cpp:enumerator}`B_OK` if
successful, and {cpp:enumerator}`B_ERROR` if not.

This function is designed for preferences applications—like the Screen
application—that permit users to make system-wide choices about the screen.
Other applications should respect those choices and refrain from modifying
them.

The current screen configuration can be obtained from the
{cpp:class}`BScreen` object.

See also: {cpp:func}`BWindow::ScreenChanged`, {ref}`The Game Kit` chapter

## set_scroll_bar_info(), get_scroll_bar_info()









Declared in: interface/InterfaceDefs.h

These functions set and report preferences that the
{cpp:class}`BScrollBar` class uses when it creates a new scroll bar.
set_scroll_bar_info() reads the values contained in the
{htype}`scroll_bar_info` structure that {hparam}`info` refers to and sets
the system-wide preferences accordingly; get_scroll_bar_info() writes the
current preferences into the structure provided.

The {htype}`scroll_bar_info` structure contains the following fields:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Field

	- Description

-
	- boolproportional
	- {cpp:expr}`true` if scroll bars should have a knob that grows and shrinks
		to show what proportion of the document is currently visible on-screen, and
		{cpp:expr}`false` if not. Scroll knobs are proportional by default.
-
	- booldouble_arrows
	- {cpp:expr}`true` if a set of double arrows (for scrolling in both
		directions) should appear at each end of the scroll bar, or
		{cpp:expr}`false` if only single arrows (for scrolling in one direction
		only) should be used. Double arrows are the default.
-
	- int32knob
	- An index that picks the pattern for the knob. Only values of 0, 1, and 2
		are currently valid. The patterns can be seen in the ScrollBar preferences
		application. The pattern at index 1 is the default.
-
	- int32min_knob_size
	- The length of the scroll knob, in pixels. This is the minimum size for a
		proportional knob and the fixed size for one that's not proportional. The
		default is 15.

:::

The user can set these preferences with the ScrollBar application.
Applications can call get_scroll_bar_info() to find out what choices the
user made, but should refrain from calling set_scroll_bar_info(). That
function is desigined for utilities, like the ScrollBar application, that
enable users to set preferences that are respected system-wide.

If successful, these functions return {cpp:enumerator}`B_OK`; if not, they
return {cpp:enumerator}`B_ERROR`.

See also: The {cpp:class}`BScrollBar` class

## set_workspace_count(), count_workspaces()









Declared in: interface/InterfaceDefs.h

These functions set and return the number of workspaces the user has
available. There can be as many as 32 workspaces and as few as 1. The
choice of how many there should be is usually left to the user and the
Workspaces application.

See also: {cpp:func}`activate_workspace() <activate::workspace>`

## system_colors()





Declared in: interface/InterfaceDefs.h

Returns a pointer to the system color map. This function duplicates the
{cpp:class}`BScreen` {cpp:func}`ColorMap() <BScreen::ColorMap>` function,
but it permits software that isn't concerned about the on-screen display to
get the color map without referring to a particular screen. (Actually it
returns the color map for the main screen.)

The {htype}`color_map` structure returned by this function belongs to the
operating system.

## tint_color()





Declared in:  interface/InterfaceDefs.h

tint_color() lightens or darkens the color {hparam}`color` by the
{hparam}`tint` amount.

Tints less than 1.0 lighten the color and tints greater than 1.0 darken
it.

Various {hparam}`tint` constants are defined by the Interface Kit as seen
{cpp:func}`here <tint::color>`.

## ui_color()





Declared in:  interface/InterfaceDefs.h

Converts the supplied {cpp:func}`color_which <color::which>` constant
{hparam}`which` to the corresponding {cpp:func}`rgb_color <rgb::color>` for
the specified user interface element.

## update_font_families()





Declared in:  interface/Font.h

Updates the list of installed fonts, so that it reflects any that have
been added or removed since the last time the list was updated. Until the
list is updated, {ref}`get_font_family()` operates assuming the set of
fonts that were installed when the application started up. If the list is
unchanged since the last update (or since startup), this function returns
{cpp:expr}`false`; if a font has been installed or an installed font has
been removed, it returns {cpp:expr}`true`.

If the {hparam}`checkOnly` flag is {cpp:expr}`true`,
{ref}`get_font_family()` only reports whether the list has changed; it
doesn't modify the current list. If the flag is {cpp:expr}`false`, it
contacts the Application Server to get the updated list, a much more
expensive operation.
