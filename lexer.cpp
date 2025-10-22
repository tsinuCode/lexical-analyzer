#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <regex>
#include <algorithm>

enum TokenType {
    KEYWORD,
    IDENTIFIER,
    NUMBER,
    OPERATOR,
    PUNCTUATION,
    UNKNOWN
};

struct Token {
    std::string value;
    TokenType type;
    int line;
    Token(std::string v, TokenType t, int l) : value(v), type(t), line(l) {}
};

class Lexer {
private:
    std::vector<std::string> keywords = {
        "alignas","alignof","and","and_eq","asm","atomic_cancel","atomic_commit","atomic_noexcept","auto",
        "bitand","bitor","bool","break","case","catch","char","char8_t","char16_t","char32_t","class","compl",
        "concept","const","consteval","constexpr","constinit","const_cast","continue","co_await","co_return",
        "co_yield","decltype","default","delete","do","double","dynamic_cast","else","enum","explicit","export",
        "extern","false","float","for","friend","goto","if","inline","int","long","mutable","namespace","new",
        "noexcept","not","not_eq","nullptr","operator","or","or_eq","private","protected","public","reflexpr",
        "register","reinterpret_cast","requires","return","short","signed","sizeof","static","static_assert",
        "static_cast","struct","switch","synchronized","template","this","thread_local","throw","true","try",
        "typedef","typeid","typename","union","unsigned","using","virtual","void","volatile","wchar_t","while",
        "xor","xor_eq"
    };

    std::vector<std::string> operators = {
        "+","-","*","/","%","=","==","!=","<",">","<=",">=","++","--","&&","||","!","&","|",
        "^","~","<<",">>","+=","-=","*=","/=","%=","&=","|=","^=","<<=",">>=","->",".","::"
    };

    std::vector<std::string> punctuations = {
        "(", ")", "{", "}", "[", "]", ";", ":", ",", ".", "?", "#"
    };

    std::string code;
    std::vector<Token> tokens;
    std::map<TokenType, int> tokenCount;

public:
    Lexer() {
        tokenCount[KEYWORD] = tokenCount[IDENTIFIER] = tokenCount[NUMBER] = 0;
        tokenCount[OPERATOR] = tokenCount[PUNCTUATION] = tokenCount[UNKNOWN] = 0;
    }

    void loadCode(const std::string& filename) {
        std::ifstream file(filename);
        if (!file.is_open()) {
            std::cerr << "Error: Could not open file " << filename << std::endl;
            return;
        }
        code.assign((std::istreambuf_iterator<char>(file)),
                     std::istreambuf_iterator<char>());
        file.close();
    }

    void loadCodeFromString(const std::string& input) {
        code = input;
    }

    void removeComments() {
        std::regex singleLine("//.*");
        code = std::regex_replace(code, singleLine, "");
        std::regex multiLine("/\\*[\\s\\S]*?\\*/");
        code = std::regex_replace(code, multiLine, "");
    }

    TokenType getTokenType(const std::string& token) {
        if (std::find(keywords.begin(), keywords.end(), token) != keywords.end())
            return KEYWORD;
        if (std::regex_match(token, std::regex("[0-9]+(\\.[0-9]+)?")))
            return NUMBER;
        if (std::regex_match(token, std::regex("[a-zA-Z_][a-zA-Z0-9_]*")))
            return IDENTIFIER;
        if (std::find(operators.begin(), operators.end(), token) != operators.end())
            return OPERATOR;
        if (std::find(punctuations.begin(), punctuations.end(), token) != punctuations.end())
            return PUNCTUATION;
        return UNKNOWN;
    }

    void tokenize() {
        tokens.clear();
        std::regex tokenRegex(
            "(auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|int|long|"
            "register|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while|"
            "alignas|alignof|and|and_eq|asm|atomic_cancel|atomic_commit|atomic_noexcept|bitand|bitor|bool|catch|"
            "char8_t|char16_t|char32_t|class|compl|concept|consteval|constexpr|constinit|const_cast|co_await|"
            "co_return|co_yield|decltype|delete|dynamic_cast|explicit|export|false|friend|inline|mutable|namespace|"
            "new|noexcept|not|not_eq|nullptr|operator|or|or_eq|private|protected|public|reflexpr|reinterpret_cast|"
            "requires|static_assert|static_cast|synchronized|template|this|thread_local|throw|true|try|typeid|"
            "typename|using|virtual|wchar_t|xor|xor_eq)|"
            "([a-zA-Z_][a-zA-Z0-9_]*)|([0-9]+(\\.[0-9]+)?)|"
            "(\\+\\+|--|==|!=|<=|>=|&&|\\|\\||<<|>>|\\+=|-=|\\*=|/=|%=|&=|\\|=|\\^=|<<=|>>=|->|::|\\+|-|\\*|/|%|=|!|<|>|&|\\||\\^|~|\\.)|"
            "([\\(\\)\\{\\}\\[\\];:,\\?#])|(\\s+)"
        );

        std::sregex_iterator iter(code.begin(), code.end(), tokenRegex);
        std::sregex_iterator end;
        int lineNum = 1;
        auto searchStart = code.cbegin();

        while (iter != end) {
            std::string match = (*iter).str();

            // ✅ fixed: access match boundaries correctly
            lineNum += std::count(searchStart, (*iter)[0].first, '\n');
            searchStart = (*iter)[0].first;

            if (std::regex_match(match, std::regex("\\s+"))) {
                ++iter;
                continue;
            }

            TokenType type = getTokenType(match);
            tokens.push_back(Token(match, type, lineNum));
            tokenCount[type]++;
            ++iter;
        }
    }

