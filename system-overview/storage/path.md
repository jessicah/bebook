# BPath

A {hclass}`BPath` object represents an absolute pathname, and provides
some simple path manipulation and querying functions. The primary features
of the class are:

-   It allocates storage for you. When you tell your {hclass}`BPath` object
which pathname you want it to represent, the object allocates storage for
the pathname automatically. When you delete the object, the storage is
freed.

-   It always represents an absolute path. The pathname strings that you use
to initialize a {hclass}`BPath` can be relative, and they can include
references to "." and "..". The {hclass}`BPath` "normalizes" the passed-in
strings to create an absolute pathname, as described in "{ref}`Initializing
and Normalizing`".

{hclass}`BPath`s are handy, but don't expect them to actually do very
much: A {hclass}`BPath` is just a pathname. It identifies the location of a
file, but it can't manipulate the file, nor can it change the structure of
the file system.

## So what do you use BPaths for?

-   You can use your {hclass}`BPath` to initialize other, more powerful
objects ({cpp:class}`BEntry`, {cpp:class}`BNode` and its kids). See
"{ref}`Converting a BPath`".

-   {hclass}`BPath`s can be passed through {cpp:class}`BMessage`s. To add a
{hclass}`BPath` to a {cpp:class}`BMessage`, you have to flatten it first:
{hclass}`BPath` implements {cpp:class}`BFlattenable` for exactly this
reason. The receiver of the {cpp:class}`BMessage` can resurrect the
flattened object as a {hclass}`BPath` object or as an {htype}`entry_ref`
structure. See "{ref}`Passing a BPath in a BMessage`".

-   {hclass}`BPath` objects are ideal for caching references to files.
{hclass}`BPath`s don't consume much in the way of system resources—they
don't contain file descriptors, for example. So they're great for keeping
track of the files that your application is interested in.

In the way that they're used, {hclass}`BPath`s and {htype}`entry_ref`s are
nearly identical. In particular, {htype}`entry_ref`s can do all three of
the things listed here. Whether you use {hclass}`BPath`s (pathnames in
general) or {htype}`entry_ref`s is largely a matter of taste.

## Initializing and Normalizing

You initialize a {hclass}`BPath`—in other words, you establish the path
that the object represents—by passing a string (or two, or a
{cpp:class}`BDirectory` and a string) to the constructor or to the
{cpp:func}`SetTo() <BPath::SetTo>` function. Upon initialization, the
{hclass}`BPath` object concatenates the strings and then "normalizes" the
passed-in strings if it has to (this emphasis is important, as we'll see in
a moment). The following elements trigger normalization:

-   a relative pathname (after concatenation; e.g. boot/lbj)

-   the presence of "." or ".." (/boot/lbj/../lbj/./fido)

-   redundant slashes (/boot//lbj)

-   a trailing slash (/boot/lbj/)

During normalization, {hclass}`BPath` conjures up an absolute pathname in
the form

-   /dir1/dir2/.../dirN/leaf

It does this by applying the following rules:

-   relative pathnames are reckoned off of the current working directory

-   "." is ignored (at the head of a path, it's taken as the cwd).

-   ".." bumps up one directory level

-   redundant slashes are coalesced

-   a trailing slash is removed.

(The one exception to this final rule is / as a full pathname.)

There's a subtle side-effect that you get with normalization: When you
normalize a pathname, all the elements in the path up to but not including
the leaf must exist. In other words, a normalized {hclass}`BPath` object
gives you the same guarantee of existence as does an {htype}`entry_ref`
structure. The subtlety, here, is that an unnormalized {hclass}`BPath`
needn't exist at all.

For example, here we create a {hclass}`BPath` for a pathname that contains
a non-existent directory:

:::{code} cpp
/* We'll assume that "/abc/def/" doesn't exist. */
BPath path("/abc/def/ghi.jkl");

/* Nonetheless, the BPath is successfully initialized.
* The Path() function returns a pointer to the object's
* pathname string.
*/
printf("Path: %sn". path.Path());
:::

On the command line we see:

:::{code} sh
$ Path: /abc/def/ghi.jkl
:::

But if we tickle the normalization machine…

:::{code} cpp
/* The redundant slash causes a normalization. */
BPath path("/abc/def//ghi.jkl");
:::

…the object is invalid:

:::{code} sh
$ Path: (null)
:::

### Forcing Initialization

Both the constructor and the {cpp:func}`SetTo() <BPath::SetTo>` function
carry an optional argument that lets you force the passed-in path to be
normalized:

:::{code} cpp
/* The trailing bool forces normalization. */
BPath path("/abc/def/ghi.jkl", true);
printf("Path: %sn", path.Path());
:::

In this case, the forced normalization nullifies the object:

:::{code} sh
$Path: (null)
:::

### Normalization by Default?

Since forcing normalization makes {hclass}`BPath`'s behaviour more
consistent and reliable, why not always normalize? Because normalization
can be expensive.

During normalization, the pathname is stat'd and prodded rather heavily.
If you're planning on using your {hclass}`BPath`'s pathname to initialize a
{cpp:class}`BEntry` or {cpp:class}`BNode`, this prodding will happen again.
Rather than incur the expense twice, you may want to live with unnormalized
{hclass}`BPath` objects, and take the normalization hit during the
subsequent initialization.

### Other Normalization Details

-   You can't force the {hclass}`BPath` constructor or {cpp:func}`SetTo()
<BPath::SetTo>` function to skip the normalization. If the path needs to be
normalized, it will be normalized.

-   {hclass}`BPath` doesn't let you ask if its pathname was normalized.

## The BPath Calling Convention

{hclass}`BPath` objects are passed back to you (by reference) by a number
of Storage Kit functions. However, you shouldn't find any functions that
ask for a {hclass}`BPath` object. This is a convention of usage:

-   If an API element returns a pathname to you, it does so in the form of a
{hclass}`BPath`. If it asks for a pathname from you (as an argument), it
asks for a {htype}`const char*`.

As an example of a function that returns a {hclass}`BPath` to you, recall
{cpp:class}`BEntry`'s {cpp:func}`GetPath() <BEntry::GetPath>` function:

:::{code} cpp
status_t BEntry::GetPath(BPath *path)
:::

(As an aside, this is where the auto-allocation comes in handy—because
{hclass}`BPath` allocates the pathname storage for you, you don't have to
mess around with ugly buffer and length arguments.)

On the other hand, {cpp:class}`BEntry`'s {cpp:func}`SetTo()
<BEntry::SetTo>` takes a pathname as a {htype}`const char*`:

:::{code} cpp
status_t BEntry::SetTo(const char *path)
:::

If you've got a {hclass}`BPath` loaded up with a pathname, you would call
this function thus:

:::{code} cpp
entry.SetTo(path.Path());
:::

The constructors and {cpp:func}`SetTo() <BPath::SetTo>` functions in (most
of) the Storage Kit classes have {htype}`const char*` versions that can be
called as shown here.

## Passing a BPath in a BMessage

Let's say you've got a {hclass}`BPath` object that you want to send to
some other application. To do this, you have to add it to a
{cpp:class}`BMessage` object through the latter's {cpp:func}`AddFlat()
<BMessage::AddFlat>` function. As an inheritor from
{cpp:class}`BFlattenable` the {hclass}`BPath` knows how to flatten itself
for just this purpose.

:::{code} cpp
BMessage msg;
BPath path("/boot/lbj/fido");

/* The check here is important, as we'll describe
* in a moment.
*/
if (msg.AddFlat("pathname", &path) != B_OK)
   /* handle the error */
:::

The receiver of the message can retrieve the pathname as a {hclass}`BPath`
object by calling {cpp:func}`FindFlat() <BMessage::FindFlat>`:

:::{code} cpp
void MyApp::MessageReceived(BMessage *msg)
{
   BPath path;

   if (msg->FindFlat("pathname", &path) != B_OK)
      /* handle the error */
   ...
}
:::

Alternatively, the pathname can be retrieved as an {htype}`entry_ref`
through {cpp:func}`FindRef() <BMessage::FindRef>`:

:::{code} cpp
void MyApp::MessageReceived(BMessage *msg)
{
   entry_ref ref;

   if (msg->FindRef("pathname", &ref) != B_OK)
      /* handle the error */
   ...
}
:::

If you want to skip all the conversion business and simply pass the
pathname as a string, use {cpp:func}`AddString() <BMessage::AddString>`.
The receiver, of course, would have to call {cpp:func}`FindString()
<BMessage::FindString>` to retrieve your pathname string.

### What's Really Going On

When you add a flattened {hclass}`BPath` to a {cpp:class}`BMessage`, the
object's pathname is turned into an {htype}`entry_ref`. If the message
receiver asks for a {hclass}`BPath` (through {cpp:func}`FindFlat()
<BMessage::FindFlat>`), the {htype}`entry_ref` is turned back into a
{hclass}`BPath` object. Therefore, it's more efficient to retrieve a
flattened {hclass}`BPath` as an {htype}`entry_ref` than it is to unflatten
it as a {hclass}`BPath` object.

The {hclass}`BPath` to {htype}`entry_ref` conversion has another, more
subtle implication: Adding a {hclass}`BPath` through {cpp:func}`AddFlat()
<BMessage::AddFlat>` performs an implicit normalization on the data that's
added to the {cpp:class}`BMessage`.

If the normalization fails, the {cpp:func}`AddFlat() <BMessage::AddFlat>`
function returns an error and the data isn't added to the
{cpp:class}`BMessage`. The original {hclass}`BPath` is untouched,
regardless of the result of the normalization.

## Converting a BPath

As mentioned earlier, most of the Storage Kit classes have constructors
and {cpp:func}`SetTo() <BPath::SetTo>` functions that accept {htype}`const
char*` arguments. If you want to turn your {hclass}`BPath` into a
{cpp:class}`BFile` (for example), you would do this (including error
checks):

:::{code} cpp
status_t err;

BFile file(path.Path());
err = InitCheck();
:::

or

:::{code} cpp
err = file.SetTo(path.Path());
:::

To convert a {hclass}`BPath` to an {htype}`entry_ref`, pass the pathname
to the {ref}`get_ref_for_path()` function:

:::{code} cpp
entry_ref ref;
status_t err;

err = get_ref_for_path(path.Path(), &ref);
:::

For you Node Monitor users: You can't convert directly to a
{htype}`node_ref` structure. The quickest way from here to there is:

:::{code} cpp
node_ref nref;
status_t err;

/* We'll skip InitCheck() and catch errors in GetNodeRef(). */
BEntry entry(path.Path());
err = entry.GetNodeRef(&nref);
:::

## Immutability

Remember, a {hclass}`BPath` represents a pathname, not a node. It isn't
"updated" when the file system changes:

-   A {hclass}`BPath`'s pathname string never changes behind your back, even
if the entry that it originally pointed to is renamed, moved, or deleted.

For example:

:::{code} cpp
BEntry entry;
BPath path;

/* Set a BPath, construct a BEntry from it, rename
* the entry, and then print the BPath's pathname.
*/
if (path.SetTo("/boot/lbj/fido") == B_OK)
   if (entry.SetTo(&path) == B_OK)
      if (entry.Rename("rover") == B_OK)
         printf("Pathname: %sn", path.Path());
:::

We see…

:::{code} sh
$ Pathname: /boot/lbj/fido
:::

...even though the entry that the {hclass}`BPath` was constructed to
represent has been renamed.
