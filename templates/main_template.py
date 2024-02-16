import json
from azure.ai.assistant.management.assistant_client import AssistantClient
from azure.ai.assistant.management.ai_client_factory import AIClientType
from azure.ai.assistant.management.conversation_thread_client import ConversationThreadClient


assistant_name = "ASSISTANT_NAME"

# open assistant configuration file
try:
    with open(f"config/{assistant_name}_assistant_config.json", "r") as file:
        config_json = json.load(file)
    ai_client_type = AIClientType[config_json["ai_client_type"]]
except FileNotFoundError:
    print(f"Configuration file for {assistant_name} not found.")
    exit(1)
except KeyError:
    print(f"AI client type not found in the configuration file for {assistant_name}.")
    exit(1)

# retrieve the assistant client
assistant_client = AssistantClient.from_json(json.dumps(config_json))

# create a new conversation thread client
conversation_thread_client = ConversationThreadClient.get_instance(ai_client_type)

# create a new conversation thread
thread_name = conversation_thread_client.create_conversation_thread()

while True:
    # Accept user input
    user_message = input("user: ")
    if user_message.lower() == 'exit':  # Allow the user to exit the chat
        print("Exiting chat.")
        break

    # Create a message to the conversation thread
    conversation_thread_client.create_conversation_thread_message(user_message, thread_name)

    # Process the user messages
    assistant_client.process_messages(thread_name)

    # Retrieve the conversation
    conversation = conversation_thread_client.retrieve_conversation(thread_name)

    # Print the last assistant response from the conversation
    assistant_message = conversation.get_last_text_message(assistant_client.name)
    print(f"{assistant_message.sender}: {assistant_message.content}")

    # add new line for better readability
    print()