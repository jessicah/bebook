# BTranslationUtils
## Constructor and Destructor
## Static Functions
::::{abi-group}

:::{cpp:function} static BBitmap BTranslationUtils::GetBitmap(const char* name, BTranslatorRoster name = NULL)
:::
:::{cpp:function} static BBitmap BTranslationUtils::GetBitmap(entry_ref ref, BTranslatorRoster name = NULL)
:::
:::{cpp:function} static BBitmap BTranslationUtils::GetBitmap(uint32 type, int32 id, BTranslatorRoster name = NULL)
:::
:::{cpp:function} static BBitmap BTranslationUtils::GetBitmap(uint32 type, const char* name, BTranslatorRoster name = NULL)
:::
:::{cpp:function} static BBitmap BTranslationUtils::GetBitmap(BPositionIO stream = NULL, BTranslatorRoster name = NULL)
:::
The first version of the function returns the image held in the file {hparam}`name`
if it exists. Otherwise, it returns the application resource of type
{cpp:enum}`B_TRANSLATOR_BITMAP` named {hparam}`name`.
The second version does the same thing,
but uses an entry_ref, {hparam}`ref`, to locate the file.
The third and fourth versions of the function search for the specified
resource and return the bitmap contained therein.
The final version returns the bitmap found in {hparam}`stream`. This form of the
function is particularly useful when used with
{cpp:class}`BMemoryIO`.
In all cases, {hparam}`use` specifies the {hclass}`BTranslatorRoster` to use in translating
the image. If {hparam}`use` is {cpp:enum}`NULL`, the default translator (as returned by
{cpp:func}`BTranslatorRoster::Default`)
is used.
If the file or stream doesn't contain a suitable bitmap, the functions
return {cpp:enum}`NULL`.
::::

::::{abi-group}

:::{cpp:function} static BBitmap BTranslationUtils::GetBitmapFile(const char* name, BTranslatorRoster name = NULL)
:::
Returns the image held in the file {hparam}`name`. If
the file doesn't contain a suitable image, the function returns
{cpp:enum}`NULL`. {hparam}`use` specifies the
{hclass}`BTranslatorRoster` used to translate the image. If
{hparam}`use` is {cpp:enum}`NULL`, the default
translator (as returned by
{cpp:func}`BTranslatorRoster::Default`)
is used.
::::
