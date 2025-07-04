from chatbot.workflow_manager import add_node, edit_node, delete_node, list_nodes


def main():
    print("\n=== Troubleshooting Workflow Admin ===")
    print("Options: add | edit | delete | list | exit")

    while True:
        command = input("\n> Command: ").strip().lower()

        if command == "add":
            node_id = input("Node ID: ").strip()
            terminal = input("Is this a terminal node? (yes/no): ").strip().lower() == 'yes'

            if terminal:
                response = input("Response message: ").strip()
                print(add_node(node_id=node_id, response=response, terminal=True))
            else:
                prompt = input("Prompt text: ").strip()
                edges = {}
                print("Enter edges (keyword:next_node), type 'done' to finish:")
                while True:
                    edge = input("edge > ").strip()
                    if edge == 'done':
                        break
                    try:
                        keyword, next_node = edge.split(":")
                        edges[keyword.strip()] = next_node.strip()
                    except:
                        print("Invalid format. Use keyword:next_node")
                print(add_node(node_id=node_id, prompt=prompt, edges=edges))

        elif command == "edit":
            node_id = input("Node ID to edit: ").strip()
            print("Fields: prompt | response | edges | terminal")
            field = input("Field to update: ").strip()
            value = input("New value: ").strip()

            if field == "edges":
                print("Enter edges (keyword:next_node), type 'done' to finish:")
                edges = {}
                while True:
                    edge = input("edge > ").strip()
                    if edge == 'done':
                        break
                    try:
                        keyword, next_node = edge.split(":")
                        edges[keyword.strip()] = next_node.strip()
                    except:
                        print("Invalid format. Use keyword:next_node")
                updates = {"edges": edges}
            elif field == "terminal":
                updates = {"terminal": value.lower() == "true"}
            else:
                updates = {field: value}

            print(edit_node(node_id=node_id, updates=updates))

        elif command == "delete":
            node_id = input("Node ID to delete: ").strip()
            print(delete_node(node_id))

        elif command == "list":
            nodes = list_nodes()
            print(f"\nNodes ({len(nodes)}):")
            for n in nodes:
                print("-", n)

        elif command == "exit":
            print("Exiting Admin Tool.")
            break

        else:
            print("Unknown command. Use: add | edit | delete | list | exit")


if __name__ == '__main__':
    main()
