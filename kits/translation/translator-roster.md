# BTranslatorRoster

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BTranslatorRoster::BTranslatorRoster()
:::
:::{cpp:function} BTranslatorRoster::BTranslatorRoster(BMessage* model)
:::

Creates a new container for translators. The no-argument constructor
creates an empty container. The
{cpp:class}`BMessage`
constructor loads all the
translators from the directories specified in the be:translator_path
named fields in {hparam}`model`.

If you just want to load the translators from the standard directories,
you can instead use the static member
{cpp:func}`~BTranslatorRoster::Default`
described below.

See also:
{cpp:func}`~BTranslatorRoster::AddTranslators`

::::

::::{abi-group}
:::{cpp:function} BTranslatorRoster::~BTranslatorRoster()
:::

Unloads any translators that were loaded and frees all memory allocated
by the {hclass}`BTranslatorRoster`.

::::

## Member Functions

::::{abi-group}
:::{cpp:function} virtual status_t BTranslatorRoster::AddTranslators(const char* load_path = NULL)
:::

Loads all the translators located in the colon-deliminated list of files
and directories found in {hparam}`load_path`. All specified paths must be absolute.
If {hparam}`load_path` is NULL, it loads the translators from the locations
specified in the TRANSLATORS environment variable. If the environment
variable is not defined, then it loads all the files in the default
directories /boot/home/config/add-ons/Translators,
/boot/home/config/add-ons/Datatypes, and
/system/add-ons/Translators.

:::{list-table}
:::

See also:
{cpp:func}`~BTranslatorRoster::Default`
static function

::::

::::{abi-group}
:::{cpp:function} virtual status_t BTranslatorRoster::Archive(BMessage* into, bool* deep = true) const
:::

Archives the {hclass}`BTranslatorRoster` by recording its loaded add-ons in the
{cpp:class}`BMessage` into.

See also:
{cpp:func}`BArchivable::Archive`,
{cpp:func}`~BTranslatorRoster::Instantiate`
static function

::::

::::{abi-group}
:::{cpp:function} virtual status_t BTranslatorRoster::GetAllTranslators(translator_id** outList, int32* outCount) const
:::

Returns, in {hparam}`outList`, an array of all the translators loaded by the
{hclass}`BTranslationRoster`. The number of elements in the array is placed in
{hparam}`outCount`. The application assumes responsibility for deallocating the
array.

:::{list-table}
:::

See also:
{cpp:func}`~BTranslatorRoster::Identify`,
{cpp:func}`~BTranslatorRoster::GetTranslators`,
{cpp:func}`~BTranslatorRoster::GetAllTranslators`

::::

::::{abi-group}
:::{cpp:function} virtual status_t BTranslatorRoster::GetConfigurationMessage(translator_id forTranslator, BMessage* ioExtension)
:::

Saves the current configuration information for
translator {hparam}`forTranslator`
in {hparam}`ioExtension`. This information may be flattened, unflattened, and
passed to
{cpp:func}`~BTranslatorRoster::Translate`
to configure it.

:::{list-table}
:::

See also:
{cpp:func}`~BTranslatorRoster::MakeConfigurationView`,
{cpp:func}`~BTranslatorRoster::Translate`

::::

::::{abi-group}
:::{cpp:function} virtual status_t BTranslatorRoster::GetInputFormats(translator_id forTranslator, const translation_format** outFormats, int32* outNumFormats)
:::
:::{cpp:function} virtual status_t BTranslatorRoster::GetOutputFormats(translator_id forTranslator, const translation_format** outFormats, int32* outNumFormats)
:::

Returns an array of the published accepted input or output formats for
translator forTranslator. outNumFormats is filled with the number of
elements in the array.

:::{list-table}
:::

See also:
{cpp:func}`~BTranslatorRoster::GetTranslatorInfo`

::::

::::{abi-group}
:::{cpp:function} virtual status_t BTranslatorRoster::GetTranslatorInfo(translator_id forTranslator, const char** outName, const char** outInfo, int32* outNumFormats)
:::

Returns public information about translator {hparam}`forTranslator`.
Sets {hparam}`outName`
with a short description of the translator, {hparam}`outInfo` with a longer
description, and {hparam}`outVersion` with the translator's version number.

:::{list-table}
:::

See also:
{cpp:func}`~BTranslatorRoster::GetInputFormats`,
{cpp:func}`~BTranslatorRoster::GetOutputFormats`

::::

::::{abi-group}
:::{cpp:function} virtual status_t BTranslatorRoster::GetTranslators(BPositionIO* inSource, BMessage* ioExtension, translator_info** outInfo, int32* outNumInfo, uint32 inHintType = 0, const char** inHintMIME = NULL, uint32 inWantType = 0)
:::

Identifies the media in {hparam}`inSource`, returning an
array of valid formats and translators equipped to handle them in
{hparam}`outInfo`. {hparam}`outNumInfo` holds the
number of elements in the array. If {hparam}`inHintType` or
{hparam}`inHintMIME` is specified, only those translators that
can accept data of the specified type are searched. If
{hparam}`inWantType` is specified, only those translators that
can output data of that type are searched.
{hparam}`ioExtension` offers an opportunity for the
application to specify additional configuration information to the add-ons.
The application assumes responsibility for deallocating the array.

:::{list-table}
:::

See also:
{cpp:func}`~BTranslatorRoster::Identify`,
{cpp:func}`~BTranslatorRoster::GetAllTranslators`

::::

