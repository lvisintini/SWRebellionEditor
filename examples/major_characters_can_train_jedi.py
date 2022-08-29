from swr_ed import MANAGERS_BY_FILE

game_directory = 'C:\Steam\steamapps\common\Star Wars - Rebellion'

manager_class = MANAGERS_BY_FILE['MJCHARSD.DAT']
manager = manager_class(game_directory)
manager.load()

for x in range(len(manager.data)):
    manager.data[x]['can_train_jedis'] = 1

manager.save()
