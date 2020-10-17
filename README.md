# SWRebellionEditor
A library with tools that let you edit data files for the Star Wars Rebellion video game (1998)

You need to setup an SW_REBELLION_DIR environment variable that contains the path to the game's folder.

This is required to run the test suite, but optional for using this code.

# Reading the data
If your are using this lib on linux you may want to:
```
$ export SW_REBELLION_DIR=/home/lvisintini/SWR/REBELLION
```
On windows, you may need to set up an environment variable for the same purpose.

Otherwise you will need to provide the path to your Rebellion directory as the first param for the manager classes:

```
from swr_ed.base import ALL_MANAGERS 
import json 
for manager_class in ALL_MANAGERS: 
    manager = manager_class('/home/lvisintini/SWR/REBELLION/') 
    manager.load() 
    print(json.dumps(manager.data, indent=2))
``` 
