# BMediaTheme
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BMediaTheme::BMediaTheme(const char* name, const char* info, const entry_ref* addOn = NULL, int32 themeID = 0)
:::
The {hclass}`BMediaTheme` constructor initializes
the theme so it can be used by the system or by an application. The
user-readable theme name is passed as the {hparam}`name`
argument, and some longer description of the theme in
{hparam}`info`.
The {hparam}`name` and
{hparam}`info` strings are copied; you can dispose of the
original strings if you wish. Both strings should be human-readable, as
they may be presented to the user in a user interface for selecting a theme
to be used.
If the theme lives in an add-on on disk, specify the
entry_ref of the add-on file in
{hparam}`addOn` and the ID assigned to the theme by its
add-on in {hparam}`themeID`.
::::

::::{abi-group}

:::{cpp:function} virtual BMediaTheme::BMediaTheme()
:::
Disposes of memory used by the theme. If you create a theme, be sure the
destructor frees any memory allocated by the theme.
::::

## Member Functions
::::{abi-group}

:::{cpp:function} virtual BBitmap* BMediaTheme::BackgroundBitmapFor(bg_kind backgroundKind)
:::
Returns the
{cpp:class}`BBitmap`
that should be used as the background for the
specified type of user interface object. Possible values for
{hparam}`backgroundKind` are detailed in
bg_kind.
::::

::::{abi-group}

:::{cpp:function} virtual rgb_color BMediaTheme::BackgroundBitmapFor(bg_kind backgroundKind)
:::
Returns the
{cpp:func}`~rgb::color`
that should be used as the background for the
specified type of user interface object. Possible values for
{hparam}`backgroundKind` are detailed in
bg_kind.
::::

::::{abi-group}

:::{cpp:function} virtual rgb_color BMediaTheme::BackgroundBitmapFor(fg_kind foregroundKind)
:::
Returns the
{cpp:func}`~rgb::color`
that should be used as the foreground for the
specified type of user interface object. Possible values for
foregroundKind are detailed in
fg_kind.
::::

::::{abi-group}

:::{cpp:function} bool BMediaTheme::GetRef(entry_ref* outRef)
:::
Sets {hparam}`outRef` to be a reference to the add-on file from which the theme was
loaded and returns {cpp:enum}`true`. If the theme wasn't loaded from an add-on, this
function returns {cpp:enum}`false`.
::::

::::{abi-group}

:::{cpp:function} int32 BMediaTheme::ID()
:::
Returns the theme's ID, as assigned by the add-on in which the theme
resides. The ID is unique only within that add-on.
If the theme isn't in an add-on, 0 is returned.
::::

::::{abi-group}

:::{cpp:function} const char* BMediaTheme::Info()
:::
Returns the user-readable long description of the theme, as specified
when the theme was created.
::::

::::{abi-group}

:::{cpp:function} virtual BControl* BMediaTheme::MakeControlFor(BParameter* parameter) = 0
:::
If you create your own theme, your implementation of this function should
return an appropriate
{cpp:class}`BControl`
to operate on the specified
{cpp:class}`BParameter`.
Applications that want to use the theme to create the controls, but
handle their layout themselves, can call this function for each parameter
in the web, rather than rely upon
{cpp:func}`~BMediaTheme::ViewFor`.
However, if an application uses {hmethod}`MakeControlFor()`
to create individual controls rather than letting
{cpp:func}`~BMediaTheme::ViewFor`
set up the entire view, the application assumes responsibility
for setting the control's value in response to value change messages.
If you want the control to send a specific message when invoked, you
should call
{cpp:func}`BInvoker::SetMessage`
on it.
::::

::::{abi-group}

:::{cpp:function} static BControl* BMediaTheme::MakeFallbackViewFor(BParameter* control)
:::
If you're implementing your own theme, and for whatever reason you want a
{cpp:class}`BParameter`
to use the standard system theme's
{cpp:class}`BControl`, call
{hmethod}`MakeFallbackViewFor()` to obtain that
{cpp:class}`BControl`.
This can be used if your theme is only intended to augment certain
controls, or if you receive a
{cpp:class}`BParameter`
you don't know anything about.
:::{admonition} Note
:class: note
Your
{cpp:func}`~BMediaTheme::MakeControlFor`
implementation should always call
{hmethod}`MakeFallbackViewFor()` if it's asked to create a
{cpp:class}`BControl` for a
{cpp:class}`BParameter`
it doesn't understand. This way, all
{cpp:class}`BParameter`s
will get some form of user interface, even if your theme doesn't specifically know how to
handle some of them. This will let your theme remain compatible with
future versions of the BeOS.
:::
::::

::::{abi-group}

:::{cpp:function} virtual BView* BMediaTheme::MakeViewFor(BParameterWeb* web, const BRect* hintRect = NULL) = 0
:::
Given the specified
{cpp:class}`BParameterWeb` and
{hparam}`hintRect`, your implementation of
this function should construct a
{cpp:class}`BView`
that contains the
{cpp:class}`BControl`s
for manipulating the
{cpp:class}`BParameter`s
in the web. The {hparam}`hintRect` is an area the
caller thinks is appropriate for you to fill with your
{cpp:class}`BView`;
your theme should try to stay within that rectangle if possible.
The web returned by this function belongs to the theme; applications
shouldn't delete it (a properly-written theme will automatically dispose
of the web when the view is closed).
This function is called by
{cpp:func}`~BMediaTheme::ViewFor`.
::::

