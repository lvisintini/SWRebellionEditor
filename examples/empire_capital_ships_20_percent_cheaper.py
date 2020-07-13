from swr_ed import MANAGERS_BY_FILE

manager_class = MANAGERS_BY_FILE['CAPSHPSD.DAT']
manager = manager_class(fetch_names=True)
manager.load()

for x in range(len(manager.data)):
    if not manager.data[x]['imperial'] and manager.data[x]['alliance']:
        continue
    manager.data[x]['maintenance'] = int(manager.data[x]['maintenance'] * 0.8)
    manager.data[x]['construction_cost'] = int(manager.data[x]['maintenance'] * 0.8)

manager.save()
