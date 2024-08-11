
import os
import ast
import json
import base64

#########################
# EDIT THESE PARAMETERS #
script_path = 'neurohackademy.py'

# Optional:
top_down = True # True for plotting the flowchart vertically, False for horizontally left to right
export_as_md=True # True to export the flowchart to a markdown file
output_path= None # Optionally can specify a path for the output file
add_to_readme=True  
########################

# Function to parse a Python script and extract functions, their inputs, and outputs
def extract_functions(script_path):
    with open(script_path, 'r') as f:
        tree = ast.parse(f.read())

    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            inputs = [arg.arg for arg in node.args.args]
            outputs = []
            for body_item in node.body:
                if isinstance(body_item, ast.Return):
                    if isinstance(body_item.value, ast.Tuple):
                        outputs = [elt.id for elt in body_item.value.elts if isinstance(elt, ast.Name)]
                    elif isinstance(body_item.value, ast.Name):
                        outputs.append(body_item.value.id)
            functions.append({
                'name': node.name,
                'inputs': inputs,
                'outputs': outputs
            })
    return functions

# Function to initialize a Mermaid diagram with a custom theme and legend
def initialize_mermaid_diagram(top_down):
    if top_down:
        initialize = [
            " %%{init: {'theme':'base', 'themeVariables': {",
            "  'primaryColor': '#ffcaca',",
            "  'primaryTextColor': '#000',",
            "  'primaryBorderColor': '#000000',",
            "  'lineColor': '#000000',",
            "  'tertiaryColor': '#fff'",
            "}}}%%",
            "graph TD",
            "classDef lightRed fill:#ffcaca,stroke:#333,stroke-width:2px;",
            "classDef lightGreen fill:#ebfcda,stroke:#333,stroke-width:2px;",
            "classDef lightBlue fill:#cefbfb,stroke:#333,stroke-width:2px;",
            "classDef lightPurple fill:#f8aaf8,stroke:#333,stroke-width:2px;",            
            "",
            "subgraph Legend",
            "    direction TB",
            "    key1[<b>Input]:::lightRed",
            "    key2[<b>Function]:::lightGreen",
            "    key3[<b>Output]:::lightBlue",
            "    key4[<b>Intermediate</b><br> Both an input and output]:::lightPurple",
            "end"
        ]
    else:
        initialize = [
            " %%{init: {'theme':'base', 'themeVariables': {",
            "  'primaryColor': '#ffcaca',",
            "  'primaryTextColor': '#000',",
            "  'primaryBorderColor': '#000000',",
            "  'lineColor': '#000000',",
            "  'tertiaryColor': '#fff'",
            "}}}%%",
            "graph LR",
            "classDef lightRed fill:#ffcaca,stroke:#333,stroke-width:2px;",
            "classDef lightGreen fill:#ebfcda,stroke:#333,stroke-width:2px;",
            "classDef lightBlue fill:#cefbfb,stroke:#333,stroke-width:2px;",
            "classDef lightPurple fill:#f8aaf8,stroke:#333,stroke-width:2px;",            
            "",
            "subgraph Legend",
            "    direction TB",
            "    key1[<b>Input]:::lightRed",
            "    key2[<b>Function]:::lightGreen",
            "    key3[<b>Output]:::lightBlue",
            "    key4[<b>Intermediate</b><br> Both an input and output]:::lightPurple",
            "end"
        ]
    return initialize

def add_function_to_diagram(func, node_connections, mermaid_diagram, icon=True):
    func_input = func.get('inputs', [])
    func_output = func.get('outputs', [])

    # Add function node if not already added
    if func['name'] not in node_connections:
        mermaid_diagram.append(f"{func['name']}((\"{func['name']}\")):::lightGreen")
        if icon:
            mermaid_diagram.append(f"{func['name']}((\"{func['name']}\n fa:fa-code\"))")
        node_connections[func['name']] = {'inputs': 0, 'outputs': 0}

    # Handle inputs
    if func_input:  # Only process if inputs exist
        for input_item in func_input:
            if input_item not in node_connections:
                mermaid_diagram.append(f"{input_item}:::lightRed")
                node_connections[input_item] = {'inputs': 0, 'outputs': 0}
            node_connections[input_item]['inputs'] += 1
            mermaid_diagram.append(f"{input_item} --> {func['name']}")
    
    # Handle outputs
    if func_output:  # Only process if outputs exist
        for output_item in func_output:
            if output_item not in node_connections:
                mermaid_diagram.append(f"{output_item}:::lightBlue")
                node_connections[output_item] = {'inputs': 0, 'outputs': 0}
            node_connections[output_item]['outputs'] += 1
            mermaid_diagram.append(f"{func['name']} --> {output_item}")
  



# Function to display the Mermaid graph
# def display_mermaid_graph(graph):
#     graph_bytes = graph.encode("utf8")
#     base64_bytes = base64.b64encode(graph_bytes)
#     base64_string = base64_bytes.decode("ascii")
#     mermaid_url = "https://mermaid.ink/img/" + base64_string
#     display(Image(url=mermaid_url))

# Function to create and optionally save the visualization
def script_to_viz(script_path, top_down, export_as_md, output_path, add_to_readme):
    functions = extract_functions(script_path)
    mermaid_diagram = initialize_mermaid_diagram(top_down)
    node_connections = {}

    for func in functions:
        add_function_to_diagram(func, node_connections, mermaid_diagram)

    for node, connections in node_connections.items():
        if connections['inputs'] > 0 and connections['outputs'] > 0:
            mermaid_diagram.append(f"{node}:::lightPurple")
        elif connections['inputs'] > 0:
            mermaid_diagram.append(f"{node}:::lightRed")
        elif connections['outputs'] > 0:
            mermaid_diagram.append(f"{node}:::lightBlue")

    mermaid_diagram_str = "\n".join(mermaid_diagram)

    with open('flowchart.mmd', 'w') as f:
        f.write(mermaid_diagram_str)

    print("Mermaid diagram saved to 'flowchart.mmd'")

    if output_path is None:
        output_path = './'

    if export_as_md:
        try:
            with open(f'{output_path}flowchart.md', 'w') as f:
                f.write("```mermaid\n")
                f.write(mermaid_diagram_str)
                f.write("\n```")
            print(f"Mermaid diagram saved to '{output_path}flowchart.md'")
        except Exception as e:
            print(f"Error saving Mermaid diagram as .md file: {e}")

    if add_to_readme:
        try:
            with open('README.md', 'r') as f:
                readme_lines = f.readlines()

            mermaid_exists = any("```mermaid" in line for line in readme_lines)

            if mermaid_exists:
                start_index, end_index = None, None
                for i, line in enumerate(readme_lines):
                    if line.strip() == "```mermaid":
                        start_index = i
                    elif start_index is not None and line.strip() == "```":
                        end_index = i
                        break

                if start_index is not None and end_index is not None:
                    readme_lines = readme_lines[:start_index] + ["```mermaid\n"] + [mermaid_diagram_str + "\n"] + ["```\n"] + readme_lines[end_index+1:]

                with open('README.md', 'w') as f:
                    f.writelines(readme_lines)
            else:
                with open('README.md', 'a') as f:
                    f.write("\n```mermaid\n")
                    f.write(mermaid_diagram_str + "\n")
                    f.write("```\n")
        except Exception as e:
            print(f"Error updating README.md: {e}")

script_to_viz(script_path, top_down, export_as_md, output_path, add_to_readme)
