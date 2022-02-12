from google.cloud import dialogflow
import json
from config import project_id


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

    with open(file='training_phrases.json', mode='r') as file:
        training_phrases = json.load(file)

    for intent, intent_params in training_phrases.items():
        training_phrases_parts = intent_params['questions']
        message_texts = intent_params['answers']
        create_intent(project_id, intent, training_phrases_parts, message_texts)


if __name__ == '__main__':
    main()
