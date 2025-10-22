# Welcome to your  project

## Project info


# Interactive Lexical Analyzer System

Developed for Compiler Design Course

## 🎓 Overview

This project is a complete Interactive Lexical Analyzer System designed for educational purposes in a Compiler Design course. 
It tokenizes and classifies C++ code, removes comments, counts tokens, and provides both CLI and web interfaces.

## 🧩 Components

1. **C++ Lexical Analyzer Engine** (`lexer.cpp`)
2. **Python Flask Backend** (`app.py`)
3. **Web Frontend** (`index.html`)
4. **Sample C++ File** (`sample.cpp`)

## 🛠️ Installation & Setup

### Prerequisites

- C++ compiler (Visual Studio, MinGW, g++, or clang++)
- Python 3.x
- Flask library

### Installing a C++ Compiler

#### Option 1: Install MinGW (Windows)
1. Download MinGW from [mingw-w64.org](https://www.mingw-w64.org/downloads/)
2. Install and add to PATH
3. Verify installation: `g++ --version`

#### Option 2: Install Visual Studio Build Tools
1. Download Visual Studio Build Tools from Microsoft
2. Install C++ build tools
3. Verify installation: `cl /?`

#### Option 3: Install TDM-GCC (Windows)
1. Download TDM-GCC from [jmeubank.github.io/tdm-gcc](https://jmeubank.github.io/tdm-gcc/)
2. Install and add to PATH
3. Verify installation: `g++ --version`

### Installing Python Dependencies

```bash
# Install Flask using requirements.txt
pip install -r requirements.txt

# Or install Flask directly
pip install flask
```

## ▶️ Running the System

### Method 1: Command Line Interface

#### On Windows with MinGW/g++:
1. **Compile the lexer:**
   ```cmd
   g++ lexer.cpp -o lexer.exe
   ```

2. **Run the lexer:**
   ```cmd
   lexer.exe
   ```
   
   You'll be prompted to:
   - Enter 1 to analyze from a file
   - Enter 2 to enter code manually

#### On Windows with Visual Studio:
1. **Compile the lexer:**
   ```cmd
   cl /EHsc lexer.cpp
   ```

2. **Run the lexer:**
   ```cmd
   lexer.exe
   ```
   
   You'll be prompted to:
   - Enter 1 to analyze from a file
   - Enter 2 to enter code manually

#### On Linux/Mac (g++):
1. **Compile the lexer:**
   ```bash
   g++ lexer.cpp -o lexer
   ```

2. **Run the lexer:**
   ```bash
   ./lexer
   ```
   
   You'll be prompted to:
   - Enter 1 to analyze from a file
   - Enter 2 to enter code manually

### Method 2: Web Interface

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

## 📁 Project Structure

```
compiler-pro/
├── lexer.cpp          # C++ lexical analyzer engine
├── app.py             # Flask backend
├── index.html         # Web frontend
├── sample.cpp         # Sample C++ file for testing
├── tokens.txt         # Output file (generated after analysis)
├── input.cpp          # Temporary file (generated during web analysis)
├── lexer.exe          # Compiled lexer (generated after compilation)
└── README.md          # This file
```

## 🧠 Features

### Core Lexical Analysis
- Tokenizes C++ code into:
  - Keywords
  - Identifiers
  - Numbers
  - Operators
  - Punctuations
- Removes single-line (`//`) and multi-line (`/* */`) comments
- Counts tokens by category
- Shows line numbers for each token

### Output
- Console display (CLI)
- File output (`tokens.txt`)
- Web interface with table display
- Summary statistics

### Web Interface Features
- Clean, responsive design
- Syntax highlighting in input area
- File upload capability
- Token results in table format
- Summary statistics display
- Export to CSV/JSON functionality

## 📈 Educational Enhancements

- Line numbers in token output
- Total token count and breakdown by type
- Export functionality for classroom exercises
- Well-commented, modular code for learning
- Easy to extend for additional token types

## 🎯 Usage Examples

### CLI Usage

```bash
# Compile
g++ lexer.cpp -o lexer

# Run with file input
./lexer
# Choose option 1, then enter filename

# Run with manual input
./lexer
# Choose option 2, then enter code
# Press Ctrl+D (Linux/Mac) or Ctrl+Z (Windows) to finish
```

### Web Usage

1. Start the server: `python app.py`
2. Visit `http://localhost:5000`
3. Enter C++ code or upload a file
4. Click "Analyze Code"
5. View results and export if needed

## 📤 Output Format

### tokens.txt
```
Developed for Compiler Design Course
=====================================

Tokens:
========================================
Line | Token               | Type
-----|---------------------|------------
   1 | #include            | PREPROCESSOR
   1 | <iostream>          | PREPROCESSOR
   3 | using               | KEYWORD
   3 | namespace           | KEYWORD
   3 | std                 | IDENTIFIER
   5 | int                 | KEYWORD
   5 | main                | IDENTIFIER
   5 | (                   | PUNCTUATION
   5 | )                   | PUNCTUATION
   6 | {                   | PUNCTUATION
   7 | int                 | KEYWORD
   7 | x                   | IDENTIFIER
   7 | =                   | OPERATOR
   7 | 10                  | NUMBER
   7 | ;                   | PUNCTUATION
...

Summary:
========================================
Total Tokens: 25
Keywords: 8
Identifiers: 7
Numbers: 2
Operators: 3
Punctuations: 5
```

## 🚀 Hosting for Class Demonstration

To host this application on a network for class demonstration:

1. **Modify app.py:**
   ```python
   if __name__ == '__main__':
       app.run(debug=True, host='0.0.0.0', port=5000)
   ```

2. **Find your IP address:**
   - Windows: `ipconfig`
   - Mac/Linux: `ifconfig`

3. **Access from other devices:**
   ```
   http://YOUR_IP_ADDRESS:5000
   ```

## 🛠️ Customization

### Adding New Keywords
Modify the `keywords` vector in [lexer.cpp](lexer.cpp):
```cpp
std::vector<std::string> keywords = {
    // ... existing keywords ...
    "new_keyword"
};
```

### Adding New Operators
Modify the `operators` vector in [lexer.cpp](lexer.cpp):
```cpp
std::vector<std::string> operators = {
    // ... existing operators ...
    "new_operator"
};
```

## 📚 Learning Outcomes

This project helps students understand:
- Token classification in programming languages
- Regular expressions for pattern matching
- Finite automata concepts
- Lexical analysis process
- Web API integration with backend processes
- Software architecture patterns

## 📝 Notes

- The lexer handles C++17 standard keywords
- Comments are completely removed from analysis
- The web interface automatically compiles the lexer on first use
- Exported CSV/JSON files can be used for assignments

## 👨‍💻 Developed By

TSINUEKAL(tsinucode)

Developed for Compiler Design Course#
here: [Setting up a custom domain](https://docs.lovable.dev/features/custom-domain#custom-domain)

