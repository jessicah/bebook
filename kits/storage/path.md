# BPath
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BPath::BPath()
:::
:::{cpp:function} BPath::BPath(const BEntry* entry)
:::
:::{cpp:function} BPath::BPath(const entry_ref* ref)
:::
:::{cpp:function} BPath::BPath(const char* path, const char* leaf = NULL, bool normalize = false)
:::
:::{cpp:function} BPath::BPath(const BDirectory* dir, const char* leaf = NULL, bool normalize = false)
:::
:::{cpp:function} BPath::BPath(const BPath& path)
:::

Creates a new {hclass}`BPath` object that represents the path that's created from
the arguments. See the analogous
{cpp:func}`~BPath::SetTo` functions for descriptions of
the flavorful constructors.

- The default constructor does nothing; it should be followed by a call to {cpp:func}`~BPath::SetTo`.
- The copy constructor makes a copy of the argument's pathname.

The constructor automatically allocates memory for the object's stored
pathname. The memory is freed when the object is deleted.

To check to see if an initialization was successful, call
{cpp:func}`~BPath::InitCheck`.

::::

::::{abi-group}

:::{cpp:function} virtual BPath::~BPath()
:::

Frees the object's pathname storage and extinguishes the object.

::::

## Member Functions
::::{abi-group}

:::{cpp:function} status_t BPath::Append(const char* path, bool normalize = false)
:::

Appends the pathname given by {hparam}`path` to the object's current pathname. {hparam}`path`
must be relative. If {hparam}`normalize` is {cpp:enum}`true`, the new pathname is normalized;
otherwise, it's normalized only if necessary.

Note that this…

:::{code}
Append("subdir/file")
:::

…is the same as (and is implemented as):

:::{code}
path.SetTo(path.Path(), "subdir/file");
:::

The {hmethod}`Append()` return value is picked up from the
{cpp:func}`~BPath::SetTo` call.

:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- Success.
-
	- {cpp:enum}`B_BAD_VALUE`.
	- {hparam}`path` contained a leading "/", or this is uninitialized.
:::
See {cpp:func}`~BPath::SetTo`
for other return values.
::::

::::{abi-group}

:::{cpp:function} status_t BPath::GetParent(BPath* path) const
:::

