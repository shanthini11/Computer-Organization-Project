import sys
import re
from instructions import*


R_Type = {
    "add": {"opcode": "0110011", "funct3": "000", "funct7": "0000000"},
    "sub": {"opcode": "0110011", "funct3": "000", "funct7": "0100000"},
    "slt": {"opcode": "0110011", "funct3": "010", "funct7": "0000000"},
    "xor": {"opcode": "0110011", "funct3": "100", "funct7": "0000000"},
    "or":  {"opcode": "0110011", "funct3": "110", "funct7": "0000000"},
    "and": {"opcode": "0110011", "funct3": "111", "funct7": "0000000"},
}

I_Type = {
    "addi": {"opcode": "0010011", "funct3": "000"},
    "lw":   {"opcode": "0000011", "funct3": "010"},
    "jalr": {"opcode": "1100111", "funct3": "000"},
}

S_Type = {
    "sw": {"opcode": "0100011", "funct3": "010"},
}

B_Type = {
    "beq": {"opcode": "1100011", "funct3": "000"},
    "bne": {"opcode": "1100011", "funct3": "001"},
    "blt": {"opcode": "1100011", "funct3": "100"},
}

J_Type = {
    "jal": {"opcode": "1101111"},
}

Registers = {
    "zero": "00000", "ra": "00001", "sp": "00010", "gp": "00011", "tp": "00100",
    "t0": "00101", "t1": "00110", "t2": "00111", "s0": "01000", "s1": "01001",
    "a0": "01010", "a1": "01011", "a2": "01100", "a3": "01101", "a4": "01110", 
    "a5": "01111", "a6": "10000", "a7": "10001", "s2": "10010", "s3": "10011",
    "s4": "10100", "s5": "10101", "s6": "10110", "s7": "10111", "s8": "11000",
    "s9": "11001", "s10": "11010", "s11": "11011", "t3": "11100", "t4": "11101",
    "t5": "11110", "t6": "11111"
}

All_Instructions = (list(R_Type.keys()) + list(I_Type.keys()) + list(S_Type.keys()) + list(B_Type.keys()) + list(J_Type.keys()) + list(Registers.keys()))


inputfilepath="/Users/shanthu/Downloads/final_test_cases/simpleBin/Ex_test_7.txt"
outputfilepath="/Users/shanthu/Desktop/VSCODE/CO-assignment-IP/outputfile.txt"

