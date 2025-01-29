import minimalmodbus
from dataclasses import dataclass

@dataclass
class Sample(object):
    batteryVoltage: float
    batteryCurrent: float
    gridVoltage: float
    loadPercent: int
    inverterVoltage: float
    loadPower: float
    acRadiatorTemperature: int
    accumulatedPower: int
    pvVoltage: float
    chChargerCurrent: float
    chargerPower: int
    radiatorTemperature: int
    batStopDischargingV: float
    batStopChargingV: float
    batLowVoltage: float
    inverterCurrent: float
    gridCurrent: float
    loadCurrent: float
    gridPower: int
    inverterFrequency: float
    gridFrequency: float
    transformerTemperature: int
    dcRadiatorTemperature: int
    accumulatedChargerPower: int
    accumulatedDischargerPower: int
    accumulatedBuyPower: int
    accumulatedSellPower: int
    accumulatedLoadPower: int
    accumulatedSelfUsePower: int
    accumulatedPvSellPower: int
    accumulatedGridChargerPower: int
    batteryPower: int
    ChargingState: str
    workState: str
    mpptState: str
    charger_priority: int
    solarUse_aim: int
    energy_use_mode: int
    float_volt: float
    absorb_volt: float

class UPS(object):
    def __init__(self, device_path: str, device_id: int, baud_rate: int):
        self.device_path = device_path
        self.device_id = device_id
        self.baud_rate = baud_rate

        self.scc = minimalmodbus.Instrument(device_path, device_id)
        self.scc.serial.baudrate = baud_rate
        self.scc.serial.timeout = 0.5

    def sample(self) -> Sample:
        pass
