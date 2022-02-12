import random
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from config import vk_token, project_id, language_code
from dialogflow import detect_intent_texts


def echo(event, vk_api):

    user_message = event.text
    user_id = event.user_id
    answer = detect_intent_texts(project_id, user_id, user_message, language_code)

    vk_api.messages.send(
        user_id=event.user_id,
        message=answer,
        random_id=random.randint(1, 1000)
    )


def main():
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)


if __name__ == '__main__':
    main()