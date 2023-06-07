import time
from pyModbusTCP.client import ModbusClient
from pyModbusTCP.utils import test_bit
from pyModbusTCP.utils import set_bit
from pyModbusTCP.utils import reset_bit

# Verbindung zum Lagersystem
ip = "192.168.200.237"


# init modbus client
c = ModbusClient(host=ip, port=502, unit_id=1,  auto_open=True)


# Bewegung des Roboters 
"""
Bit     Sensor

0       Bewegung in X-Richtung erlaubt
1       Bewegung in X-Richtung beendet 
2       Bewegung in Y-Richtung erlaubt
3       Bewegung in Y-Richtung beendet
4       Greifer ist oben
5       Greifer ist unten
6       Greifer ist geöffnet 
7       Greifer ist geschlossen 
8       Teil vorhanden 
9       Sicherheitstür geschlossen 
"""

"""
Bit     Aktor

0-3     X-Koordinate des Lagerplatzes 
4       Bewegung in X-Richtung starten 
5-8     Y-Koordinate des Lagerplatzes 
9       Bewegung in Y-Richtung starten
10      Greifer nach oben bewegen
11      Greifer nach unten bewegen 
12      Greifer öffnen
13      Greifer schließen
14      Bewegungsfreigabe setzen
15      Beleuctung einschalten 

"""
# Koordinatenspeicherung des Lagerplatzes 

"""
Bit     Aktor

0-3     X-Koordinate des Lagerplatzes 
5-8     Y- Koordiante des Lagerplatzes 

"""
# Untergeordnete Deziamlzahlen der Koordinatenspeicherung 
"""
Dec     Func

0       Referenzpunkt der Achse
1-9     Koordinate 
10      Zugangsband 1
11      Zugangsband 2
12      Zugangsband 3 
13      -
14      Schritt entgegen Achsrichtung 
15      Schritt in Achsrichtung 


"""