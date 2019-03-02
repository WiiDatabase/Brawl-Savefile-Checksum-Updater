Brawl Savefile Checksum Updater
========
This little Python program **updates the checksum of the Super Smash Bros. Brawl Savefile**.

It's as simple as taking a file, cutting off the CRC32 sum found at the end (or near the end) and calculating the new CRC32 sum (and replacing the old).

It only suppors the two `autosv.bin` files atm, rest should be easy. It can also edit the number of available golden hammers on the milestone wall.

**Only tested with a PAL savegame!** Offsets for other regions may be different, but the checks are the same.

## Usage
Extract your Smashbros. Brawl savegame with the [SaveGame Manager GX](https://wiidatabase.de/downloads/wii-tools/savegame-manager-gx-beta/) and copy the folder to the script's location.

Then start Python in the same directory and use it like this:
```python
import bscu
print(bscu.SaveFile("0001000052534250")) # Shows some info about the savefile
bscu.SaveFile("0001000052534250").set_golden_hammers(5) # Will set golden hammers to 5 and update the checksum
bscu.SaveFile("0001000052534250").update_autosave_checksum() # Updates the autosave checksum manually
```
  
## Credits
* Daeken for original Struct.py that I still use over five different projects \*sigh\*

## Screenshot
![Screenshot](screenshot.png?raw=true)