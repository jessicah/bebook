# BString

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BString::BString()
:::
:::{cpp:function} BString::BString(const char* string)
:::
:::{cpp:function} BString::BString(const char* string, int32 maxLength)
:::
:::{cpp:function} BString::BString(const BString& string)
:::

Creates a new {hclass}`BString` object that allocates enough storage to accommodate
{hparam}`string` (or
{hparam}`string`->{cpp:func}`~BString::String`,
or up to {hparam}`maxLength` bytes), and then copies
the string into the storage. Without an argument, the new {hclass}`BString` is
empty. You can also set a {hclass}`BString`'s data by using
{cpp:func}`~BString::SetTo`,
{cpp:func}`~BString::Adopt`, or
the {cpp:func}`~BString::Adopt`.

::::

::::{abi-group}
:::{cpp:function} ~BString::BString()
:::

Frees the object's allocated memory, and destroys the object.

::::

## Member Functions

::::{abi-group}
:::{cpp:function} inline BString& BString::Append(const BString& source)
:::
:::{cpp:function} BString& BString::Append(const BString& source, int32 charCount)
:::
:::{cpp:function} inline BString& BString::Append(const char* source)
:::
:::{cpp:function} BString& BString::Append(const char* source, int32 charCount)
:::
:::{cpp:function} BString& BString::Append(char c, int32 charCount)
:::

:::{cpp:function} BString& BString::Prepend(const BString& source)
:::
:::{cpp:function} BString& BString::Prepend(const BString& source, int32 charCount)
:::
:::{cpp:function} BString& BString::Prepend(const char* source)
:::
:::{cpp:function} BString& BString::Prepend(const char* source, int32 charCount)
:::
:::{cpp:function} BString& BString::Prepend(char c, int32 charCount)
:::

:::{cpp:function} BString& BString::Insert(const BString& source, int32 insertAt)
:::
:::{cpp:function} BString& BString::Insert(const BString& source, int32 charCount, int32 insertAt)
:::
:::{cpp:function} BString& BString::Insert(const BString& source, int32 sourceOffset, int32 charCount, int32 insertAt)
:::
:::{cpp:function} BString& BString::Insert(const char* source, int32 insertAt)
:::
:::{cpp:function} BString& BString::Insert(const char* source, int32 charCount, int32 insertAt)
:::
:::{cpp:function} BString& BString::Insert(const char* source, int32 sourceOffset, int32 charCount, int32 insertAt)
:::
:::{cpp:function} BString& BString::Insert(char c, int32 charCount, int32 insertAt)
:::

These functions add characters to the end (append), beginning (prepend),
or middle (insert) of the {hclass}`BString`'s string. In
each case, the {hclass}`BString`
automatically reallocates to accommodate the new data. All of these
functions return *this.

{hmethod}`Append()` copies {hparam}`charCount`
characters from {hparam}`source` and adds them to the end
of this {hclass}`BString`. If {hparam}`charCount`
isn't specified, the entire string is
copied; this is the same as the
{cpp:func}`~BString::operator`.
The single character version
of {hmethod}`Append()` adds {hparam}`count`
copies of the character {hparam}`c` to the end of the object.

{hmethod}`Prepend()` does the same as {hmethod}`Append()`,
except it adds the characters to the
beginning of this {hclass}`BString`,
shifting the existing data "to the right" to
make room.

{hmethod}`Insert()` adds the designated characters at
{hparam}`insertAt` (zero-based) in this
{hclass}`BString`. The {hclass}`BString`'s
existing data (at location {hparam}`insertAt` and higher) is
shifted right to make room for the new data. The {hparam}`sourceOffset` argument is
an offset (zero-based) into the source string.

::::

::::{abi-group}
:::{cpp:function} BString& BString::CharacterEscape(const char* original, const char* setOfCharsToEscape, char escapeWithChar)
:::
:::{cpp:function} BString& BString::CharacterEscape(const char* setOfCharsToEscape, char escapeWithChar)
:::

