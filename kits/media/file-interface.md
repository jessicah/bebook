# BFileInterface
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BFileInterface::BFileInterface()
:::
Constructor.
::::

## Member Functions
::::{abi-group}

:::{cpp:function} virtual void BFileInterface::DisposeFileFormatCookie(int32 cookie) = 0
:::
This function must be implemented to dispose of a {hparam}`cookie` used for
iterating over file formats your node supports. If the cookie is a
reference to a data block, you should free it; otherwise, you can just
return without doing anything.
::::

::::{abi-group}

:::{cpp:function} virtual status_t BFileInterface::HandleMessage(int32 message, const void* data, size_t size)
:::
Implement this function to handle messages that arrive on your control
port; see
{cpp:func}`BMediaNode::HandleMessage`
for details.
::::

::::{abi-group}

:::{cpp:function} virtual status_t BFileInterface::GetDuration(bigtime_t* outDuration) = 0
:::
Implement this function to return in {hparam}`outDuration` the duration, in
microseconds of the media data in the file currently being worked on.
If there is no file in use, or the file isn't valid, return a negative
error code; otherwise, return {cpp:enum}`B_OK`.
::::

::::{abi-group}

:::{cpp:function} virtual status_t BFileInterface::GetNextFileFormat(int32* cookie, media_file_format* outFormat) = 0
:::
The first time this function is called, {hparam}`cookie` will be 0. Return
information about the first file format you support in {hparam}`outFormat` and set
cookie to some meaningful (non-zero) value that you can use to track
where you are in the list of formats you support, then return {cpp:enum}`B_OK`.
On successive calls to {hmethod}`GetNextFileFormat()`, you should return successive
file format information and change {hparam}`cookie` as necessary to remember where
you are in the list. Return {cpp:enum}`B_OK` each time you successfully return
information about a file format.
Once you run out of formats, return {cpp:enum}`B_ERROR`.
::::

::::{abi-group}

:::{cpp:function} virtual status_t BFileInterface::GetRef(const entry_ref* outRef, BMimeType* outMimeType) = 0
:::
:::{cpp:function} virtual status_t BFileInterface::SetRef(const entry_ref& file, bool create, bigtime_t* outDuration) = 0
:::
Implement {hmethod}`GetRef()` function to return,
in {hparam}`outRef`, the entry_ref of the
file with which the node is currently working. You should also return the
MIME type of the file in {hparam}`outMimeType`.
When an application or other client wants your node to use a specific
file, the {hmethod}`SetRef()` function will be called. The file to be used is
specified by {hparam}`file`, which may or may not exist.
If {hparam}`create` is {cpp:enum}`true`, you
should create a new file (erasing an existing file, if one's already
there), initialize the file for writing, then store 0 in {hparam}`outDuration`.
If {hparam}`create` is {cpp:enum}`false`,
you should open the existing file and put the actual
running time of the file into {hparam}`outDuration`.
Return {cpp:enum}`B_OK` if successful; otherwise, return a negative error code, as
appropriate. If you forget to implement these functions, they'll always
return {cpp:enum}`B_ERROR`.
::::

::::{abi-group}

:::{cpp:function} virtual status_t BFileInterface::SniffRef(const entry_ref* file, char* outMimeType, float* outQuality) = 0
:::
When the system (or an application program) finds an unknown file, it can
call {cpp:class}`BMediaRoster`
to try to identify the file. Your node's {hmethod}`SniffRef()`
function will be called so your node can look at the file.
Inspect the file referenced by file. If you can handle the format, set
{hparam}`outMimeType` to the MIME
type of the file format (the buffer is 256 bytes
long), and set {hparam}`outQuality` to indicate how well you can process the file
(where 0.0 means you can't handle it at all and 1.0 means the file format
is a privately-owned format that your application handles perfectly).
If you know how to identify the file, but not how to play or record it,
return 0.0 for {hparam}`outQuality`.
If you know how to decode only some parts of the file, but not all of
them, set {hparam}`outQuality` to 0.4 or to 0.6 if you can handle both audio and
video contained in the file, but not other forms of media data that are
present.
Set {hparam}`outQuality` to 0.9 if
you can handle the format very well, but it's a
publicly-defined format whose specifications you don't control. You
should only return an {hparam}`outQuality` value of 1.0 if the file format
specifications are in your control and you implement them perfectly.
Interpolate between these values to give the best estimate you can of
your ability to handle the file, so selection of the most suitable node
can be made. For instance, if your node does low-quality but high-speed
processing of an audio format, you might subtract a little bit from the
{hparam}`outQuality` value you might otherwise return.
Return {cpp:enum}`B_OK` if you successfully sniff the file and have something to say
about its contents; otherwise return an appropriate error code. If you
don't know the file format at all, you should return {cpp:enum}`B_MEDIA_NO_HANDLER`.
::::
