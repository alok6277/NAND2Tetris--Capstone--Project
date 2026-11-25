import sys
import re

COMP = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "M": "1110000",
    "!D": "0001101", "!A": "0110001", "!M": "1110001",
    "-D": "0001111", "-A": "0110011", "-M": "1110011",
    "D+1": "0011111", "A+1": "0110111", "M+1": "1110111",
    "D-1": "0001110", "A-1": "0110010", "M-1": "1110010",
    "D+A": "0000010", "D+M": "1000010",
    "D-A": "0010011", "D-M": "1010011",
    "A-D": "0000111", "M-D": "1000111",
    "D&A": "0000000", "D&M": "1000000",
    "D|A": "0010101", "D|M": "1010101"
}

DEST = {
    "": "000", "M": "001", "D": "010",
    "MD": "011", "A": "100", "AM": "101",
    "AD": "110", "AMD": "111"
}

JUMP = {
    "": "000", "JGT": "001", "JEQ": "010",
    "JGE": "011", "JLT": "100", "JNE": "101",
    "JLE": "110", "JMP": "111"
}

SYMBOLS = {
    "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
    "SCREEN": 16384, "KBD": 24576
}

for i in range(16):
    SYMBOLS[f"R{i}"] = i


def clean_lines(filename):
    with open(filename, "r") as file:
        lines = file.readlines()

    result = []

    for line in lines:
        line = line.split("//")[0].strip()
        line = line.replace(" ", "").replace("\t", "")
        if line:
            result.append(line)

    return result


def first_pass(lines):
    instructions = []
    rom_address = 0

    for line in lines:
        if line.startswith("(") and line.endswith(")"):
            label = line[1:-1]
            SYMBOLS[label] = rom_address
        else:
            instructions.append(line)
            rom_address += 1

    return instructions


def assemble(input_file, output_file):
    lines = clean_lines(input_file)
    instructions = first_pass(lines)

    output = []
    variable_address = 16

    for line_number, line in enumerate(instructions, 1):

        if line.startswith("@"):
            symbol = line[1:]

            if symbol.isdigit():
                address = int(symbol)
            else:
                if symbol not in SYMBOLS:
                    SYMBOLS[symbol] = variable_address
                    variable_address += 1

                address = SYMBOLS[symbol]

            if address < 0 or address > 32767:
                raise ValueError(f"Invalid address: {address}")

            machine_code = format(address, "016b")

        else:
            if ";" in line:
                comp_dest, jump = line.split(";")
            else:
                comp_dest = line
                jump = ""

            if "=" in comp_dest:
                dest, comp = comp_dest.split("=")
            else:
                dest = ""
                comp = comp_dest

            if comp not in COMP:
                raise ValueError(f"Invalid comp: {comp}")

            if dest not in DEST:
                raise ValueError(f"Invalid dest: {dest}")

            if jump not in JUMP:
                raise ValueError(f"Invalid jump: {jump}")

            machine_code = (
                "111" + COMP[comp] + DEST[dest] + JUMP[jump]
            )

        output.append(machine_code)

    with open(output_file, "w") as file:
        file.write("\n".join(output) + "\n")

    print("Assembly successful!")
    print("Total instructions:", len(output))
    print("Output saved to:", output_file)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: py assembler.py input.asm output.hack")
        sys.exit(1)

    try:
        assemble(sys.argv[1], sys.argv[2])
    except (ValueError, KeyError) as error:
        print("Assembly Error:", error)
        sys.exit(1)
