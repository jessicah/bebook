# Images
## Image Functions
::::{abi-group}





:::{cpp:function} status_t Images::get_image_info(image_id image, image_info* info)
:::
:::{cpp:function} status_t Images::get_next_image_info(team_id team, int32* cookie, image_info* info)
:::
:::{code}
struct {} image_info
:::
These functions copy, into the {hparam}`info` argument, the image_info structure
for a particular image. The get_image_info() function gets the
information for the image identified by {hparam}`image`.
The get_next_image_info() function lets you step through the list of a
team's images through iterated calls. The {hparam}`team` argument identifies the
team you want to look at; a {hparam}`team` value of 0 means the team of the calling
thread. The {hparam}`cookie` argument is a placemark; you set it to 0 on your first
call, and let the function do the rest. The function returns {cpp:enum}`B_BAD_VALUE`
when there are no more images to visit:
:::{code}
/* Get the image_info for every image in this team. */
image_info info;
int32 cookie = 0;
while (get_next_image_info(0, &cookie, &info) == B_OK)
   ...
:::
The image_info structure is:
:::{code}
typedef struct {
    image_id   id;
    image_type type;
    int32      sequence;
    int32      init_order;
    B_PFV      init_routine;
    B_PFV      term_routine;
    dev_t      device;
    ino_t      node;
    char       name[MAXPATHLEN];
    void*      text;
    void*      data;
    int32      text_size;
    int32      data_size;
} image_info;
:::
The fields are:
:::{list-table}
---
header-rows: 1
---
-
	- Field
	- Description
-
	- id.
	- The image's image_id number.
-
	- type.
	- A constant (listed below) that tells whether this is an app, library, or add-on image.
-
	- sequenceandinit_order.
	- These are zero-based ordinal numbers that give the order in which the image was loaded and initialized, compared to all the other images in this team.
-
	- init_routineandterm_routine.
	- These are pointers to the functions that are used to intialize and terminate the image (more specifically, the image's main thread). The B_PFV type is a cover for a pointer to a (void*) function.
-
	- device.
	- The device that the image file lives on.
-
	- node.
	- The node number of the image file.
-
	- name.
	- The full pathname of the file whence sprang the image.
-
	- textandtext_size.
	- The address and the size (in bytes) of the image's text segment.
-
	- dataanddata_size.
	- The address and size of the image's data segment.
:::
The self-explanatory image_type constants are:
- {cpp:enum}`B_APP_IMAGE`
- {cpp:enum}`B_LIBRARY_IMAGE`
- {cpp:enum}`B_ADD_ON_IMAGE`

:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- The image was found; {hparam}`info` contains valid information.
-
	- {cpp:enum}`B_BAD_VALUE`.
	- {hparam}`image` doesn't identify an existing image, {hparam}`team` doesn't identify an existing team, or there are no more images to visit.
:::
::::

::::{abi-group}



:::{cpp:function} status_t Images::get_image_symbol(image_id image, char* symbol_name, int32 symbol_type, void** location)
:::
:::{cpp:function} status_t Images::get_nth_image_symbol(image_id image, int32 n, int32* name_length, int32* symbol_type, void** location)
:::
get_image_symbol() returns, in
{hparam}`location`, a pointer to the address of the
symbol that's identified by the {hparam}`image`,
{hparam}`symbol_name`, and {hparam}`symbol_type`
arguments. An example demonstrating the use of this function is given in
"Symbols."
get_nth_image_symbol() returns information about
the {hparam}`n`'th symbol in the
given {hparam}`image`. The information is returned in the arguments:
- {hparam}`name` is the name of the symbol. You have to allocate the {hparam}`name` buffer before you pass it in—the function copies the name into the buffer.
- You point {hparam}`name_length` to an integer that gives the length of the name buffer that you're passing in. The function uses this value to truncate the string that it copies into name. The function then resets {hparam}`name_length` to the full (untruncated) length of the symbol's name (plus one byte to accommodate a terminating {cpp:enum}`NULL`). To ensure that you've gotten the symbol's full name, you should compare the in-going value of {hparam}`name_length` with the value that the function sets it to. If the in-going value is less than the full length, you can then re-invoke get_nth_image_symbol() with an adequately lengthened {hparam}`name` buffer, and an increased {hparam}`name_length` value.

Keep in mind that name_length is reset each time you call
get_nth_image_symbol(). If you're calling the function iteratively (to
retrieve all the symbols in an image), you need to
reset the {hparam}`name_length`
value between calls.
- The function sets {hparam}`symbol_type` to {cpp:enum}`B_SYMBOL_TYPE_DATA` if the symbol is a variable, {cpp:enum}`B_SYMBOL_TYPE_TEXT` if the symbol is a function, or {cpp:enum}`B_SYMBOL_TYPE_ANY` if the executable format doesn't distinguish between the two. The argument's value going into the function is of no consequence.
- The function sets {hparam}`location` to point to the symbol's address.

