
## fundamental of Machibe Learning
## Fundamental of Deep Learning
## Deep Learning framework
## Pytorch
## TensorFlow 
## How self attention works
## Transformer Architecture
## Types of Transformers
    * Encoder Only(BERT) - BERT Architecture
    * Decoder Only(GPT) - GPT Architecture
    * Encoder-Decoder(T5, BART) - T5 Architecture
## Fine Tuning
## Kafka

## LLM
- An LLM, or Large Language Model, is a machine-learning model trained on a large amount of text data to understand and generate human-like language. Modern LLMs are primarily based on the Transformer architecture.

- When a user sends a prompt, the text is first tokenized into tokens and converted into token IDs. These are processed by the Transformer, which uses mechanisms such as self-attention to understand the relationship between tokens. The model then predicts the next token repeatedly until it generates the complete response.

## transformer
- A Transformer is a neural-network architecture introduced for processing sequential data and is the foundation of modern LLMs.
- The input text is first tokenized and converted into token IDs, and those IDs are converted into embeddings. The Transformer then processes these representations using mechanisms such as self-attention.

## Self-Attention
- It allows the modal to understand the relationship between the tokens in the given text context. 
- Ex: in the sentance, It helps the model to determine that which earlier word are import to understand with the current word.
- It helps LLM to predict the next token more accurately.
- E.g., The cat sat on the mat because it was tired. The self-attention mechanism helps the model understand that 'it' refers to the 'cat' and not the 'mat'.

## Q(Query), K(Key), V(Value)
- **Query**: represents what information the current token is looking for.
- **Key**: represents the information each token can provide for matching.
- **Value**: represents the actual information that will be passed forward. The attention mechanism compares Queries with Keys to calculate relevance scores and then uses those scores to create a weighted combination of Values.

## How to build a LLM?
- Total 5 stages are there to build an LLM.
    * **Stage 1: Data — Where Every AI Model Begins**
        - Collect the huge of data data/inofrmation, these data can comes from different resocuces like, website, articles, books research papaers, etc.
            * Real lige example: Before sending our child to school we collect the books or study meterial.
        - Collecting the data/information is not enough, because it might inlcudes duplicates data, wrong information, harmful content, same paragraph multiple times, if we directly train a model on these raw data then model may learn unwanted patterns.
        - next concept is tokenization, model cannot understand text directly, so we need to convert text into tokens. Tokenization is the process of splitting the text into smaller units called tokens. These tokens can be words, subwords, or even characters.

    * **Stage 2: Pretraining — Where the Model Learns Everything It Can**
        - In this stage, model is trained on the huge amount of collected data, to understand the patterns, structure, grammar, facts, and relationships between words.
            - During pretraining, the model learns to predict the next token in a sequence given the previous tokens. This is done by feeding the model with a sequence of tokens and asking it to predict the next token. If the model's prediction is incorrect, the model adjusts its internal parameters to make better predictions in the future.

    * **Stage 3: Supervised Fine-Tuning — Teaching the Model to Become an Assistant**
        - During this stage, model will learn to behave as a assistant, model learns its job is to answer to question and help people.
    
    * **Stage 4: Reward Modeling — Teaching the AI What Humans Prefer**
        - Supoose model predict two answer for the one questions and for answers are correct but model doesn't know which answer will human prefer so during this stage model learns the human prefereances.

    * **Stage 5: Reinforcement Learning — Refining the Model Into a Reliable Assistant**
        - RLHF (Reinforcement Learning from Human Feedback).

 
 ## RAG Deep Dive

- Suppose I upload a 100-page PDF into your RAG system.

- **Explain exactly what happens during the ingestion process.**
    - **How do you extract text from the PDF?**
    - **How do you decide the chunk size?**
    - **What is chunk overlap and why do we need it?**
    - **How do you convert each chunk into an embedding?**
    - **What exactly do you store in the vector database?**


    ## Answer
    1. Extract text from the PDF: we can extract text from pdf by using some tools such as PyPDF2, PDFMiner, or modern OCR tools (Tesseract, PaddleOCR) depending on complexity. 
    2. Split the text into chunks: We can't send the 100 pages of the document into the model or LLM, because it has the limitation of context window size. so we will split the text into chunks
    3. Chunk size: It define how much text goes into one chunks
        ex: one chunk_size = 500 tokens, if the text is less than 500 tokens then it will go in one chunk else it will be split into multiple chunks
    4. Chunk Overlap: It define the similarity beteween two chunks. 

**Complete Flow:** "When a user uploads a PDF, I first extract the text using a PDF parser or document loader. Then I split the text into meaningful chunks with an appropriate chunk size and overlap to preserve context between chunks. Each chunk is converted into a numerical vector using an embedding model. We then store those embeddings in a vector database such as Pinecone along with metadata like document ID, page number, source, and sometimes the original chunk text. During retrieval, the user's query is embedded and used for similarity search to retrieve the most relevant chunks, which are then provided as context to the LLM to generate a grounded response."

**Complete ingestion flow**

          PDF
           ↓
    Text Extraction
           ↓
       Chunking
           ↓
  Add Metadata
           ↓
Embedding Model
           ↓
     Vector Embeddings
           ↓
       Pinecone

**Complete Retrieval flow**

    User Query
        ↓
    Query Embedding
        ↓
    Pinecone Search
        ↓
    Relevant Chunks
        ↓
    (Optional) Reranking
        ↓
    Top-K Context
        ↓
    Prompt + Context
        ↓
    LLM
        ↓
    Final Answer
        
    
            
