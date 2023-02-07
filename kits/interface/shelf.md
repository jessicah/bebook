# BShelf
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BShelf::BShelf(BView* view, bool allowsDragging = true, const char* name = NULL)
:::
:::{cpp:function} BShelf::BShelf(const entry_ref* ref, BView* view, bool allowsDragging = true, const char* name = NULL)
:::
:::{cpp:function} BShelf::BShelf(BDataIO* stream, BView* view, bool allowsDragging = true, const char* name = NULL)
:::

Initializes the {hclass}`BShelf` object so that it serves a
container view. The versions that accept an entry_ref or {cpp:class}`BDataIO` argument prime the
shelf so that it (initially) contains the replicants that are archived in
the referred to file or stream using
{cpp:func}`~BShelf::Save`. The
{hparam}`ref`/{hparam}`stream` argument is also
used as the archival repository when you tell your
{hclass}`BShelf` to
{cpp:func}`~BShelf::Save` itself.

If the {hparam}`allowsDragging` flag is {cpp:enum}`true`, the user will be able to drag
replicant view within the container's bounds. If the flag is {cpp:enum}`false`,
dropped views stay where they're first put.

{hparam}`name` is the {hclass}`BShelf`'s handler name. The name can be important: It's
compared to the replicant's shelf_type field, as explained in
{cpp:func}`~BShelf::AddReplicant`.

:::{admonition} Warning
:class: warning
There's an archive-accepting version of the {hclass}`BShelf` constructor declared
in Shelf.h. Don't use it.
:::
::::

::::{abi-group}

:::{cpp:function} virtual BShelf::~BShelf()
:::

The destructor calls {cpp:func}`~BShelf::Save`,
and then frees the object.

::::

## Hook Functions
::::{abi-group}

:::{cpp:function} virtual BPoint BShelf::AdjustReplicantBy(BRect destRect, BMessage* archive) const
:::

This hook function is invoked automatically when a replicant is dropped
on the {hclass}`BShelf`. It gives the shelf a chance to fine-tune the placement of
the {hclass}`BDragger` and its target view.

