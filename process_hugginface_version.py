import json
from collections import defaultdict,Counter

import pandas as pd
import numpy as np
from tqdm.notebook import trange, tqdm
from scipy.spatial.distance import cosine

from datasets import load_dataset

task = "allsides" # options = ["ambigqa","story","agnews","allsides","perspectrum","exfever"]

qrels_df = pd.read_json("hf://datasets/trumancai/perspective-information-retrieval-"+task+"/qrels/test.jsonl", lines=True)
queries_df = pd.read_json("hf://datasets/trumancai/perspective-information-retrieval-"+task+"/queries.jsonl", lines=True)
corpus_df = pd.read_json("hf://datasets/trumancai/perspective-information-retrieval-"+task+"/corpus.jsonl", lines=True)

qrels = qrels_df.to_dict('records')
queries = queries_df.to_dict('records')
corpus = corpus_df.to_dict('records')

qid2ind,cid2ind = {},{}
for i, q in enumerate(queries):
  qid2ind[q["_id"]] = str(i)

for i, c in enumerate(corpus):
  cid2ind[c["_id"]] = str(i)

# convert the hugginface dataset back to the original format
datasets={}
datasets[task] = {"queries":[],"source_queries":[],"perspectives":[],"corpus":[],"key_ref":{},"query_labels":[]}

for q in queries:
  datasets[task]["queries"].append(q["text"])
  meta = json.loads(q["meta"])
  datasets[task]["source_queries"].append(meta["src_query"])
  datasets[task]["perspectives"].append(meta["perspective"])

  temp_ref = {"none":"none"}
  q_label = "none"
  if task == "ambigqa":
    q_label = "perspective"
    temp_ref = {"perspective":"perspective"}

  if task == "story":
    q_label = "analogy"
    temp_ref = {"entities":"entity", "analogy":"analogy"}

  if task == "agnews":
    q_label = "subtopic"
    temp_ref = {"relates to":"subtopic", "happened in":"location"}

  if task == "allsides":
    q_label = "left"
    temp_ref = {"left":"left", "right":"right", "center":"center"}

  if task == "perspectrum":
    q_label = "support"
    temp_ref = {"support":"support", "oppose":"undermine", "relates to":"general"}

  if task == "exfever":
    q_label = "NOT ENOUGH INFO"
    temp_ref = {"supports":"SUPPORT", "refutes":"REFUTE", "no information":"NOT ENOUGH INFO"}

  for k in temp_ref.keys():
    if k in meta["perspective"]:
      q_label = temp_ref[k]

  datasets[task]["query_labels"].append(q_label)

for c in corpus:
  datasets[task]["corpus"].append(c["text"])


datasets[task]["key_ref"] =  defaultdict(list)

for rel in qrels:
  if rel["score"]== 1:
    datasets[task]["key_ref"][qid2ind[rel["query-id"]]].append(cid2ind[rel["corpus-id"]])


print("original dataset...")

for k,v in datasets.items():
    print(k)
    q_len = [len(x.split()) for x in v["queries"]]
    c_len = [len(x.split()) for x in v["corpus"]]

    print("Query size and length",len(v["queries"]),sum(q_len)/len(q_len))
    print("Corpus size and length",len(v["corpus"]),sum(c_len)/len(c_len))


def evaluation(key_ref, corpus_scores, query_labels, dataset_name):
    # evaluation of a dataset    
    recall_threshold = [1,5,10]
    recall_results = [0 for thresh in recall_threshold]
    
    if "source" in dataset_name:
        parts = ["none"]
    else:
        if dataset_name == "perspectrum":
            parts = ["support","undermine","general"]
        elif dataset_name == "agnews":
            parts = ["subtopic", "location"]
        elif dataset_name == "story":
            parts = ["analogy", "entity"]
        elif dataset_name == "ambigqa":
            parts = ["perspective"]
        elif dataset_name == "allsides":
            parts = ["left","right","center"]
        elif dataset_name == "exfever":
            parts = ["SUPPORT","REFUTE","NOT ENOUGH INFO"]
    
    parts_size = [0 for x in parts]
        
    for lb in query_labels:
        parts_size[parts.index(lb)] += 1
            
    partial_recall_results = []
    for i in range(len(parts)):
        partial_recall_results.append([0 for thresh in recall_threshold])

    
    for k,v in key_ref.items():
        for j, thresh in enumerate(recall_threshold):
            # important: find one is ok, this can be modified
            ranked_scores = (-np.array(corpus_scores[int(k)])).argsort()[:thresh]
            
            indicator = 0
            try:
                for index in v:
                    if int(index) in ranked_scores:
                        indicator = 1 
            except:
                for index in [v]:
                    if int(index) in ranked_scores:
                        indicator = 1                
            recall_results[j] += indicator
            partial_recall_results[parts.index(query_labels[int(k)])][j] += indicator
    
    final_results = [result/len(key_ref.items()) for result in recall_results]
        
    print("overall",end=": ")
    for i, thresh in enumerate(recall_threshold):
        print("Recall@"+str(thresh)+":",round(final_results[i],3),end="; ")
        
    macro_threshs = [[] for x in recall_threshold]
    print()
    for t, recall_results in enumerate(partial_recall_results):
        print(parts[t],end=": ")
        final_results = [result/parts_size[t] for result in recall_results]
        
        for i, thresh in enumerate(recall_threshold):
            print("Recall@"+str(thresh)+":",round(final_results[i],3),end="; ")
            macro_threshs[i].append(final_results[i])
        print()
                
##### after this line, use the eval function in demo.ipynb, e.g., dpr_main() ######
