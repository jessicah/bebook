:::{cpp:class} BTranslator
:::

# BTranslator

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BTranslator::BTranslator()
:::

The constructor must create and return a new instance of your
{hclass}`BTranslator` subclass. Note that the constructor doesn't
{cpp:func}`Acquire() <BTranslator::Acquire>` the object it returns.
::::

::::{abi-group}
:::{cpp:function} BTranslator::~BTranslator()
:::

Note that the destructor is protected; you can only delete a
{hclass}`BTranslator` object from within the implementation of the
subclass. From outside the class, you call {cpp:func}`Release()
<BTranslator::Release>`.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} BTranslator* BTranslator::Acquire()
:::

:::{cpp:function} BTranslator* BTranslator::Release()
:::

:::{cpp:function} int32 BTranslator::ReferenceCount()
:::

:::{admonition} Warning
:class: warning
{hmethod}`ReferenceCount()` Is For Debugging use only!
:::

{hmethod}`Acquire()` and {hmethod}`Release()` increment and decrement the
object's reference count. The count starts at 1 (i.e .the object is
implicitly acquired when it's created); if the count falls to 0, the object
is deleted.

When you add a {hclass}`BTranslator` to a {cpp:class}`BTranslatorRoster`,
the {hclass}`BTranslator` is automatically {hmethod}`Acquire()`'d. When the
{cpp:class}`BTranslatorRoster` is deleted, its {hclass}`BTranslator`s are
{hmethod}`Release()`'d. Thus, when you instantiate a {hclass}`BTranslator`
and add it to a {cpp:class}`BTranslatorRoster`, you and the Roster maintain
joint ownership of the object. To give up ownership (such that the
{cpp:class}`BTranslatorRoster` will destroy the object when the Roster
itself is destroyed), call {hmethod}`Release()` after adding the
{hclass}`BTranslator` to the Roster.

{hmethod}`Acquire()` and {hmethod}`Release()` both return a pointer to the
{hclass}`BTranslator` that was just acquired or released. If
{hmethod}`Release()` caused the object to be deleted, it retruns
{cpp:expr}`NULL`.

{hmethod}`ReferenceCount()`, which returns the current reference count
value, is meant for debugging purposes only. It is not thread-safe! Don't
predicate your code on the value it returns.
::::

::::{abi-group}
:::{cpp:function} virtual status_t BTranslator::GetConfigurationMessage(BMessage* ioExtension)
:::

Hook function that asks the object to write its current state into the
{cpp:class}`BMessage`* argument. See {ref}`GetConfigMessage()` [Translator
Add-ons] for details.
::::

::::{abi-group}
:::{cpp:function} virtual status_t BTranslator::Identify(BPositionIO* inSource, const translation_format* inFormat, BMessage* ioExtension, translator_info* outInfo, uint32* outType) = 0
:::

Hook function called by the Translator Roster to ask the
{hclass}`BTranslator` if it knows how to convert {hparam}`inSource` into
the type described by {hparam}`outType`. See {ref}`Identify()` [Translator
Add-ons] for details.
::::

::::{abi-group}
:::{cpp:function} virtual const translation_format* BTranslator::InputFormats(int32* count) const
:::

:::{cpp:function} virtual const translation_format* BTranslator::OutputFormats(int32* count) const
:::

These functions should be implemented to return arrays of
{htype}`translation_format` structures that describe the formats that this
object supports. If the functions aren't implemented, the object's
{cpp:func}`Identify() <BTranslator::Identify>` function will be called each
time an application requests a translation. Both functions should set
{hparam}`count` to the number of elements in the format array.

:::{admonition} Important
:class: important
Unlike the analogous translator add-on format arrays, the arrays returned
by these functions don't have to be terminated by an empty
{htype}`translation_format` structure.
:::
::::

::::{abi-group}
:::{cpp:function} virtual status_t BTranslator::MakeConfigurationView(BMessage* ioExtension, BView** outView, BRect* outExtent)
:::

Hook function that lets the {hclass}`BTranslator` supply a configuration
view. See {ref}`MakeConfig()` [Translator Add-ons] for details.
::::

::::{abi-group}
:::{cpp:function} virtual status_t BTranslator::MakeConfigurationView(BPositionIO* inSource, const translator_info* inInfo, BMessage* ioExtension, uint32* outType, BPositionIO* outDestination) = 0
:::

Hook function that asks the {hclass}`BTranslator` to translate data from
{hparam}`inSource` to format {hparam}`outType`, writing the output to
{hparam}`outDestination`. See {cpp:func}`Translate()
<BTranslator::Translate>` [Translator Add-ons] for details.
::::

::::{abi-group}
:::{cpp:function} virtual const char * BTranslator::TranslatorInfo() const = 0
:::

:::{cpp:function} virtual const char * BTranslator::TranslatorName() const = 0
:::

:::{cpp:function} virtual int32 BTranslator::TranslatorVersion() const = 0
:::

{hmethod}`TranslatorInfo()` returns a pointer to the translator's long
name, e.g. "aiff translator by the Pie Man (pie@the.man)".

{hmethod}`TranslatorName()` returns a pointer to the translator's short
name, e.g. "aiff translator". The short name should be appropriate for
display in a menu.

{hmethod}`TranslatorVersion()` gives an "MM.mm" version number for the
translator. For example, a {hmethod}`TranslatorVersion()` of 314 is
interpreted as version 3.14.
::::
