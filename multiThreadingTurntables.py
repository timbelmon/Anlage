import threading
import anlageTurnTableController

anlageTurntable231 = anlageTurnTableController.AnlageController("192.168.200.231")
anlageTurntable232 = anlageTurnTableController.AnlageController("192.168.200.232")
anlageTurntable233 = anlageTurnTableController.AnlageController("192.168.200.233")
anlageTurntable234 = anlageTurnTableController.AnlageController("192.168.200.234")

t1 = threading.Thread(target=anlageTurntable231.default_behaviour, args=[])
t2 = threading.Thread(target=anlageTurntable232.default_behaviour, args=[])
t3 = threading.Thread(target=anlageTurntable233.default_behaviour, args=[])
t4 = threading.Thread(target=anlageTurntable234.default_behaviour, args=[])

t1.start()
t2.start()
t3.start()
t4.start()