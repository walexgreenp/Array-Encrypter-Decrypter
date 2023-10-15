import tkinter as tk

# Dictionary that maps assembly instruction to corresponding opcode.
instructions_to_opcodes = {
    "add": "0x00",
    "addi": "0x08",
    "addiu": "0x09",
    "addu": "0x00",
    "and": "0x00",
    "andi": "0x0C",
    "beq": "0x04",
    "blez": "0x06",
    "bne": "0x05",
    "bgtz": "0x07",
    "div": "0x00",
    "divu": "0x00",
    "jalr": "0x00",
    "jr": "0x00",
    "lb": "0x20",
    "lbu": "0x24",
    "lhu": "0x25",
    "lui": "0x0F",
    "lw": "0x23",
    "mfhi": "0x00",
    "mthi": "0x00",
    "mflo": "0x00",
    "mtlo": "0x00",
    "mult": "0x00",
    "multu": "0x00",
    "nor": "0x00",
    "xor": "0x00",
    "or": "0x00",
    "ori": "0x0D",
    "sb": "0x28",
    "sh": "0x29",
    "slt": "0x00",
    "slti": "0x0A",
    "sltiu": "0x0B",
    "sltu": "0x00",
    "sll": "0x00",
    "srl": "0x00",
    "sra": "0x00",
    "sub": "0x00",
    "subu": "0x00",
    "sw": "0x2B",
}

# Dictionary that maps register names/acronyms to their actual register value
reg_to_val = {
    "$zero": "0x00",
    "$at": "0x01",
    "$v0": "0x02",
    "$v1": "0x03",
    "$a0": "0x04",
    "$a1": "0x05",
    "$a2": "0x06",
    "$a3": "0x07",
    "$t0": "0x08",
    "$t1": "0x09",
    "$t2": "0x0A",
    "$t3": "0x0B",
    "$t4": "0x0C",
    "$t5": "0x0D",
    "$t6": "0x0E",
    "$t7": "0x0F",
    "$s0": "0x10",
    "$s1": "0x11",
    "$s2": "0x12",
    "$s3": "0x13",
    "$s4": "0x14",
    "$s5": "0x15",
    "$s6": "0x16",
    "$s7": "0x17",
    "$t8": "0x18",
    "$t9": "0x19",
    "$k0": "0x1A",
    "$k1": "0x1B",
    "$gp": "0x1C",
    "$sp": "0x1D",
    "$fp": "0x1E",
    "$ra": "0x1F"
}

# Dictionary that maps R type instructions to their funct field
inst_to_func = {
    "add": "0x20",
    "addu": "0x21",
    "and": "0x24",
    "div": "0x1A",
    "divu": "0x1B",
    "jalr": "0x09",
    "jr": "0x08",
    "mfhi": "0x10",
    "mthi": "0x11",
    "mflo": "0x12",
    "mtlo": "0x13",
    "mult": "0x18",
    "multu": "0x19",
    "nor": "0x27",
    "xor": "0x26",
    "or": "0x25",
    "slt": "0x2A",
    "sltu": "0x2B",
    "sll": "0x00",
    "srl": "0x02",
    "sra": "0x03",
    "sub": "0x22",
    "subu": "0x23"
}

# Unpack rs, rt, and rd for R type instructions
def unpack_r_instruction(instruction):
    # If instruction doesn't start with "$"
    if instruction[0] != "$":
        return -1
    
    # Instructino starts with "$"
    else:
        comma_index = instruction.find(",")

        # If no comma at end of string
        if comma_index == -1:
            if instruction[1].isdigit():
                register_hex = instruction[1:]
            elif instruction in reg_to_val:
                register_hex = reg_to_val[instruction]
            else:
                return -1
            
        # If comma at end of string
        else:
            # Register written directly
            if instruction[1].isdigit():
                register_hex = instruction[1:]
            # Register written with acronym
            elif instruction in reg_to_val:
                register_hex = reg_to_val[instruction[:comma_index]]
            else:
                return -1
                    
        # Remove the "0x" prefix
        if len(register_hex) >= 2 and register_hex[0:2] == "0x":
            register_hex = register_hex[2:]

            # Convert the hexadecimal string to an integer
            register_bin = int(register_hex, 16)

        # Convert the integer to a 6-bit binary string
        binary_string = format(register_bin, '05b')

        return binary_string