::::{abi-group}

:::{cpp:function} static BMediaTheme* BMediaTheme::PreferredTheme()
:::
:::{cpp:function} static status_t BMediaTheme::SetPreferredTheme(BMediaTheme* newPreferredTheme)
:::
{hmethod}`PreferredTheme()` returns the current preferred theme;
{hmethod}`SetPreferredTheme()`
changes the preferred theme to the theme specified by
{hparam}`newPreferredTheme`.
The preferred theme is the theme that will be used for creating node
controlling user interfaces if no specific theme is requested when the
interface is created.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`
	- The preferred theme was changed without error.
-
	- {cpp:enum}`B_NOT_ALLOWED`
	- Access to the settings file denied.
-
	- Other errors.
	- Directory and file I/O errors may occur while updating the settings file.
:::
See also:
{cpp:func}`~BMediaTheme::ViewFor`,
{cpp:func}`~BMediaTheme::MakeViewFor`
::::

::::{abi-group}

:::{cpp:function} const char* BMediaTheme::Name()
:::
Returns the user-readable name of the theme, as specified when the theme
was created.
::::

::::{abi-group}

:::{cpp:function} static BView* BMediaTheme::ViewFor(BParameterWeb* web, const BRect* hintRect = NULL, BMediaTheme* usingTheme = NULL)
:::
Given a
{cpp:class}`BParameterWeb`
web, typically returned by
{cpp:func}`BMediaRoster::GetParameterWebFor`,
this function creates a
{cpp:class}`BView`
suitable for adding to a
{cpp:class}`BWindow`
to allow the user to configure the node the web
describes, including a diagram indicating the data flow path through the
node, and controls to let the user configure each control point.
:::{admonition} Note
:class: note
This function is the public interface for creating a view for
configuring a node (the
{cpp:func}`~BMediaTheme::MakeViewFor`
function is the hook you override
if you're implementing your own theme).
:::
The returned view is created using the theme specified by {hparam}`usingTheme`; if
this argument is {cpp:enum}`NULL`, the preferred theme is used. The {hparam}`hintRect`
parameter specifies the rectangle the view should try to occupy, and is
passed to {hmethod}`MakeViewFor()`.
::::

## Global C Functions
::::{abi-group}


:::{cpp:function} status_t BMediaTheme::get_theme_at(int32 n, const char** outName, int32* outID)
:::
This function is called after the theme add-on is loaded, to
determine what themes are available in the add-on. It's called repeatedly,
with successively-higher values of {hparam}`n`, until it
returns an error.
Your add-on's implementation of this function should set
{hparam}`outName` to point to the
{hparam}`n`th theme's name,
{hparam}`outInfo` to point to information describing the
{hparam}`n`th theme, and {hparam}`outID`
should be set to the {hparam}`n`th theme's ID number,
which used internally by your add-on to distinguish among the themes it
supports.
::::

::::{abi-group}


:::{cpp:function} BMediaTheme* BMediaTheme::make_theme(int32 themeID, image_id imageID)
:::
If you're writing a theme to be loaded from an add-on file, you
must implement make_theme() to create a
{hclass}`BMediaTheme` for the specified
{hparam}`themeID`. {hparam}`imageID` is
the image_id of the add-on in which the theme is
located.
::::

## Constants
::::{abi-group}

:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_GENERAL_BG`
	- Used when nothing else is applicable.
-
	- {cpp:enum}`B_SETTINGS_BG`
	- Used for panels or windows full of controls.
-
	- {cpp:enum}`B_PRESENTATION_BG`
	- Used for windows that present actual media content.
-
	- {cpp:enum}`B_EDIT_BG`
	- Used for windows that edit media content.
-
	- {cpp:enum}`B_CONTROL_BG`
	- Used for drawing controls.
-
	- {cpp:enum}`B_HILITE_BG`
	- Used when highlighting information, such as selected media data.
:::
These constants identify parts of the user interface that a theme can
customize the appearance of by altering the color or bitmap that's used
in the background for various user interface elements. They're used when
calling
{cpp:func}`~BMediaTheme::BackgroundBitmapFor` and
{cpp:func}`~BMediaTheme::BackgroundColorFor`.
For example, the {cpp:enum}`B_PRESENTATION_BG` color
and/or bitmap would be used as the background of a window in which an
oscilloscope display shows the waveform of a sound wave being played back,
and a window used for editing the waveform would have its' background in
the color specified by {cpp:enum}`B_EDIT_BG` (or using the
bitmap specified by {cpp:enum}`B_EDIT_BG`, if one exists),
except for the part of the wave that's selected by the user, which would
have the background color or bitmap specified by
{cpp:enum}`B_HILITE_BG`.
::::

::::{abi-group}

:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_GENERAL_FG`
	- Used when nothing else is applicable.
-
	- {cpp:enum}`B_SETTINGS_FG`
	- Used for panels or windows full of controls.
-
	- {cpp:enum}`B_PRESENTATION_FG`
	- Used for windows that present actual media content.
-
	- {cpp:enum}`B_EDIT_FG`
	- Used for windows that edit media content.
-
	- {cpp:enum}`B_CONTROL_FG`
	- Used for drawing controls.
-
	- {cpp:enum}`B_HILITE_FG`
	- Used when highlighting information, such as selected media data.
:::
The foreground color kinds are used when calling
{cpp:func}`~BMediaTheme::ForegroundColorFor`
to obtain the color to use when drawing the foreground portions of various
interface elements.
::::
