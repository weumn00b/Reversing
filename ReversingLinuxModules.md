# Reversing Linux Modules
---

### Files

Our first step in this walkthrough is to look at what files we downloaded from the CTF.

We can see that we have a file named "brainstorm.ko" and a file named "logs"


We then want to look into what the ".ko" extension [signifies](https://docs.legato.io/latest/getStartedKO.html). ".ko" files are used to "extend" the kernel of a Linux Distribution.  From my understanding, this means that they are some sort of binary files, probably coded in C.

Looking at the logs file, it appears to be gibberish. We will probably need to decode this to get our flag.


### Ghidra

Now that we have a basic understanding of the files, its time to open the "brainstorm.ko" file, and start to dig into what is happening. 

The first thing I see are these functions that have been created:



Looking at "keys_read", I bet that they are installing some sort of keylogger. We'll save that for later.

Our first question is: 
###### **Who is the author?**

A good thing to know in Ghidra is the search tool. There are many different ways you can search for references to things, but I mainly just search all the fields.



There are 2 results, they both link to this line that says "author=0xEr3n".



Next Question:

###### **What is the name of the function used to register keyboard events?**

Right here is when we need to start figuring out what our file is doing. if we look in our "spy_init" function. We can see that after a directory and file is made, a function named register_keyboard_notifier is being called. 



Next Question:

###### **What is the name of the function that converts keycodes to strings?**

This one is really easy. In our functions we saw a keycode_to_string function. I assumed that this was the correct function. It was.



Next Question:

###### What file does the module create to store logs? Provide the full path.

This is defined in the spy_init function. We can see pretty clearly that a function called `debugfs` is being used to create a directory named `spyyy`. Looking into debugfs, its [mentioned](https://docs.kernel.org/filesystems/debugfs.html) that its typically mounted to `/sys/kernel/debug`. The next thing I saw is that debugfs is creating some sort of file. It mentions `DAT_00100c6c` as one of the arguments. I looked into this a little more, and saw that `DAT_00100c6c` references characters.



I concluded that the full path to the logs was `/sys/kernel/debug/spyyy/keys`

Next Question:

###### **What Message does the module print when imported?**

I started by searching for print in the program. I saw `printk` being executed as `spy` was loaded and unloaded.



Looking at the print statement while loading, you will observe that it's argument is `DAT_00100c71`.



Looking at the data that is referenced, you can see `6w00tw00t` is being referenced by the `printk` statement.



[Looking into printk](https://en.wikipedia.org/wiki/Printk), you can see that 6 is actually a log level that denotes an informational message. The message being displayed is actually `w00tw00t`.

Next Question:

###### **What is the XOR key used to obfuscate the keys? (e.g. 0x01, 0x32)**

This question is a little harder. The function to focus on is `spy_cb`, as this is what is doing the obfuscation. In the function, there appears to be a lot of math, but the `do{}` statement is where all the heavy lifting is done. 



the XOR operation in C is `^`, and you can see that the first line of the `do` statement is executing the shift. It is shifting by 0x19.

Next Question:

###### **What is the password entered for adam?**

This is where you should look at the log file. Now that you know that the obfuscation is done by XORing by 0x19 bites, you can reverse the obfuscation in the log file. Reversing XOR is as simple as just performing the XOR again. You could look up the ASCII character codes and do this by hand, but a python script is the fastest way.



We can see the password inputted by adam in the log file!
