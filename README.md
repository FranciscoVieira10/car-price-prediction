# AutoValue — Car Price Prediction

AutoValue is a machine learning project that estimates used-car listing prices based on vehicle characteristics.

The project covers the complete machine learning workflow, from exploratory data analysis and preprocessing to model training, evaluation, and deployment through an interactive Streamlit application.

## Features

- Interactive car price estimation.
- Dependent vehicle selection based on available combinations in the dataset.
- Support for eight European markets: Austria, Belgium, Germany, Spain, France, Italy, Luxembourg, and the Netherlands.
- A trained CatBoost regression model.
- Automated tests for predictions and input validation.

## Dataset

The project uses European used-car listing data.

After preprocessing, the dataset contains **108,273 vehicles**. Each vehicle is represented by nine input features:

| Feature | Description |
|---|---|
| Make | Car manufacturer |
| Model | Vehicle model |
| Mileage | Distance travelled in kilometres |
| Vehicle age | Age in years |
| Power | Engine power in horsepower |
| Fuel category | Type of fuel |
| Transmission | Transmission type |
| Body type | Vehicle body style |
| Country | European market |

The prediction target is the **advertised listing price**, not the final transaction price.

## Model Development

Several regression models were trained and compared, starting with simple baselines and progressing to more complex algorithms.

| Model | Test MAE |
|---|---:|
| Dummy Regressor | €34,978.86 |
| Linear Regression | €20,882.85 |
| Random Forest | €6,359.84 |
| **CatBoost** | **€5,686.50** |

CatBoost was selected as the final model based on its performance.

### Final Model Performance

| Metric | Test Result |
|---|---:|
| MAE | €5,686.50 |
| RMSE | €30,342.40 |
| R² | 0.9218 |

The relatively high RMSE reflects the influence of rare, exceptionally expensive vehicles that produce larger prediction errors.

## Running the Application

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
python -m streamlit run src/app.py
```

The final CatBoost model is stored in `models/catboost_final.joblib` using Git LFS. Make sure the model file has been downloaded correctly.

## Running the Tests

```bash
python -m unittest discover -s tests -v
```

The project currently contains 11 automated tests covering input validation, dataset categories, and prediction behaviour.

## Technologies

Python, Pandas, NumPy, Scikit-learn, CatBoost, Matplotlib, Streamlit, Joblib and Jupyter Notebook.

## Limitations

Predictions are estimates based on historical advertised prices. Accuracy may be lower for rare or expensive vehicles, unusual feature combinations, or markets and conditions that are not well represented in the training data.

The model should not be interpreted as providing guaranteed market valuations.

## Project Status

Model development and local application implementation are complete. Public deployment is the next step.