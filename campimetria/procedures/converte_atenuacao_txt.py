
import os
def read_file_to_list(file_path, start_line=6):
   
    values = []
    try:
        with open(file_path, 'r') as file:
            for current_line_number, line in enumerate(file, start=1):
                if current_line_number >= start_line:
                    values.append(int(line.strip()))
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return values

if __name__ == "__main__":
    # Example usage
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "atenuacao_teste", "exame.txt"))
    result = read_file_to_list(file_path)
    print("Extracted values:")
    print(result)