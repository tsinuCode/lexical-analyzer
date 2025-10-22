from flask import Flask, request, jsonify, send_from_directory
import subprocess
import os
import json
import re
from collections import defaultdict

app = Flask(__name__)

# Enable CORS for all routes
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# C++ keywords
KEYWORDS = {
    "alignas", "alignof", "and", "and_eq", "asm", "atomic_cancel", "atomic_commit", "atomic_noexcept",
    "auto", "bitand", "bitor", "bool", "break", "case", "catch", "char", "char8_t", "char16_t", "char32_t",
    "class", "compl", "concept", "const", "consteval", "constexpr", "constinit", "const_cast", "continue",
    "co_await", "co_return", "co_yield", "decltype", "default", "delete", "do", "double", "dynamic_cast", "else", "enum", "explicit", "export", "extern", "false", "float", "for", "friend", "goto", "if",
    "inline", "int", "long", "mutable", "namespace", "new", "noexcept", "not", "not_eq", "nullptr", "operator",
    "or", "or_eq", "private", "protected", "public", "reflexpr", "register", "reinterpret_cast", "requires",
    "return", "short", "signed", "sizeof", "static", "static_assert", "static_cast", "struct", "switch",
    "synchronized", "template", "this", "thread_local", "throw", "true", "try", "typedef", "typeid",
    "typename", "union", "unsigned", "using", "virtual", "void", "volatile", "wchar_t", "while", "xor", "xor_eq"
}

# C++ operators
OPERATORS = {
    "+", "-", "*", "/", "%", "=", "==", "!=", "<", ">", "<=", ">=", "++", "--", "&&", "||", "!", "&", "|",
    "^", "~", "<<", ">>", "+=", "-=", "*=", "/=", "%=", "&=", "|=", "^=", "<<=", ">>=", "->", ".", "::"
}

# C++ punctuations
PUNCTUATIONS = {
    "(", ")", "{", "}", "[", "]", ";", ":", ",", ".", "?", "#"
}

def remove_comments(code):
    """Remove single-line and multi-line comments from C++ code."""
    # Remove single line comments
    code = re.sub(r'//.*', '', code)
    
    # Remove multi-line comments
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    
    return code

def tokenize(code):
    """Tokenize C++ code into different categories."""
    # Remove comments first
    code = remove_comments(code)
    
    # Regex to match all tokens
    token_regex = (
        r'(auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|int|long|'
        r'register|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while|'
        r'alignas|alignof|and|and_eq|asm|atomic_cancel|atomic_commit|atomic_noexcept|bitand|bitor|bool|catch|'
        r'char8_t|char16_t|char32_t|class|compl|concept|consteval|constexpr|constinit|const_cast|co_await|'
        r'co_return|co_yield|decltype|delete|dynamic_cast|explicit|export|false|friend|inline|mutable|namespace|'
        r'new|noexcept|not|not_eq|nullptr|operator|or|or_eq|private|protected|public|reflexpr|reinterpret_cast|'
        r'requires|static_assert|static_cast|synchronized|template|this|thread_local|throw|true|try|typeid|'
        r'typename|using|virtual|wchar_t|xor|xor_eq)|'  # keywords
        r'([a-zA-Z_][a-zA-Z0-9_]*)|'  # identifiers
        r'([0-9]+(\.[0-9]+)?)|'      # numbers
        r'(\+\+|--|==|!=|<=|>=|&&|\|\||<<|>>|\+=|-=|\*=|/=|%=|&=|\|=|\^=|<<=|>>=|->|::|\+|-|\*|/|%|=|!|<|>|&|\||\^|~|\.)|'  # operators
        r'([\(\)\{\}\[\];:,\?#])|'  # punctuations
        r'(\s+)'  # whitespace
    )
    
    tokens = []
    token_count = defaultdict(int)
    
    # Split code into lines to track line numbers
    lines = code.split('\n')
    
    for line_num, line in enumerate(lines, 1):
        # Find all matches in this line
        for match in re.finditer(token_regex, line):
            token = match.group(0)
            
            # Skip whitespace
            if re.match(r'\s+', token):
                continue
                
            # Classify token
            if token in KEYWORDS:
                token_type = "KEYWORD"
            elif token in OPERATORS:
                token_type = "OPERATOR"
            elif token in PUNCTUATIONS:
                token_type = "PUNCTUATION"
            elif re.match(r'[0-9]+(\.[0-9]+)?', token):
                token_type = "NUMBER"
            elif re.match(r'[a-zA-Z_][a-zA-Z0-9_]*', token):
                token_type = "IDENTIFIER"
            else:
                token_type = "UNKNOWN"
                
            tokens.append({
                'value': token,
                'type': token_type,
                'line': line_num
            })
            
            token_count[token_type] += 1
    
    return tokens, token_count

def format_tokens_output(tokens, token_count):
    """Format tokens and summary into a string similar to the C++ version."""
    output = "Developed for Compiler Design Course\n"
    output += "=====================================\n\n"
    
    output += "Tokens:\n"
    output += "========================================\n"
    output += "Line | Token               | Type\n"
    output += "-----|---------------------|------------\n"
    
    for token in tokens:
        output += f"{token['line']:4d} | {token['value']:<19} | {token['type']}\n"
    
    output += "\nSummary:\n"
    output += "========================================\n"
    total = sum(token_count.values())
    output += f"Total Tokens: {total}\n"
    for token_type, count in token_count.items():
        output += f"{token_type}s: {count}\n"
    
    return output