{hparam}`destRect` is the rectangle (in the container view's coordinates) in which
the dropped replicant is about to be drawn. Exactly what the rectangle
means depends on the relationship between the dragger and its target:

- If the dragger is the target's parent, then {hparam}`destRect` encloses the {cpp:class}`BDragger`'s frame.
- Otherwise (if the target is the parent, or if the two views are siblings), {hparam}`destRect` encloses the target's frame. Note that in the case of siblings, the {cpp:class}`BDragger`'s frame isn't included in the rectangle.

{hparam}`archive` is the archive message that was dropped on the shelf.

The {cpp:class}`BPoint` that this
function returns offsets (is added into) the
location of the replicant. If you don't want to move the replicant,
return {cpp:class}`BPoint`(0, 0).
Note that the {cpp:class}`BDragger`
and the view are both moved by this offset, even in the case where
{hparam}`destRect` doesn't include the
dragger's frame.

This function ignores the "allows dragging" flag given in the {hclass}`BShelf`
constructor. In other words, you can adjust a replicant's placement
through this function even if the {hclass}`BShelf` doesn't otherwise allow dragging.

::::

::::{abi-group}

:::{cpp:function} virtual bool BShelf::CanAcceptReplicantMessage(BMessage* archive) const
:::
:::{cpp:function} virtual bool BShelf::CanAcceptReplicantView(BRect destRect, BView* view, BMessage* archive) const
:::

These hook functions are invoked from within
{cpp:func}`~BShelf::AddReplicant` whenever a
replicant is dropped on the {hclass}`BShelf`. You can implement these functions to
reject unwanted replicants.

{hmethod}`CanAcceptReplicantMessage()` is called first; the argument is the archive
that (should) contain the replicated view. If you don't like the look of
the archive, return {cpp:enum}`false` and the message will be thrown away. Note that
you shouldn't return {cpp:enum}`false` if the archive doesn't seem to be in the
correct form (specifically, if it doesn't contain any views). Rejection
of such messages is handled more elegantly (and after this function is
invoked) by the {cpp:func}`~BShelf::AddReplicant` function.

{hmethod}`CanAcceptReplicantView()` is invoked after the message has been
unarchived. {hparam}`destRect` is the rectangle that the replicant will occupy in
the {hclass}`BShelf`'s container view's coordinates. {hparam}`view` is the replicated view
itself. {hparam}`archive` is the original message.

If either function returns {cpp:enum}`false`, the replicant is rejected and the
message is thrown away (it isn't passed on to another handler). A return
of {cpp:enum}`true` does the obvious thing.

::::

::::{abi-group}

:::{cpp:function} virtual void BShelf::ReplicantDeleted(int32 index, const BMessage* archive, const BView* view)
:::

This hook function is invoked from within
{cpp:func}`~BShelf::DeleteReplicant` to indicate a
replicant has been deleted from the {hclass}`BShelf`. It is called after the view
has been removed from the shelf with the {hparam}`index` of the replicant in the
shelf, its {hparam}`archive` message, and the detached {hparam}`view`.

::::

## Member Functions
::::{abi-group}

:::{cpp:function} status_t BShelf::AddReplicant(BMessage* archive, BPoint point)
:::

This function is invoked automatically when a replicant is dropped on the
{hclass}`BShelf`. The {hparam}`archive` message contains the
{cpp:class}`BDragger` archive that's being
dropped; {hparam}`point` is where, within the container view's bounds, the message
was dropped. The function goes through these steps to reject and adjust
the replicant:

- First, it invokes the {cpp:func}`~BShelf::CanAcceptReplicantMessage` hook function. If the hook returns {cpp:enum}`false`, then {hmethod}`AddReplicant()` doesn't add the replicant.
- Next, it looks for a shelf_type string field in the {cpp:class}`BMessage`. If it finds one and the value of the field doesn't match the {hclass}`BShelf`'s name, the replicant is rejected.
- If type enforcement is {cpp:enum}`true` (see {cpp:func}`~BShelf::SetTypeEnforced`) and the shelf has a name, then the {cpp:class}`BMessage` must have a shelf_type string and this string must match the shelf name. Otherwise, the replicant is rejected.There's no specific API for adding the shelf_type field to a view. If you want to configure your views to accept only certain {hclass}`BShelf` objects, you have to add the field directly as part of the view's {cpp:func}`~BView::Archive` implementation.
- The archive message is then unarchived (the replicant is instantiated). If the archive doesn't contain a {cpp:class}`BView`, the message is passed on to another handler ({cpp:enum}`B_DISPATCH_MESSAGE` is returned).
- {cpp:func}`~BShelf::CanAcceptReplicantView` hook function is called next (with a return of {cpp:enum}`false` meaning rejection).
- Finally, {cpp:func}`~BShelf::AdjustReplicantBy` is called, and the replicant is drawn in the container view.

Except in the case of a no-view archive, {hmethod}`AddReplicant()` returns
{cpp:enum}`B_SKIP_MESSAGE`.

:::{admonition} Note
:class: note
If you want the ensure that the replicant is unique within the
container view, add a "be:unique_replicant" entry of type {cpp:enum}`B_BOOL_TYPE` to
the archive with the value {cpp:enum}`true`.
:::

It's possible to archive a {hclass}`BDragger` and call this function yourself,
although that's not its expected use.

::::

::::{abi-group}

:::{admonition} Warning
:class: warning
{hmethod}`Archive()` is currently a no-op that
returns {cpp:enum}`B_ERROR`. You can't archive
a {hclass}`BShelf`. If you want to archive something, archive the shelf's contents
by calling {cpp:func}`~BShelf::Save`.
:::
::::

::::{abi-group}

:::{cpp:function} int32 BShelf::CountReplicants() const
:::

Returns the number of replicants attached to the shelf.

::::

::::{abi-group}

:::{cpp:function} status_t BShelf::DeleteReplicant(BView* replicant_view)
:::
:::{cpp:function} status_t BShelf::DeleteReplicant(const BMessage* archive)
:::
:::{cpp:function} status_t BShelf::DeleteReplicant(uint32 uid)
:::

Removes the specified replicant from the shelf. It identifies replicants
by either a view, a replicant message, or a unique id.

::::

::::{abi-group}

:::{cpp:function} int32 BShelf::IndexOf(const BView* replicant_view) const
:::
:::{cpp:function} int32 BShelf::IndexOf(const BMessage* archive) const
:::
:::{cpp:function} int32 BShelf::IndexOf(uint32 uid) const
:::
:::{cpp:function} BMessage* BShelf::ReplicantAt(int32 index, BView** view = NULL, uint32* view = NULL, status_t err = NULL) const
:::

{hmethod}`IndexOf()` returns the index of a specified replicant in the shelf, or -1
if no such replicant exists. It accepts either a view, a replicant
message, or a unique id as identifiers.

{hmethod}`ReplicantAt()` returns information about a replicant in a shelf given its
{hparam}`index` (as returned by {hmethod}`IndexOf()`). It returns the
{cpp:class}`BMessage` archive of the
replicant or {cpp:enum}`NULL` if the index is invalid. It returns the {hparam}`view` of the
replicant as well as its {hparam}`uid`, if these parameters are non-{cpp:enum}`NULL`. It
returns an error message in {hparam}`err` if there was an error in initializing the
given replicant.

::::

::::{abi-group}

:::{cpp:function} status_t BShelf::Save()
:::
:::{cpp:function} BDataIO* BShelf::SaveLocation(entry_ref* ref) const
:::
:::{cpp:function} status_t BShelf::SetSaveLocation(BDataIO* data_io)
:::
:::{cpp:function} status_t BShelf::SetSaveLocation(const entry_ref* ref)
:::
:::{cpp:function} virtual void BShelf::SetDirty(bool flag)
:::
:::{cpp:function} bool BShelf::IsDirty()
:::

Writes the shelf's contents (the replicants that it contains) as an archive
to the entry_ref or {cpp:class}`BDataIO` object that was
specified in the constructor. You can also set the location where the shelf
is saved with {hmethod}`SetSaveLocation()` and fetch it with
{hmethod}`SaveLocation()`. The entry_ref is
stored in {hparam}`ref` (if ref is
non-{cpp:enum}`NULL`) and the {cpp:class}`BDataIO` the shelf will be
written to is returned. If the shelf will be written to an
entry_ref that is not a {cpp:class}`BDataIO`,
{hmethod}`SaveLocation()` returns {cpp:enum}`NULL`.

By default, the save is only performed if the object's "dirty" flag is
set—in other words, if it has changed since it was last written.
You can force set the dirty flag by calling {hmethod}`SetDirty()`.

{hmethod}`IsDirty()` returns the current state of the "dirty" flag.

::::

::::{abi-group}

:::{cpp:function} void BShelf::SetAllowsDragging(bool state)
:::
:::{cpp:function} bool BShelf::AllowsDragging() const
:::

{hmethod}`SetAllowsDragging()` determines whether the {hclass}`BShelf` accepts replicants
dragged into the view by the user. {hmethod}`AllowsDragging()` returns whether the
{hclass}`BShelf` accepts replicants dragged by the user into the container view's
frame

::::

::::{abi-group}

:::{cpp:function} void BShelf::SetAllowsZombies(bool state)
:::
:::{cpp:function} bool BShelf::AllowsZombies() const
:::
:::{cpp:function} void BShelf::SetDisplaysZombies(bool state)
:::
:::{cpp:function} bool BShelf::DisplaysZombies() const
:::

{hmethod}`SetAllowsZombies()` determines whether the
{hclass}`BShelf` accepts zombie views.
{hmethod}`AllowsZombies()` returns whether the
{hclass}`BShelf` accepts zombie views. A zombie view is one
whose associated executable cannot be located.

Similarly, {hmethod}`SetDisplaysZombies()` determines whether
the {hclass}`BShelf` displays zombie views and
{hmethod}`DisplaysZombies()` returns whether the
{hclass}`BShelf` displays zombie views.

::::

::::{abi-group}

:::{cpp:function} void BShelf::SetTypeEnforced(bool state)
:::
:::{cpp:function} bool BShelf::IsTypeEnforced() const
:::

These two methods set and return the type enforcement flag. When it is
{cpp:enum}`true`, the shelf compares its name to the shelf_type field of any
dropped messages. The replicant is accepted only if the two match. If the
dropped message does not have a shelf_type field, then it is rejected.
Type enforcement is {cpp:enum}`false` by default.

::::

## Static Functions
::::{abi-group}

:::{cpp:function} static BArchivable* BShelf::Instantiate(BMessage* archive)
:::
:::{admonition} Warning
:class: warning
{hmethod}`Instantiate()` is currently a no-op that
returns {cpp:enum}`NULL`. You can't archive a
{hclass}`BShelf`. If you want to archive something, archive
the shelf's contents by calling
{cpp:func}`~BShelf::Save`.
:::
::::

## Scripting Support
::::{abi-group}

The "Replicant" property provides access to the replicants contained in a
{hclass}`BShelf`. It also allows you to manipulate the replicants themselves by
forwarding certain messages to a "suite/vnd.Be-replicant" interface. This
interface consists of the following messages:

MessageSpecifierDescriptionB_COUNT_PROPERTIESB_DIRECT_SPECIFIERReturns number of replicants in the shelf.B_CREATE_PROPERTIESB_DIRECT_SPECIFIERAdds the archived replicant in the BMessage "data" to the view at the BPoint in "location."B_DELETE_PROPERTYB_INDEX_SPECIFIER, B_REVERSE_INDEX_SPECIFIER, B_NAME_SPECIFIER, B_ID_SPECIFIERRemoves the specified replicant from the shelf.B_GET_PROPERTYB_INDEX_SPECIFIER, B_REVERSE_INDEX_SPECIFIER, B_NAME_SPECIFIER, B_ID_SPECIFIERArchives the specified replicant into a BMessage in "result."anything elseB_INDEX_SPECIFIER, B_REVERSE_INDEX_SPECIFIER, B_NAME_SPECIFIER, B_ID_SPECIFIERDirects the scripting message to the replicant interface "suite/vnd.Be-replicant" (described below), first popping the current specifier off the stack.
::::

::::{abi-group}

The replicant ID

MessageSpecifierDescriptionB_GET_PROPERTYB_DIRECT_SPECIFIERReturns the replicant ID.
::::

::::{abi-group}

The name of the replicant view

MessageSpecifierDescriptionB_GET_PROPERTYB_DIRECT_SPECIFIERReturns the name of the replicant view.
::::

::::{abi-group}

The replicant add-on MIME signature

MessageSpecifierDescriptionB_GET_PROPERTYB_DIRECT_SPECIFIERReturns the signature of the add-on containing the code for the replicant.
::::

::::{abi-group}

The supported scripting suites

MessageSpecifierDescriptionB_GET_PROPERTYB_DIRECT_SPECIFIERReturns "suite/vnd.Be-replicant" in "suites" and a flattened BPropertyInfo describing the scripting suite in "messages."
::::

::::{abi-group}

Redirects messages to the replicant view

MessageSpecifierDescriptionanyB_DIRECT_SPECIFIERDirects the scripting message to the replicant view, first popping the current specifier off the specifier stack.
::::
