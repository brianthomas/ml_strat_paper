import gzip
import h5py
import json
import os
import pandas as pd

def open_datafiles(version:str, lpt:float=-2.5, contentType:str="decadal_report")->list:

    return openlda_viz(version), open_timeseries(version), open_topic_distrib(version, contentType), open_stable_topics(version, lpt)

def openlda_viz(version:str)->pd.DataFrame:

    lda_viz_filename = f"../data/pyLDAvis_data_{version}.json.gz"

    # Load data which contain mapping of top keywords to topics
    with gzip.open(lda_viz_filename, 'r') as fin:
        pyldavis_data = json.loads(fin.read().decode('utf-8'))


    #with open(lda_viz_filename, 'r') as f0:
    #    pyldavis_data =json.load(f0)

    return pd.DataFrame(json.loads(pyldavis_data)['tinfo'])

def open_timeseries(version:str)->pd.DataFrame:

    timeseries_filename = f"../data/time_series_characteristics_{version}.csv.gz"

    # Load in data with CAGR info, each row is a topic number (index off by one)
    return pd.read_csv(timeseries_filename, compression='gzip', index_col=False)


def open_topic_distrib(version:str, contentType:str="decadal_report")->pd.DataFrame:

    # data file to use
    if contentType == 'decadal_report':
        topic_distrib_filename = f"../data/topic_distributions_decadal2010_panel_reports_{version}.csv.gz"
    elif contentType == 'whitepapers':
        topic_distrib_filename = f"../data/topic_distributions_2010_whitepapers_{version}.csv.gz"
    else:
        raise Exception (f"Unknown contentType: {contentType}")

    # Read in document inference information
    return pd.read_csv(topic_distrib_filename, compression='gzip', index_col=False)


def open_stable_topics(version:str, lpt:float=-2.5)->pd.DataFrame:
    return pd.read_csv(f'../data/stable_topics_{version}_lp{lpt}.csv')

def doc_tcs_by_topic (doc_data, threshold:float=0.01, id_col:str="Unnamed: 0"):
    ''' find the TCS score for topics in the document data passed '''

    # Save para ids then drop
    doc_data = doc_data.drop([id_col], axis=1)

    topics = doc_data.columns
    tcs = { str(t):0.0 for t in topics }

    # get topics for each paper
    for i in range(0, len(doc_data)):
        row_data = doc_data[doc_data.index==i]

        # now add in data which have inference higher than threshold
        for t in topics:
            inf = float(row_data[t])
            if inf > threshold:
                tcs[t] += inf

    return tcs

def topic_name(topic:int, lda_viz_data:pd.DataFrame)->str:

    topic_keys = lda_viz_data[lda_viz_data['Category']== f'Topic{topic}']
    sorted_keys = topic_keys.sort_values(by="logprob", ascending=False)
    name = ""
    # capture top 5 keywords
    for i in range(0,5):
        name = name + sorted_keys[i:i+1]['Term'].to_string(index=False).strip() + ", "

    return name[:-2]

def create_dataset(document_scores, timeseries_data:pd.DataFrame, lda_viz_data:pd.DataFrame, which_cagr:str='CAGR', ignore_topics:list=[], flex_min_cagr:bool=False, min_cagr:float=0.0, max_doc_score:float=1.0)->pd.DataFrame:
    """ Assemble a dataset of document score vs cagr, counts and ri """

    topic_cagr = timeseries_data[which_cagr]
    topic_count = timeseries_data['count']

    topics = [str(topic) for topic in topic_cagr.index if topic not in ignore_topics]
    topic_keywords = [topic_name(int(t), lda_viz_data) for t in topics if t not in ignore_topics]
    score_vals = [document_scores[t] for t in topics if t not in ignore_topics]

    norm_score_vals = [document_scores[t]/max_doc_score for t in topics if t not in ignore_topics]

    cagr_vals = [v for t,v in topic_cagr.items() if t not in ignore_topics]
    count_vals = [v for t,v in topic_count.items() if t not in ignore_topics]

    # find the minimum cagr in this dataset; this provides a lower bound of RI at 0.0
    data_min_cagr = sorted(cagr_vals)[0]
    if flex_min_cagr:
        min_cagr = data_min_cagr
        print(f'MIN_CAGR: {min_cagr}')
    else:
        print(f'Data MIN_CAGR: {data_min_cagr}')

    # we use min_cagr to keep from calcuation of ri metric
    ri_vals = [(v-min_cagr)*topic_count[t] for t,v in topic_cagr.items() if t not in ignore_topics]

    result = pd.DataFrame({'topic': topics, 'raw_doc_tcs': score_vals, 'doc_tcs': norm_score_vals, 'tcs':count_vals,
                           'cagr': cagr_vals, 'keywords': topic_keywords, 'ri': ri_vals})

    # clean up nulls and return
    return result[~result['cagr'].isnull()]

# some code to load h5py file we need to use
def load_topic_bibcode_h5py(viz_data_loc: os.PathLike)->pd.DataFrame:
    #Load object parameters from an hdf database.
    #Args:
    #    viz_data_loc: path to opinionated hdf file
    
    with h5py.File(viz_data_loc, "r") as f0:
        embedding = f0["embedding"][:]
        topic_coherences = f0["topic_coherences"][:]
        paper_ids = f0["paper_ids"][:]
        bibcodes = f0["bibcodes"][:]

    df = pd.DataFrame(embedding)
    df.index = paper_ids
    df['year'] = [ int(bibcode[0:4]) for bibcode in bibcodes]
        
    return df
