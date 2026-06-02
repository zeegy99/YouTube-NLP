# YouTube-NLP

Thesis:
We will scrape certain Finance/Macroeconomic YouTube channels to see if they have any price impact on stocks.


Pipeline:

Every day we will scrape to see if new videos have come out. We cache the most recent videos to prevent slow lookups, and transcribe the transcripts into csv files and store them in the cloud. 


ToDo:
1. Develop in-house NLP Model trained on Financial News to understand transcripts over pre-existing models.
2. Build RAG (Retrieval-Augmented Generation) model which assumes the transcripts to be the truth. Pulling from this RAG Model, we are able to predict future stock prices. We are able to backtest by filtering out information the model has seen by removing vector embeddings.
3. Turn this into an agent and give it a stock account to trade with.

