import sys
from chatbot.engine import ChatbotEngine


def main():
    print("\n==============================")
    print(" Welcome to Smart Troubleshooter")
    print("==============================")
    print("Type 'exit' to quit.\n")

    engine = ChatbotEngine()

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ['exit', 'quit']:
            print("\nBot: Goodbye! Stay safe.")
            break

        response = engine.respond(user_input)
        print(f"Bot: {response}\n")


if __name__ == "__main__":
    main()
