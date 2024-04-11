#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>

static inline void native_cpuid(unsigned int *eax, unsigned int *ebx,
                                unsigned int *ecx, unsigned int *edx)
{
    /* ecx is often an input as well as an output. */
    asm volatile("cpuid"
                 : "=a" (*eax),
                   "=b" (*ebx),
                   "=c" (*ecx),
                   "=d" (*edx)
                 : "0" (*eax), "2" (*ecx)
                 : "memory");
}

static int __init cpuinfo_init(void)
{
    unsigned eax, ebx, ecx, edx;

    printk(KERN_INFO "Loading CPUInfo Module\n");

    // Processor Vendor ID
    eax = 0;
    native_cpuid(&eax, &ebx, &ecx, &edx);
    printk(KERN_INFO "Vendor ID: %c%c%c%c%c%c%c%c%c%c%c%c\n",
           (ebx) & 0xFF, (ebx >> 8) & 0xFF, (ebx >> 16) & 0xFF, (ebx >> 24) & 0xFF,
           (edx) & 0xFF, (edx >> 8) & 0xFF, (edx >> 16) & 0xFF, (edx >> 24) & 0xFF,
           (ecx) & 0xFF, (ecx >> 8) & 0xFF, (ecx >> 16) & 0xFF, (ecx >> 24) & 0xFF);

    // Processor Features
    eax = 1;
    native_cpuid(&eax, &ebx, &ecx, &edx);
    printk(KERN_INFO "Stepping: %d\n", eax & 0xF);
    printk(KERN_INFO "Model: %d\n", (eax >> 4) & 0xF);
    printk(KERN_INFO "Family: %d\n", (eax >> 8) & 0xF);
    printk(KERN_INFO "Processor Type: %d\n", (eax >> 12) & 0x3);
    printk(KERN_INFO "Extended Model: %d\n", (eax >> 16) & 0xF);
    printk(KERN_INFO "Extended Family: %d\n", (eax >> 20) & 0xFF);

    // Processor Serial Number (if available)
    eax = 3;
    native_cpuid(&eax, &ebx, &ecx, &edx);
    printk(KERN_INFO "Serial Number: 0x%08x%08x\n", edx, ecx);

    return 0;
}

static void __exit cpuinfo_exit(void)
{
    printk(KERN_INFO "Unloading CPUInfo Module\n");
}

module_init(cpuinfo_init);
module_exit(cpuinfo_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Pattapon Vichanukroh");
MODULE_DESCRIPTION("A simple Linux char driver for the CPUID");