:::{cpp:function} BString& BString::CharacterDeescape(const char* original, char escapeWithChar)
:::
:::{cpp:function} BString& BString::CharacterDeescape(char escapeWithChar)
:::

{hmethod}`CharacterEscape` scans a string for occurrences of the individual
characters in the string {hparam}`setOfCharsToEscape` and inserts into the string
the byte indicated by {hparam}`escapeWithChar` before each such occurrence. The
first form copies the original string into the {hclass}`BString`; the second form
operates on the existing {hclass}`BString`.

{hmethod}`CharacterDeescape()` undoes this operation by scanning the string and
removing all occurrences of the byte {hparam}`escapeWithChar`. The first form
copies the {hparam}`original` string into the
{hclass}`BString`, while the second form
operates on the existing {hclass}`BString`.

::::

::::{abi-group}
:::{cpp:function} int BString::Compare(const BString& string) const
:::
:::{cpp:function} int BString::Compare(const BString& string, int32 range) const
:::
:::{cpp:function} int BString::Compare(const char* string) const
:::
:::{cpp:function} int BString::Compare(const char* string, int32 range) const
:::
:::{cpp:function} int Compare(const BString& astring, const BString& bstring)
:::
:::{cpp:function} int Compare(const BString* astring, const BString* bstring)
:::

:::{cpp:function} int BString::ICompare(const BString& string) const
:::
:::{cpp:function} int BString::ICompare(const BString& string, int32 range) const
:::
:::{cpp:function} int BString::ICompare(const char* string) const
:::
:::{cpp:function} int BString::ICompare(const char* string, int32 range) const
:::
:::{cpp:function} int ICompare(const BString& astring, const BString& bstring)
:::
:::{cpp:function} int ICompare(const BString* astring, const BString* bstring)
:::

These functions compare this {hclass}`BString` with the argument
string ({hmethod}`Compare()`
is case-sensitive, {hmethod}`ICompare()` is case-insensitive); they return 0 if the
two strings are the same, 1 if this {hclass}`BString` is "greater than" the
argument, and -1 if the argument is greater than this {hclass}`BString`. Two
strings are compared by comparing the ASCII or UTF-8 values of their
respective characters. A longer string is greater than a shorter (but
otherwise similar) string—"abcdef" is greater than "abcde".

Given a {hparam}`range` argument, the functions only compare the first {hparam}`range`
characters.

The `global` functions return 0 if the arguments are equal, 1 if
{hparam}`astring` is
greater than {hparam}`bstring`, and -1 if {hparam}`bstring` is greater than {hparam}`astring`.

You can also compare two strings through the comparison operators ==,
!=, <, <=, >, and >=.

::::

::::{abi-group}
:::{cpp:function} BString& BString::CopyInto(BString& destination, int32 sourceOffset, int32 charCount) const
:::
:::{cpp:function} void BString::CopyInto(char* destination, int32 sourceOffset, int32 charCount) const
:::

:::{cpp:function} BString& BString::MoveInto(BString& destination, int32 sourceOffset, int32 charCount)
:::
:::{cpp:function} void BString::MoveInto(char* destination, int32 sourceOffset, int32 charCount)
:::

{hmethod}`CopyInto()` copies a substring from this
{hclass}`BString` into {hparam}`destination`.
{hmethod}`MoveTo()` does the same, but it removes the original substring (from this
{hclass}`BString`). If {hparam}`destination` is a
{hclass}`BString`, storage for the substring is
automatically allocated; if the {hparam}`destination` is a char*, the caller is
responsible for allocating sufficient storage.

The substring comprises {hparam}`charCount` characters starting at character
{hparam}`sourceOffset` (zero-based). After the substring is removed, the remaining
characters move (to the left) to fill in the gap ({hmethod}`MoveTo()` only). For
example:

:::{code}
BString source, destination;
source.SetTo("abcdefg");
source.MoveInto(&destination, 2, 3);

/* source.String() == "abfg" */
/* destination.String() == "cde" */
:::

The functions return destination (or void).

::::

