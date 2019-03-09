# Miscellaneous Scripts
> A collection of scripts and small tools that didn't quite deserve their own repository.

This is a collection of various scripts that I have made that were not substantial enough to warrant their own repository, but were still worthy of sharing.


## Contents
### Maximum Replacer
Renaming operations can sometimes be tricky. Maya comes with a renaming ability, but it is rather trivial.  When cases arise where the functionality of built-in renaming is not sufficient, it is not uncommon to create a one-time script or even resort to manual renaming.  Coincidentally, [regular expressions](https://en.wikipedia.org/wiki/Regular_expression) are especially proficient in pattern matching and can be used to aid string substitution.  Maximum Replacer lets you select and rename rename objects using regular expressions, making those convoluted rename operations a walk in the park.  Providing your regular expressions are up-to-scratch, of course.
#### Notes
- To use this tool efficiently, you will have to know how to use regular expressions.
- In both Max and Maya, all renames are grouped into a chunk.  Therefore, a single undo can reverse all rename operations in one go, regardless of the count.
- The Maya plugin uses [Python's re library](https://docs.python.org/2/library/re.html) and therefore its rules about substitution, such as formats for groups, applies here.


## Meta
Daniel Green – [@KasumiL5x](https://twitter.com/kasumil5x) – dgreen@bournemouth.ac.uk

All scripts are distributed under the MIT license unless otherwise stated. See ``LICENSE`` for more information.

[https://github.com/KasumiL5x](https://github.com/KasumiL5x)