To retrieve image_id numbers on which these functions can act, use the
{cpp:func}`~get::next`
function. Such numbers are also returned directly
when you load an add-on image through the
{cpp:func}`~load::add`
function.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- The symbol was found.
-
	- {cpp:enum}`B_BAD_IMAGE_ID`.
	- {hparam}`image` doesn't identify an existing image.
-
	- {cpp:enum}`B_BAD_INDEX`.
	- {hparam}`n` is out-of-bounds.
:::
::::

::::{abi-group}



:::{cpp:function} image_id Images::load_add_on(const char* pathname)
:::
:::{cpp:function} status_t Images::unload_add_on(image_id image)
:::
load_add_on() loads an add-on image,
identified by {hparam}`pathname`, into your
application's address space.
- {hparam}`pathname` can be absolute or relative; if it's relative, it's reckoned off the base path specified by the ADDON_PATH environment variable.
- The function returns an image_id (a positive integer) that represents the loaded image. Image ID numbers are unique across the system.

An example that demonstrates the use of load_add_on() is given in
"{cpp:func}`~Images::LoadingAnAddOnImage`."
You can load the same add-on image twice; each time you load the add-on a
new, unique image_id is created and returned.
unload_add_on() removes the add-on image identified by the argument. The
image's symbols are removed, and the memory that they represent is freed.
If the argument doesn't identify a valid image, the function returns
{cpp:enum}`B_ERROR`. Otherwise, it returns {cpp:enum}`B_OK`.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- Positiveimage_idvalue (load) or{cpp:enum}`B_OK`(unload).
	- Success.
-
	- {cpp:enum}`B_ERROR`.
	- The image couldn't be loaded (for whatever reason), or image isn't a valid image ID.
:::
::::

::::{abi-group}


:::{cpp:function} thread_id Images::load_image(int argc, const char** argv, const char ** env)
:::
Loads an app image into the system (it doesn't load the image into the
caller's address space), creates a separate team for the new application,
and spawns and returns the ID of the team's main thread. The image is
identified by the pathname given in {hparam}`argv`[0].
The arguments are passed to the image's main() function (they show up
there as the function's similarly named arguments):
:::{list-table}
---
header-rows: 1
---
-
	- Parameter
	- Description
-
	- argc
	- Gives the number of entries that are in the {hparam}`argv` array.
-
	- argv
	- Is a list of the parameters to be passed to the image. The first string in the {hparam}`argv` array must be the name of the image file. You then install any other arguments you want in the array, and terminate the array with a {cpp:enum}`NULL` entry. Note that the value of {hparam}`argc` shouldn't count {hparam}`argv`'s terminating {cpp:enum}`NULL`.
-
	- envp
	- Is an array of environment variables that are also passed to main(). Typically, you use the global environ pointer:extern char **environ; load_image(..., environ);
:::
The {hparam}`argv` and {hparam}`envp`
arrays are copied into the new thread's address space.
If you allocated either of these arrays, it's safe to free them
immediately after load_image() returns.
The thread that's returned by load_image() is in a suspended state. To
start the thread running, you pass the thread_id to
{cpp:func}`~resume::thread` or
{cpp:func}`~wait::for`.
An example that demonstrates the use of load_image()
is given in
"Loading an App Image."
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- Positive integers.
	- Success.
-
	- {cpp:enum}`B_ERROR`.
	- Failure, for whatever reason.
:::
::::
