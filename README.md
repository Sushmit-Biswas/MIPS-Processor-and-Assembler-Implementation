# 🖥️ MIPS Processor Implementation

> A non-pipelined MIPS processor implementation in Python with example programs demonstrating core MIPS architecture concepts.

## 🌟 Overview

This project implements a MIPS processor simulator that executes common MIPS assembly instructions. It includes example programs demonstrating practical applications and core architectural concepts.

## 🎯 Featured Programs

### 1. Factorial Calculator
```mermaid
flowchart TD
    A[Start] --> B[Input n]
    B --> C[Initialize: 
    result = 1
    i = 1]
    C --> D{i <= n?}
    D -->|Yes| E[result = result * i]
    E --> F[i = i + 1]
    F --> D
    D -->|No| G[Store Result]
    G --> H[End]
```

- 🧮 Calculates factorial of a number
- 🔄 Iterative implementation
- 💾 Memory-efficient register usage
- 🔢 Handles positive integers up to n=10

### 2. Binary Search Implementation
```mermaid
flowchart TD
    A[Start] --> B[Initialize bounds]
    B --> C[Calculate mid]
    C --> D{Key Found?}
    D --> |Yes| E[Return index]
    D --> |No| F{Compare}
    F --> |Key < mid| G[Update upper bound]
    F --> |Key > mid| H[Update lower bound]
    G --> C
    H --> C
    D --> |Bounds crossed| I[Return -1]
```
- 🔍 Searches for a index-key in a sorted array
- 📊 Works with sorted arrays
- 🔍 Efficient searching algorithm
- 📝 Returns index or -1 if not found

## 🛠️ Technical Architecture

```mermaid
flowchart TD
    A[Instruction Memory] --> CU[Control Unit]
    CU --> |Control Signals| RF[Register File]
    CU --> |Control Signals| ALU[ALU]
    RF --> |Data| ALU
    ALU --> |Result| RF
    DM[Data Memory] <--> |Load/Store| RF
    PC[Program Counter] --> A
    CU --> |Next PC| PC
```

## ⚙️ Features

- ✨ Complete instruction cycle simulation (Fetch → Decode → Execute → Memory → Writeback)
- 🔧 Support for R-format, I-format, and J-format instructions
- 💾 Configurable memory and register file
- 🔍 Step-by-step execution monitoring
- 📊 Memory state visualization

## 🚀 Getting Started

1. **Setup Requirements**
   ```bash
   python 3.x
   ```

2. **Run the assembler**
   ```bash
   python assembler.py
   ```

3. **Run the Simulator**
   ```bash
   python Processor.py
   ```

4. **Test Assembly Programs**
   - Use MARS MIPS simulator for assembly code verification
   - Load `.asm` files and execute


## 🔬 Instruction Support

| Category | Instructions |
|----------|-------------|
| Arithmetic | `add`, `sub`, `addi`, `mul` |
| Logical | `and`, `or`, `ori` |
| Data Transfer | `lw`, `sw`, `lui` |
| Control Flow | `beq`, `bne`, `j` |
| Shift Ops | `sll`, `srl` |

## 📈 Performance Metrics

- Single-cycle execution
- Predictable instruction timing
- No pipeline hazards

## 👥 Contributing

Feel free to fork, enhance, and submit pull requests. Areas for improvement:
- Pipeline implementation
- More test programs
- Extended instruction support

## 📝 License

MIT License - feel free to use and modify for educational purposes.
