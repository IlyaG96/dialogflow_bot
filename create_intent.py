from google.cloud import dialogflow
import json
import argparse
from environs import Env


def create_intent(project_id, display_name, training_phrases_parts, message_texts):

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={'parent': parent, 'intent': intent}
    )


def main():
    env = Env()
    env.read_env()
    project_id = env.str('PROJECT_ID')

    parser = argparse.ArgumentParser(
        description="Путь к файлу json")
    parser.add_argument("-p", "--json_path", required=True)
    args = parser.parse_args()

    with open(file=args.json_path, mode='r') as file:
        training_phrases = json.load(file)

    for intent, intent_params in training_phrases.items():
        training_phrases_parts = intent_params['questions']
        message_texts = intent_params['answers']
        create_intent(project_id, intent, training_phrases_parts, message_texts)


if __name__ == '__main__':
    main()
