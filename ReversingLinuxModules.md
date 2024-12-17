# Reversing Linux Modules
---

## Files
---

Our first step in this walkthrough is to look at what files we downloaded from the CTF.

We can see that we have a file named "brainstorm.ko" and a file named "logs"
<br>
<br><br>
![Pasted image 20241216213725](https://github.com/user-attachments/assets/f98ae060-0f7b-48f5-8b89-a16da77883f2)
<br>
<br>
We then want to look into what the ".ko" extension [signifies](https://docs.legato.io/latest/getStartedKO.html). ".ko" files are used to "extend" the kernel of a Linux Distribution.  From my understanding, this means that they are some sort of binary files, probably coded in C.
<br><br><br>
![Pasted image 20241216213901](https://github.com/user-attachments/assets/e2f54ccb-819e-4cc3-995d-1935302f05d4)
<br><br>
Looking at the logs file, it appears to be gibberish. We will probably need to decode this to get our flag.
<br><br><br>
## Ghidra
---
 
Now that we have a basic understanding of the files, its time to open the "brainstorm.ko" file, and start to dig into what is happening. 

The first thing I see are these functions that have been created:
 <br><br><br>
![Pasted image 20241216214338](https://github.com/user-attachments/assets/3496c219-b4d8-4fe8-864c-43a4ea581c96)

 <br><br>
Looking at "keys_read", I bet that they are installing some sort of keylogger. We'll save that for later.
 
 

### **Who is the author?**
---
 
A good thing to know in Ghidra is the search tool. There are many different ways you can search for references to things, but I mainly just search all the fields.
 <br><br><br>
 ![Pasted image 20241216214748](https://github.com/user-attachments/assets/f45c524e-70dc-4690-8a3e-92323ead5224)
<br><br>
 
There are 2 results, they both link to this line that says "author=0xEr3n".
 <br><br><br>
 ![Pasted image 20241216214856](https://github.com/user-attachments/assets/78a355bc-7124-413a-a10e-ada64b0f605d)

### **What is the name of the function used to register keyboard events?**
---
 
Right here is when we need to start figuring out what our file is doing. if we look in our "spy_init" function. We can see that after a directory and file is made, a function named register_keyboard_notifier is being called. 
 <br><br><br>
 ![Pasted image 20241216220808](https://github.com/user-attachments/assets/726f9eca-e08c-4c4b-ba19-faa81e8330b0)

 
 <br><br><br><br><br>
### **What is the name of the function that converts keycodes to strings?**
---
 
This one is really easy. In our functions we saw a keycode_to_string function. I assumed that this was the correct function. It was.
 
 ![Pasted image 20241216221047](https://github.com/user-attachments/assets/7b577f96-8e3c-42cb-b3f5-0afb92101b52)

### What file does the module create to store logs? Provide the full path.
---
 
This is defined in the spy_init function that is shown above. We can see pretty clearly that a function called `debugfs` is being used to create a directory named `spyyy`. Looking into debugfs, its [mentioned](https://docs.kernel.org/filesystems/debugfs.html) that its typically mounted to `/sys/kernel/debug`. The next thing I saw is that debugfs is creating some sort of file. It mentions `DAT_00100c6c` as one of the arguments. I looked into this a little more, and saw that `DAT_00100c6c` references characters.
 
 ![Pasted image 20241216222008](https://github.com/user-attachments/assets/57841be5-ebc2-48fa-ac83-d4bb04aa1937)


 
I concluded that the full path to the logs was `/sys/kernel/debug/spyyy/keys`

### **What Message does the module print when imported?**
---
 
I started by searching for print in the program. I saw `printk` being executed as `spy` was loaded and unloaded.
 
 
 ![Pasted image 20241216222425](https://github.com/user-attachments/assets/587d2377-c6d1-47e1-91e4-620898d463fd)

Looking at the print statement while loading, you will observe that it's argument is `DAT_00100c71`.
 
 ![Pasted image 20241216222727](https://github.com/user-attachments/assets/eb1c6035-6198-4b4b-aa1e-47b1034d84ec)

 
Looking at the data that is referenced, you can see `6w00tw00t` is being referenced by the `printk` statement.
 
 ![Pasted image 20241216223329](https://github.com/user-attachments/assets/c67ed92b-5d50-4813-a0d5-299522a1885e)

 
[Looking into printk](https://en.wikipedia.org/wiki/Printk), you can see that 6 is actually a log level that denotes an informational message. The message being displayed is actually `w00tw00t`.
 

### **What is the XOR key used to obfuscate the keys? (e.g. 0x01, 0x32)**
---
 
This question is a little harder. The function to focus on is `spy_cb`, as this is what is doing the obfuscation. In the function, there appears to be a lot of math, but the `do{}` statement is where all the heavy lifting is done. 
 
 ![Pasted image 20241216223820](https://github.com/user-attachments/assets/96f6e114-f831-4846-950c-832778a310c3)

 
the XOR operation in C is `^`, and you can see that the first line of the `do` statement is executing the shift. It is shifting by 0x19.

### **What is the password entered for adam?**
---
 
This is where you should look at the log file. Now that you know that the obfuscation is done by XORing by 0x19 bites, you can reverse the obfuscation in the log file. Reversing XOR is as simple as just performing the XOR again. You could look up the ASCII character codes and do this by hand, but a Python script is the fastest way (I have an example in this GitHub Repo).
 
 ![Pasted image 20241216224953](https://github.com/user-attachments/assets/3315d014-3cde-4f98-9809-97e15975b6ae)

 
You can see the password inputted by adam in the log file!
