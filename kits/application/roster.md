# BRoster
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BRoster::BRoster()
:::
Sets up the object's connection to the roster service.
When an application constructs its
{cpp:class}`BApplication` object, the system
constructs a {hclass}`BRoster` object and assigns it to the
{cpp:func}`~BRoster::be` global variable. A {hclass}`BRoster` is
therefore readily available from the time the
application is initialized until the time it quits; you don't have to
construct one. The constructor is public only to give programs that don't
have {cpp:class}`BApplication`
objects access to the roster.
::::

::::{abi-group}

:::{cpp:function} BRoster::~BRoster()
:::
Does nothing.
::::

## Member Functions
::::{abi-group}

:::{cpp:function} status_t BRoster::ActivateApp(team_id team) const
:::

Activates the {hparam}`team` application (by bringing one of its windows to the
front and making it the active window). This function works only if the
target application has a window on-screen. The newly activated
application is notified with a {cpp:enum}`B_APP_ACTIVATED` message.

See also:
{cpp:func}`BApplication::AppActivated`

::::

::::{abi-group}

:::{cpp:function} void BRoster::AddToRecentDocuments(const entry_ref* document, const char* appSig = NULL) const
:::
:::{cpp:function} void BRoster::GetRecentDocuments(BMessage* refList, int32 maxCount, const char* ofType = NULL, const char* openedByAppSig = NULL) const
:::
:::{cpp:function} void BRoster::GetRecentDocuments(BMessage* refList, int32 maxCount, const char* ofTypeList[] = NULL, int32 ofTypeListCount, const char* openedByAppSig = NULL) const
:::

{hmethod}`AddToRecentDocuments()` adds the document file
specified by {hparam}`document` to
the list of recent documents. If you wish to record that a specific
application used the document, you can specify the signature of that
application using the {hparam}`appSig` argument; otherwise
you can specify {cpp:enum}`NULL`.

{hmethod}`GetRecentDocuments()` returns a list of the most recent documents. The
{cpp:class}`BMessage`
{hparam}`refList` will be filled out with information about the
{hparam}`maxCount` most recently used documents. If you want to
obtain a list of documents
of a specific type, you can specify a pointer to that MIME type string in
the {hparam}`ofType` argument. Likewise, if you're only interested in files that
want to be opened by a specific application, specify that application's
signature in {hparam}`openedByAppSig`; if you don't care, pass
{cpp:enum}`NULL`.

If you want to get a list of files of multiple types, you can specify a
pointer to an array of strings in {hparam}`ofTypeList`, and the number of types in
the list in {hparam}`ofTypeListCount`.

Specifying {cpp:enum}`NULL` for {hparam}`ofType` will fetch all files of all types.

The resulting {hparam}`refList` will have a field,
refs, containing the
entry_refs to the resulting list of files.

::::

::::{abi-group}

:::{cpp:function} void BRoster::AddToRecentFolders(const entry_ref* folder, const char* appSig = NULL) const
:::
:::{cpp:function} void BRoster::GetRecentFolders(BMessage* refList, int32 maxCount, const char* openedByAppSig = NULL) const
:::

{hmethod}`AddToRecentFolders()` adds the folder specified by {hparam}`folder` to the list of
recent folders. If you wish to record that a specific application used
the folder, you can specify the signature of that application using the
{hparam}`appSig` argument; otherwise you can use {cpp:enum}`NULL`.

{hmethod}`GetRecentFolders()` returns a list of the most recently-accessed folders.
The {cpp:class}`BMessage` {hparam}`refList` will be filled out with information about the
{hparam}`maxCount` most recently used folders. If you're only interested in folders
that were used by a specific application, specify that application's
signature in {hparam}`openedByAppSig`; if you don't care, pass {cpp:enum}`NULL`.

The resulting {hparam}`refList` will have a field,
refs, containing the
entry_refs to the resulting list of folders.

::::

::::{abi-group}

:::{cpp:function} status_t BRoster::Broadcast(BMessage* message) const
:::
:::{cpp:function} status_t BRoster::Broadcast(BMessage* message, BMessenger reply_to) const
:::

