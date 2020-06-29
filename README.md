# SWRebellionEditor
A library with tools that let you edit data files for the Star Wars Rebellion video game (1998)

You need to setup an SW_REBELLION_DIR environment variable that contains the path to the game's folder.

This is required to run the test suite, but optional for using this code.

# Reading the data
```
from swr_ed.base import ALL_MANAGERS 
import json 
for manager_class in ALL_MANAGERS: 
    manager = manager_class('/home/lvisintini/SWR/REBELLION/GDATA') 
    manager.load_file() 
    print(json.dumps(manager.data_dicts, indent=2))
``` 
