from src.generate_data import generate_data
from src.preprocess import preprocess_data
from src.eda import run_eda
from src.forecast import train_model
from src.inventory import create_inventory_recommendations

def main():
    print("\nSTEP 1/5: Generate sample retail data")
    generate_data()
    print("\nSTEP 2/5: Clean the data")
    preprocess_data()
    print("\nSTEP 3/5: Create EDA charts")
    run_eda()
    print("\nSTEP 4/5: Train forecasting model")
    train_model()
    print("\nSTEP 5/5: Create inventory recommendations")
    create_inventory_recommendations()
    print("\nPIPELINE COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