Sends the {hparam}`message` to every running application, except to those
applications ({cpp:enum}`B_ARGV_ONLY`) that don't accept messages. The {hparam}`message` is
sent asynchronously with a timeout of 0. As is the case for other
message-sending functions, the caller retains ownership of the message.

This function returns immediately after setting up the broadcast
operation. It doesn't wait for the messages to be sent and doesn't report
any errors encountered when they are. It returns an error only if it
can't start the broadcast operation. If successful in getting the
operation started, it returns {cpp:enum}`B_OK`.

Replies to the broadcasted {hparam}`message` will be sent via the {hparam}`reply_to`
{cpp:class}`BMessenger`, if specified. If {hparam}`reply_to` is absent, the replies will be lost.

See also: {cpp:func}`BMessenger::SendMessage`

::::

::::{abi-group}

:::{cpp:function} status_t BRoster::FindApp(const char* type, entry_ref* app) const
:::
:::{cpp:function} status_t BRoster::FindApp(entry_ref* file, entry_ref* app) const
:::

Finds the application associated with the MIME data {hparam}`type` or with the
specified {hparam}`file`, and modifies the {hparam}`app` entry_ref structure so that it
refers to the executable file for that application. If the {hparam}`type` is an
application signature, this function finds the application that has that
signature. Otherwise, it finds the preferred application for the {hparam}`type`. If
the {hparam}`file` is an application executable, {hmethod}`FindApp()` merely copies the file
reference to the {hparam}`app` argument. Otherwise, it finds the preferred
application for the filetype.

In other words, this function goes about finding an application in the
same way that {cpp:func}`~BRoster::Launch`
finds the application it will launch.

If it can translate the {hparam}`type` or {hparam}`file` into a reference to an application
executable, {hmethod}`FindApp()` returns {cpp:enum}`B_OK`. If not, it returns an error code,
typically one describing a file system error.

See also: {cpp:func}`~BRoster::Launch`

::::

::::{abi-group}

:::{cpp:function} status_t BRoster::GetAppInfo(const char* signature, app_info* appInfo) const
:::
:::{cpp:function} status_t BRoster::GetAppInfo(entry_ref* executable, app_info* appInfo) const
:::
:::{cpp:function} status_t BRoster::GetRunningAppInfo(team_id team, app_info* appInfo) const
:::
:::{cpp:function} status_t BRoster::GetActiveAppInfo(app_info* appInfo) const
:::

These functions return (in {hparam}`appInfo`) information about a specific
application. In all cases, the application must be running.

{hmethod}`GetAppInfo()` finds an app that has the
given {hparam}`signature`, or that was launched from the
{hparam}`executable` file. If there's more than one such
app, the function chooses one at random.
{hmethod}`GetRunningAppInfo()` reports on the app
that corresponds to the given {hparam}`team`
identifier.
{hmethod}`GetActiveAppInfo()` reports on the
currently active app.
 If they're able to fill in the
{cpp:func}`~app::info`
structure with meaningful values, these functions return
{cpp:enum}`B_OK`.
{hmethod}`GetActiveAppInfo()` returns
{cpp:enum}`B_ERROR` if there's no active application.
{hmethod}`GetRunningAppInfo()` returns
{cpp:enum}`B_BAD_TEAM_ID` if {hparam}`team`
isn't a valid team identifier for a running application.
{hmethod}`GetAppInfo()` returns
{cpp:enum}`B_ERROR` if the application isn't running.

The app_info structure contains the following fields:

:::{list-table}
---
header-rows: 1
---
-
	- Field
	- Description
-
	- thread_idthread
	- The identifier for the application's main thread of execution, or -1 if the application isn't running. (The main thread is the thread in which the application is launched and in which its main() function runs.)
-
	- thread_idteam
	- The identifier for the application's team, or -1 if the application isn't running. (This will be the same as the team passed to {hmethod}`GetRunningAppInfo()`.)
