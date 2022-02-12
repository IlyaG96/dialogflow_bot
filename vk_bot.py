from environs import Env


def main():
    env = Env()
    env.read_env()
    vk_token = env.str('VK_TOKEN')

if __name__ == '__main__':
    main()