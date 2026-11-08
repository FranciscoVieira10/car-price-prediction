
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

    # Select make
    car["make"] = ask_option("Make", valid_categories["make"])

    # Show fuels available for the selected make
    available_fuels = sorted(
        valid_categories["models_by_make_and_fuel"][car["make"]].keys()
    )

    car["fuel_category"] = ask_option("Fuel category", available_fuels)

    # Show models available for the selected make and fuel
    available_models = valid_categories["models_by_make_and_fuel"][car["make"]][car["fuel_category"]]

    car["model"] = ask_option("Model", available_models)

    # Select remaining categories
    # Show transmissions available for the selected make, fuel and model
    available_transmissions = valid_categories["transmissions_by_make_fuel_model"][car["make"]][car["fuel_category"]][car["model"]]

    car["transmission"] = ask_option("Transmission", available_transmissions)

    # Show body types available for the selected make, fuel and model
    available_body_types = valid_categories["body_types_by_make_fuel_model"][car["make"]][car["fuel_category"]][car["model"]]

    car["body_type"] = ask_option("Body type", available_body_types)

    car["country_code"] = ask_option(
        "Country", valid_categories["country_code"]
    )

    # Load model and predict price
    model = load_model()
    predicted_price = predict_price(model, car)

    print(f"\nEstimated price: €{predicted_price:,.2f}")


if __name__ == "__main__":
    main()
