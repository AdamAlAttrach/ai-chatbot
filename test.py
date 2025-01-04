import pandas as pd

def print_row_description(csv_file, row_index):
    """
    Prints the 'description' field of a specific row in the CSV file.
    Args:
        csv_file (str): Path to the CSV file.
        row_index (int): Index of the row to validate.
    """
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Check if the 'description' field exists
    if 'description' not in df.columns:
        print("The 'description' field does not exist in the CSV.")
        return
    
    # Check if the row index is valid
    if row_index < 0 or row_index >= len(df):
        print(f"Invalid row index. The CSV has {len(df)} rows.")
        return
    
    # Print the description of the specified row
    description = df.loc[row_index, 'description']
    print(f"Description for row {row_index}:")
    print(description)

# Example usage
csv_file = 'vehiclestest.csv'  # Path to your CSV with the 'description' field
row_index = 0  # Index of the row to validate
print_row_description(csv_file, row_index)
