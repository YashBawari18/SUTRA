import re
import json

with open('../dashboard/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find the start of const DATA = {
start_idx = html.find('const DATA = {')
if start_idx != -1:
    start_idx += len('const DATA = ')
    
    # Simple brace counting to find the end of the JSON object
    brace_count = 0
    end_idx = -1
    in_string = False
    escape = False
    
    for i in range(start_idx, len(html)):
        c = html[i]
        if not escape and c == '"':
            in_string = not in_string
            
        if not in_string:
            if c == '{':
                brace_count += 1
            elif c == '}':
                brace_count -= 1
                if brace_count == 0:
                    end_idx = i + 1
                    break
        
        if c == '\\':
            escape = not escape
        else:
            escape = False
            
    if end_idx != -1:
        json_str = html[start_idx:end_idx]
        try:
            data = json.loads(json_str)
            with open('seed_data.json', 'w', encoding='utf-8') as out:
                json.dump(data, out, indent=2)
            print("Successfully extracted seed_data.json")
        except Exception as e:
            print("Failed to parse extracted string as JSON:", e)
    else:
        print("Failed to find end of DATA object")
else:
    print("Could not find 'const DATA = {'")
