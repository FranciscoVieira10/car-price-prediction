import json
import unittest
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent


class TestValidCategories(unittest.TestCase):
    """Checks that the menu options in the JSON match the real dataset."""

    @classmethod
    def setUpClass(cls):
        with open(PROJECT_ROOT / "config" / "valid_categories.json", encoding="utf-8") as file:
            cls.categories = json.load(file)

        cls.df = pd.read_csv(PROJECT_ROOT / "data" / "processed" / "cars_clean.csv")

    def test_every_model_has_body_types_and_transmissions(self):
        for make, fuels in self.categories["models_by_make_and_fuel"].items():
            for fuel, models in fuels.items():
                for model in models:
                    self.assertTrue(self.categories["body_types_by_make_fuel_model"][make][fuel][model])
                    self.assertTrue(self.categories["transmissions_by_make_fuel_model"][make][fuel][model])
                    self.assertIn(model, self.categories["power_median_by_make_fuel_model"][make][fuel])

    def test_body_type_combinations_exist_in_dataset(self):
        real = set(zip(self.df["make"], self.df["fuel_category"], self.df["model"], self.df["body_type"]))

        for make, fuels in self.categories["body_types_by_make_fuel_model"].items():
            for fuel, models in fuels.items():
                for model, body_types in models.items():
                    for body_type in body_types:
                        self.assertIn((make, fuel, model, body_type), real)

    def test_transmission_combinations_exist_in_dataset(self):
        real = set(zip(self.df["make"], self.df["fuel_category"], self.df["model"], self.df["transmission"]))

        for make, fuels in self.categories["transmissions_by_make_fuel_model"].items():
            for fuel, models in fuels.items():
                for model, transmissions in models.items():
                    for transmission in transmissions:
                        self.assertIn((make, fuel, model, transmission), real)


if __name__ == "__main__":
    unittest.main()
