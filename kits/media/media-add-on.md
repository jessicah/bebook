:::{cpp:class} BMediaAddOn
:::

# BMediaAddOn

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BMediaAddOn::BMediaAddOn(image_id image)
:::

This is the {hclass}`BMediaAddOn` constructor; your derived class should
perform whatever initialization is necessary in the constructor, and handle
any activities necessary in order to properly comply with the media add-on
protocol.

The {htype}`image_id` identifies the add-on image from which the add-on
was loaded. Your make_media_addon() function should be sure to save the
image ID passed to it and pass that value through to the
{hclass}`BMediaAddOn` constructor, or the Media Kit will be unhappy with
you.
::::

::::{abi-group}
:::{cpp:function} BMediaAddOn::~BMediaAddOn()()
:::

You should never delete a {hclass}`BMediaAddOn` yourself; the Media Server
will do this when the add-on is no longer needed. However, if you're
implementing a media add-on, this is a good place to handle disposing of
memory you've allocated.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} virtual status_t BMediaAddOn::AutoStart(int32 index, BMediaNode** outNode, int32* outInternalID, bool* outHasMore) = 0
:::

If {cpp:func}`WantsAutoStart() <BMediaAddOn::WantsAutoStart>` returns
{cpp:expr}`true`, you'll get repeated calls to {hmethod}`AutoStart()` when
your add-on is loaded.

Your {hmethod}`AutoStart()` function should be implemented to instantiate
nodes to your liking, one for each call to {hmethod}`AutoStart()`. Each
time {hmethod}`AutoStart()` is called, {hparam}`index` will be one higher
than the previous pass. After creating the new node, store a pointer to it
in {hparam}`outNode`, and set {hparam}`outInternalID` to the internal ID of
the flavor represented by that node.

Before returning, set {hparam}`outHasMore` to {cpp:expr}`true` if there
are more nodes to start, and {cpp:expr}`false` if there aren't.

Return {cpp:enumerator}`B_OK` if you return a valid node. If there aren't
any more nodes to be started, return {cpp:enumerator}`B_BAD_INDEX`. If the
specified index fails, but there may be other nodes to start, return
{cpp:enumerator}`B_ADDON_FAILED`.
::::

::::{abi-group}
:::{cpp:function} virtual int32 BMediaAddOn::CountFlavors()
:::

Implement this hook function to return the number of flavors your add-on
can deal with.
::::

::::{abi-group}
:::{cpp:function} virtual status_t BMediaAddOn::GetConfigurationFor(BMediaNode* node, BMessage* config)
:::

Implement this function to save information about how the given
{hparam}`node` is configured into the specified message. This lets the
node's configuration be saved to disk for future rehydration using
{cpp:func}`InstantiateNodeFor() <BMediaAddOn::InstantiateNodeFor>`.

Note that it's not reasonable to save information about what connections
are routed through the node, since the other nodes probably won't exist
when the node is rehydrated. It's up to the application to reconstruct the
connections itself, as it wishes.

If the configuration information is stashed into {hparam}`config` without
errors, return {cpp:enumerator}`B_OK`; otherwise, return an appropriate
error code.
::::

::::{abi-group}
:::{cpp:function} virtual status_t BMediaAddOn::GetFileFormatList(int32 flavorID, media_file_format* outWritableFormats, int32 inWriteItems, int32* outWriteItems, media_file_format* outReadableFormats, int32 inReadItems, int32* outReadItems, void* reserved)
:::

If your add-on provides nodes that can either read or write media data
from files, you should implement this function to describe the
{htype}`media_file_format`s you can read and write.

On input, the {hparam}`flavorID` argument indicates which flavor you
should return information about. You should fill the array
{hparam}`outWritableFormats` with a list of the file formats the
corresponding flavor can write, and the {hparam}`outReadableFormats` array
with a list of the file formats the flavor can read. The
{hparam}`inWriteItems` and {hparam}`inReadItems` arguments indicate how
many items can be stored in each array.

:::{admonition} Note
:class: note
Both {hparam}`outWritableFormats` and {hparam}`outReadableFormats` can be
{cpp:expr}`NULL`. Don't write into these arrays if the corresponding
pointer is {cpp:expr}`NULL`.
:::

