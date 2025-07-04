import json
import os

WORKFLOW_PATH = os.path.join(os.path.dirname(__file__), '../data/troubleshooting_tree.json')

def load_tree():
    try:
        with open(WORKFLOW_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading tree: {e}")
        return {}

def save_tree(tree):
    try:
        with open(WORKFLOW_PATH, 'w', encoding='utf-8') as f:
            json.dump(tree, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving tree: {e}")
        return False

def add_node(node_id, prompt=None, response=None, edges=None, terminal=False):
    tree = load_tree()

    if node_id in tree:
        return f"Node '{node_id}' already exists."

    node_data = {}
    if terminal:
        node_data['response'] = response or "Response here."
        node_data['terminal'] = True
    else:
        node_data['prompt'] = prompt or "Prompt here."
        node_data['edges'] = edges or {}

    tree[node_id] = node_data
    success = save_tree(tree)
    return f"Node '{node_id}' added." if success else "Failed to save tree."

def edit_node(node_id, updates):
    tree = load_tree()
    node = tree.get(node_id)

    if not node:
        return f"Node '{node_id}' not found."

    node.update(updates)
    success = save_tree(tree)
    return f"Node '{node_id}' updated." if success else "Failed to save changes."

def delete_node(node_id):
    tree = load_tree()

    if node_id not in tree:
        return f"Node '{node_id}' not found."

    del tree[node_id]

    # Remove references from other nodes
    for nid, ndata in tree.items():
        if 'edges' in ndata:
            to_remove = [k for k, v in ndata['edges'].items() if v == node_id]
            for key in to_remove:
                del ndata['edges'][key]

    success = save_tree(tree)
    return f"Node '{node_id}' deleted." if success else "Failed to save changes."

def list_nodes():
    tree = load_tree()
    return list(tree.keys())