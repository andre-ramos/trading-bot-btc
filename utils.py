from enum import auto
from enum import Enum

class TimeFrame(Enum):

        timestamp = "%Y-%m-%d %H:%M:%S"
        m1 = "1m"
        m5 = "5m"
        m15 = "15m" #tempo ancora, niveis de resistencia, checar no m5 e m1 se é espelhado
        m30 = "30m"
        m45 = "45m"
        Hour = "1h"
        Hour2 = "2h"
        Hour4 = "4h"
        Day = "1day"
        Week = "1week"
        Month = "1month"