On output, you should set {hparam}`outWriteItems` to be the number of file
formats you can write—even if it's larger than {hparam}`inWriteItems`. This
lets the caller resize the array and call you back to get the complete
list. Likewise, {hparam}`outReadItems` should be set to the number of file
formats you can read.

The {hparam}`reserved` argument isn't currently used, and should always be
specified as {cpp:expr}`NULL`.

:::{admonition} Warning
:class: warning
Only implement this function if your node derives from
{cpp:class}`BFileInterface`.
:::

If an error occurs, return an appropriate error code; otherwise, return
{cpp:enumerator}`B_OK`.
::::

::::{abi-group}
:::{cpp:function} virtual status_t BMediaAddOn::GetFileFormatList(int32 flavorNum, const flavor_info** outInfo)
:::

Implement {hmethod}`GetFlavorAt()` to store in {hparam}`outInfo` a pointer
to a static {htype}`flavor_info` structure describing one flavor supported
by your add-on. The data pointed to by {hparam}`outInfo` will be copied by
the Media Kit after {hmethod}`GetFlavorAt()` returns. For example, if your
add-on only supports one flavor:

:::{code} cpp
flavor_info flavorInfo;

status_t MyMediaAddOn::GetFlavorAt(int32 n, const flavor_info** out_info)
{
   if (n != 0) {
      return B_ERROR;
   }

   flavorInfo->internal_id = n;
   flavorInfo->name = strdup("My Media Node");
   flavorInfo->info = strdup("This node receives video from spy cameras
   at area pizza parlors and determines which one is the least busy.");
   flavorInfo->kinds = B_BUFFER_CONSUMER | B_PHYSICAL_OUTPUT;
   flavorInfo->flavor_flags = 0;
   flavorInfo->possible_count = 0;

   // Set up the list of input formats. We only support
   // raw video input.

   flavorInfo->in_format_count = 1;
   media_format* aFormat = new media_format;
   aFormat->type = B_MEDIA_RAW_VIDEO;
   aFormat->u.raw_video = media_raw_video_format::wildcard;
   flavorInfo->in_formats = aFormat;

   // We don't output.

   flavorInfo->out_format_count = 0;
   flavorInfo->out_formats = 0;

   // And set up the result pointer

   *out_info = flavorInfo;
   return B_OK;
}
:::

:::{admonition} Note
:class: note
If you allocate memory for the {htype}`flavor_info` structure, be sure to
discard it before your add-on is unloaded (the destructor is a good place
to do this). If you forget to discard the memory, you'll leak, and that can
be really embarrassing.
:::

If {hparam}`flavorNum` is greater than {hmethod}`CountFlavors()`-1 (in
other words, if the requested number is larger than the number of flavors
you support), return {cpp:enumerator}`B_ERROR`. Otherwise, return
{cpp:enumerator}`B_OK` or, if an error occurs, an appropriate error code.
::::

::::{abi-group}
:::{cpp:function} image_id BMediaAddOn::ImageID()
:::

Returns the add-on's image ID, as specified by the {hclass}`BMediaAddOn`
{cpp:func}`constructor <BMediaAddOn::BMediaAddOn()>`.

Your make_media_addon() function should be sure to save the image ID
passed to it and pass that value through to the {hclass}`BMediaAddOn`
constructor, or the Media Kit will be unhappy with you.
::::

::::{abi-group}
:::{cpp:function} virtual status_t BMediaAddOn::InitCheck(const char** outFailureText)
:::

Implement this hook function to set {hparam}`outFailureText` to point to a
static text buffer that contains a message explaining why your add-on
failed the most recent operation requested by the Media Server. This
doesn't include errors reported by nodes instantiated by your add-on, but
only to errors caused directly by your {hclass}`BMediaAddOn`-derived
object.

The buffer pointed to by {hparam}`outFailureText` shouldn't go away until
the add-on is reloaded or a new call to {hmethod}`InitCheck()` is made.

Also returned is the actual result code from that operation; if all is
well, {cpp:enumerator}`B_OK` should be returned.
::::

::::{abi-group}
:::{cpp:function} virtual BMediaNode* BMediaAddOn::InstantiateNodeFor(const flavor_info* info, BMessage* config, status_t* outError)
:::

Given the information in {hparam}`info` (which might be a copy of
information you previously returned from a {cpp:func}`GetFlavorAt()
<BMediaAddOn::GetFlavorAt>` call), you should instantiate a new object of
the node class referenced by {hparam}`info`'s {hparam}`internal_id` field
and return a pointer to that node.

The {hparam}`config` message might contain information saved by a previous
instance of the same flavor node, and should be used to configure the new
node if possible. {hparam}`config` will never be {cpp:expr}`NULL`, although
it may not have any fields of interest in it.

The simplest implementation of this function, in which there's no
configuration possible, might look like this:

:::{code} cpp
BMediaNode* BMyConsumerAddOn::InstantiateNodeFor(const flavor_info* info,
            BMessage* config, status_t* outError) {
   return new MyConsumerNode((const char *) "My Consumer Node");
}
:::

If a new instance can't be instantiated, set {hparam}`outError` to an
appropriate error code and return {cpp:expr}`NULL`. Otherwise, set
{hparam}`outError` to {cpp:enumerator}`B_OK`.
::::

::::{abi-group}
:::{cpp:function} virtual status_t BMediaAddOn::SniffRef(const entry_ref& file, BMimeType* outMimeType, float* outQuality, int32* outInternalID)
:::

:::{cpp:function} virtual status_t BMediaAddOn::SniffType(BMimeType& mimeType, float* outQuality, int32* outInternalID)
:::

:::{cpp:function} virtual status_t BMediaAddOn::SniffTypeKind(BMimeType& mimeType, uint64 inKinds, float* outQuality, int32* outInternalID, void* reserved)
:::

If your add-on supports {cpp:class}`BFileInterface` nodes, you may
implement {hmethod}`SniffRef()`. Given the specified {hparam}`file`,
examine the file and set {hparam}`outMimeType` to describe the MIME type of
the file.

Additionally, you can implement {hmethod}`SniffType()` to report how well
your add-on can handle a file containing data of the MIME type specified by
{hparam}`mimeType`.

:::{admonition} Note
:class: note
If your node deals with both producers and consumers, you shouldn't
implement {hmethod}`SniffType()`. Implement {hmethod}`SniffTypeKind()`
instead. If {hmethod}`SniffTypeKind()` is implemented,
{hmethod}`SniffType()` won't be called.
:::

{hmethod}`SniffTypeKind()` limits the search to the kinds indicated by
{hparam}`inKinds`. This lets the caller indicate whether it's looking for a
consumer or a producer, for example.

In any case, you should also store, in {hparam}`outQuality`, a value
representing the quality level at which your add-on can interpret the data
in the file (where 0.0 means you can't handle it well at all and 1.0 means
you can handle it perfectly), and in {hparam}`outInternalID`, the internal
ID of the flavor that handles the data.

:::{admonition} Warning
:class: warning
Don't implement these functions if your add-on doesn't support
{cpp:class}`BFileInterface` nodes.
:::

Return {cpp:enumerator}`B_OK` if you've successfully identified the node;
otherwise, return an appropriate error code.
::::

::::{abi-group}
:::{cpp:function} virtual bool BMediaAddOn::WantsAutoStart()
:::

Implement this hook function to return {hparam}`true` if there are one or
more node flavors supported by your add-on that want to be instantiated
automatically when the add-on is loaded, instead of waiting until they're
explicitly instantiated by an application's request later. Return
{cpp:expr}`false` otherwise.
::::

## Global C Functions

### make_media_addon()



make_media_addon() is the global C function your add-on needs to implement
in order to make itself available to the world. It will be called when the
Media Server loads your add-on, and you should return an instance of your
{hclass}`BMediaAddOn`-derived class, with the appropriate overrides to the
hook functions.

The {hparam}`addonID` argument is your add-on's image ID. Your
make_media_addon() function should be sure to save the image ID passed to
it and pass that value through to the {hclass}`BMediaAddOn`
{cpp:func}`constructor <BMediaAddOn::BMediaAddOn()>`, or the Media Kit will
be unhappy with you.

This function can be quite simple:

:::{code} cpp
BMediaAddOn* make_media_addon(image_id myImage) {
   return new MyConsumerAddOn(myImage);
}
:::

It simply creates an instance of the add-on object (in this case,
{hclass}`MyConsumerAddOn`), and returns it.

## Defined Types

### dormant_flavor_info

Declared in: media/MediaAddOn.h

:::{code} cpp
struct dormant_flavor_info : public flavor_info, public BFlattenable {
   dormant_node_info();
   virtual ~dormant_node_info();
   dormant_flavor_info(const dormant_flavor_info&);
   dormant_flavor_info& operator=(const dormant_flavor_info&);
   dormant_flavor_info& operator=(const flavor_info&);

   dormant_node_info node_info;

   void set_name(const char* in_name);
   void set_info(const char* in_info);
   void add_in_format(const media_format& in_format);
   void add_out_format(const media_format& out_format);

   virtual bool IsFixedSize() const;
   virtual type_code TypeCode() const;
   virtual ssize_t FlattenedSize() const;
   virtual status_t Flatten(void* buffer, ssize_t size) const;
   virtual status_t Unflatten(type_code c, const void* buf, ssize_t size);

private:
   void assign_atoms(const flavor_info& that);
   media_addon_id addon;
   int32 flavor_id;
   char name[B_MEDIA_NAME_LENGTH];
private:
   char reserved[128];
};
:::

The {htype}`dormant_flavor_info` structure describes a flavor in a dormant
node.

### dormant_node_info

Declared in: media/MediaAddOn.h

:::{code} cpp
struct dormant_node_info {
   dormant_node_info();
   ~dormant_node_info();
   media_addon_id addon;
   int32 flavor_id;
   char name[B_MEDIA_NAME_LENGTH];
private:
   char reserved[128];
};
:::

The {htype}`dormant_node_info` structure describes a node that resides in
an add-on and that may not be in memory. You might use it when issuing the
{cpp:func}`BMediaRoster::InstantiateDormantNode` to instantiate a node, for
example.

The {hparam}`addon` field indicates the ID number of the media add-on in
which the node resides, and the {hparam}`flavor_id` is the flavor ID
internal to that add-on indicating which flavor the node should represent.
The {hparam}`name` field is the node's name.

### flavor_info

Declared in: media/MediaAddOn.h

:::{code} cpp
struct flavor_info {
   char* name;
   char* info;
   uint64 kinds;
   uint32 flavor_flags;
   int32 internal_id;
   int32 possible_count;

   int32 in_format_count;
   uint32 in_format_flags;
   const media_format* in_formats;

   int32 out_format_count;
   uint32 out_format_flags;
   const media_format* out_formats;

   uint32 _reserved_[16];

private:
   flavor_info& operator=(const flavor_info& other);
};
:::

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Field

	- Description

-
	- nameandinfo
	- Provide a human-readable name, and information about the flavor.
-
	- kinds
	- Should be set to the node kind. See {ref}`node_kind`
-
	- flavor_flags
	- Contains flags providing additional information about the flavor.

		{cpp:enumerator}`B_FLAVOR_IS_GLOBAL`

		: The flavor will be forced into the Media Add-on Server, and only one
		instance of it will exist.

		{cpp:enumerator}`B_FLAVOR_IS_LOCAL`

		: The flavor will be forced into the loading application, and many instances
		of it may exist.

		If neither flag is specified, the Media Kit will decide what to do with
		the flavor.
-
	- internal_id
	- Is an internal ID number that your add-on can use to identify the flavor;
		the flavor will be requested by the Media Kit using this ID number.
-
	- possible_count
	- Specifies to the Media Kit the maximum number of instances of your node
		can be in existence at the same time. For example, if your node provides
		support for a particular sound card, this value should be equal to the
		number of cards you support that are currently installed in the computer.
-
	- in_format_count
	- Specifies how many input formats the flavor supports.
-
	- in_formats
	- Is a list of all the input formats supported by the flavor.
-
	- in_format_flags
	- Provides informational flags about the flavor's inputs. There currently
		aren't any defined flags, so set this field to 0.
-
	- out_format_count
	- Specifies how many output formats the flavor supports.
-
	- out_formats
	- Is a list of all the output formats supported by the flavor.
-
	- out_format_flags
	- Provides informational flags about the flavor's outputs. There currently
		aren't any defined flags, so set this field to 0.

:::
