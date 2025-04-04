binary_file = "/Users/shanthu/Downloads/final_valuation_framework_mar30_2025_students_v5/automatedTesting/tests/bin/simple/simple_3.txt"
output_file = "/Users/shanthu/Downloads/trace_output-2.txt"


registers = {
    "00000": 0, "00001": 0, "00010": 380, "00011": 0, "00100": 0, "00101": 0,
    "00110": 0, "00111": 0, "01000": 0, "01001": 0, "01010": 0,
    "01011": 0, "01100": 0, "01101": 0, "01110": 0, "01111": 0,
    "10000": 0, "10001": 0, "10010": 0, "10011": 0, "10100": 0,
    "10101": 0, "10110": 0, "10111": 0, "11000": 0, "11001": 0,
    "11010": 0, "11011": 0, "11100": 0, "11101": 0, "11110": 0, "11111": 0
}

memory_allocation = {
    "0x00010000": 0, "0x00010004": 0, "0x00010008": 0, "0x0001000C": 0, "0x00010010": 0, "0x00010014": 0,
    "0x00010018": 0, "0x0001001C": 0, "0x00010020": 0, "0x00010024": 0, "0x00010028": 0, "0x0001002C": 0,
    "0x00010030": 0, "0x00010034": 0, "0x00010038": 0, "0x0001003C": 0, "0x00010040": 0, "0x00010044": 0,
    "0x00010048": 0, "0x0001004C": 0, "0x00010050": 0, "0x00010054": 0, "0x00010058": 0, "0x0001005C": 0,
    "0x00010060": 0, "0x00010064": 0, "0x00010068": 0, "0x0001006C": 0, "0x00010070": 0, "0x00010074": 0,
    "0x00010078": 0, "0x0001007C": 0
}
def load_binary(binary_file):
    with open(binary_file, "r") as f:
        return [line.strip() for line in f.readlines()]

def bin_to_dec(bin_str):
    return int(bin_str, 2)


def signext(bin_str, bit_length=32):
    x = int(bin_str, 2)
    if bin_str[0] == "1":
        x=x- (1 << bit_length)
    return x

def flip(code):
    return code & -2

def I_Type(line, PC):
    opcode = line[25:32]
    rd = line[20:25]
    rs1 = line[12:17]
    imm = signext(line[0:12], 12)
    funct3 = line[17:20]

    if funct3 == "000" and opcode == "0010011":  # ADDI
        registers[rd] = registers[rs1] + imm
    elif funct3 == "000" and opcode == "1100111":  # JALR
        j=PC+4
        PC = (registers[rs1] + imm) // (2 * 2)
        registers[rd]=j
        return (PC)
    elif funct3 == "010" and opcode == "0000011":  # LW
        i = registers[rs1] + imm
        registers[rd] = memory_allocation.get(hex(i), 0)
    return PC + 4

def R_Type(line):
    opcode = line[25:32]
    rd = line[20:25]
    rs1 = line[12:17]
    rs2 = line[7:12]
    funct7 = line[0:7]
    funct3 = line[17:20]
    
    if funct3 == "000" and funct7 == "0000000":
        registers[rd] = registers[rs1] + registers[rs2]
    elif funct3 == "000" and funct7 == "0100000":
        registers[rd] = registers[rs1] - registers[rs2]
    elif funct3 == "111" and funct7 == "0000000":
        registers[rd] = registers[rs1] & registers[rs2]
    elif funct3 == "110" and funct7 == "0000000":
        registers[rd] = registers[rs1] | registers[rs2]

def S_Type(line):
    opcode = line[25:32]
    imm1 = signext(line[20:25])
    imm2=signext(line[0:7])
    funct3 = line[17:20]
    rs1 = line[12:17]
    rs2 = line[7:12]
    imm = (imm2 << 5) | imm1
    if funct3 == "010":  # SW
        i = registers[rs1] + imm
        j= hex(i).upper()
        if j in memory_allocation:
            memory_allocation[j] = registers[rs2]


def B_Type(line,PC):
    opcode = line[25:32]
    imm = signext(line[0]+line[24]+line[1:7]+line[20:24]+"0",13)
    funct3 = line[17:20]
    rs1 = line[12:17]
    rs2 = line[7:12]

    if funct3=="000" and registers[rs1]==registers[rs2]:
        return PC+imm
    elif funct3=="001" and registers[rs1]!=registers[rs2]:
        return PC+imm
    return PC+4

def J_Type(line,PC):
    opcode = line[25:32]
    rd = line[20:25]
    imm1 = signext(line[0] + line[12:20] + line[11] + line[1:11] + "0", 21)
    registers[rd]=PC+4
    return PC+imm1

def Instructiontype(line, PC):
    opcode = line[25:32]
    if opcode == "0110011":
        R_Type(line)
        PC+=4
    elif opcode in ["0010011", "0000011", "1100111"]:
        PC = I_Type(line, PC)
    elif opcode == "0100011":
        S_Type(line)
        PC+=4
    elif opcode == "1100011":
        PC = B_Type(line, PC)
    elif opcode == "1101111":
        PC = J_Type(line, PC)
    return PC

def outputfile_binary(output_file, PC, registers):
    if PC == 0:
        with open(output_file, "w") as f:
            pass 
    else:
        with open(output_file, "a") as f:

            f.write(f"0b{PC:032b} ")
            f.write(" ".join(f"0b{registers[i]:032b}" for i in sorted(registers.keys())) + "\n")

def outputmemory_binary(output_file, memory_allocation):
    with open(output_file, "a") as f:
        for i, j in memory_allocation.items():
            f.write(f"{i}:0b{j:032b}\n")

if __name__ == "__main__":
    binaryfile = load_binary(binary_file)
    PC = 0
    open(output_file, "w").close()
    

    for line in binaryfile:
        PC = Instructiontype(line, PC)
        outputfile_binary(output_file, PC, registers)
    outputmemory_binary(output_file, memory_allocation)

