# Open-Typer pack generator

Simple Python program for random pack generating.

## How to use

### Generating packs for all supported languages

```
make
```

The output will be saved in the `out` directory.

### Creating your own packs

Start by creating a configuration file, for example `mypack.conf`.

**Each line represents one lesson.**

```
fj
dk
a
%r
%s
```

In this example, the first lesson contains letters `f` and `j`.

`%r` won't add any new letters and will mark the lesson as `Revision`.

`%s` will enable uppercase letters (the new key is shift).

To add special characters, such as `%` or `\`

```
%%
\\
```

If you wish to include randomly generated words from a word list, you can create one using the `create-wordlist.py` tool.

Get some text files and create the word list:

`./create-wordlist.py text1.txt text2.txt text3.txt -o wordlist.txt`

Make sure you have Python 3 installed and generate the pack like this:

`./generate.py mypack.conf -w wordlist.txt -o mypack.typer`

Or without the word list:

`./generate.py mypack.conf -o mypack.typer`