def convert_to_hex(instruction):
    final_instruction = ""
    components = instruction.split()
    # Opcode == "add"
    opcode = components[0]

    opcode = opcode.lower()  # Convert to lowercase for case-insensitive matching

    if opcode == "j" or opcode == "jal" or opcode == "jr":
        if len(components) != 2:
            return "Invalid instruction (jump instruction format: \"j [label]\")"
        
        return "Jump instruction. Will jump to " + components[1] + ". (Actual address is based on your machine.)"


    # Get opcode for instruction
    if opcode in instructions_to_opcodes:
        # Get opcode for instruction
        opcode_hex = instructions_to_opcodes[opcode]

        # Remove the "0x" prefix
        opcode_hex = opcode_hex[2:]

        # Convert the hexadecimal string to an integer
        opcode_bin = int(opcode_hex, 16)

        # Convert the integer to a 6-bit binary string
        binary_string = format(opcode_bin, '06b')

    else:
        return "Invalid instruction (unknown instruction)"
    
    # Handle R type instruction
    if binary_string == "000000":
        if(len(components) != 4):
            return "Invalid instruction (R type instruction must have 3 registers for parameters)"

        if opcode in inst_to_func:
            func_hex = inst_to_func[opcode]
        else:
            return "Invalid instruction (Instruction not recognized)"
        func_hex = func_hex[2:]
        func_bin = int(func_hex, 16)
        func_bin_string = format(func_bin, '06b')

        # unpack rs, rt, and rd values
        # Handle shamt field
        shamt_bin_string = "00000"
        if opcode == "sll" or opcode == "srl" or opcode == "sra":
            rt = "00000"
            shamt = components[3]
            shamt_bin = int(shamt, 10)
            shamt_bin_string = format(shamt_bin, '05b')

        else:
            rt = unpack_r_instruction(components[3])

        rs = unpack_r_instruction(components[2])
        rd = unpack_r_instruction(components[1])

        if rs == -1 or rt == -1 or rd == -1:
            return "Unknown instruction (Register doesn't exist or missing \"$\" before register value)"
        
        # Unpack shamt values
        final_instruction = binary_string + rs + rt + rd + shamt_bin_string + func_bin_string

        # Convert the binary string to an integer
        hex_instruction = int(final_instruction, 2)

        # Convert the integer to a hexadecimal string
        hex_string = "0x"+(hex(hex_instruction)[2:].zfill(8))

    else:
        if(len(components) != 4):
            return "Invalid instruction (I type instruction must have 2 registers followed by an immedeate for parameters)"
       
        # Instruction is an I type
        rs = unpack_r_instruction(components[1])
        rt = unpack_r_instruction(components[2])

        if(components[3][0:2] == "0x"):
            imm = int(components[3][2:], 16)
            if imm > 65536:
                return "Invalid immediate, value is too large"

        else:
            if(any(char.isalpha() for char in components[3])):
                return "Invalid immediate, no characters allowed only integers"
            imm = int(components[3])
            if imm > 65536:
                return "Invalid immediate, value is too large"

        imm_bin = format(imm, '16b')
        imm_bin = imm_bin.replace(' ', '0')  # Replace spaces with zeros
        
        final_instruction = binary_string + rs + rt + imm_bin

        hex_instruction = int(final_instruction, 2)
        hex_string = "0x"+(hex(hex_instruction)[2:].zfill(8))

    return [final_instruction, hex_string]

def assemble_instruction():
    instruction = entry.get()
    result = convert_to_hex(instruction)
    result_text.delete("1.0", tk.END)  # Clear previous content
    if isinstance(result, list):
        final_instruction, hex_string = result
        result_text.insert(tk.END, f"Binary: {final_instruction}\nHexadecimal: {hex_string}")
    else:
        result_text.insert(tk.END, result)


# Gui main loop
root = tk.Tk()
root.title("MIPS Instruction Assembler")

instruction_label = tk.Label(root, text="Enter a MIPS instruction:")
instruction_label.pack()

entry = tk.Entry(root)
entry.pack()

assemble_button = tk.Button(root, text="Assemble", command=assemble_instruction)
assemble_button.pack()

result_text = tk.Text(root, width=40, height=5)
result_text.pack()

root.mainloop()
