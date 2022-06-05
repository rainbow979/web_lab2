from functools import partial

from summarizer.transformer_embeddings.bert_embedding import BertEmbedding
from summarizer.cluster_features import ClusterFeatures

import numpy as np

# origin from bert-extractive-summarizer/summarizer/bert.py
# split sentences based on srt file and simpler
class bert:

    def __init__(self, custom_model, custom_tokenizer, gpu_id=0):
        
        self.model = BertEmbedding('bert-base-uncased', custom_model, custom_tokenizer, gpu_id)
        self.model_func = partial(self.model, hidden=-2, reduce_option='mean', hidden_concat=False)
        
    def __call__(
        self,
        text,
        ratio=0.2,
        min_length=10,
        max_length=100,
        use_first=True,
        algorithm='kmeans'
        ):
        first_embedding = None
        sentences = text.split('。')
        sentences = [c for c in sentences if len(c) >= min_length and len(c) <= max_length]
        hidden = self.model_func(sentences)
        num_sentences = None
        if use_first:
            num_sentences = num_sentences - 1 if num_sentences else num_sentences

            if len(sentences) <= 1:
                return sentences, hidden

            first_embedding = hidden[0, :]
            hidden = hidden[1:, :]
            
        summary_sentence_indices = ClusterFeatures(
            hidden, algorithm).cluster(ratio, num_sentences)

        if use_first:
            summary_sentence_indices = [i + 1 for i in summary_sentence_indices]
            summary_sentence_indices.insert(0, 0)

            hidden = np.vstack([first_embedding, hidden])

        sentences = [sentences[j] for j in summary_sentence_indices]
        embeddings = np.asarray([hidden[j] for j in summary_sentence_indices])

        return sentences