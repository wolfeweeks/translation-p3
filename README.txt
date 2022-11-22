This program was written with Python. Python files do not require MAKEFILEs, so 
it would be pointless to make and/or require one.

I had to rename the parser file to "my_parser" to avoid shadowing an existing
python module.

The possible invocations are as follows:
  1. "P2"
      -if you want to write your file in the console

  2. "P2 < file.cs4280"
      -if you want to redirect a file through stdin
      -"file" can be any name

  3. "P2 file"
      -if you want to pass the file name as an argument
      -"file" can be any name