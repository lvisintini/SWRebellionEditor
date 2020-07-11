from swr_ed import MANAGERS_BY_FILE

manager_class = MANAGERS_BY_FILE['MJCHARSD.DAT']
manager = manager_class(fetch_names=True)
manager.load_file()

for x in range(len(manager.data)):
    manager.data[x]['can_train_jedis'] = 1

manager.save_file()
