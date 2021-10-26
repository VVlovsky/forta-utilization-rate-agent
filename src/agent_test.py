from src.agent import UtilizationRate


class TestUtilizationRate:
    def test_removes_old_logs(self):
        ur = UtilizationRate("SMILE")
        ur.add_rate(0.1, 50)
        ur.add_rate(0.1, 100)
        ur.add_rate(0.11, 120)
        ur.add_rate(0.12, 140)
        ur.add_rate(0.12, 160)
        ur.add_rate(0.12, 3701)
        _, _ = ur.analyze()

        assert len(ur.rates) == 4

    def test_returns_false_if_rate_dif_below_th(self):
        ur = UtilizationRate("HAPPY")
        ur.add_rate(0.1, 50)
        ur.add_rate(0.1, 100)
        ur.add_rate(0.12, 120)
        ur.add_rate(0.12, 140)
        ur.add_rate(0.1, 160)
        ur.add_rate(0.12, 3701)
        changed, _ = ur.analyze()

        assert not changed

    def test_returns_true_if_rate_dif_above_th(self):
        ur = UtilizationRate("SUNNY")
        ur.add_rate(0.12, 50)
        ur.add_rate(0.1, 100)
        ur.add_rate(0.2, 120)
        ur.add_rate(0.13, 140)
        ur.add_rate(0.12, 160)
        ur.add_rate(0.23, 3701)
        changed, _ = ur.analyze()

        assert changed
