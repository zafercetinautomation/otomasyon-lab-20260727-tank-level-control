"""İki sensörlü otomatik tank dolum kontrolünün eğitim simülasyonu."""

from dataclasses import dataclass, field


@dataclass
class TankState:
    """Bir PLC taramasından sonra gözlemlenen kontrol durumu."""

    cycle_enabled: bool = False
    fill_requested: bool = False
    inlet_valve: bool = False
    tank_full: bool = False
    sensor_fault: bool = False


@dataclass
class TankController:
    """TwinCAT örneğindeki histerezis ve alarm mantığını simüle eder."""

    state: TankState = field(default_factory=TankState)
    _previous_start: bool = False
    _previous_reset: bool = False

    def scan(
        self,
        *,
        auto_mode: bool = True,
        start: bool = False,
        stop: bool = False,
        low_sensor: bool = False,
        high_sensor: bool = False,
        reset_alarm: bool = False,
    ) -> TankState:
        """Bir PLC taraması çalıştırır ve güncel durumu döndürür."""

        start_edge = start and not self._previous_start
        reset_edge = reset_alarm and not self._previous_reset
        self._previous_start = start
        self._previous_reset = reset_alarm

        sensor_invalid = high_sensor and not low_sensor
        if sensor_invalid:
            self.state.sensor_fault = True

        if stop or not auto_mode:
            self.state.cycle_enabled = False
            self.state.fill_requested = False

        if (
            reset_edge
            and not sensor_invalid
            and not self.state.cycle_enabled
        ):
            self.state.sensor_fault = False

        if start_edge and auto_mode and not self.state.sensor_fault:
            self.state.cycle_enabled = True
            self.state.fill_requested = not high_sensor

        if self.state.sensor_fault:
            self.state.cycle_enabled = False
            self.state.fill_requested = False
        elif self.state.cycle_enabled:
            if high_sensor:
                self.state.fill_requested = False
            elif not low_sensor:
                self.state.fill_requested = True

        self.state.tank_full = (
            high_sensor and low_sensor and not self.state.sensor_fault
        )
        self.state.inlet_valve = (
            auto_mode
            and self.state.cycle_enabled
            and self.state.fill_requested
            and not high_sensor
            and not self.state.sensor_fault
        )
        return self.state


def format_status(
    label: str,
    state: TankState,
    *,
    low_sensor: bool,
    high_sensor: bool,
) -> str:
    """Demo çıktısını okunabilir Türkçe metne dönüştürür."""

    valve = "AÇIK" if state.inlet_valve else "KAPALI"
    return (
        f"{label} | vana={valve} | alt={int(low_sensor)} | "
        f"üst={int(high_sensor)} | dolu={int(state.tank_full)} | "
        f"hata={int(state.sensor_fault)}"
    )


def demo() -> None:
    """Dolum, durma ve histerezis davranışını gösterir."""

    controller = TankController()
    scenarios = [
        ("Başlatıldı", dict(start=True, low_sensor=False, high_sensor=False)),
        ("Alt seviyeye ulaştı", dict(low_sensor=True, high_sensor=False)),
        ("Tank doldu", dict(low_sensor=True, high_sensor=True)),
        ("Histerezis bölgesi", dict(low_sensor=True, high_sensor=False)),
        ("Yeni dolum", dict(low_sensor=False, high_sensor=False)),
    ]

    for label, inputs in scenarios:
        state = controller.scan(**inputs)
        print(
            format_status(
                label,
                state,
                low_sensor=inputs["low_sensor"],
                high_sensor=inputs["high_sensor"],
            )
        )


if __name__ == "__main__":
    demo()
