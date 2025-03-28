import sys
import os
import subprocess


def parse_brainfuck(filtered_code):
    stack = []
    for i, char in enumerate(filtered_code):
        if char == '[':
            stack.append(i)
        elif char == ']':
            if not stack:
                raise SyntaxError(f"Unmatched closing bracket at position {i}")
            stack.pop()
    if stack:
        raise SyntaxError(
            f"Unmatched opening bracket(s) at position(s): {stack}")
    return filtered_code


def brainfuck_scanner(file_path):
    valid_commands = {'>', '<', '+', '-', '.', ',', '[', ']'}
    output_lines = []
    filtered_code = []

    print(f"Attempting to read file: {file_path}")

    try:
        if not os.path.exists(file_path):
            print(f"Error: The file '{file_path}' does not exist.")
            return None

        with open(file_path, 'rb') as file:
            while True:
                byte = file.read(1)
                if not byte:
                    break

                char = byte.decode('utf-8', errors='ignore')

                if char in valid_commands:
                    output_lines.append(f'term: "{char}"')
                    filtered_code.append(char)
                elif char.strip() == '':
                    continue
                else:
                    output_lines.append(
                        f'<invalid_token>: error, invalid term "{char}"')

        try:
            parse_brainfuck(filtered_code)
            output_lines.append("Bracket validation: Success")
        except SyntaxError as e:
            output_lines.append(f"Bracket validation: {e}")
            filtered_code = None

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    try:
        with open('validation.txt', 'w') as output_file:
            for line in output_lines:
                output_file.write(line + '\n')
        print("Scanning and parsing results written to 'validation.txt'")
    except Exception as e:
        print(f"Error writing to 'validation.txt': {e}")

    return filtered_code


def generate_assembly(parsed_code, output_file):
    assembly = [
        "section .bss",
        "    tape resb 30000",
        "",
        "section .text",
        "    global _start",
        "",
        "_start:",
        "    mov rsi, tape",
    ]

    loop_counter = 0
    loop_stack = []

    for command in parsed_code:
        if command == "+":
            assembly.append("    inc byte [rsi]")
        elif command == "-":
            assembly.append("    dec byte [rsi]")
        elif command == ">":
            assembly.append("    inc rsi")
        elif command == "<":
            assembly.append("    dec rsi")
        elif command == ".":
            assembly.extend([
                "    mov rax, 1",
                "    mov rdi, 1",
                "    mov rdx, 1",
                "    syscall"
            ])
        elif command == ",":
            assembly.extend([
                "    mov rax, 0",
                "    mov rdi, 0",
                "    mov rdx, 1",
                "    syscall"
            ])
        elif command == "[":
            loop_start = f"loop_start_{loop_counter}"
            loop_end = f"loop_end_{loop_counter}"
            loop_stack.append((loop_start, loop_end))
            assembly.append(f"{loop_start}:")
            assembly.append("    cmp byte [rsi], 0")
            assembly.append(f"    je {loop_end}")
            loop_counter += 1
        elif command == "]":
            if not loop_stack:
                raise SyntaxError("Unmatched closing bracket ']'")
            loop_start, loop_end = loop_stack.pop()
            assembly.append(f"    jmp {loop_start}")
            assembly.append(f"{loop_end}:")

    assembly.extend([
        "    mov rax, 60",
        "    xor rdi, rdi",
        "    syscall"
    ])

    with open(output_file, "w") as f:
        f.write("\n".join(assembly))
    print(f"Assembly code generated in '{output_file}'")


def assemble_and_link(assembly_file, output_binary):
    try:
        # Assemble the .s file into an object file
        object_file = assembly_file.replace('.s', '.o')
        subprocess.run(['as', assembly_file, '-o', object_file], check=True)
        print(f"Object file '{object_file}' created successfully.")

        # Link the object file to create the final executable
        subprocess.run(['ld', object_file, '-o', output_binary], check=True)
        print(f"Executable binary '{output_binary}' created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during assembling or linking: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scanner.py input.bf")
    else:
        input_file = sys.argv[1]
        parsed_code = brainfuck_scanner(input_file)

        if parsed_code:
            assembly_file = "program.s"
            output_binary = "program"
            generate_assembly(parsed_code, assembly_file)
            assemble_and_link(assembly_file, output_binary)

