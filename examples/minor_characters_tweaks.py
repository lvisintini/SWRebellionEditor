from swr_ed import MANAGERS_BY_FILE

manager_class = MANAGERS_BY_FILE['MNCHARSD.DAT']
manager = manager_class(fetch_names=True)
manager.load_file()

for x in range(len(manager.data)):
    manager.data[x]['wont_betray_own_side'] = 1
    manager.data[x]['jedi_level_base'] = manager.data[x]['jedi_level_base'] * 2
    manager.data[x]['jedi_level_variance'] = manager.data[x]['jedi_level_variance'] * 2
    manager.data[x]['jedi_probability'] = manager.data[x]['jedi_probability'] * 2
    manager.data[x]['can_train_jedis'] = 1

manager.save_file()
