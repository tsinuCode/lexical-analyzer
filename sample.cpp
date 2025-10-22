// Sample C++ program for lexical analyzer testing
// This file demonstrates various token types

#include <iostream>
#include <vector>
#include <string>

using namespace std;

// Global constants
const int MAX_SIZE = 100;
const double PI = 3.14159;

// Function declaration
int calculateArea(int radius);
void printMessage(string msg);

int main() {
    // Variable declarations
    int x = 10;
    float y = 3.14;
    char ch = 'A';
    bool flag = true;
    
    /* Multi-line comment
       demonstrating comment removal */
       
    // Conditional statement
    if (x > 0 && y < 5.0) {
        cout << "Positive number" << endl;
        x = x + 1;
    } else if (x == 0) {
        cout << "Zero" << endl;
    } else {
        cout << "Negative number" << endl;
        x = x - 1;
    }
    
    // Loop construct
    for (int i = 0; i < 5; i++) {
        cout << "Iteration: " << i << endl;
    }
    
    // While loop
    while (x > 0) {
        x--;
    }
    
    // Switch statement
    switch (ch) {
        case 'A':
            cout << "Character A" << endl;
            break;
        case 'B':
            cout << "Character B" << endl;
            break;
        default:
            cout << "Other character" << endl;
    }
    
    // Function call
    int area = calculateArea(5);
    printMessage("Program completed");
    
    return 0;
}

// Function definition
int calculateArea(int radius) {
    return PI * radius * radius;
}

void printMessage(string msg) {
    cout << msg << endl;
}