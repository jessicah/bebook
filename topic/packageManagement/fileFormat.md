---
myst:
  substitutions:
    toc: "<abbr title='Table of Contents'>TOC</abbr>"
---

# Haiku Package File Format

This document specifies the Haiku Package (HPKG) file format, which was designed for efficient use
by Haiku's package file system. It is somewhat inspired by the [XAR
Format](http://code.google.com/p/xar/) (separate {{toc}} and data heap), but aims for greater
compactness (no XML for the {{toc}}).

Three stacked format layers can be identified:

- A generic container format for structured data.
- An archive format specifying how file system data is stored in the container.
- A package format, extending the archive format with attributes for package management.

## The Data Container Format

An HPKG file consists of four sections:

Header
: Identifies the file as an HPKG file and provides access to the other sections.

Heap
: Contains arbitrary (mostly unstructured) data referenced by the next two sections.

{{toc}}
: The main section, containing structured data with references to unstructured data in the heap
  section.

Package Attributes
: A section similar to the {{toc}}. Rather than describing the data contained in the file, it specifies
  meta data of the package as a whole.

The {{toc}} and Package Attributes sections aren't really separate sections, as they are stored at the
end of the heap.

All numbers in the HPKG are stored in big endian format or
[LEB128](http://en.wikipedia.org/wiki/LEB128) encoding.

### Header

The header has the following structure:

```
struct hpkg_header {
	uint32 magic;
	uint16 header_size;
	uint16 version;
	uint64 total_size;
	uint16 minor_version;

	uint16 heap_compression;
	uint32 heap_chunk_size;
	uint64 heap_size_compressed;
	uint64 heap_size_uncompressed;

	uint32 attributes_length;
	uint32 attributes_strings_length;
	uint32 attributes_strings_count;
	uint32 reserved1;

	uint64 toc_length;
	uint64 toc_strings_length;
	uint64 toc_strings_count;
};
```

magic
: The string `hpkg` ({cpp:enum}`B_HPKG_MAGIC`).

header_size
: The size of the header. This is also the absolute offset of the heap.

version
: The version of the HPKG format the file conforms to. The current version is 2
  ({cpp:enum}`B_HPKG_VERSION`).

total_size
: The total file size.

minor_version
: The minor version of the HPKG format the file conforms to. The current minor version is 0
  ({cpp:enum}`B_HPKG_MINOR_VERSION`}). Additions of new attributes to the attributes or {{toc}} sections
  should generally only increment the minor version. When a file with a greater minor version is
  encountered, the reader should ignore unknown attributes.


heap_compression
: Compressiong format used for the heap.

heap_chunk_size
: The size of the chunks the uncompressed heap data is divided into.

heap_size_compressed
: The compressed size of the heap. This includes all administrative data (the chunk size array).

heap_size_uncompressed
: The uncompressed size of the heap. This is only the size of the raw data (including the {{toc}} and
  attribute section), not including administrative data (the chunk size array).


attributes_length
: The uncompressed size of the package attributes section.

attributes_strings_length
: The size of the strings subsection of the package attributes section.

attributes_strings_count
: The number of entries in the strings subsection of the package attributes section.


reserved1
: Reserved for later use.


toc_length
: The uncompressed size of the {{toc}} section.

toc_strings_length
: The size of the strings subsection of the {{toc}} section.

toc_strings_count
: The number of entries in the strings subsection of the {{toc}} section.

### Heap

The heap provides storage for arbitrary data. Data from various sources are concatenated without
padding or separators, forming the uncompressed heap. A specific section of data is usually
referenced (e.g. in the {{toc}} and attributes sections) by an offset and the number of bytes. These
references always point into the uncompressed heap, even if the heap is actually stored in a
compressed format. The `heap_compression` field in the header specifies which format is used. The
following values are defined:

:::{list-table}
---
align: left
---
-
	- 0
	- {cpp:expr}`B_HPKG_COMPRESSION_NONE`
	- no compression
-
	- 1
	- {cpp:expr}`B_HPKG_COMPRESSION_ZLIB`
	- zlib (LZ77) compression
:::

The uncompressed heap data is divided into equally sized chunks (64 KiB). The last chunk in the heap
may have a different uncompressed length from the preceding chunks. The uncompressed length of the
last chunk can be dervied. Each individual chunk may be stored compressed or not.

Unless `B_HPKG_COMPRESSION_NONE` is specified, a `uint16` array at the end of the heap contains the
actual in-file (compressed) size of each chunk (minus 1 -- 0 means 1 byte), save for the last one,
which is omitted since it is implied. A chunk is only stored compressed, if compression actually
saves space. That is, if the chunk's compressed size equals its uncompressed size, the data isn't
compressed. If `B_HPKG_COMPRESSION_NONE` is specified, the chunk size table is omitted entirely.

The {{toc}} and the package attributes sections are stored (in this order) at the end of the
uncompressed heap. The offset of the package attributes section is therefore
{cpp:expr}`heap_size_uncompressed - attributes_length` and the offset of the {{toc}} section is
{cpp:expr}`heap_size_uncompressed - attributes_length - toc_length`.

### {{toc}}

The {{toc}} section contains a list of attribute trees. AN attribute has an ID, a data type, and a
value, and can have child attributes.

The main {{toc}} section refers to any attribute by its unique ID (see below) and stores the attribute's
value, either as a reference into the heap, or as inline data.

An optimization exists for shared string attribute values. A string value used by more than one
attribute is stored in the strings subsection, and is referenced by an index into that subsection.

Hence the {{toc}} section consists of two subsections:

Strings
: A table of commonly used strings.

Main {{toc}}
: The attribute trees.

#### Attribute Data Types

These are the specified data type values for attributes:

:::{list-table}
---
align: left
---
-
	- 0
	- `B_HPKG_ATTRIBUTE_TYPE_INVALID`
	- invalid
-
	- 1
	- `B_HPKG_ATTRIBUTE_TYPE_INT`
	- signed integer
-
	- 2
	- `B_HPKG_ATTRIBUTE_TYPE_UINT`
	- unsigned integer
-
	- 3
	- `B_HPKG_ATTRIBUTE_TYPE_STRING`
	- UTF-8 string
-
	- 4
	- `B_HPKG_ATTRIBUTE_TYPE_RAW`
	- raw data
:::

#### Strings

The strings subsection consists of a list of null-terminated UTF-8 strings. The section itself is
termined by a null byte.

Each string is implicitly assigned the (null-based) index at which it appears in the list, i.e. the
nth string has the index `n - 1`. The string is referenced by this index in the main {{toc}} subsection.

#### Main {{toc}}

The main {{toc}} subsection consists of a list of attribute entries terminated by a null byte. An
attribute entry is stored as:

Attribute tag
: An unsigned LEB128 encoded number.

Attribute value
: The value of the attribute encoded as described below.

Attribute child list
: Only is this attribute is marked to have children: A list of attribute entries terminated by a
  null byte.

The attribute tag encodes four pieces of information:

    (encoding << 11) + (hasChildren << 10) + (dataType << 7) + id + 1

encoding
: Specifies the encoding of the attribute value as described below.

hasChildren
: 1, if the attribute has children, 0 otherwise

dataType
: The data type of the attribute (`B_HPKG_ATTRIBUTE_TYPE_...`).

id
: The ID of the attribute (`B_HPKG_ATTRIBUTE_ID_...`).

#### Attribute Values

The value of each of the data types can be encoded in different ways, which is defined by the
encoding value:

- `B_HPKG_ATTRIBUTE_TYPE_INT` and `B_HPKG_ATTRIBUTE_TYPE_UINT`:
  :::{list-table}
  ---
  align: left
  ---
	-
		- 0
		- `B_HPKG_ATTRIBUTE_ENCODING_INT_8_BIT`
		- int8/uint8
	-
		- 1
		- `B_HPKG_ATTRIBUTE_ENCODING_INT_16_BIT`
		- int16/uint16
	-
		- 2
		- `B_HPKG_ATTRIBUTE_ENCODING_INT_32_BIT`
		- int32/uint32
	-
		- 4
		- `B_HPKG_ATTRIBUTE_ENCODING_INT_64_BIT`
		- int64/uint64
  :::
- `B_HPKG_ATTRIBUTE_TYPE_STRING`:
  :::{list-table}
  ---
  align: left
  ---
	-
		- 0
		- `B_HPKG_ATTRIBUTE_ENCODING_STRING_INLINE`
		- null-terminated UTF-8 string
	-
		- 1
		- `B_HPKG_ATTRIBUTE_ENCODING_STRING_TABLE`
		- unsigned LEB128: index into string table
- `B_HPKG_ATTRIBUTE_TYPE_RAW`:
  :::{list-table}
  ---
  align: left
  ---
	-
		- 0
		- `B_HPKG_ATTRIBUTE_ENCODING_RAW_INLINE`
		- unsigned LEB128: size; followed by raw bytes
	-
		- 1
		- `B_HPKG_ATTRIBUTE_ENCODING_RAW_HEAP`
		- unsigned LEB128: size; unsigned LEB128; offset into the uncompressed heap

### Package Attributes

The package attributes section contains a list of attribute trees, just like the {{toc}} section. The
structure of this section follow the {{toc}}, i.e. there's a subsection for shared strings, and a
subsection that stores a list of attribute entries terminated by a null byte. An entry has the same
format as the ones in the {{toc}} (only using different attribute IDs).

## The Archive Format

This section specifies how file system objects (files, directories, symlinks) are stored in an HPKG
file. It builds on top of the container format, defining the types of attributes, their order, and
allowed values.

E.g. a "bin" directory, containing a symlink and a file:

```
bin           0  2009-11-13 12:12:09  drwxr-xr-x
  awk         0  2009-11-13 12:11:16  lrwxrwxrwx  -> gawk
  gawk   301699  2009-11-13 12:11:16  -rwxr-xr-x
```

could be represented by this attribute tree:

- B_HPKG_ATTRIBUTE_ID_DIR_ENTRY : string : "bin"
	- B_HPKG_ATTRIBUTE_ID_FILE_TYPE : uint : 1 (0x1)
	- B_HPKG_ATTRIBUTE_ID_FILE_MTIME : uint : 1258110729 (0x4afd3f09)
	- B_HPKG_ATTRIBUTE_ID_DIR_ENTRY : string : "awk"
		- B_HPKG_ATTRIBUTE_ID_FILE_TYPE : uint : 2 (0x2)
		- B_HPKG_ATTRIBUTE_ID_FILE_MTIME : uint : 1258110676 (0x4afd3ed4)
		- B_HPKG_ATTRIBUTE_ID_SYMLINK_PATH : string : "gawk"
	- B_HPKG_ATTRIBUTE_ID_DIR_ENTRY : string : "gawk"
		- B_HPKG_ATTRIBUTE_ID_FILE_PERMISSIONS : uint : 493 (0x1ed)
		- B_HPKG_ATTRIBUTE_ID_DATA : raw : size: 301699, offset: 0
		- B_HPKG_ATTRIBUTE_ID_FILE_ATTRIBUTE : string : "BEOS:APP_VERSION"
			- B_HPKG_ATTRIBUTE_ID_FILE_ATTRIBUTE_TYPE : uint : 1095782486 (0x41505056)
			- B_HPKG_ATTRIBUTE_ID_DATE : raw : size: 680, offset: 301699
		- B_HPKG_ATTRIBUTE_ID_FILE_ATTRIBUTE : string : "BEOS:TYPE"
			- B_HPKG_ATTRIBUTE_ID_FILE_ATTRIBUTE_TYPE : uint : 1296649555 (0x4d4d4d53)
			- B_HPKG_ATTRIBUTE_ID_DATA : raw : size: 35, offset: 302379

### Attribute IDs

The following attribute IDs are specified by the archive format. ANy other attributes will be
ignored.

...

### {{toc}} Attributes

The {{toc}} can directly contain any number of attributes of the `B_HPKG_ATTRIBUTE_ID_DIRECTORY_ENTRY`
type, which in turn contain descendant attributes as specified in the previous section. Any other
attributes are ignored.

## The Package Format

This section specifies how informative package attributes (package-name, version, provides,
requires, etc.) are stored in an HPKG file. It builds on top of the container format, defining the
types of attributes, their order, and allowed values.

E.g. a `.PackageInfo` file, containing a package description that is being converted into a package
file:

```
name		mypackage
version		0.7.2-1
architecture	x86
summary		"is a very nice package"
description	"has lots of cool features\nand is written in MyC++"
vendor		"Me, Myself & I, Inc."
packager	"me@test.com"
copyrights	{ "(C) 2009-2011, Me, Myself & I, Inc." }
licenses	{ "Me, Myself & I Commercial License"; "MIT" }
provides {
	cmd:me
	lib:libmyself = 0.7
}
requires {
	haiku >= r1
	wget
}
```

could be represented by this attribute tree:

-
-
-

### Attribute IDs

The following attribute IDs are specified by the package format. Any other attributes will be
rejected.

...

## Haiku Package Repository Format

Very similar to the package format, there's a Haiku Package Repository (HPKR) file format. Such a
file contains informative attributes about the package repository, and package attributes for all
packages contained in the repository. However, this format does not contain any files.

Two stacked format layers can be identified:

- A generic container format for structured data.
- A package format, extending the archive format with attributes for package management.

### The Data Container Format

An HPKR file consists of three sections:

Header
: Identifies the file as an HPKR file, and provides access to the other sections.

Heap
: Contains the next two sections.

Repository Info
: A section containing an archived {cpp:class}`BMessage` of a {cpp:class}`BRepositoryInfo` object.

Package Attributes
: A section just like the package attributes section of the HPKG, only that this section contains
  the package attributes of all the packages contained in the repository (not just one).

The Repository Info and Package Attributes sections aren't really separate sections, as they are
stored at the end of the heap.

#### Header

The header has the following structure:

```
struct hpkg_repo_header {
	uint32	magic;
	uint16	header_size;
	uint16	version;
	uint64	total_size;
	uint16	minor_version;

	// heap
	uint16	heap_compression;
	uint32	heap_chunk_size;
	uint64	heap_size_compressed;
	uint64	heap_size_uncompressed;

	// repository info section
	uint32	info_length;
	uint32	reserved1;

	// package attributes section
	uint64	packages_length;
	uint64	packages_strings_length;
	uint64	packages_strings_count;
};
```

magic
: The string `hpkr` ({cpp:enum}`B_HPKG_REPO_MAGIC`).

header_size
: The size of the header. This is also the absolute offset of the heap.

version
: The version of the HPKR format that the file conforms to. The current version is 2
  ({cpp:enum}`B_HPKG_REPO_VERSION`).

total_size
: The total file size.

minor_version
: The minor version of the HPKR format that the file conforms to. THe current minor version is 0
  ({cpp:enum}`B_HPKG_REPO_MINOR_VERSION`). Additions of new attributes to the attributes section
  should generally only increment the minor version. When a file with a greater minor version is
  encountered, the reader should ignore unknown attributes.

heap_compression
: Compression format used for the heap.

heap_chunk_size
: The size of the chunks the uncompressed heap data are divided into.

heap_size_compressed
: The compressed size of the heap. THis is only the size of the raw data (including the repository
info and attributes section), not including administrative data (the chunk size array).

info_length
: The uncompressed size of the repository info section.

reserved1
: Reserved for later use.

packages_length
: The uncompressed size of the package attributes section.

packages_strings_length
: The size of the strings subsection of the package attributes section.

packages_strings_count
: The number of entries in the strings subsection of the package attributes section.

### Attribute IDs

The package repository format defines only the top-level attribute ID
{cpp:enum}`B_HPKG_ATTRIBUTE_ID_PACKAGE`. An attribute with that ID represents a package. Its child
attributes specify the various meta information for the package as defined in the Package Format
Attribute IDs section.

#### B_HPKG_ATTRIBUTE_ID_PACKAGE ("package")

- Type: string
- Value: Name of the package. The value is duplicated by the
  {cpp:enum}`B_HPKG_ATTRIBUTE_ID_PACKAGE_NAME` child attribute.
- Allowed Values: any string matching `<entity_name_char>+`, with `<entity_name_char>` being any
  character but `-`, `/`, `=`, `!`, `<`, `>`, or whitespace.
- Child Attributes:
	- Any `B_HPKG_ATTRIBUTE_ID_PACKAGE_*` top level attribute defined in the Package Format
	Attribute IDs section.