::::{abi-group}
:::{cpp:function} int32 BString::CountChars() const
:::
:::{cpp:function} inline int32 BString::Length() const
:::

{hmethod}`CountChars()` returns the length of the object's string measured in
characters; {hmethod}`Length()` returns the length measured in bytes.

::::

::::{abi-group}
:::{cpp:function} int32 BString::FindFirst(const BString& string) const
:::
:::{cpp:function} int32 BString::FindFirst(const BString& string, int32 offset) const
:::
:::{cpp:function} int32 BString::FindFirst(const char* string) const
:::
:::{cpp:function} int32 BString::FindFirst(const char* string, int32 offset) const
:::
:::{cpp:function} int32 BString::FindFirst(char c) const
:::
:::{cpp:function} int32 BString::FindFirst(char c, int32 offset) const
:::

:::{cpp:function} int32 BString::FindLast(const BString& string) const
:::
:::{cpp:function} int32 BString::FindLast(const BString& string, int32 offset) const
:::
:::{cpp:function} int32 BString::FindLast(const char* string) const
:::
:::{cpp:function} int32 BString::FindLast(const char* string, int32 offset) const
:::
:::{cpp:function} int32 BString::FindLast(char c) const
:::
:::{cpp:function} int32 BString::FindLast(char c, int32 offset) const
:::

:::{cpp:function} int32 BString::IFindFirst(const BString& string) const
:::
:::{cpp:function} int32 BString::IFindFirst(const BString& string, int32 offset) const
:::
:::{cpp:function} int32 BString::IFindFirst(const char* string) const
:::
:::{cpp:function} int32 BString::IFindFirst(const char* string, int32 offset) const
:::

:::{cpp:function} int32 BString::IFindLast(const BString& string) const
:::
:::{cpp:function} int32 BString::IFindLast(const BString& string, int32 offset) const
:::
:::{cpp:function} int32 BString::IFindLast(const char* string) const
:::
:::{cpp:function} int32 BString::IFindLast(const char* string, int32 offset) const
:::

These functions return the index of the first or last occurrence (within
this {hclass}`BString`) of a substring or character.
{hmethod}`FindFirst()` and {hmethod}`FindLast()` are
case-sensitive; {hmethod}`IFindFirst()` and {hmethod}`IFindLast()` are case-insensitive. The
functions return B_ERROR if the character isn't found.

The {hparam}`offset` versions only look in the portion of this
{hclass}`BString` that starts at character
{hparam}`offset` (for
{hmethod}`[I]FindFirst()`), or that ends at character
{hparam}`offset` (for {hmethod}`[I]FindLast()`).
For example, in this example…

:::{code}
BString astring("AbcAbcAbc");
astring.FindLast("Abc", 7);
:::

…the {hmethod}`FindLast()` call returns 3, the index of the last complete instance
of "Abc" that occurs before character 7.

::::

::::{abi-group}
:::{cpp:function} char* BString::LockBuffer(int32 maxLength)
:::
:::{cpp:function} BString& BString::UnlockBuffer(int32 length = -1)
:::

