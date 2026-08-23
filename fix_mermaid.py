import re
import glob
import os

files = glob.glob("instructor/*.qmd") + glob.glob("student/*.qmd") + glob.glob("*.qmd")

def replace_in_mermaid(content):
    # Find ```{mermaid} ... ``` blocks
    def process_block(match):
        block = match.group(0)
        # replace \n with <br/> inside node strings
        lines = block.split('\n')
        new_lines = []
        for line in lines:
            if 'flowchart' in line or '```' in line or 'style' in line or 'subgraph' in line:
                new_lines.append(line)
            else:
                # Replace \n with <br/> inside quotes
                new_line = re.sub(r'\\n', '<br/>', line)
                new_lines.append(new_line)
        return '\n'.join(new_lines)

    return re.sub(r'```{mermaid}[\s\S]*?```', process_block, content)

for fpath in files:
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        new_content = replace_in_mermaid(content)
        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated: {fpath}")

print("Done processing mermaid line breaks!")
