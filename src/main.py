from pathlib import Path
import json

from src.predict import load_model, predict_price
from src.validation import ask_integer, ask_option


def main():
    # Locate the categories file
    project_root = Path(__file__).resolve().parent.parent
    categories_path = project_root / "config" / "valid_categories.json"

    # Load valid categories
    with open(categories_path, "r", encoding="utf-8") as file:
        valid_categories = json.load(file)

    # Ask for numerical characteristics
    car = {
        "mileage_numeric": ask_integer("Mileage (km): "),
        "vehicle_age": ask_integer("Vehicle age (years): "),
        "power_hp": ask_integer("Power (hp): ", minimum=1)
    }

    # Select make and model
    car["make"] = ask_option("Make", valid_categories["make"])

    car["model"] = ask_option(
        "Model",
        valid_categories["models_by_make"][car["make"]]
    )

    # Select the remaining categories
    car["fuel_category"] = ask_option(
        "Fuel category", valid_categories["fuel_category"]
    )

    car["transmission"] = ask_option(
        "Transmission", valid_categories["transmission"]
    )

    car["body_type"] = ask_option(
        "Body type", valid_categories["body_type"]
    )

    car["country_code"] = ask_option(
        "Country", valid_categories["country_code"]
    )

    # Load model and predict
    model = load_model()
    predicted_price = predict_price(model, car)

    print(f"\nEstimated price: €{predicted_price:,.2f}")


if __name__ == "__main__":
    main()