    void printTokens() {
        std::cout << "Tokens:\n========================================\n";
        std::cout << "Line | Token               | Type\n";
        std::cout << "-----|---------------------|------------\n";
        for (const auto& t : tokens) {
            std::string typeStr;
            switch (t.type) {
                case KEYWORD: typeStr = "KEYWORD"; break;
                case IDENTIFIER: typeStr = "IDENTIFIER"; break;
                case NUMBER: typeStr = "NUMBER"; break;
                case OPERATOR: typeStr = "OPERATOR"; break;
                case PUNCTUATION: typeStr = "PUNCTUATION"; break;
                default: typeStr = "UNKNOWN"; break;
            }
            printf("%4d | %-19s | %s\n", t.line, t.value.c_str(), typeStr.c_str());
        }
    }

    void saveToFile(const std::string& filename) {
        std::ofstream out(filename);
        if (!out.is_open()) {
            std::cerr << "Error: Could not create " << filename << std::endl;
            return;
        }
        out << "Developed for Compiler Design Course\n=====================================\n\n";
        out << "Line | Token               | Type\n";
        out << "-----|---------------------|------------\n";
        for (const auto& t : tokens) {
            std::string typeStr;
            switch (t.type) {
                case KEYWORD: typeStr = "KEYWORD"; break;
                case IDENTIFIER: typeStr = "IDENTIFIER"; break;
                case NUMBER: typeStr = "NUMBER"; break;
                case OPERATOR: typeStr = "OPERATOR"; break;
                case PUNCTUATION: typeStr = "PUNCTUATION"; break;
                default: typeStr = "UNKNOWN"; break;
            }
            out << t.line << " | " << t.value << " | " << typeStr << "\n";
        }
        out << "\nSummary:\n========================================\n";
        out << "Total Tokens: " << tokens.size() << "\n";
        out << "Keywords: " << tokenCount[KEYWORD] << "\n";
        out << "Identifiers: " << tokenCount[IDENTIFIER] << "\n";
        out << "Numbers: " << tokenCount[NUMBER] << "\n";
        out << "Operators: " << tokenCount[OPERATOR] << "\n";
        out << "Punctuations: " << tokenCount[PUNCTUATION] << "\n";
        out.close();
        std::cout << "Results saved to " << filename << std::endl;
    }

    void analyze() {
        removeComments();
        tokenize();
        printTokens();
        saveToFile("tokens.txt");
        std::cout << "\nSummary:\n========================================\n";
        std::cout << "Total Tokens: " << tokens.size() << "\n";
        std::cout << "Keywords: " << tokenCount[KEYWORD] << "\n";
        std::cout << "Identifiers: " << tokenCount[IDENTIFIER] << "\n";
        std::cout << "Numbers: " << tokenCount[NUMBER] << "\n";
        std::cout << "Operators: " << tokenCount[OPERATOR] << "\n";
        std::cout << "Punctuations: " << tokenCount[PUNCTUATION] << "\n";
    }
};

int main() {
    Lexer lexer;
    int choice;
    std::cout << "Interactive Lexical Analyzer\n============================\n";
    std::cout << "1. Analyze from file\n2. Enter code manually\nChoose an option (1 or 2): ";
    std::cin >> choice;
    std::cin.ignore();

    if (choice == 1) {
        std::string filename;
        std::cout << "Enter file name: ";
        std::getline(std::cin, filename);
        lexer.loadCode(filename);
    } else if (choice == 2) {
        std::string input, line;
        std::cout << "Enter C++ code (Ctrl+Z or Ctrl+D to end):\n";
        while (std::getline(std::cin, line)) input += line + "\n";
        lexer.loadCodeFromString(input);
    } else {
        std::cout << "Invalid choice!\n";
        return 1;
    }

    lexer.analyze();
    return 0;
}
