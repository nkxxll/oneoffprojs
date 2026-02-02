import re
import sys


def reformat_todo(content: str) -> str:
    lines = content.splitlines()
    result = []
    done_section = True  # after heading, first section is done items
    in_code_block = False
    
    for line in lines:
        # Track code block state
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            result.append(line)
            continue
        
        # Inside code block - preserve as-is
        if in_code_block:
            result.append(line)
            continue
        stripped = line.strip()
        
        # Date heading
        if re.match(r'^#\s+\w+\s+\d{1,2}\s+\w+\s+\d{4}', stripped):
            if result:
                result.append("")
            result.append(stripped)
            result.append("")
            done_section = True
            continue

        # old Date heading
        if re.match(r'^#\s+\w+\s+\w+\s+\d{1,2}\s+\d{4}', stripped):
            if result:
                result.append("")
            result.append(stripped)
            result.append("")
            done_section = True
            continue
        
        # Blank line = switch from done to todo section
        if not stripped:
            if result and result[-1] != "":
                result.append("")
                done_section = False
            continue
        
        # Bullet point (note under a todo) - keep as is
        if stripped.startswith("- "):
            # If it's already a checkbox, keep it
            if re.match(r'^- \[[x ]\]', stripped):
                result.append(stripped)
            else:
                # Sub-bullet, indent it
                result.append("  " + stripped)
        else:
            # Regular line -> convert to checkbox
            prefix = "- [x]" if done_section else "- [ ]"
            result.append(f"{prefix} {stripped}")
    
    return "\n".join(result) + "\n"


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <input_file> [output_file]")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else input_path
    
    with open(input_path, "r") as f:
        content = f.read()
    
    reformatted = reformat_todo(content)
    
    with open(output_path, "w") as f:
        f.write(reformatted)
    
    print(f"Reformatted {input_path} -> {output_path}")


if __name__ == "__main__":
    main()