def try_compile_and_run_lexer():
    """Try to compile and run the C++ lexer, return None if not possible."""
    try:
        # Check if lexer.exe already exists
        if os.path.exists('lexer.exe'):
            return True
            
        # Try to compile with different compilers
        compilers = [
            ['g++', 'lexer.cpp', '-o', 'lexer.exe'],
            ['cl', '/EHsc', 'lexer.cpp'],
        ]
        
        for compiler_cmd in compilers:
            try:
                result = subprocess.run(compiler_cmd, capture_output=True, text=True, timeout=30)
                if result.returncode == 0 and os.path.exists('lexer.exe'):
                    return True
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue
                
        return False
    except Exception:
        return False

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Get the C++ code from the request
        cpp_code = request.form['code']
        
        # Save the code to input.cpp
        with open('input.cpp', 'w') as f:
            f.write(cpp_code)
        
        # Try to use the C++ lexer first
        use_cpp_lexer = try_compile_and_run_lexer()
        
        if use_cpp_lexer and os.path.exists('lexer.exe'):
            try:
                # Run the lexer
                result = subprocess.run(['lexer.exe'], 
                                      input='1\ninput.cpp\n', 
                                      capture_output=True, 
                                      text=True,
                                      timeout=30)
                
                # Read the tokens.txt file
                if os.path.exists('tokens.txt'):
                    with open('tokens.txt', 'r') as f:
                        tokens_data = f.read()
                else:
                    tokens_data = "No tokens file generated"
                
                return jsonify({
                    'success': True,
                    'output': tokens_data,
                    'raw_output': result.stdout,
                    'raw_error': result.stderr,
                    'method': 'cpp'
                })
            except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
                # Fall back to Python implementation
                pass
        
        # Fall back to Python implementation
        tokens, token_count = tokenize(cpp_code)
        tokens_data = format_tokens_output(tokens, token_count)
        
        # Save to tokens.txt
        with open('tokens.txt', 'w') as f:
            f.write(tokens_data)
        
        return jsonify({
            'success': True,
            'output': tokens_data,
            'method': 'python'
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/analyze_json', methods=['POST'])
def analyze_json():
    try:
        # Get the C++ code from the request
        cpp_code = request.form['code']
        
        # Save the code to input.cpp
        with open('input.cpp', 'w') as f:
            f.write(cpp_code)
        
        # Try to use the C++ lexer first
        use_cpp_lexer = try_compile_and_run_lexer()
        
        if use_cpp_lexer and os.path.exists('lexer.exe'):
            try:
                # Run the lexer
                result = subprocess.run(['lexer.exe'], 
                                      input='1\ninput.cpp\n', 
                                      capture_output=True, 
                                      text=True,
                                      timeout=30)
                
                # Parse tokens.txt to extract structured data
                tokens = []
                summary = {}
                
                if os.path.exists('tokens.txt'):
                    with open('tokens.txt', 'r') as f:
                        lines = f.readlines()
                        
                    # Parse tokens section
                    in_tokens_section = False
                    in_summary_section = False
                    
                    for line in lines:
                        # Check for section headers
                        if line.startswith('Line | Token'):
                            in_tokens_section = True
                            in_summary_section = False
                            continue
                        elif line.startswith('Summary:'):
                            in_tokens_section = False
                            in_summary_section = True
                            continue
                        # Skip separator lines
                        elif line.startswith('-----'):
                            continue
                        # Skip empty lines
                        elif line.strip() == '':
                            continue
                            
                        if in_tokens_section and '|' in line:
                            parts = line.split('|')
                            if len(parts) >= 3:
                                try:
                                    line_num = int(parts[0].strip())
                                    token_value = parts[1].strip()
                                    token_type = parts[2].strip()
                                    tokens.append({
                                        'line': line_num,
                                        'value': token_value,
                                        'type': token_type
                                    })
                                except ValueError:
                                    continue
                                    
                        if in_summary_section and ':' in line:
                            parts = line.split(':')
                            if len(parts) == 2:
                                key = parts[0].strip()
                                # Map C++ output keys to what the HTML expects
                                key_mapping = {
                                    'Total Tokens': 'Total Tokens',
                                    'Keywords': 'Keywords',
                                    'Identifiers': 'Identifiers',
                                    'Numbers': 'Numbers',
                                    'Operators': 'Operators',
                                    'Punctuations': 'Punctuations'
                                }
                                mapped_key = key_mapping.get(key, key)
                                try:
                                    value = int(parts[1].strip())
                                    summary[mapped_key] = value
                                except ValueError:
                                    summary[mapped_key] = parts[1].strip()
                
                return jsonify({
                    'success': True,
                    'tokens': tokens,
                    'summary': summary,
                    'method': 'cpp'
                })
            except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
                # Fall back to Python implementation
                pass
        
        # Fall back to Python implementation
        tokens, token_count = tokenize(cpp_code)
        summary = {f"{token_type}s": count for token_type, count in token_count.items()}
        summary["Total Tokens"] = sum(token_count.values())
        
        return jsonify({
            'success': True,
            'tokens': tokens,
            'summary': summary,
            'method': 'python'
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)