# Beyond Relevance: Evaluate and Improve Retrievers on Perspective Awareness
This is the github repo for our COLM 2024 paper "Beyond Relevance: Evaluate and Improve Retrievers on Perspective Awareness" ([Link](https://openreview.net/forum?id=7VPKtz8CHN#discussion)).

In this paper, we  propose a novel retrieval benchmark, PIR, to study if and how current retrievers can handle nuanced perspective changes in user queries from real-world scenarios. For example, when asked to verify a claim, a retrieval system is expected to identify evidence from both supporting vs. contradicting perspectives, for the downstream system to make a fair judgment call.

Along with the dataset, we propose PAP as a simple and effective method to improve the perspective awareness of current retrievers with minimum change in the retrieval pipeline.

## Demo Data Format
Check our dataset format in mini-datasets at **./demo_pir_dataset** for a demo version of all the tasks included in our experiments. Do send an email for the full-size datasets.

    tasks: a string indicating which task the retrieval data belongs to (perspectrum, agnews, story, ambigqa, allsides, exfever). 
    
        queries: the queries for the retrieval, with the perspectives

        source_queries: a list of the root queries of the queries, corresponding to the queries with the same index

        perspectives: a list of the perspectives of the queries, corresponding to the queries with the same index

        key_ref: a map from the query number (string) to the retrieval target index in the corpus

        query_labels: a list of labels showing the query characteristics, for evaluation purposes

        corpus: a list of the retrieval targets
        

## Dataset
Check our updated dataset at Hugging Face with another round of manual filtering: https://huggingface.co/trumancai/ + perspective-information-retrieval-{dataset} 

dataset = story, perspectrum, exfever, ambigqa, agnews, allsides

You can check **./process_hugginface_version.py** to process and experiment with the hugginface version.

We sincerely acknowledge [Haoyang Wen](https://www.haoyangwen.com/) for further advice: (1) some questions in the AGNews dataset are hard for humans; (2) some corpus entries in the AmbigQA dataset are too short to provide full information. The authors will work on fixing these issues soon. Please contact the authors if there are any further suggestions.

## Experiments

We provide the code for the main experiments in **./demo.ipynb**. You can run the Jupyter Notebook to replicate our experiments with various retrievers and our projection-based methods.

## Others
If you have any other questions about this repo, you are welcome to open an issue or send me an [email](mailto:xinranz3@andrew.cmu.edu), I will respond to that as soon as possible.