-
	- port_idport
	- The port where the application's main thread receives messages, or -1 if the application isn't running.
-
	- uint32flags
	- A bitfield that contains information about the behavior of the application.The flags bitfield can be tested (with the bitwise & operator) against these two constants:B_BACKGROUND_APP.The application won't appear in the Deskbar's application list.B_ARGV_ONLY.The application can't receive messages. Information can be passed to it at launch only, in an array of argument strings (as on the command line).flags also contains a value that explains the application's launch behavior. This value is retrieved by masking flags with the {cpp:enum}`B_LAUNCH_MASK` constant. For example:unit32 behavior = theInfo.flags & B_LAUNCH_MASK;The result will match one of these three modes:B_EXCLUSIVE_LAUNCH.The application can be launched only if an application with the same signature isn't already running.B_SINGLE_LAUNCH.The application can be launched only once from the same executable file. However, an application with the same signature might be launched from a different executable. For example, if the user copies an executable file to another directory, a separate instance of the application can be launched from each copy.B_MULTIPLE_LAUNCH.There are no restrictions. The application can be launched any number of times from the same executable file.These modes affect {hclass}`BRoster`'s {hmethod}`Launch()` function. {hmethod}`Launch()` can always start up a {cpp:enum}`B_MULTIPLE_LAUNCH` application. However, it can't launch a {cpp:enum}`B_SINGLE_LAUNCH` application if a running application was already launched from the same executable file. It can't launch a {cpp:enum}`B_EXCLUSIVE_LAUNCH` application if an application with the same signature is already running.
-
	- entry_refref
	- A reference to the file that was, or could be, executed to run the application. (This will be the same as the executable passed to {hmethod}`GetAppInfo()`.)
-
	- char[]signature
	- The signature of the application. (This will be the same as the signature passed to {hmethod}`GetAppInfo()`.)
:::

See also:
{cpp:func}`~BRoster::Launch`,
{cpp:func}`BApplication::GetAppInfo`

::::

::::{abi-group}

:::{cpp:function} void BRoster::GetAppList(BList* teams) const
:::
:::{cpp:function} void BRoster::GetAppList(const char* signature, BList* teams) const
:::

Fills in the {hparam}`teams` {cpp:class}`BList`
with team identifiers for applications in the
roster. Each item in the list will be of type team_id. It must be cast to
that type when retrieving it from the list, as follows:

:::{code}
BList* teams = new BList;
be_roster->GetAppList(teams);
team_id who = (team_id)teams->ItemAt(someIndex);
:::

The list will contain one item for each instance of an application that's
running. For example, if the same application has been launched three
times, the list will include the team_ids for all three running instances
of that application.

If a {hparam}`signature` is passed, the list identifies only applications running
under that signature. If a {hparam}`signature` isn't specified, the list identifies
all running applications.

See also:
{cpp:func}`~BRoster::TeamFor`, the
{cpp:func}`~BMessenger::Constructor`

::::

::::{abi-group}

:::{cpp:function} void BRoster::GetRecentApps(BMessage* refList, int32 maxCount) const
:::

{hmethod}`GetRecentApps()` returns a list of the most recently-launched
applications. The {cpp:class}`BMessage`
{hparam}`refList` will be filled out with information
about the {hparam}`maxCount` most recently-launched applications.

The resulting {hparam}`refList` will have a field, "refs", containing the
entry_refs to the resulting applications.

::::

::::{abi-group}

:::{cpp:function} status_t BRoster::Launch(const char* type, BMessage* message = NULL, team_id* team = NULL) const
:::
:::{cpp:function} status_t BRoster::Launch(const char* type, BList* messages, team_id* team = NULL) const
:::
:::{cpp:function} status_t BRoster::Launch(const char* type, int argc, char** argv, team_id* team = NULL) const
:::
:::{cpp:function} status_t BRoster::Launch(const entry_ref* file, const BMessage* message = NULL, team_id* team = NULL) const
:::
:::{cpp:function} status_t BRoster::Launch(const entry_ref* file, const BList* messages, team_id* team = NULL) const
:::
:::{cpp:function} status_t BRoster::Launch(const entry_ref* file, int argc, char** argv, team_id* team = NULL) const
:::

