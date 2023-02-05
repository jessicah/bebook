# BBitmapStream

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BBitmapStream::BBitmapStream(BBitmap* map = NULL)
:::

Creates a new instance of {hclass}`BBitmapStream`. If {hparam}`map` is {cpp:expr}`NULL`, the stream
is initialized to be empty. Otherwise, the {cpp:class}`BBitmap` is converted to a translator bitmap
and placed in the stream. The application shares the {cpp:class}`BBitmap` with the
{hclass}`BBitmapStream` object. It therefore shouldn't delete the {cpp:class}`BBitmap` without first
calling {cpp:func}`~BBitmapStream::DetachBitmap`.
::::

::::{abi-group}
:::{cpp:function} ~BBitmapStream::BBitmapStream()
:::

Frees all memory allocated by the
{cpp:class}`BTranslatorRoster`.

::::

## Member Functions

::::{abi-group}
:::{cpp:function} status_t BBitmapStream::DetachBitmap(BBitmap** outMap)
:::

Returns, in {hparam}`outMap`, a {cpp:class}`BBitmap` representing the image contained in the
{hclass}`BBitmapStream`. Once {hmethod}`DetachBitmap()` has been called, no further operations
should be performed on the {hclass}`BBitmapStream`.


:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_NO_ERROR`
	- Success.
-
	- {cpp:enum}`B_BAD_VALUE`
	- {hparam}`outMap` is {cpp:expr}`NULL`.
-
	- {cpp:enum}`B_ERROR`
	- There is no {cpp:class}`BBitmap` available.
:::
::::

::::{abi-group}
:::{cpp:function} off_t BBitmapStream::Position() const
:::
:::{cpp:function} ssize_t BBitmapStream::ReadAt(off_t position, void* buffer, size_t size)
:::
:::{cpp:function} off_t BBitmapStream::Seek(off_t position, int32 whence)
:::
:::{cpp:function} status_t BBitmapStream::SetSize(off_t size) const
:::
:::{cpp:function} ssize_t BBitmapStream::WriteAt(off_t pos, const void* data, size_t size)
:::

These methods provide the implementation for the {cpp:class}`BPositionIO`. The class functions
identically to {cpp:class}`BPositionIO` with the exception of {hmethod}`ReadAt()` and
{hmethod}`WriteAt()`, which read and write only translator bitmaps as described in the class
introduction.
::::

::::{abi-group}
:::{cpp:function} off_t BBitmapStream::Size() const
:::

Returns the number of bytes in the translator bitmap in the stream.
::::
