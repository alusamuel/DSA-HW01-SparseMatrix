# Sparse Matrix Operations in Python

This project implements a `SparseMatrix` class in Python that supports **loading**, **saving**, **addition**, **subtraction**, and **multiplication** of sparse matrices. It also includes a **text-based loader animation** for long operations and a command-line interface to demonstrate the functionality.


## Features

- Load sparse matrix from a file.
- Perform matrix operations: `add`, `subtract`, and `multiply`.
- Save results to text files.
- Display matrix data in a clean format.
- Text-based loader animation using threading.
- Error handling for file I/O and dimension mismatches.


## File Structure

```

.
├── easy\_sample\_01\_2.txt         # First matrix file (input)
├── easy\_sample\_01\_3.txt         # Second matrix file (input)
├── addition\_result.txt          # Output after addition
├── subtraction\_result.txt       # Output after subtraction
├── multiplication\_result.txt    # Output after multiplication
├── sparse\_matrix.py             # Main Python script
└── README.md                    # Project documentation

```


## Matrix File Format

Matrix input files must follow this structure:

```

rows=3
cols=3
(0, 1, 4)
(1, 0, 2)
(2, 2, 5)

````

- The first two lines define the number of rows and columns.
- The remaining lines represent non-zero values in the format `(row, col, value)`.


## How to Run

1. Clone or download the repository.

2. Place your matrix input files (`easy_sample_01_2.txt` and `easy_sample_01_3.txt`) in the same directory.

3. Run the script:

```bash
python sparse_matrix.py
````

The program will:

* Load two matrices from the text files.
* Print the matrices.
* Perform addition, subtraction, and multiplication.
* Display the results in the terminal.
* Save the results to respective output text files.


## Example Output

```
Matrix 1:
(0, 1, 4)
(1, 0, 2)

Matrix 2:
(0, 1, 1)
(2, 2, 3)

Performing Addition...
Addition Result:
(0, 1, 5)
(1, 0, 2)
(2, 2, 3)
```


## Dependencies

This project uses only built-in Python libraries:

* `os`
* `sys`
* `time`
* `threading`


## Notes

* Multiplication requires the number of columns in Matrix 1 to match the number of rows in Matrix 2.
* All results are saved to `.txt` files in the current working directory.


## License

This project is open-source and free to use under the MIT License.


## Author

Samuel Rurangamirwa
[GitHub](https://github.com/alusamuel) | [LinkedIn](https://linkedin.com/in/samuelrurangamirwa)

