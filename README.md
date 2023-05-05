## TGPubmedSearch
Simple Telegram bot that can search for articles in PubMed database based on user queries.

### Installation
Clone repository and run following command:

```bash
pip install -r requirements.txt
```

You will also need to obtain a Telegram API Token and PubMed API key and email. See [here](https://core.telegram.org/bots#creating-a-new-bot) for instructions on creating a Telegram bot, and [here](https://ncbiinsights.ncbi.nlm.nih.gov/2017/11/02/new-api-keys-for-the-e-utilities/) for instructions on obtaining a PubMed API key.

### Example usage
To start the bot, run the **main.py** script with the required arguments.
```bash
python main.py --telegram_api_token YOUR_TELEGRAM_API_TOKEN --pubmed_api_email YOUR_PUBMED_API_EMAIL --pubmed_api_key YOUR_PUBMED_API_KEY
```

Once the bot is running, you can interact with it in Telegram by searching for its name and starting a chat. The bot will respond to the following commands:

1. **/start**: Initializes the bot and provides instructions on how to use it.
2. **/pubmed_search**: Initiates a PubMed search. The bot will ask for the query to search for.

