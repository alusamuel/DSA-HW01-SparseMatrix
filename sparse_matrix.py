import time
import sys
import os
import threading

class SparseMatrix:
    """
    A class to represent a sparse matrix and perform operations on it.
    """

    def __init__(self, matrixFilePath=None, numRows=None, numCols=None):
        """
        Initialize the sparse matrix.

        Args:
            matrixFilePath (str, optional): Path to the file containing matrix data.
            numRows (int, optional): Number of rows in the matrix.
            numCols (int, optional): Number of columns in the matrix.
        """
        self.matrix = {}
        if matrixFilePath:
            self.loadFromFile(matrixFilePath)
        else:
            self.numRows = numRows
            self.numCols = numCols

    def loadFromFile(self, matrixFilePath):
        """
        Load matrix data from a file.

        Args:
            matrixFilePath (str): Path to the file containing matrix data.
        """
        try:
            with open(matrixFilePath, 'r') as file:
                lines = file.readlines()
                self.numRows = int(lines[0].split('=')[1].strip())
                self.numCols = int(lines[1].split('=')[1].strip())
                for line in lines[2:]:
                    line = line.strip().strip('()')
                    row, col, value = map(int, line.split(','))
                    self.matrix[(row, col)] = value
        except FileNotFoundError:
            print(f"Error: The file {matrixFilePath} was not found.")
        except Exception as e:
            print(f"An error occurred while loading the file: {e}")

    def getElement(self, currRow, currCol):
        """
        Retrieve the value at the specified row and column.

        Args:
            currRow (int): Row index.
            currCol (int): Column index.

        Returns:
            int: The value at the specified row and column, default to 0 if not found.
        """
        return self.matrix.get((currRow, currCol), 0)

    def setElement(self, currRow, currCol, value):
        """
        Set the value at the specified row and column.

        Args:
            currRow (int): Row index.
            currCol (int): Column index.
            value (int): Value to set.
        """
        if value != 0:
            self.matrix[(currRow, currCol)] = value
        elif (currRow, currCol) in self.matrix:
            del self.matrix[(currRow, currCol)]

    def add(self, other):
        """
        Add two matrices and return the result.

        Args:
            other (SparseMatrix): The matrix to add.

        Returns:
            SparseMatrix: The result of the addition.
        """
        result = SparseMatrix(numRows=max(self.numRows, other.numRows), numCols=max(self.numCols, other.numCols))

        for (row, col), value in self.matrix.items():
            if row < result.numRows and col < result.numCols:
                result.setElement(row, col, value + other.getElement(row, col))

        for (row, col), value in other.matrix.items():
            if row < result.numRows and col < result.numCols:
                result.setElement(row, col, self.getElement(row, col) + value)

        return result

    def subtract(self, other):
        """
        Subtract two matrices and return the result.

        Args:
            other (SparseMatrix): The matrix to subtract.

        Returns:
            SparseMatrix: The result of the subtraction.
        """
        result = SparseMatrix(numRows=max(self.numRows, other.numRows), numCols=max(self.numCols, other.numCols))

        for (row, col), value in self.matrix.items():
            if row < result.numRows and col < result.numCols:
                result.setElement(row, col, value - other.getElement(row, col))

        for (row, col), value in other.matrix.items():
            if row < result.numRows and col < result.numCols:
                result.setElement(row, col, self.getElement(row, col) - value)

        return result

    def multiply(self, other):
        """
        Multiply two matrices and return the result.

        Args:
            other (SparseMatrix): The matrix to multiply.

        Returns:
            SparseMatrix: The result of the multiplication.
        """
        # Check if multiplication is possible
        if self.numCols != other.numRows:
            print("Error: Number of columns in the first matrix must equal the number of rows in the second matrix for multiplication.")
            sys.exit(1)  # Terminate the program if dimensions are incompatible

        # Initialize result matrix with correct dimensions
        result = SparseMatrix(numRows=max(self.numRows, other.numRows), numCols=max(self.numCols, other.numCols))

        # Perform multiplication
        for (row, col), value in self.matrix.items():
            for other_col in range(other.numCols):
                other_value = other.getElement(col, other_col)
                if other_value != 0:
                    current_value = result.getElement(row, other_col)
                    result.setElement(row, other_col, current_value + value * other_value)

        return result

    def saveToFile(self, filePath):
        """
        Save the matrix to a file.

        Args:
            filePath (str): Path to the file where the matrix will be saved.
        """
        try:
            with open(filePath, 'w') as file:
                file.write(f"rows={self.numRows}\n")
                file.write(f"cols={self.numCols}\n")
                for (row, col), value in self.matrix.items():
                    file.write(f"({row}, {col}, {value})\n")
        except Exception as e:
            print(f"An error occurred while saving the file: {e}")

    def __str__(self):
        """
        Return a string representation of the matrix.

        Returns:
            str: String representation of the matrix.
        """
        return "\n".join([f"({row}, {col}, {value})" for (row, col), value in self.matrix.items()])