Launches the application associated with a MIME {hparam}`type` or with a particular
{hparam}`file`. If the MIME {hparam}`type` is an application signature, this function
launches the application with that signature. Otherwise, it launches the
preferred application for the type. If the {hparam}`file` is an application
executable, it launches that application. Otherwise, it launches the
preferred application for the file type and passes the {hparam}`file` reference to
the application in a {cpp:enum}`B_REFS_RECEIVED` message. In other words, {hmethod}`Launch()`
finds the application to launch just as {cpp:func}`~BRoster::FindApp` finds the application
for a particular {hparam}`type` or {hparam}`file`.

If a {hparam}`message` is specified, it will be sent to the application on-launch
where it will be received and responded to before the application is
notified that it's ready to run. Similarly, if a list of {hparam}`messages` is
specified, each one will be delivered on-launch. The caller retains
ownership of the {cpp:class}`BMessage`
objects (and the container {cpp:class}`BList`); they won't
be deleted for you.

Sending an on-launch message is appropriate if it helps the launched
application configure itself before it starts getting other messages. To
launch an application and send it an ordinary message, call {hmethod}`Launch()` to
get it running, then set up a {cpp:class}`BMessenger` object for the application and
call {cpp:class}`BMessenger`'s
{cpp:func}`~BMessenger::SendMessage` function.

If the target application is already running, {hmethod}`Launch()` won't launch it
again, unless it permits multiple instances to run concurrently (it
doesn't wait for the messages to be sent or report errors encountered
when they are). It fails for {cpp:enum}`B_SINGLE_LAUNCH` and {cpp:enum}`B_EXCLUSIVE_LAUNCH`
applications that have already been launched. Nevertheless, it assumes
that you want the messages to get to the application and so delivers them
to the currently running instance.

Instead of messages, you can launch an application with an array of
argument strings that will be passed to its main() function. {hparam}`argv`
contains the array and {hparam}`argc` counts the number of strings. If the
application accepts messages, this information will also be packaged in a
{cpp:enum}`B_ARGV_RECEIVED` message that the application will receive on-launch.

If successful, {hmethod}`Launch()` places the identifier for the newly launched
application in the variable referred to by {hparam}`team` and returns {cpp:enum}`B_OK`. If
unsuccessful, it sets the {hparam}`team` variable to -1 and returns an error
code, typically one of the following:

:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_BAD_VALUE`.
	- The {hparam}`type` or {hparam}`file` is not valid, or an attempt is being made to send an on-launch message to an application that doesn't accept messages (that is, to a {cpp:enum}`B_ARGV_ONLY` application).
-
	- {cpp:enum}`B_ALREADY_RUNNING`.
	- The application is already running and can't be launched again (it's a {cpp:enum}`B_SINGLE_LAUNCH` or {cpp:enum}`B_EXCLUSIVE_LAUNCH` application).
-
	- {cpp:enum}`B_LAUNCH_FAILED`.
	- The attempt to launch the application failed for some other reason, such as insufficient memory.
-
	- A file system error.
	- The {hparam}`file` or {hparam}`type` can't be matched to an application.
:::

See also: the
{cpp:class}`BMessenger` class,
{cpp:func}`~BRoster::GetAppInfo`,
{cpp:func}`~BRoster::FindApp`

::::

::::{abi-group}




:::{cpp:function} status_t BRoster::StartWatching(BMessenger target, uint32 events = B_REQUEST_LAUNCHED | B_REQUEST_QUIT) const
:::
:::{cpp:function} status_t BRoster::StopWatching(BMessenger target) const
:::

{hmethod}`StartWatching()` initiates the application event monitor, which is used
for keeping track of events such as application launches. The caller
specifies the events to monitor through the {hparam}`events` argument; {hparam}`target` is
the {cpp:class}`BMessenger` to which the corresponding notification messages are sent.
The {hparam}`events` flags and the corresponding messages are listed below:

FlagMessageB_REQUEST_LAUNCHEDB_SOME_APP_LAUNCHEDB_REQUEST_QUITB_SOME_APP_QUITB_REQUEST_ACTIVATEDB_SOME_APP_ACTIVATED

The fields in a notification message describe the application that was
launched, quit, or activated:

FieldTypeDescriptionmime_sigB_STRING_TYPEMIME signatureteamB_INT32_TYPEteam_idthreadB_INT32_TYPEthread_idflagsB_INT32_TYPEapplication flagsrefB_REF_TYPEexecutable's entry_ref

{hmethod}`StopWatching()` terminates the application monitor previously initiated
for a given {cpp:class}`BMessenger`.

::::

::::{abi-group}

:::{cpp:function} team_id BRoster::TeamFor(const char* signature) const
:::
:::{cpp:function} team_id BRoster::TeamFor(entry_ref* executable) const
:::
:::{cpp:function} bool BRoster::IsRunning(const char* signature) const
:::
:::{cpp:function} bool BRoster::IsRunning(entry_ref* executable) const
:::

Both these functions query whether the application identified by its
{hparam}`signature` or by a reference to its {hparam}`executable` file is running.
{hmethod}`TeamFor()` returns its team identifier if it is, and
{cpp:enum}`B_ERROR` if it's not. {hmethod}`IsRunning()` returns
{cpp:enum}`true` if it is, and {cpp:enum}`false` if it's
not.

If the application is running, you probably will want its team identifier
(to set up a {cpp:class}`BMessenger`
, for example). Therefore, it's most economical to
simply call {hmethod}`TeamFor()` and forego {hmethod}`IsRunning()`.

If more than one instance of the {hparam}`signature` application is running, or if
more than one instance was launched from the same {hparam}`executable` file,
{hmethod}`TeamFor()` arbitrarily picks one of the instances and returns its
team_id.

See also: {cpp:func}`~BRoster::GetAppList`

::::

## Global Variables
::::{abi-group}

:::{code}
BRoster* be_roster
:::

This variable points to the application's global {hclass}`BRoster` object. The
{hclass}`BRoster` keeps a roster of all running applications and can add
applications to the roster by launching them. It's initialized when the
application starts up.

::::

## Constants
::::{abi-group}




:::{code}
B_BACKGROUND_APP
B_ARGV_ONLY
B_LAUNCH_MASK
:::
These constants are used to get information from the flags field of an
{cpp:func}`~app::info`
structure.
See also:
{cpp:func}`BRoster::GetAppInfo`,
"{cpp:func}`~Constants::Launch`" below
::::

::::{abi-group}




:::{code}
B_MULTIPLE_LAUNCH
B_SINGLE_LAUNCH
B_EXCLUSIVE_LAUNCH
:::
These constants explain whether an application can be launched any number
of times, only once from a particular executable file, or only once for a
particular application signature. This information is part of the flags
field of an
{cpp:func}`~app::info`
structure and can be extracted using the
{cpp:enum}`B_LAUNCH_MASK` constant.
See also:
{cpp:func}`BRoster::GetAppInfo`,
"{cpp:func}`~Constants::Application`" above
::::

## Defined Types
::::{abi-group}


:::{code}
typedef struct {
    thread_id thread;
    team_id   team;
    port_id   port;
    uint32    flags;
    entry_ref ref;
    char      signature[B_MIME_TYPE_LENGTH];
    app_info(void);
    ~app_info(void);
} app_info
:::
This structure is used by
{cpp:class}`BRoster`'s
{cpp:func}`~BRoster::GetAppInfo`,
{cpp:func}`~BRoster::GetRunningAppInfo`,
and
{cpp:func}`~BRoster::GetActiveAppInfo`
functions to report information about an
application. Its constructor ensures that its fields are initialized to
invalid values. To get meaningful values for an actual application, you
must pass the structure to one of the
{cpp:class}`BRoster`
functions. See those functions for a description of the various fields.
::::