if __name__ == "__main__":
    with open(inputfilepath, "r") as file:
        data = file.readlines()
    binary_output_list = []
    labels_pointer = {}
    stack_pointer = 0
    global_correct = True

    #a helper function which returns the two's complement of a binary. if positive, the width is adjusted later
    def twos_complement(bits,number):
       if number >= 0:
        return bin(number)
       else:
        x = bin(abs(number))
        x = "0"*(bits+2-len(x)) + x[2:]
        y = "1"*bits
        x = int(x, base=2)^int(y, base=2) 
        x += 0b1
        return bin(x)
       

      
    def check_registers(line: int, *reg: int) : 
        correct_f = True
        for j in reg:
            i = one_line_data[j]
        
            valid_register = False
            for valid_reg in Registers:
                if i == valid_reg:
                   valid_register = True
                   break
            if not valid_register:
                correct_f = False
                print("Error encountered at line " + str(line + 1) + ", given register " + str(i) + " does not match any known register.")

        if correct_f == False:
            global global_correct
            global_correct = False
            return True
    # in some cases, the opcode was printed first which was not in regards to the architecture, so this flips it.
    def hot_fix_1(*args):
        x = ''
        for i in args[::-1]:
            x += str(i)
        return ''.join(reversed(args))
    
    def check_syntax(*args):
        '''
        tries to see if the syntax of the instruction is correct, each register must be followed by (,
        ), or ,. 
        '''
        correct_f = True
        try:
            for i in range(2, len(args), 2):
                if args[i] != "," and args[i] != "(" and args[i] == ")":
                    correct_f *= True
                else:
                    correct_f *= False
        except:
            pass

        return correct_f


    
    #apparently labels should not be on their separate lines! have to throw an instruction on the same line! this assembler was not made like that, this loop is to fix that.
    corrections = 0
    for index, line in enumerate(data):
        if (":" in line):
            x_l = data[:index+corrections]
            x_r = data[index+1+corrections:]
            line = line.split(":")
            line[0] += ":"
            data = x_l + line + x_r
            corrections += 1

    #getting all labels and their corresponding pointers first
    stack_pointer = 0
    line_index = 0

    for one_line in data:
        one_line_data = list(filter(lambda x: x, re.split(",| |\(|\)|\t|\n", one_line)))
    
        if len(one_line_data) == 0:
           line_index += 1
           continue

    
        if one_line_data[0].endswith(":"):
            label = one_line_data[0].rstrip(':')
            labels_pointer[label] = stack_pointer
            line_index += 1
            continue 

    stack_pointer += 4
    line_index += 1


    stack_pointer = 0
    line_index = 0 
    for one_line in data:
        syntax = list(filter(lambda x: x, re.split(" |\t|\n", one_line)))
        one_line_data = list(filter(lambda x: x, re.split(",| |\(|\)|\t|\n", one_line)))
        binary_output = ''
    
        correct = True

    
        if len(one_line_data) == 0:
            line_index += 1
            continue

        if not check_syntax(" ".join(syntax)):
          print("Incorrect syntax found at line " + str(line_index + 1) + ", binary creation failed")
          global_correct = False
          line_index += 1
          continue


        if one_line_data[0][-1] == ":":
            line_index += 1
            continue

        temp_labels = list(map(lambda x: x + ":", list(labels_pointer.keys())))
        valid_instructions= set(All_Instructions + temp_labels)
        if one_line_data[0] in valid_instructions:
            correct = True
        else:
            correct = False

        global_correct = correct

        if not correct:
            print("Error encountered at line " + str(line_index + 1), end=", ")
            line_index += 1
            continue

        stack_pointer += 4
        line_index += 1


        # R_Type
        if one_line_data[0] in R_Type:
            if len(one_line_data) != 4:
                print("Syntax error encountered in line",line+1,"binary could not be created")
                global_correct = False
                continue
            if check_registers(line, 1, 2, 3):
                continue
            binary_output += hot_fix_1(R_Type[one_line_data[0]]["opcode"], Registers[one_line_data[1]], R_Type[one_line_data[0]]["funct3"], Registers[one_line_data[2]], Registers[one_line_data[3]], R_Type[one_line_data[0]]["funct7"])

        
        # I_Type
        
        elif one_line_data[0] in I_Type:
            if len(one_line_data) > (x:=4):
                print(f"Error encountered in line {line+1}, number of arguments exceed 4, binary could not be created")
                global_correct = False
                continue
            if one_line_data[0] == "lw":
                if check_registers(line, 1, 3):
                    continue
                if int(one_line_data[2]) > 2047 or int(one_line_data[2]) < -2048:
                    continue
                else:
                    x = twos_complement(12, int(one_line_data[2]))
                    one_line_data[2] = '0' * (14 - len(x)) + x[2:]
                    binary_output += hot_fix_1(I_Type[one_line_data[0]]["opcode"], Registers[one_line_data[1]], I_Type[one_line_data[0]]["funct3"], Registers[one_line_data[2]], one_line_data[3])
            else:
                if check_registers(line, 1, 2):
                    continue
                if int(one_line_data[3]) > 2047 or int(one_line_data[3]) < -2048:
                    continue
                else:
                    x = twos_complement(12, int(one_line_data[3]))
                    one_line_data[3] = '0' * (14 - len(x)) + x[2:]
                    binary_output += hot_fix_1(I_Type[one_line_data[0]]["opcode"], Registers[one_line_data[1]], I_Type[one_line_data[0]]["funct3"], Registers[one_line_data[2]], one_line_data[3])

        # S_Type  
        elif one_line_data[0] in S_Type:
            if len(one_line_data) > 4:
                print("Error encountered in line",line+1,"binary could not be created")
                global_correct = False
                continue
            if check_registers(line, 1, 3):
                continue
            if int(one_line_data[2]) > 2047 or int(one_line_data[2]) < -2048:
                continue
            else:
                x = twos_complement(12, int(one_line_data[2]))
                one_line_data[2] = '0' * (14 - len(x)) + x[2:][::-1]
            binary_output += one_line_data[2][11:4:-1] + Registers[one_line_data[1]] + Registers[one_line_data[3]] + S_Type["sw"]["funct3"] + one_line_data[2][4::-1] + S_Type["sw"]["opcode"]

        # B_Type
        elif one_line_data[0] in B_Type:
            if len(one_line_data) > 4:
                print("Error encountered in line",line+1,"binary could not be created")
                global_correct = False
                continue
            if check_registers(line, 1, 2):
                continue
        try:
            if int(one_line_data[3]) > 2047 or int(one_line_data[3]) < -2048:
                continue
        except ValueError:
            if one_line_data[3] in labels_pointer:
                x = twos_complement(13, labels_pointer[one_line_data[3]] - stack_pointer + 4)
                x = "0" * (15 - len(x)) + x[2:12]
            else:
                global_correct = False
                continue
        if isinstance(x, int):
            x = twos_complement(13, x)
            x = "0" * (15 - len(x)) + x[2:]
        one_line_data[3] = x[::-1]
        binary_output += one_line_data[3][11] + one_line_data[3][9:3:-1] + Registers[one_line_data[2]] + Registers[one_line_data[1]] + B_Type[one_line_data[0]]["funct3"] + one_line_data[3][3::-1] + one_line_data[3][10] + B_Type[one_line_data[0]]["opcode"]

        # J_Type
        if one_line_data[0] in J_Type:
            if len(one_line_data) > 3:
                print("Error encountered in line",line+1," number of arguments exceed 3, binary could not be created")
                global_correct = False
                continue
            if check_registers(line, 1):
                continue
            try:
                x = int(one_line_data[2])
                if x > 2*19 - 1 or x < -2*19:
                    continue
            except ValueError:
                if one_line_data[2] in labels_pointer.keys():
                    x = twos_complement(21, labels_pointer[one_line_data[2]] - stack_pointer + 4)
                else:
                    global_correct = False
                    continue
            if isinstance(x, int):
                x = twos_complement(21, x)
            one_line_data[2] = '0' * (23 - len(x)) + x[2:]
            one_line_data[2] = one_line_data[2][:20][::-1]
                
            binary_output += one_line_data[2][19] + one_line_data[2][9::-1] + one_line_data[2][10] + one_line_data[2][18:10:-1] + Registers[one_line_data[1]] + J_Type["jal"]["opcode"]
                
  
 
    if binary_output_list.count("00000000000000000000000001100011") == 0:
        print("Virtual halt not found, binary creation failed")
        global_correct = False
    
    
    if global_correct:
        print("No errors detected, binary created successfully.")
        with open(outputfilepath, "w") as output_file:
            for binary in binary_output_list:
                output_file.write(binary + "\n")
            else:
                print("Errors detected, binary creation failed.")
    output_file.close() 