Initializes the argument with the pathname to the parent directory of
this. Destructive parenting is acceptable (sociologically, it's a given):

:::{code}
BPath path("/boot/lbj/fido");
path.GetParent(&path);
:::

Other details…

- {hmethod}`GetParent()` makes a call to {cpp:func}`~BPath::SetTo`, but it's guaranteed not to tickle the normalization machine.
- You can't get the parent of "/".

:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- Hello, mother.
-
	- {cpp:enum}`B_ENTRY_NOT_FOUND`.
	- You tried to get the parent of "/".
-
	- {cpp:enum}`B_BAD_VALUE`.
	- {hparam}`path` is {cpp:enum}`NULL`.
-
	- {cpp:enum}`B_NO_MEMORY`.
	- Couldn't allocate storage for the pathname.
:::

If the initialization isn't successful, the argument's
{cpp:func}`~BPath::InitCheck` is set
to {cpp:enum}`B_NO_INIT`.

::::

::::{abi-group}

:::{cpp:function} status_t BPath::InitCheck() const
:::

Returns the status of the most recent construction or
{cpp:func}`~BPath::SetTo` call.

:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- The initialization was successful.
-
	- {cpp:enum}`B_NO_INIT`.
	- The object is uninitialized (this includes {cpp:func}`~BPath::Unset`).
-
	- For other errors.
	- See {cpp:func}`~BPath::SetTo`
:::
::::

::::{abi-group}

:::{cpp:function} const char* BPath::Path() const
:::
:::{cpp:function} const char* BPath::Leaf() const
:::

These functions return the object's full path and leaf name,
respectively. For example:

:::{code}
BPath path("/boot/lbj/fido");
printf("Path: %sn", path.Path());
printf("Leaf: %sn", path.Leaf());
:::

Produces…

:::{code}
$ Path: /boot/lbj/fido
$ Leaf: fido
:::

In both cases, the returned pointers belong to the {hclass}`BPath` object. When the
{hclass}`BPath` is deleted, the pointers go with it.

If the {hclass}`BPath` isn't initialized, the functions
return pointers to {cpp:enum}`NULL`.

::::

::::{abi-group}

:::{cpp:function} BPath::SetTo(const BEntry* entry)
:::
:::{cpp:function} BPath::SetTo(const char* path, const char* leaf = NULL, bool normalize = false)
:::
:::{cpp:function} BPath::SetTo(const BDirectory* dir, const char* leaf = NULL, bool normalize = false)
:::
:::{cpp:function} BPath::Unset()
:::

The {hmethod}`SetTo()` function frees the pathname that the object currently holds,
and re-initializes the object according to the arguments:

- The first version concatenates the {hparam}`path` and {hparam}`leaf` strings (interposing a "/" if necessary). If {hparam}`path` is relative, the concatenated pathname is appended to the current working directory. Note that you don't have to split your pathname into two parts to call this constructor; the optional {hparam}`leaf` argument is provided simply as a convenience.
- The second version performs a similar operation using the path of the {cpp:class}`BDirectory` as the initial part of the pathname.
- The third version initilizes the object with the {hparam}`path` and name of the {hparam}`entry`.

Regarding the {hparam}`leaf` argument:

- The {hparam}`leaf` string can contain directories—it needn't be just a leaf name.
- However, {hparam}`leaf` must be a relative pathname (it can't start with "/").

If set to {cpp:enum}`true`, the {hparam}`normalize` argument tells the object to normalize the
new pathname. By default ({cpp:enum}`false`), the pathname is normalized only if
necessary. Note that the default doesn't mean that the object absolutely
won't normalize, it just won't do it if it doesn't think it's necessary.
See  "{cpp:func}`~BPath::Initializing`" for the full story on
normalizing a pathname, including the conditions that trigger default
normalization. Normalizing has no meaning with the
{cpp:class}`BEntry` version of
{hmethod}`SetTo()`.

Storage for the pathname is allocated by the {hclass}`BPath` object and is freed
when the object is deleted (or when you re-initialize through {hmethod}`SetTo()`).
The path and leaf arguments are copied into the allocated storage.

Other details…

- Destructive setting is safe:/* This works... */ path.SetTo(path.Path(), ...);
- Currently, {hmethod}`SetTo()` only checks pathname and filename length if it has to normalize.

{hmethod}`Unset()` frees the object's pathname storage and sets the
{cpp:func}`~BPath::InitCheck`
value to {cpp:enum}`B_NO_INIT`.

:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- Successful initialization.
-
	- {cpp:enum}`B_BAD_VALUE`.
	- {hparam}`path` is {cpp:enum}`NULL`, {hparam}`leaf` isn't relative (it starts with a "/"), or {hparam}`dir` is uninitialized.
-
	- {cpp:enum}`B_BAD_VALUE`.
	- A directory in the path doesn't exist (normalization only).
-
	- {cpp:enum}`B_NAME_TOO_LONG`.
	- A pathname element is too long (normalization only).
-
	- {cpp:enum}`B_NO_MEMORY`.
	- Couldn't allocate storage for the pathname.
:::

The return value is also recorded in
{cpp:func}`~BPath::InitCheck`.

::::

::::{abi-group}

The following functions are implemented in accordance with the rules set
down by the {cpp:class}`BFlattenable` class. You never need to invoke these functions
directly; they're implemented so a {hclass}`BPath` can added to a
{cpp:class}`BMessage` (see
"{cpp:func}`~BPath::Passing`"). But in case you're
interested…

::::

::::{abi-group}

:::{cpp:function} virtual bool BPath::AllowsTypeCode(type_code code) const
:::

Returns {cpp:enum}`true` if {hparam}`code` is
{cpp:enum}`B_REF_TYPE`, and {cpp:enum}`false` otherwise.

::::

::::{abi-group}

:::{cpp:function} virtual status_t BPath::Flatten(void* buffer, ssize_t size) const
:::

Converts the object's pathname to an entry_ref and writes it into {hparam}`buffer`.
Currently, {hparam}`size` is ignored.

:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- Peachy.
-
	- {cpp:enum}`B_NAME_TOO_LONG`.
	- The pathname is too long (> 1024 characters).
-
	- {cpp:enum}`B_ENTRY_NOT_FOUND`.
	- A directory in the path doesn't exist.
:::
::::

::::{abi-group}

:::{cpp:function} virtual ssize_t BPath::FlattenedSize() const
:::

Returns the size of the entry_ref that represents the flattened pathname.

::::

::::{abi-group}

:::{cpp:function} virtual bool BPath::IsFixedSize() const
:::

Returns {cpp:enum}`false`.

::::

::::{abi-group}

:::{cpp:function} virtual type_code BPath::TypeCode() const
:::

Returns {cpp:enum}`B_REF_TYPE`.

::::

::::{abi-group}

:::{cpp:function} virtual status_t BPath::Unflatten(type_code code, const void* buffer, ssize_t size)
:::

Initializes the {hclass}`BPath` with the flattened entry_ref data that's found in
{hparam}`buffer`. The type code must be {cpp:enum}`B_REF_TYPE`.

:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- Success.
-
	- {cpp:enum}`B_BAD_VALUE`.
	- Wrong type code (not {cpp:enum}`B_REF_TYPE`).
-
	- {cpp:enum}`B_ENTRY_NOT_FOUND`.
	- A directory in the entry_ref data doesn't exist.
:::

The {hmethod}`Unflatten()` return value is recorded in
{cpp:func}`~BPath::InitCheck`.

::::

## Operators
::::{abi-group}

:::{cpp:function} BPath& BPath::operator=(const BPath& path)
:::
:::{cpp:function} BPath& BPath::operator=(const char* string)
:::

Initializes this with a copy of the pathname that's gotten from the
argument. Also sets
{cpp:func}`~BPath::InitCheck`.

::::

::::{abi-group}

:::{cpp:function} bool BPath::operator==(const BPath& path) const
:::
:::{cpp:function} bool BPath::operator==(const char* string) const
:::
:::{cpp:function} bool BPath::operator!=(const BPath& path) const
:::
:::{cpp:function} bool BPath::operator!=(const char* string) const
:::

Compares this's pathname with the pathname taken from the argument. The
comparison is a simple strcmp(); neither path is normalized or otherwise
altered before the comparison is made. For example:

:::{code}
BPath path("/boot/lbj/fido");
chdir("/boot");
printf("Are they equal? %dn", path == "lbj/fido");
:::

Displays:

:::{code}
$ Are they equal? 0
:::
::::
