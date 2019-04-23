Brawl Savefile Checksum Updater
========
This little Python program **updates the checksum of the Super Smash Bros. Brawl Savefile**.

It's as simple as taking a file, cutting off the CRC32 sum found at the end and calculating the new CRC32 sum (and replacing the old).

It only suppors the `autosv.bin` and `net.bin` files atm (`advsv.bin` has no checksum?). It can also edit the number of available golden hammers on the milestone wall.

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

## More research
* The *1 files are just backups and are the exact same as the *0 files
* **advsv0.bin** contains Subspace Emissary data
* **collect.vff** contains Custom Stages, Photos and Replays (can be extracted with e.g. [Wii.py3](https://github.com/Brawl345/Wii.py3))
* **net0.bin** contains Wi-Fi data
* **autosv0.bin** contains the rest, like Stickers, Trophies, Classic data, etc.
* **banner.bin** is obviously the savegame banner
* **wc24pubk.mod** is the public key for decrypting WiiConnect24 data
  
## Screenshot
![Screenshot](screenshot.png?raw=true)