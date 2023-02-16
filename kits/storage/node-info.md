:::{cpp:class} BNodeInfo
:::

# BNodeInfo

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BNodeInfo::BNodeInfo()
:::

:::{cpp:function} BNodeInfo::BNodeInfo(BNode* node)
:::

The default constructor creates a new, uninitialized {hclass}`BNodeInfo`
object. To initialize you have to follow this construction with a call to
{cpp:func}`SetTo() <BNodeInfo::SetTo>`.

The {cpp:class}`BNode` version intializes the {hclass}`BNodeInfo` by
passing the argument to {cpp:func}`SetTo() <BNodeInfo::SetTo>`; see
{cpp:func}`SetTo() <BNodeInfo::SetTo>` for details (and error codes).
::::

::::{abi-group}
:::{cpp:function} BNodeInfo::~BNodeInfo()
:::

Destroys the object. The {cpp:class}`BNode` object that was used to
initialize the object isn't touched.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} status_t BNodeInfo::GetAppHint(entry_ref* app_ref) const
:::

:::{cpp:function} status_t BNodeInfo::SetAppHint(const entry_ref app_ref)
:::

These functions get and set the "app hint" for the node. The app hint is
an {htype}`entry_ref` that identifies the executable that should be used
when launching the node. Of course, the {htype}`entry_ref` may not point to
an application, or it might point to an application with the wrong
signature (and so on)—that's why this is merely a hint.

{hmethod}`GetAppHint()` function initializes the {htype}`entry_ref` to the
hint recorded in the "BEOS:PPATH" attribute of the node; the argument must
be allocated before it's passed in.

{hmethod}`SetAppHint()` stores the path corresponding to the
{htype}`entry_ref` in the "BEOS:PPATH" attribute of the node. Since the
path to the application is stored instead of its {htype}`entry_ref`, the
hint will break if the application is subsequently moved.

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
	- The ref was successfully retrieved or set.
-
	- {cpp:enumerator}`B_ENTRY_NOT_FOUND`.
	- The attribute "BEOS:PPATH" doesn't exist. ({hmethod}`Get`)
-
	- {cpp:enumerator}`B_NOT_ALLOWED`.
	- The node is on a read-only volume. ({hmethod}`Set`)

:::

See Also: {cpp:func}`BMimeType::GetAppHint`
::::

::::{abi-group}
:::{cpp:function} virtual status_t BNodeInfo::GetIcon(BBitmap* icon, icon_size which = B_LARGE_ICON) const
:::

:::{cpp:function} virtual status_t BNodeInfo::SetIcon(const BBitmap* icon, icon_size which = B_LARGE_ICON)
:::

:::{cpp:function} status_t BNodeInfo::GetTrackerIcon(BBitmap* icon, icon_size which = B_LARGE_ICON)
:::

:::{cpp:function} static status_t BNodeInfo::GetTrackerIcon(entry_ref* ref, BBitmap* icon, icon_size which = B_LARGE_ICON)
:::

{hmethod}`GetIcon()` and {hmethod}`SetIcon()` get and set the icon data
that's stored in the node's attributes. You specify which icon you want
(large or small) by passing {cpp:enumerator}`B_LARGE_ICON` or
{cpp:enumerator}`B_MINI_ICON` as the {hparam}`which` argument. The icon is
passed in or returned through the {hparam}`icon` argument. The icon data is
copied out of or into the {cpp:class}`BBitmap` object.

The bitmap (if you're calling {hmethod}`SetIcon()`) or icon (for
{hmethod}`GetIcon()` and {hmethod}`GetTrackerIcon()`) must be the proper
size: 32x32 for the large icon, 16x16 for the small one.

If you want to erase the node's icon, pass {cpp:expr}`NULL` as the
{hparam}`icon` argument to {hmethod}`SetIcon()`.

:::{admonition} Note
:class: note
The icon attributes are stored as "BEOS: L:STD_ICON" (large icon) and
"BEOS: M:STD_ICON" (small, or "mini" icon).
:::

{hmethod}`GetTrackerIcon()` finds the icon that the Tracker uses to
display the node. The `static` version lets you identify the node as an
{htype}`entry_ref`. Both versions follow the same ordered path in trying to
find the icon:

1.    First, it looks in the node's attributes. If the attribute doesn't exist,
it…

