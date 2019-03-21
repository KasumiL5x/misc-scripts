# Miscellaneous Scripts
> A collection of scripts and small tools that didn't quite deserve their own repository.

This is a collection of various scripts that I have made that were not substantial enough to warrant their own repository, but were still worthy of sharing.

## Contents
### Maximum Replacer
Renaming operations can sometimes be tricky. Maya comes with a renaming ability, but it is rather trivial.  When cases arise where the functionality of built-in renaming is not sufficient, it is not uncommon to create a one-time script or even resort to manual renaming.  Coincidentally, [regular expressions](https://en.wikipedia.org/wiki/Regular_expression) are especially proficient in pattern matching and can be used to aid string substitution.  Maximum Replacer lets you select and rename rename objects using regular expressions, making those convoluted rename operations a walk in the park.  Providing your regular expressions are up-to-scratch, of course.

<img src="https://raw.githubusercontent.com/KasumiL5x/misc-scripts/master/maya/maximumreplacer/maximumreplacer.png" width="50%" alt="Maximum Replacer" />

#### Notes
- To use this tool efficiently, you will have to know how to use regular expressions.
- In both Max and Maya, all renames are grouped into a chunk.  Therefore, a single undo can reverse all rename operations in one go, regardless of the count.
- The Maya plugin uses [Python's re library](https://docs.python.org/2/library/re.html) and therefore its rules about substitution, such as formats for groups, applies here.

---

### Welcome
Who doesn't want to be welcomed to their Maya session?  Add this to your `userSetup.mel` to be greeted with a warm message.  It displays only once Maya is fully done loading and is **ready to use**, which is why I use it.

![Welcome](https://raw.githubusercontent.com/KasumiL5x/misc-scripts/master/maya/welcome/welcome.png)

---

### AnimCurve Toolbox
[animCurve](http://help.autodesk.com/cloudhelp/2016/ENU/Maya-Tech-Docs/Nodes/animCurve.html) nodes in Maya are fantastic. They are, however, astonishingly difficult to locate within Maya unless you are one with the code-foo – they can only be created and keyframed through scripting. AnimCurve Toolbox is a very modest tool to assist with using animCurve nodes. It allows for creation, simple editing, and selection of various types of the node.

<img src="https://raw.githubusercontent.com/KasumiL5x/misc-scripts/master/maya/animcurvetb/animcurvetb.png" width="30%" alt="AnimCurve Toolbox" />

#### Usage
Creating curves is very simple. Within the **Create** group, there exists a dropdown with various types of animCurve node, followed by a textbox where a name can be specified. Below is a button for creating the desired curve type, which is named appropriately.

The lower section, **Edit**, contains yet another dropdown, this time with an accompanying button to its side. The dropdown will display all animCurve nodes within the scene (including ones created externally to this tool). The aforementioned button will refresh the dropdown with the current state of the scene. This tool does not automatically update this list, so remember to press the button.

Adding keyframes to animCurve nodes shouldn't be hard. Unfortunately, Maya has a penchant for making things hard. Luckily, this tool makes it easy. Clicking the **Add Keyframe** button will prompt you for both a time and value for the key. The currently active curve in the dropdown above will be used.

Since animCurve nodes are not DAG objects, they will appear in the Outliner only when *DAG Objects Only* is disabled. Disabling this clutters the list, and can make finding your nodes difficult. Instead, this tool provides a Select button. Clicking this button will replace the active selection with the curve specified in the dropdown above. If **shift** is held when clicking the button, the selection will instead be appended.

The Graph Editor is ideal for editing animCurve keyframes. Instead of having to select them using this tool, or by hand, and then opening the Graph Editor manually, the **Graph Editor** button in the tool will select the curve specified in the above dropdown and then open the graph editor for easy and quick editing.

#### Notes
If you have added keyframes to an animCurve node but do not see anything in the Graph Editor, try connecting something to the animCurve's **input** plug and that should rectify the problem.

---

### Align Faces
A feature largely missing from a number of 3D software packages is the ability to align a camera perfectly to a face's normal (thank you, Modo!). Aligning the camera to a face, or average of selected faces, can be very useful for UV mapping, or even just scene navigation. This script will align the active viewport's camera to the average angle of the selected faces, maintaining its distance. Usage is simple. Call the `look_at_selected_faces()` method with at least one face selected.

![AlignFaces](https://raw.githubusercontent.com/KasumiL5x/misc-scripts/master/maya/alignfaces/alignfaces.png)

---

### Value Checker
This script lets you validate the values of many objects at the same time.  You can select any number of objects matching a regular expression (or text string) by name, filter further by their type, and then determine which from the resulting list you wish to check.  You can check one attribute at a time for all chosen elements to see if its value is what you expect.  There are also three checkboxes for validation of zero translation, zero rotation, and unit scale, which is especially helpful for rigging.  This version only supports equality checking, but it would be easy to add others.

<img src="https://raw.githubusercontent.com/KasumiL5x/misc-scripts/master/maya/valuechecker/valuechecker.png" width="30%" alt="AnimCurve Toolbox" />

## Meta
Daniel Green – [@KasumiL5x](https://twitter.com/kasumil5x) – dgreen@bournemouth.ac.uk

All scripts are distributed under the MIT license unless otherwise stated. See ``LICENSE`` for more information.

[https://github.com/KasumiL5x](https://github.com/KasumiL5x)
