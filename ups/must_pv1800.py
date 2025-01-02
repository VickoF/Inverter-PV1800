from . import Sample, UPS
import time
import minimalmodbus

class MustPV1800(UPS):
    def __init__(self, device_path: str):
        super().__init__(device_path, 4, 19200)

        # Определение
        self.work_states = {
            0: "PowerOn",
            1: "SelfTest",
            2: "OffGrid",
            3: "GridTie",
            4: "ByPass",
            5: "Stop",
            6: "GridCharging",
        }
        self.charging_states = {
            0: "Stop",
            1: "Absorb charge",
            2: "Float charge",
            3: "EQ charge",
        }
        self.mppt_states = {
            0: "Stop",
            1: "MPPT",
            2: "Current limiting",
        }
  
    def extract_register_data(self, registers: list[int], mapping: dict) -> dict:
        result = {}

        for key, (index, multiplier) in mapping.items():
            try:
                value = registers[index] * multiplier
                # корректировка с словарями (для str полей)
                if key == "work_state":
                    result[key] = self.work_states.get(value, f"Unknown {value}")
                elif key == "charging_state":
                    result[key] = self.charging_states.get(value, f"Unknown {value}")
                elif key == "mppt_state":
                    result[key] = self.mppt_states.get(value, f"Unknown {value}")
                else:
                    # корректировка для определённых значений
                    if key in ["inverter_frequency", "grid_power", "battery_power", "battery_current"]:
                        if value > 32000:
                            value = abs(value - 65536)  # Коррекция значений больше 65536 (16бит)
                    result[key] = value
            except IndexError:
                # если индекс нет значит None
                result[key] = None
            except Exception as e:
                # ошибоки если есть 
                print(f"Error processing {key}: {e}")
                result[key] = None
        
        return result
        
        

    def sample(self) -> Sample:
        try:
            # Чтение 40 регистров с паузой между запросами
            main_registers = []
            main_registers.extend(self.scc.read_registers(25200, 75))
            time.sleep(0.1) 
            solar_registers = self.scc.read_registers(15200, 20)
            time.sleep(0.1)  
            battery_registers = self.scc.read_registers(20100, 30)

            # Маппинг
            # ключ : [индекс диапазона, множитель]
            main_mapping = {
                "work_state":                           [1, 1],
                "battery_voltage":                      [5, 0.1],
                "inverter_voltage":                     [6, 0.1],
                "grid_voltage":                         [7, 0.1],
                "inverter_current":                     [10, 0.1],
                "grid_current":                         [11, 0.1],
                "load_current":                         [12, 0.1],
                "grid_power":                           [14, 1],
                "load_power":                           [15, 1],
                "load_percent":                         [16, 1],
                "inverter_frequency":                   [25, 0.01],
                "grid_frequency":                       [26, 0.01],
                "ac_radiator_temperature":              [33, 1],
                "transformer_temperature":              [34, 1],
                "dc_radiator_temperature":              [35, 1],
                "accumulated_charger_power":            [45, 1],
                "accumulated_discharger_power":         [47, 1],
                "accumulated_buy_power":                [49, 1],
                "accumulated_sell_power":               [51, 1],
                "accumulated_load_power":               [53, 1],
                "accumulated_self_use_power":           [55, 1],
                "accumulated_pv_sell_power":            [57, 1],
                "accumulated_grid_charger_power":       [59, 1],
                "battery_power":                        [73, 1],
                "battery_current":                      [74, 1],
            }
            solar_mapping = {
                "charging_state":                       [1, 1],
                "mppt_state":                           [2, 1],
                "pv_voltage":                           [5, 0.1],
                "ch_charger_current":                   [7, 0.1],
                "charger_power":                        [8, 1],
                "radiator_temperature":                 [9, 1],
                "accumulated_power":                    [17, 1],
            }
            battery_mapping = {
                "bat_stop_discharging_v":               [18, 0.1],
                "bat_stop_charging_v":                  [19, 0.1],
                "bat_low_voltage":                      [27, 0.1],           
            }

            # Обработка данных
            main_data = self.extract_register_data(main_registers, main_mapping)
            solar_data = self.extract_register_data(solar_registers, solar_mapping)
            battery_data = self.extract_register_data(battery_registers, battery_mapping)

            return Sample(
                main_data["battery_voltage"],
                main_data["battery_current"],
                main_data["grid_voltage"],
                main_data["load_percent"],
                main_data["inverter_voltage"],
                main_data["load_power"],
                main_data["ac_radiator_temperature"],
                solar_data["accumulated_power"],
                solar_data["pv_voltage"],
                solar_data["ch_charger_current"],
                solar_data["charger_power"],
                solar_data["radiator_temperature"],
                battery_data["bat_stop_discharging_v"],
                battery_data["bat_stop_charging_v"],
                battery_data["bat_low_voltage"],
                main_data["inverter_current"],
                main_data["grid_current"],
                main_data["load_current"],
                main_data["grid_power"],
                main_data["inverter_frequency"],
                main_data["grid_frequency"],
                main_data["transformer_temperature"],
                main_data["dc_radiator_temperature"],
                main_data["accumulated_charger_power"],
                main_data["accumulated_discharger_power"],
                main_data["accumulated_buy_power"],
                main_data["accumulated_sell_power"],
                main_data["accumulated_load_power"],
                main_data["accumulated_self_use_power"],
                main_data["accumulated_pv_sell_power"],
                main_data["accumulated_grid_charger_power"],
                main_data["battery_power"],
                solar_data["charging_state"],
                main_data["work_state"],
                solar_data["mppt_state"],                
            )

        except minimalmodbus.ModbusException as e:
            print(f"Error reading registers: {e}")
            return None
