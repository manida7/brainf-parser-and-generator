# **🧠 Brainfuck Compiler Assignment: Parsing and Assembly Code Generation**

## **Overview**
In this assignment, you will extend your existing **Brainfuck scanner** to implement:
1. A **parser** that analyzes the structure of Brainfuck code and ensures it is correct.
2. A **code generator** that produces **x86_64 assembly code** from the parsed Brainfuck.
3. An end-to-end **compiler** that takes a Brainfuck source file, generates assembly, and compiles it into an **executable** using `as` and `ld`.

At the end, you will be able to run your compiled Brainfuck program **directly from the command line**.

---

## ✅ **Assignment Goals**
- **Write a Brainfuck parser** that:
  - **Matches loops** (`[` and `]`).
  - **Validates proper nesting and structure**.
  - **Organizes commands for translation**.
- **Write a code generator** that:
  - **Generates x86_64 assembly** (`.s` file) from the parsed Brainfuck.
  - Handles:
    - Memory operations (`+`, `-`, `>`, `<`).
    - I/O (`.`, `,`).
    - Loops (`[` and `]`).
- **Compile and link** the generated `.s` file into an executable using `as` and `ld`.
- **Run the compiled program** and test it.

---

## 📂 **Input & Output**

### **Input**:
- A Brainfuck source code file (e.g., `program.bf`).

### **Output**:
- An executable file (e.g., `program`), compiled from Brainfuck.

---

## ⚙️ **Steps to Complete the Assignment**

### **Step 1: Parsing Brainfuck**
- Write a **parser** that takes the **tokens produced by the scanner**.
- **Validate matching loops**:
  - Check that every `[` has a corresponding `]`.
  - Handle **nested loops**.
- Organize the program into a **sequence of instructions**.

> **Hint:** You can represent the program as a list of operations, where loops are recursively represented as sub-lists or loop nodes.

---

### **Step 2: Generating Assembly (Code Generator)**
- From the parsed representation, **generate x86_64 assembly** that:
  - Implements each Brainfuck command as assembly:
    | Brainfuck Command | Assembly Action                              |
    |-------------------|----------------------------------------------|
    | `+`               | Increment byte at pointer                    |
    | `-`               | Decrement byte at pointer                    |
    | `>`               | Move pointer right                           |
    | `<`               | Move pointer left                            |
    | `.`               | Output byte at pointer (syscall)              |
    | `,`               | Input byte to pointer (syscall)               |
    | `[` and `]`       | Loop start and end, using labels and jumps   |
- **Loops**:
  - Use **labels** to create jump points for `[` and `]`.
  - Ensure that loops are properly nested and labeled uniquely.

> **Hint:** You can create unique labels like `loop_start_1`, `loop_end_1`, `loop_start_2`, etc.

---

### **Step 3: Assembling & Linking**
- Assemble the generated `.s` file into an object file:
```bash
as program.s -o program.o
```
- Link the object file to create the final executable:
```bash
ld program.o -o program
```

### **Step 4: Running the Brainfuck Program**
- Run your compiled binary:
```bash
./program
```

---

## 🚨 **Important Requirements**
- **The compiler should be called via command-line**, accepting a **file path** to the Brainfuck source code:
```bash
./bf_compiler program.bf
```
- **Generated assembly file** should be saved as `program.s`.
- **Compiled binary** should be named `program`.
- You must **automate the assembly and linking** within your toolchain or compiler pipeline.
- Loops must be **validated and compiled correctly** — unmatched brackets should raise **errors during parsing**.

---

## 🔑 **Deliverables**
1. **Parser code**.
2. **Code generator (assembly generator) code**.
3. **Sample generated `.s` file**.
4. **Compiled executable (`program`)**.
5. **makefile** having the compilation command.

---

## 💡 **Hints and Tips**
- **Start small** — first generate assembly for `+` and `-`.
- Add pointer movement (`>` and `<`).
- Add I/O (`.` and `,`).
- Finally, add loop support (`[` and `]`).
- Test incrementally, writing **very simple Brainfuck programs** and checking if your assembly works.

---

## ✅ **Minimal Example to Compile and Run**
Given this Brainfuck file `program.bf`:
```brainfuck
++++[>++++<-]>.
```

Expected steps:
```bash
./bf_compiler program.bf    # Generate assembly and compile executable
./program                  # Run the compiled Brainfuck program
```

Expected output:
```
P  # ASCII character 80 (after incrementing byte 80 times)
```

## 🚀 **Final Note**
This assignment completes your **Brainfuck compiler**. After this, you'll have a tool that:
1. Scans Brainfuck.
2. Parses and validates it.
3. Generates real assembly.
4. Produces executable binaries you can run on your system.

### p.s. Don't forget — **we provide a cozy server to run your compiler and assembler if needed!** 😉

---
