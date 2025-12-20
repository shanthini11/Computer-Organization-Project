# Computer-Organization-Project
This repository consists of all our CO- project code for this semester project

Brief about the project:
Assembler: Converts RISC-V assembly instructions into 32-bit binary machine code while performing rigorous syntax and semantic validation
Simulator: Executes the generated binary instructions, emulating a RISC-V processor and producing detailed execution traces of registers and memory

Key Features:
- Supports core RV32I instruction formats: R, I, S, B, and J types
- Accurate instruction encoding based on RISC-V specifications
- Label resolution and PC-relative addressing for branches and jumps
- Comprehensive error detection (invalid instructions, registers, immediates, missing virtual halt, etc.)
- Cycle-by-cycle register trace generation during simulation
- Memory state dump after program termination