::::{abi-group}
:::{cpp:function} virtual status_t BTranslatorRoster::Identify(BPositionIO* inSource, BMessage* ioExtension, translator_info* outInfo, uint32 inHintType = 0, const char** inHintMIME = NULL, uint32 inWantType = 0)
:::

Identifies the media in {hparam}`inSource`, returning a
best guess of the format and the translator best equipped to handle it in
{hparam}`outInfo`. If {hparam}`inHintType` or
{hparam}`inHintMIME` is specified, only those translators that
can accept data of the specified type are searched. If
{hparam}`inWantType` is specified, only those translators that
can output data of that type are searched.
{hparam}`ioExtension` offers an opportunity for the
application to specify additional configuration information to the
add-ons.

If more than one translator can identify {hparam}`inSource`,
then the one with the highest quality*capability is returned.

:::{list-table}
:::

See also:
{cpp:func}`~BTranslatorRoster::GetTranslators`,
{cpp:func}`~BTranslatorRoster::GetAllTranslators`

::::

::::{abi-group}
:::{cpp:function} virtual status_t BTranslatorRoster::MakeConfigurationView(translator_id forTranslator, BMessage* ioExtension, BView** outView, BRect* outExtent)
:::

Returns, in {hparam}`outView`, a
{cpp:class}`BView` containing
controls to configure translator
{hparam}`forTranslator`. It is the application's responsibility to attach the
{cpp:class}`BView`
to a
{cpp:class}`BWindow`.
The initial size of the
{cpp:class}`BView` is given in
{hparam}`outExtent` but may
be resized by the application.

:::{list-table}
:::

See also:
{cpp:func}`~BTranslatorRoster::GetConfigurationMessage`,
{cpp:func}`~BTranslatorRoster::Translate`

::::

::::{abi-group}
:::{cpp:function} virtual status_t BTranslatorRoster::Translate(BPositionIO* inSource, const translator_info* inInfo, BMessage* ioExtension, BPositionIO* outDestination, uint32 inWantOutType, uint32 inHintType = 0, const char* inHintMIME = NULL)
:::
:::{cpp:function} virtual status_t BTranslatorRoster::Translate(translator_id inTranslator, BPositionIO* inSource, BMessage* ioExtension, BPositionIO* outDestination, uint32 inWantOutType)
:::

These two functions carry out data conversion, converting the data in
{hparam}`inSource` to type
{hparam}`inWantoutType` and placing the resulting output in
{hparam}`outDestination`. {hparam}`inInfo` should
always contain either the output of an
{cpp:func}`~BTranslatorRoster::Identify`
call or NULL. The translation uses the translator identified
by `inInfo->infoTranslator`
or {hparam}`inTranslator` as appropriate. If {hparam}`inInfo` is
NULL, {hmethod}`Translate()` will call first
{cpp:func}`~BTranslatorRoster::Identify`
to discover the format of
the input stream. {hparam}`ioExtension`, if it is not NULL, provides a
communication path between the translator and the application. {hparam}`inHintType`
and {hparam}`inHintMIME`, if provided, are passed as hints to the translator.

:::{list-table}
:::

::::

## Static Functions

::::{abi-group}
:::{cpp:function} BTranslatorRoster* BTranslatorRoster::Default()
:::

This returns a {hclass}`BTranslatorRoster` loaded with the default set of
translators, loaded from the colon-deliminated list of files and
directories found in the environment variable TRANSLATORS. If no such
variable exists, the translators are loaded from the default locations
/boot/home/config/add-ons/Translators,
/boot/home/config/add-ons/Datatypes, and
/system/add-ons/Translators.

The instance of {hclass}`BTranslatorRoster` returned by this function is global to
the application and should not be deleted. Although you can add
translators to the returned {hclass}`BTranslatorRoster`, this is not recommended.
It's better to use a new instance of the class.

See also:
{cpp:func}`~BTranslatorRoster::AddTranslators`

::::

::::{abi-group}
:::{cpp:function} BTranslatorRoster* BTranslatorRoster::Instantiate(BMessage* from)
:::

Returns a new {hclass}`BTranslatorRoster`
object, allocated by new and created with
the version of the constructor that takes a
{cpp:class}`BMessage`
archive. However, if the archive doesn't contain data for a
{hclass}`BTranslatorRoster` object,
{hmethod}`Instantiate()` returns NULL.

See also:
{cpp:func}`BArchivable::Instantiate`,
{cpp:func}`~instantiate::object`,
{cpp:func}`~BTranslatorRoster::Archive`

::::

::::{abi-group}
:::{cpp:function} const char* BTranslatorRoster::Version(int32* outCurVersion, int32* outMinVersion, int32* inAppVersion = B_TRANSLATION_CURRENT_VERSION)
:::

Sets {hparam}`outCurVersion` to the Translation Kit
protocol version number and {hparam}`outMinVersion` to the
minimum protocol version number supported. Returns a human-readable string
containing version information. Currently,
{hparam}`inAppVersion` must be
B_TRANSLATION_CURRENT_VERSION.

::::

## Archived Fields

The {cpp:func}`~BTranslatorRoster::Archive()` function adds the following field
to its {cpp:class}`BMessage` argument:

:::{list-table}
---
header-rows: 1
---

-
	- Field
	- Type code
	- Description
-
	- `be:translator_path` (array)
	- {cpp:enum}`B_STRING_TYPE`
	- The location of the Translation Kit add-on (one field per add-on).
:::
