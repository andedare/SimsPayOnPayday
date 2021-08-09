# Career Pay on Payday

This mod stops households from immediately receiving salary each day. Instead, pay is deferred to next Friday household
is active.

This repository requires [Sims 4 Community Library](https://github.com/ColonolNutty/Sims4CommunityLibrary) API to 
compile. Instructions can be found in `Libraries/S4CL`.

This source is based on the template, additional instructions can be found: in the wiki 
[here](https://github.com/ColonolNutty/s4cl-template-project/wiki/Project-Setup)!

---
Content below comes from Template and provides additional instructions to allow building this project.

## Decompile EA Python Scripts.

1. Inside `<Project>/settings.py`, change `should_decompile_ea_scripts` to `True`
2. If it does not exist, create a folder in your project with the name `EA`. i.e. <Project>/EA
3. Run the `decompile_scripts.py` script
4. It will decompile the EA scripts and put them inside of the folder: `<Project>/EA/...`
5. Inside of the <Project>/EA folder, you should see four folders (base, core, generated, simulation)
6. In PyCharm, highlight all four folders (Not Zip files) (`base`, `core`, `generated`, `simulation`) and Right Click them -> `Mark Directory as...` -> `Sources Root`


## Decompile Scripts From Other Mods.

1. Inside `<Project>/settings.py`, change `should_decompile_ea_scripts` to `False`
2. Inside `<Project>/settings.py`, change `should_decompile_custom_scripts` to `True`
3. If it does not exist, create a folder in your project with the name `custom_scripts_for_decompile`. i.e. `<Project>/custom_scripts_for_decompile`
4. Put the script files (.pyc) of the mod you wish to decompile, inside of the `custom_scripts_for_decompile` folder. (Every ts4script file is a zip file and can be opened and extracted like one!)
5. Run the `decompile_scripts.py` script
6. It will decompile the custom scripts and put them inside of the folder: `<Project>/custom_scripts_for_decompile/_decompiled/...`