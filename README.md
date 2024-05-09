# Beyond Relevance: Evaluate and Improve Retrievers on Perspective Awareness
This is the github repo for our ArXiv paper "Beyond Relevance: Evaluate and Improve Retrievers on Perspective Awareness" ([Link](https://arxiv.org/abs/2405.02714)).

In this paper, we  propose a novel retrieval benchmark, PIR, to study if and how current retrievers can handle nuanced perspective changes in user queries from real-world scenarios. For example, when asked to verify a claim, a retrieval system is expected to identify evidence from both supporting vs. contradicting perspectives, for the downstream system to make a fair judgment call.

Along with the dataset, we propose PAP as a simple and effective method to improve the perspective awareness of current retrievers with minimum change on the retrieval pipeline.

## Data Format
Check our dataset format in mini-datasets at **./demo_pir_dataset** for a demo version of all the tasks included in our experiments. Do send an email for the full-size datasets.

    tasks: a string indicating which task the retrieval data belongs to (perspectrum, agnews, story, ambigqa, allsides, exfever). 
    
        queries: the queries for the retrieval, with the perspectives

        source_queries: a list of the root queries of the queries, corresponding to the queries with the same index

        perspectives: a list of the perspectives of the queries, corresponding to the queries with the same index

        key_ref: a map from the query number (string) to the retrieval target index in the corpus

        query_labels: a list of labels showing the query characteristics, for evaluation purposes

        corpus: a list a the retrieval targets
        

## Experiments

We provide the code for the main experiments in **./demo.ipynb**. You can run the Jupyter Notebook to replicate our experiments with various retrievers and our projection-based methods.

## Others
If you have any other questions about this repo, you are welcome to open an issue or send me an [email](mailto:xinranz3@andrew.cmu.edu), I will respond to that as soon as possible.