{hmethod}`LockBuffer()` returns a pointer to the object's string; you're allowed to
manipulate this pointer directly. The {hparam}`maxLength` argument lets you ask the
object to allocate some extra space at the end of the string before
passing you the pointer. If {hparam}`maxLength` is less than the string's current
length, the argument is ignored (pass 0 if you want to lock the buffer
but don't need to pre-allocate extra space).

{hmethod}`UnlockBuffer()` tells the object that you're done manipulating the string
pointer. {hparam}`length` is the string's new length; if you pass -1, the {hclass}`BString`
gets the length by calling strlen() on the string. The functions returns
`*this`.

Every {hmethod}`LockBuffer()` must be balanced by a
subsequent {hmethod}`UnlockBuffer()`. In
between the two calls, you may not call any {hclass}`BString` functions. Many of
the {hclass}`BString` functions assert an error if they're called while the buffer
is locked.

See "Direct Data Access" for an example.

::::

::::{abi-group}
:::{cpp:function} BString& BString::Remove(int32 startingAt, int32 charCount)
:::
:::{cpp:function} BString& BString::RemoveFirst(const BString& string)
:::
:::{cpp:function} BString& BString::RemoveFirst(const char* string)
:::

:::{cpp:function} BString& BString::RemoveLast(const BString& string)
:::
:::{cpp:function} BString& BString::RemoveLast(const char* string)
:::

:::{cpp:function} BString& BString::RemoveAll(const BString& string)
:::
:::{cpp:function} BString& BString::RemoveAll(const char* string)
:::

:::{cpp:function} BString& BString::RemoveSet(const char* charSet)
:::

These functions remove characters from the {hclass}`BString` and reallocate the
object's storage so it fits the new (smaller) data. The functions return
`*this`.

{hmethod}`Remove()` removes {hparam}`charCount`
characters, starting with character {hparam}`startingAt`
(zero-based).

{hmethod}`RemoveFirst()`, {hmethod}`RemoveLast()`,
and {hmethod}`RemoveAll()` remove, respectively, the
first, last and every occurrence of string within the object.

{hmethod}`RemoveSet()` removes all occurrences of every
character in the {hparam}`charSet`
string. For example:

:::{code}
BString string("ab abc abcd");
string.RemoveSet("db");
/* 'string' now contains "a ac ac" */
:::
::::

::::{abi-group}
:::{cpp:function} BString& BString::Replace(const char* old, const char* new, int32 count, int32 offset = 0)
:::
:::{cpp:function} BString& BString::Replace(char old, char new, int32 count, int32 offset = 0)
:::

:::{cpp:function} BString& BString::ReplaceFirst(const char* old, const char* new)
:::
:::{cpp:function} BString& BString::ReplaceFirst(char old, char new)
:::

:::{cpp:function} BString& BString::ReplaceLast(const char* old, const char* new)
:::
:::{cpp:function} BString& BString::ReplaceLast(char old, char new)
:::

:::{cpp:function} BString& BString::ReplaceAll(const char* old, const char* new, int32 offset = 0)
:::
:::{cpp:function} BString& BString::ReplaceAll(char old, char new, int32 offset = 0)
:::

:::{cpp:function} BString& BString::ReplaceSet(const char* oldSet, const char* new)
:::
:::{cpp:function} BString& BString::ReplaceSet(const char* oldSet, char new)
:::

:::{cpp:function} BString& BString::IReplace(const char* old, const char* new, int32 count, int32 offset = 0)
:::
:::{cpp:function} BString& BString::IReplace(char old, char new, int32 count, int32 offset = 0)
:::

:::{cpp:function} BString& BString::IReplaceFirst(const char* old, const char* new)
:::
:::{cpp:function} BString& BString::IReplaceFirst(char old, char new)
:::

:::{cpp:function} BString& BString::IReplaceLast(const char* old, const char* new)
:::
:::{cpp:function} BString& BString::IReplaceLast(char old, char new)
:::

:::{cpp:function} BString& BString::IReplaceAll(const char* old, const char* new, int32 offset = 0)
:::
:::{cpp:function} BString& BString::IReplaceAll(char old, char new, int32 offset = 0)
:::

:::{cpp:function} BString& BString::IReplaceSet(const char* oldSet, const char* new)
:::
:::{cpp:function} BString& BString::IReplaceSet(const char* oldSet, char new)
:::

These functions find occurrences of {hparam}`old`
within the {hclass}`BString`, and replace
them with {hparam}`new`. In the {hmethod}`Replace…()`
functions, the search for {hparam}`old` is
case-insensitive; in the {hmethod}`IReplace…()` functions, the search is
case-insensitive. The functions return `*this`.

{hmethod}`[I]Replace()` replaces the first
{hparam}`count` occurrences that start on or after
the character at {hparam}`offset`.

{hmethod}`[I]ReplaceFirst()` and {hmethod}`[I]ReplaceLast()`
replace only the first and last
occurrence (respectively).

{hmethod}`[I]ReplaceAll()` replaces all occurrence that start on or after the
character at {hparam}`offset`.

{hmethod}`[I]ReplaceSet()` is slightly different from the others: It replaces each
occurrence of any character in {hparam}`oldSet` with the character or the entire
string given by new. For example:

:::{code}
BString astring("a-b-c");
astring.ReplaceSet("abc", "ABC");
/* astring is now "ABC-ABC-ABC" */
:::
::::

::::{abi-group}
:::{cpp:function} inline BString& BString::SetTo(const char* source)
:::
:::{cpp:function} BString& BString::SetTo(const char* source, int32 charCount)
:::
:::{cpp:function} BString& BString::SetTo(const BString& source)
:::
:::{cpp:function} BString& BString::SetTo(const BString& source, int32 charCount)
:::
:::{cpp:function} BString& BString::SetTo(char c, int32 charCount)
:::

:::{cpp:function} BString& BString::Adopt(const BString& source)
:::
:::{cpp:function} BString& BString::Adopt(const BString& source, int32 charCount)
:::

These functions initialize a {hclass}`BString`'s string data. Storage for the data
is automatically allocated by the functions. The object's current data is
wholly replaced by the new data. The functions return `*this`.

{hmethod}`SetTo()` copies {hparam}`charCount`
characters from {hparam}`source` into this object. If
{hparam}`charCount` isn't given, the entire string is copied; this form is
equivalent to the = operator. The single character version of {hmethod}`SetTo()`
sets the object's data to a {hparam}`charCount`-length string that consists
entirely of the character {hparam}`c`.

{hmethod}`Adopt()` moves {hparam}`charCount`
characters from {hparam}`source` into this object, and then
clears {hparam}`source`'s data (pointer). Note that source will be empty after you
call {hmethod}`Adopt()`, even if {hparam}`charCount`
is less than source's full length.

::::

::::{abi-group}
:::{cpp:function} inline const char* BString::String() const
:::
:::{cpp:function} inline char BString::ByteAt(int32 index) const
:::

{hmethod}`String()` returns a pointer to the object's
string, guaranteed to be NULL
terminated. You may not modify or free the pointer. If the {hclass}`BString` is
deleted, the pointer becomes invalid.

{hmethod}`ByteAt()` returns the {hparam}`index`'th
character in the string. If {hparam}`index` is out of
bounds, the function returns 0. Except for the boundary check, this
function is the same as the [] operator.

::::

::::{abi-group}
:::{cpp:function} BString& BString::ToLower()
:::
:::{cpp:function} BString& BString::ToUpper()
:::
:::{cpp:function} BString& BString::Capitalize()
:::
:::{cpp:function} BString& BString::CapitalizeEachWord()
:::

{hmethod}`ToLower()` converts every character in the string to lower case;
{hmethod}`ToUpper()`
converts them all to upper case. Non-alphabetic characters aren't
affected.

{hmethod}`Capitalize()` converts the first alphabetic character in the word to upper
case, and the rest to lower case. {hmethod}`CapitalizeEachWord()` converts the first
alphabetic character in each "word" to upper case, and the rest to lower
case. A word is a group of alphabetic characters delimited by
non-alphabetic characters.

The functions return `*this`.

:::{admonition} Warning
:class: warning
{hmethod}`Capitalize()` and
{hmethod}`CapitalizeEachWord()` are broken in Release 4.0.

:::

::::

::::{abi-group}
:::{cpp:function} BString& BString::Truncate(int32 charCount, bool lazy = true)
:::

{hmethod}`Truncate()` shrinks the object's string so
that it's {hparam}`charCount` characters
long. This function will not lengthen the string: If {hparam}`charCount` is equal
to or greater than the string's current character count, the function
does nothing.

If {hparam}`lazy` is false, the string
is immediately reallocated to trim it to the
new size (and the excess is immediately freed). If it's true, the string
is set to the new size, but the excess isn't freed until the next storage
manipulating function is called. It's slightly more efficient to be lazy;
otherwise, the two forms of the function are identical.

The function return `*this`.

::::

## Operators

::::{abi-group}
:::{cpp:function} BString& BString::operator=(const BString& string)
:::
:::{cpp:function} BString& BString::operator=(const char* string)
:::
:::{cpp:function} BString& BString::operator=(const char character)
:::

Sets the contents of the {hclass}`BString` to
{hparam}`string` or {hparam}`character`, and returns
`*this->LockBuffer()`.

::::

::::{abi-group}
:::{cpp:function} inline BString& BString::operator+=(const BString& string)
:::
:::{cpp:function} BString& BString::operator+=(const char* string)
:::
:::{cpp:function} BString& BString::operator+=(const char character)
:::

Appends {hparam}`string` or {hparam}`character`
to this {hclass}`BString`, and returns `*this`.

::::

::::{abi-group}
:::{cpp:function} BString& BString::operator<<(const BString& string)
:::
:::{cpp:function} BString& BString::operator<<(const char* string)
:::
:::{cpp:function} BString& BString::operator<<(char c)
:::
:::{cpp:function} BString& BString::operator<<(uint32 val)
:::
:::{cpp:function} BString& BString::operator<<(int32 val)
:::
:::{cpp:function} BString& BString::operator<<(uint64 val)
:::
:::{cpp:function} BString& BString::operator<<(int64 val)
:::
:::{cpp:function} BString& BString::operator<<(float val)
:::

Converts the right operand to a string (if necessary), and appends it to
the left operand. Floating point values are always written with two
decimal digits:

:::{code}
BString astring("The result is: "), bstring(" bps");
float result = 12.5;
astring << result << bstring;
:::

Here, astring becomes "The result is: 12.50 bps".

Multiple append operations are evaluated from left to right, so that only
the leftmost operand is modified. For example:

:::{code}
BString astring("a"), bstring("b"), cstring("c");
astring << bstring << cstring;
:::

Here, bstring is appended to astring,
and then cstring is appended to the
result; thus, astring is "abc", and
bstring is still "b".

::::

::::{abi-group}
:::{cpp:function} char BString::operator[](int32 index) const
:::
:::{cpp:function} inline char& BString::operator[](int32 index)
:::

Returns the character at {hparam}`index` in the string. No boundary checking is
done—it's up to the caller to ensure that {hparam}`index` is in
bounds.

::::

::::{abi-group}
:::{cpp:function} inline bool BString::operator==(const BString& string) const
:::
:::{cpp:function} bool BString::operator==(const char* string) const
:::
:::{cpp:function}  inline bool operator==(const char* string, const BString& string) const
:::

:::{cpp:function} inline bool BString::operator!=(const BString& string) const
:::
:::{cpp:function} inline bool BString::operator!=(const char* string) const
:::

:::{cpp:function}  inline bool operator!=(const char* string, const BString& string) const
:::

:::{cpp:function} inline bool BString::operator<(const BString& string) const
:::
:::{cpp:function} bool BString::operator<(const char* string) const
:::
:::{cpp:function}  inline bool operator<(const char* string, const BString& string) const
:::

:::{cpp:function} inline bool BString::operator>(const BString& string) const
:::
:::{cpp:function} bool BString::operator>(const char* string) const
:::
:::{cpp:function}  inline bool operator>(const char* string, const BString& string) const
:::
:::{cpp:function} inline bool BString::operator>=(const BString& string) const
:::
:::{cpp:function} bool BString::operator>=(const char* string) const
:::
:::{cpp:function}  inline bool operator>=(const char* string, const BString& string) const
:::

Case-sensitive comparison of two strings. Two strings are compared by
comparing the ASCII or UTF-8 values of their respective characters. A
longer string is greater than a shorter (but otherwise similar)
string—"abcdef" is greater than "abcde".

The global versions of these operators are provided so you don't have to
worry about the order of the operands; for example:

:::{code}
if (astring == "Okay")
/* ...is equivalent to... */
if ("Okay" == astring)
:::
::::

