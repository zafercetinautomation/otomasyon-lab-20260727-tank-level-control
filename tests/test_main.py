import unittest

from src.main import TankController


class TankControllerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.controller = TankController()

    def start_empty_tank(self):
        return self.controller.scan(
            start=True,
            low_sensor=False,
            high_sensor=False,
        )

    def test_start_opens_valve_for_empty_tank(self) -> None:
        state = self.start_empty_tank()

        self.assertTrue(state.cycle_enabled)
        self.assertTrue(state.inlet_valve)

    def test_high_sensor_closes_valve_and_marks_tank_full(self) -> None:
        self.start_empty_tank()
        state = self.controller.scan(
            low_sensor=True,
            high_sensor=True,
        )

        self.assertFalse(state.inlet_valve)
        self.assertTrue(state.tank_full)

    def test_hysteresis_keeps_valve_closed_between_sensors(self) -> None:
        self.start_empty_tank()
        self.controller.scan(low_sensor=True, high_sensor=True)
        state = self.controller.scan(
            low_sensor=True,
            high_sensor=False,
        )

        self.assertFalse(state.inlet_valve)
        self.assertFalse(state.fill_requested)

    def test_level_below_low_sensor_starts_new_fill(self) -> None:
        self.start_empty_tank()
        self.controller.scan(low_sensor=True, high_sensor=True)
        self.controller.scan(low_sensor=True, high_sensor=False)
        state = self.controller.scan(
            low_sensor=False,
            high_sensor=False,
        )

        self.assertTrue(state.inlet_valve)
        self.assertTrue(state.fill_requested)

    def test_stop_has_priority(self) -> None:
        self.start_empty_tank()
        state = self.controller.scan(
            stop=True,
            low_sensor=False,
            high_sensor=False,
        )

        self.assertFalse(state.cycle_enabled)
        self.assertFalse(state.inlet_valve)

    def test_auto_mode_off_closes_valve(self) -> None:
        self.start_empty_tank()
        state = self.controller.scan(
            auto_mode=False,
            low_sensor=False,
            high_sensor=False,
        )

        self.assertFalse(state.cycle_enabled)
        self.assertFalse(state.inlet_valve)

    def test_inconsistent_sensors_latch_fault(self) -> None:
        self.start_empty_tank()
        state = self.controller.scan(
            low_sensor=False,
            high_sensor=True,
        )

        self.assertTrue(state.sensor_fault)
        self.assertFalse(state.inlet_valve)
        self.assertFalse(state.tank_full)

    def test_fault_resets_only_after_sensors_are_consistent(self) -> None:
        self.start_empty_tank()
        self.controller.scan(low_sensor=False, high_sensor=True)

        still_faulted = self.controller.scan(
            low_sensor=False,
            high_sensor=True,
            reset_alarm=True,
        )
        self.assertTrue(still_faulted.sensor_fault)

        self.controller.scan(
            low_sensor=True,
            high_sensor=False,
            reset_alarm=False,
        )
        reset = self.controller.scan(
            low_sensor=True,
            high_sensor=False,
            reset_alarm=True,
        )

        self.assertFalse(reset.sensor_fault)
        self.assertFalse(reset.inlet_valve)


if __name__ == "__main__":
    unittest.main()
