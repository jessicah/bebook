# System Information
## System Info Functions and Structures
::::{abi-group}






:::{cpp:function} status_t System Information::get_system_info(system_info* info)
:::
:::{code}
struct {} system_info
struct {} cpu_info
enum cpu_type
enum platform_type
:::
The get_system_info() function tells you more than you want to know about
the physical capacities and other statistics of your operating system.
The function takes a pointer to an allocated system_info structure and
fills it in.
:::{code}
typedef struct {
   machine_id  id;
   bigtime_t  boot_time;
   int32  cpu_count;
   cpu_type  cpu_type;
   int32  cpu_revision;
   cpu_info  cpu_infos[B_MAX_CPU_NUM];
   int64  cpu_clock_speed;
   int64  bus_clock_speed;
   platform_type  platform_type;
   int32  max_pages;
   int32  used_pages;
   int32  page_faults;
   int32  max_sems;
   int32  used_sems;
   int32  max_ports;
   int32  used_ports;
   int32  max_threads;
   int32  used_threads;
   int32  max_teams;
   int32  used_teams;
   char   kernel_name[B_FILE_NAME_LENGTH];
   char   kernel_build_date[B_OS_NAME_LENGTH];
   char   kernel_build_time[B_OS_NAME_LENGTH];
   int64  kernel_version;
} system_info
:::
The system_info structure holds information about the machine and the
state of the kernel. The structure's fields are:
:::{list-table}
---
header-rows: 1
---
-
	- Field
	- Description
-
	- id.
	- The 64-bit number (encoded as two int32s) that uniquely identifies this machine.
-
	- boot_time.
	- The time at which the computer was last booted, measured in microseconds since January 1st, 1970.
-
	- cpu_count.
	- The number of CPUs.
-
	- cpu_typeandcpu_revision.
	- The type constant and revision number of the CPUs.
-
	- cpu_infos.
	- An array of cpu_info structures, one for each CPU.
-
	- cpu_clock_speed.
	- The speed (in Hz) at which the CPUs operate.
-
	- bus_clock_speed.
	- The speed (in Hz) at which the bus operates.
-
	- platform_type.
	- One of the platform type constants.
-
	- max_resourcesandused_resources.
	- The five pairs of max/used fields give the total number of RAM pages, semaphores, and so on, that the system can create, and the number that are currently in use.
-
	- page_faults.
	- The number of times the system a read a page of memory into RAM due to a page fault.
-
	- kernel_name.
	- The (leaf) name of the kernel.
-
	- kernel_build_dateandkernel_build_time.
	- Human-readable strings that tell you when the kernel was built.
-
	- kernel_version.
	- A number that identifies the kernel version.
:::
The cpu_info structure is:
:::{code}
typedef struct {
      bigtime_t active_time;
} cpu_info;
:::
:::{list-table}
---
header-rows: 1
---
-
	- Field
	- Description
-
	- active_time
	- Is the number of microseconds spent doing useful work since the machine was booted.
:::
Relatedly, {cpp:enum}`B_MAX_CPU_COUNT` is currently 8.
The machine_id type is:
:::{code}
typedef int32 machine_id[2];
:::
The cpu_type constants are:
:::{code}
typedef enum {
    B_CPU_PPC_601 = 1,
    B_CPU_PPC_603 = 2,
    B_CPU_PPC_603e = 3,
    B_CPU_PPC_604 = 4,
    B_CPU_PPC_604e = 5,
    B_CPU_PPC_686 = 13,
    B_CPU_AMD_29K,
    B_CPU_X86,
    B_CPU_MC6502,
    B_CPU_Z80,
    B_CPU_ALPHA,
    B_CPU_MIPS,
    B_CPU_HPPA,
    B_CPU_M68K,
    B_CPU_ARM,
    B_CPU_SH,
    B_CPU_SPARC
} cpu_type;
:::
The platform_type constants are:
:::{code}
typedef enum {
    B_BEBOX_PLATFORM = 0,
    B_MAC_PLATFORM,
    B_AT_CLONE_PLATFORM,
    B_ENIAC_PLATFORM,
    B_APPLE_II_PLATFORM,
    B_CRAY_PLATFORM,
    B_LISA_PLATFORM,
    B_TI_994A_PLATFORM,
    B_TIMEX_SINCLAIR_PLATFORM,
    B_ORAC_1_PLATFORM,
    B_HAL_PLATFORM
} platform_type;
:::
I haven't tried it, but I really don't think the BeOS would work at all
well on a Timex Sinclair (see
{cpp:func}`~is::computer`).
get_system_info() always returns
{cpp:enum}`B_OK`.
::::

::::{abi-group}


:::{cpp:function} int32 System Information::is_computer_on()
:::
Returns 1 if the computer is on. If the computer isn't on, the value
returned by this function is undefined.
::::

::::{abi-group}


:::{cpp:function} double System Information::is_computer_on_fire()
:::
Returns the temperature of the motherboard if the computer is currently
on fire. Smoldering doesn't count. If the computer isn't on fire, the
function returns some other value.
::::
