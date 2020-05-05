# shine6-tool
_All I wanted was to fix some of the ugly RGB lighting effects the Ducky Shine 6 comes with..._


This is a collection of mostly Python utlities for modifying the Ducky Shine 6 keyboard.
As with most things like this, I cannot make any gaurantee that using this won't brick your keyboard. All I can say is that I have yet to brick my own.

If you get into trouble, try installing their Software and running `FWUpdate.exe -force`. It should put things back to normal.

## Utilities
### custom_rgb_test.py
Basic test of having the host system control the lighting of each key to create a smooth realtime effect.

### extract.py
Extracts firmware from FWUpdate.exe v1.02.10 (Packaged with Shine6 desktop software).  
The output directory will be populated with a firmware binary for each layout.

**Usage**
```
python extract.py -i FWUpdate.exe -o temp/
```

### flash.py
Flashes specified firmware to keyboard. This has not been thoroughly tested, so use at your own risk!

**Usage**
```
python flash.py -i "temp/US Layout V1.02.10.dat"
```


## Special Thanks
A huge thanks to all the work done on [pok3r_re_firmware](https://github.com/pok3r-custom/pok3r_re_firmware). It was often enough to get me going in the right direction.

## License
License information can be found in the LICENSE file in the root directory.
