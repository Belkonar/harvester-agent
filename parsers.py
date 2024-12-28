from typing import Dict, List
import json

def fs_add(fields: Dict[str,List[str]], name: str, kind: str):
    if fields.__contains__(name):
        fields[name].append(kind)
    else:
        fields[name] = [kind]

def dive(prefix: str, element, fields: Dict[str,List[str]] = {}) -> Dict[str,List[str]]:
    # Handle dictionaries (objects in JSON)
    if isinstance(element, dict):
        fs_add(fields, f"{prefix}", "object")
         
        for prop_name, prop_value in element.items():
            dive(f"{prefix}.{prop_name}", prop_value, fields)
    
    # Handle lists (arrays in JSON)
    elif isinstance(element, list):
        fs_add(fields, f"{prefix}", "array")
        
        for elem in element:
            dive(f"{prefix}[]", elem, fields)
    
    # Handle booleans
    elif isinstance(element, bool):
        fs_add(fields, prefix, "boolean")
    
    # Handle other types
    else:
        # Get the type name for other values
        value_kind = type(element).__name__
        fs_add(fields, prefix, value_kind.lower())

    return fields


def scan(data) -> Dict[str,List[str]]:
    if isinstance(data, str):
        data = json.loads(data)
    return dive("", data)

