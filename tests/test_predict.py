import unittest

from src.predict import load_model, predict_price


class FakeModel:
    def predict(self, car_df):
        return [32000.0]


class TestPredict(unittest.TestCase):

    def test_predict_price(self):
        model = FakeModel()

        car = {
            "make": "BMW",
            "mileage_numeric": 80000
        }

        result = predict_price(model, car)

        self.assertEqual(result, 32000.0)


class TestRealModel(unittest.TestCase):
    """Sanity checks with the real CatBoost model."""

    @classmethod
    def setUpClass(cls):
        cls.model = load_model()
        cls.car = {
            "make": "Alfa Romeo",
            "model": "145",
            "mileage_numeric": 80000,
            "vehicle_age": 5,
            "power_hp": 190,
            "fuel_category": "Diesel",
            "transmission": "Manual",
            "body_type": "Sedan",
            "country_code": "AT",
        }

    def test_price_is_positive(self):
        self.assertGreater(predict_price(self.model, self.car), 0)

    def test_higher_mileage_lowers_price(self):
        low = predict_price(self.model, {**self.car, "mileage_numeric": 30000})
        high = predict_price(self.model, {**self.car, "mileage_numeric": 250000})

        self.assertLess(high, low)

    def test_older_car_lowers_price(self):
        new = predict_price(self.model, {**self.car, "vehicle_age": 2})
        old = predict_price(self.model, {**self.car, "vehicle_age": 15})

        self.assertLess(old, new)


if __name__ == "__main__":
    unittest.main()
