from src import *
from dotenv import load_dotenv

def main() -> None:
    load_dotenv()
    API_KEY = os.getenv('API_KEY')

    Bot(intents=discord.Intents.all()).run(API_KEY)

if __name__ == '__main__':
    main()

