import json
import os
from chatbot.nlp_utils import keyword_detect, simple_llm_fallback

class ChatbotEngine:
    def __init__(self, workflow_path=None):
        self.workflow_path = workflow_path or os.path.join(os.path.dirname(__file__), '../data/troubleshooting_tree.json')
        self.workflows = self.load_workflows()
        self.session = {
            'current_node': 'root',
            'context': {},
            'history': []
        }

    def load_workflows(self):
        try:
            with open(self.workflow_path, 'r', encoding='utf-8') as f:
                workflows = json.load(f)
            return workflows
        except Exception as e:
            print(f"Error loading workflows: {e}")
            return {}

    def reset_session(self):
        self.session = {
            'current_node': 'root',
            'context': {},
            'history': []
        }

    def respond(self, user_input):
        # Normalize input
        user_input = user_input.lower().strip()

        # Check for session reset commands
        if user_input in ['restart', 'reset']:
            self.reset_session()
            return "Session reset. How can I assist you now?"

        # Detect intent/keywords
        detected_intent = keyword_detect(user_input, self.workflows)

        if detected_intent:
            # If we detect a new intent and we are not in root, reset to root for new flow
            if self.session['current_node'] != 'root' and detected_intent != self.session.get('current_intent'):
                self.reset_session()
                self.session['current_intent'] = detected_intent
                self.session['current_node'] = detected_intent
                self.session['history'].append(f"Intent detected: {detected_intent}")
                return self.get_current_prompt()
            
            # Continue existing flow
            if self.session['current_node'] == 'root':
                self.session['current_intent'] = detected_intent
                self.session['current_node'] = detected_intent
                self.session['history'].append(f"Intent detected: {detected_intent}")
                return self.get_current_prompt()
        
        # If in a decision tree, traverse based on input
        if self.session['current_node'] and self.session['current_node'] != 'root':
            next_node = self.traverse_decision_tree(self.session['current_node'], user_input)
            if next_node:
                self.session['current_node'] = next_node
                self.session['history'].append(f"Moved to node: {next_node}")
                # Check if next node is terminal
                if self.is_terminal_node(next_node):
                    response = self.workflows[next_node].get('response', "Here's what I suggest.")
                    self.reset_session()
                    return response + "\n\nYou can type another issue or 'exit' to quit."
                else:
                    return self.get_current_prompt()
            else:
                # Unable to traverse, fallback response
                fallback = simple_llm_fallback(user_input)
                return fallback
        
        # No intent detected and not in flow
        fallback = simple_llm_fallback(user_input)
        return fallback

    def get_current_prompt(self):
        node = self.session['current_node']
        node_data = self.workflows.get(node, {})
        prompt = node_data.get('prompt', "Please provide more details.")
        return prompt

    def traverse_decision_tree(self, current_node, user_input):
        """
        Traverse the workflow decision tree based on user input.
        Matches keywords in user_input with edges defined in workflows.
        Returns the next node id or None if no match.
        """
        node_data = self.workflows.get(current_node, {})
        edges = node_data.get('edges', {})

        # Check user input keywords against edges
        for keyword, next_node in edges.items():
            if keyword in user_input:
                return next_node
        
        return None

    def is_terminal_node(self, node):
        node_data = self.workflows.get(node, {})
        return node_data.get('terminal', False)
