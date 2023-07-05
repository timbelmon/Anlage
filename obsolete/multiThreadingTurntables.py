import threading
import Anlage.anlageTurnTableController as anlageTurnTableController

anlageTurntable231 = anlageTurnTableController.AnlageController("192.168.200.231")
anlageTurntable232 = anlageTurnTableController.AnlageController("192.168.200.232")
anlageTurntable233 = anlageTurnTableController.AnlageController("192.168.200.233")
anlageTurntable234 = anlageTurnTableController.AnlageController("192.168.200.234")

anlageTurntable231.default_behaviour(True)
anlageTurntable232.default_behaviour(True)
anlageTurntable233.default_behaviour(True)
anlageTurntable234.default_behaviour(True)