def loader(stop_event):
    """
    Display a simple text-based loader animation.

    Args:
        stop_event (threading.Event): Event to signal when to stop the loader.
    """
    animation = "|/-\\"
    idx = 0
    while not stop_event.is_set():
        print(f"Calculating... {animation[idx % len(animation)]}", end="\r")
        idx += 1
        time.sleep(0.1)

def main():
    """
    Main function to test the SparseMatrix class.
    """
    try:
        # Load matrices from files
        matrix1 = SparseMatrix(matrixFilePath='easy_sample_01_2.txt')
        matrix2 = SparseMatrix(matrixFilePath='easy_sample_01_3.txt')

        # Print matrices
        print("Matrix 1:")
        print(matrix1)
        print("\nMatrix 2:")
        print(matrix2)

        # Perform addition
        print("\nPerforming Addition...")
        stop_event = threading.Event()
        loader_thread = threading.Thread(target=loader, args=(stop_event,))
        loader_thread.start()
        addition_result = matrix1.add(matrix2)
        time.sleep(2)  # Simulate a delay for calculation
        stop_event.set()
        loader_thread.join()
        sys.stdout.write("\033[K")  # Clear the loader line
        print("\nAddition Result:")
        print(addition_result)
        addition_file_path = os.path.join(os.getcwd(), 'addition_result.txt')
        addition_result.saveToFile(addition_file_path)
        print(f"\nAddition result saved to: {addition_file_path}")

        # Perform subtraction
        print("\nPerforming Subtraction...")
        stop_event = threading.Event()
        loader_thread = threading.Thread(target=loader, args=(stop_event,))
        loader_thread.start()
        subtraction_result = matrix1.subtract(matrix2)
        time.sleep(2)  # Simulate a delay for calculation
        stop_event.set()
        loader_thread.join()
        sys.stdout.write("\033[K")  # Clear the loader line
        print("\nSubtraction Result:")
        print(subtraction_result)
        subtraction_file_path = os.path.join(os.getcwd(), 'subtraction_result.txt')
        subtraction_result.saveToFile(subtraction_file_path)
        print(f"\nSubtraction result saved to: {subtraction_file_path}")

        # Perform multiplication
        print("\nPerforming Multiplication...")
        stop_event = threading.Event()
        loader_thread = threading.Thread(target=loader, args=(stop_event,))
        loader_thread.start()
        multiplication_result = matrix1.multiply(matrix2)
        time.sleep(2)  # Simulate a delay for calculation
        stop_event.set()
        loader_thread.join()
        sys.stdout.write("\033[K")  # Clear the loader line
        print("\nMultiplication Result:")
        print(multiplication_result)
        multiplication_file_path = os.path.join(os.getcwd(), 'multiplication_result.txt')
        multiplication_result.saveToFile(multiplication_file_path)
        print(f"\nMultiplication result saved to: {multiplication_file_path}")

    except ValueError as ve:
        print(f"Value Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()