2.    …gets the node's preferred app (as a signature), and asks the File Type
database if that signature declares an icon for this node's file type. If
the node doesn't have a preferred app, or if the app doesn't designate an
icon for the node's type, the function…

3.    …asks the File Type database for the icon based on the node's file type.
If still empty-handed, the function…

4.    …asks the File Type database for the preferred app based on the node's
file type, and then asks that app for the icon it uses to display this
node's file type. If still nothing, we…

5.    …quit.

The function doesn't tell you which branch of the path it found the icon
in.

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
	- The icon was found or set.
-
	- {cpp:enumerator}`B_NO_INIT`.
	- The {hclass}`BNodeInfo` is uninitialized.
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- The bitmap or icon wasn't the proper size.
-
	- Attribute errors.
	- See the error codes for {cpp:func}`BNode::ReadAttr` and
		{cpp:func}`BNode::WriteAttr`.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BNodeInfo::GetPreferredApp(char* signature, app_verb verb = B_OPEN) const
:::

:::{cpp:function} status_t BNodeInfo::SetPreferredApp(const char* signature, app_verb verb = B_OPEN)
:::

These functions get and set the node's "preferred app." This is the
application that's used to access the node when, for example, the user
double-clicks the node in a Tracker window.

-   The preferred app is identified by {hparam}`signature`, a MIME string.

-   The {hparam}`app_verb` argument specifies the type of access; currently,
the only {hparam}`app_verb` is {cpp:enumerator}`B_OPEN`.

If a node doesn't have a preferred app, the Tracker looks in the File Type
database for an app that can open the node's file type.

:::{admonition} Note
:class: note


The attribute that stores the preferred app is named "BEOS:PREF_APP".


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
	- {cpp:enumerator}`B_OK`.
	- The preferred app was found or set.
-
	- {cpp:enumerator}`B_NO_INIT`.
	- The {hclass}`BNodeInfo` is uninitialized.
-
	- {cpp:enumerator}`B_BAD_VALUE`
	- ({hmethod}`Set…()` only). The {hparam}`signature` argument is too long
		(greater than {cpp:enumerator}`B_MIME_TYPE_LENGTH`).
-
	- Attribute errors.
	- See the error codes for {cpp:func}`BNode::ReadAttr` and
		{cpp:func}`BNode::WriteAttr`.

:::
::::

::::{abi-group}
:::{cpp:function} virtual status_t BNodeInfo::GetType(char* type) const
:::

:::{cpp:function} virtual status_t BNodeInfo::SetType(const char* type)
:::

These functions get and set the node's file type. The file type, passed in
or returned through {hparam}`type`, is a MIME string.

:::{admonition} Note
:class: note
The attribute that stores the file type is named "BEOS:TYPE".
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
	- {cpp:enumerator}`B_OK`.
	- The type was found or set.
-
	- {cpp:enumerator}`B_NO_INIT`.
	- The {hclass}`BNodeInfo` is uninitialized.
-
	- Attribute errors.
	- See the error codes for {cpp:func}`BNode::ReadAttr` and
		{cpp:func}`BNode::WriteAttr`.

:::
::::

::::{abi-group}
:::{cpp:function} status_t BNodeInfo::InitCheck() const
:::

Returns the status of the most recent initialization.

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
	- The object was successfully initialized.
-
	- {cpp:enumerator}`B_NO_INIT`.
	- The {hclass}`BNodeInfo` is uninitialized.

:::

See {cpp:func}`SetTo() <BNodeInfo::SetTo>` for more error codes.
::::

::::{abi-group}
:::{cpp:function} status_t BNodeInfo::SetTo(BNode* node)
:::

Initializes the {hclass}`BNodeInfo` object by pointing it to
{hparam}`node`, which must be a valid (initialized) {cpp:class}`BNode`
object. The {hclass}`BNodeInfo` maintains its own {cpp:class}`BNode`
pointer: You shouldn't delete {hparam}`node` while the {hclass}`BNodeInfo`
is accessing it; other changes to the {cpp:class}`BNode` are permitted, but
you may want to avoid such antics. Re-initializing a {hclass}`BNodeInfo`
doesn't affect the previous {cpp:class}`BNode` object.

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
	- The object was successfully initialized.
-
	- {cpp:enumerator}`B_BAD_VALUE`.
	- {hparam}`node` is uninitialized.

:::
::::
