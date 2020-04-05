# kerbal-ksm-debugger

Tested using Python 3.6.9

---

This project is a python module, which means it is run in the following way:

`python3 -m ksm_debugger`

There will also be a py2exe version of the tool released for easy Windows access.

## Module documentation:

---

Help can be acquired by:

`python3 -m ksm_debugger --help`

---

### Required arguments:

ksm_debugger requires one argument that corresponds to the path of the input .ksm file.

For example, if there was a file called `launch.ksm` it would be opened using:

`python3 -m ksm_debugger launch.ksm`

This can be an absolute or relative path and should work on both linux and Windows, and possibly MacOS too.

---

### Optional arguments:

ksm_debugger has the option of either displaying output to the terminal it is run in, or storing the same output in a file.

This can be specified using `-o` / `--output`

For example, if I wanted to put the debug information of the same `launch.ksm` file into a file named `launch_debug.txt` it would be done using the following:

`python3 -m ksm_debugger launch.ksm -o launch_debug.txt`

---

If you have any questions / suggestions let me know.

I do plan to clean up the code a little more, but I tried to write comments on every function and class to make it easier to look at. This is mostly a quick and dirty version of my ksm debugger written in Java, in Python.