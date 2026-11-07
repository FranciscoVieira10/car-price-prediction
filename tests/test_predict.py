import unittest

from src.predict import predict_price


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


if __name__ == "__main__":
    unittest.main()
