# Interactive Lexical Analyzer System - Usage Instructions

## 🎓 Educational Project for Compiler Design Course

This document provides complete instructions for using the Interactive Lexical Analyzer System.

## 📋 System Components

1. **C++ Lexical Analyzer Engine** (`lexer.cpp`) - Core tokenization logic
2. **Python Flask Backend** (`app.py`) - Web API server
3. **Web Frontend** (`index.html`) - Interactive user interface
4. **Sample C++ File** (`sample.cpp`) - Test code
5. **Python Test Script** (`test_lexer.py`) - Standalone tokenization demo

## ▶️ Quick Start Guide

### Option 1: Web Interface (Recommended for Students)

1. **Start the Flask server:**
   ```bash
   python app.py
   ```

2. **Open your browser and go to:**
   ```
   http://localhost:5000
   ```

3. **Use the web interface:**
   - Write/paste C++ code in the text area
   - Or upload a .cpp file
   - Click "Analyze Code" to see results
   - Export results to CSV/JSON if needed

### Option 2: Command Line Interface

#### Using the Python Test Script (No compilation needed):
```bash
python test_lexer.py
```
This will analyze a sample C++ program and save results to `tokens.txt`.

#### Using the C++ Lexer (Requires C++ compiler):
1. **Compile the lexer:**
   - Windows (MinGW): `g++ lexer.cpp -o lexer.exe`
   - Windows (Visual Studio): `cl /EHsc lexer.cpp`
   - Linux/Mac: `g++ lexer.cpp -o lexer`

2. **Run the lexer:**
   - Windows: `lexer.exe`
   - Linux/Mac: `./lexer`

3. **Choose input method:**
   - Option 1: Analyze from file
   - Option 2: Enter code manually

## 🧪 Testing the System

### Test Files Included:
- `sample.cpp` - Comprehensive C++ code example
- `test_lexer.py` - Python implementation for testing without compilation

### Expected Output:
The system generates a `tokens.txt` file with:
1. Tokenized output in table format (line number, token, type)
2. Summary statistics (total tokens, count by category)

## 🎯 Learning Outcomes

This system demonstrates:
- Token classification in programming languages
- Regular expressions for pattern matching
- Lexical analysis process
- Web API integration with backend processes
- Software architecture patterns

## 🛠️ Troubleshooting

### If you see "cl is not recognized" or "g++ is not recognized":
1. Install a C++ compiler:
   - Windows: Install MinGW, Visual Studio Build Tools, or TDM-GCC
   - Linux: Install build-essential package
   - Mac: Install Xcode command line tools

2. Add the compiler to your PATH environment variable

### If the web interface doesn't load:
1. Ensure Flask is installed: `pip install flask`
2. Check that port 5000 is not in use
3. Try accessing `http://127.0.0.1:5000` instead of `localhost:5000`

## 📚 Educational Use Cases

### Classroom Demonstrations:
1. Show real-time tokenization of student-submitted code
2. Compare tokenization results of different C++ constructs
3. Demonstrate comment removal functionality

### Student Exercises:
1. Modify the lexer to support additional token types
2. Add support for C++11/14/17/20 features
3. Extend the web interface with additional visualizations
4. Implement error handling for malformed C++ code

## 📤 Exporting Results

The web interface allows exporting to:
- CSV format (for spreadsheet analysis)
- JSON format (for programmatic processing)

## 🏗️ Extending the System

### Adding New Keywords:
Modify the `keywords` vector in `lexer.cpp` and `KEYWORDS` set in `test_lexer.py`.

### Adding New Operators:
Modify the `operators` vector in `lexer.cpp` and `OPERATORS` set in `test_lexer.py`.

### Adding New Punctuations:
Modify the `punctuations` vector in `lexer.cpp` and `PUNCTUATIONS` set in `test_lexer.py`.

## 📝 Notes for Instructors

1. The system is designed to be educational, with well-commented code
2. Both C++ and Python implementations are provided for comparison
3. The web interface makes demonstrations more engaging
4. Export functionality supports classroom exercises and assignments
5. The modular design allows for easy extension and modification

## 👨‍💻 Developed By

Developed for Compiler Design Course