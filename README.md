# SWRebellionEditor
A Windows-only library with tools that let you edit data files for the Star Wars Rebellion video game (1998)

# Reading the data
```
from swr_ed.base import ALL_MANAGERS 
import json 
game_directory = 'C:\Steam\steamapps\common\Star Wars - Rebellion'
for manager_class in ALL_MANAGERS: 
    manager = manager_class(game_directory) 
    manager.load() 
    print(json.dumps(manager.data, indent=2))
```

# Setting up

Because this is a really old game and the library makes use of DLL libraries that come with the game, we need to make sure to install the 32bit version of Python3 (currently 3.10.6).

While the DLLs used are mostly just simple resource files but the library uses the Windows 32 bit API to make use of them.

# Other useful links and software

### swrebellion.net 

Most of the work in this repo would not be possible without the help and data available in https://swrebellion.net/ (in particular [this forum thread](https://swrebellion.net/forums/topic/282-mechanics-inside-rebellion/))

While the site itself sees little activity and it is sometimes unavailable, it seems that someone is keeping it alive.


### RebEd v0.26: 

RebEd is an editor for Star Wars Rebellion / Supremacy ((c) Lucas Arts Company) made by Revolution (revolution@workmail.com) in contribution with a lot of people.

This is the software this code is attempting to reverse engineer and update to 2022 standards.

You can find it online with a simple search

### ResourceHacker

ResourceHacker comes in handy to inspect/update the contents of the DLL libraries included with the game.

This project aims to make it possible to update such things from a handy interfase.

However, this may take a while and you may want to use ResourceHacker in the meantime