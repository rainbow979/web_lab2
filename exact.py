'''import spacy
import zh_core_web_lg
import neuralcoref

nlp = zh_core_web_lg.load()
neuralcoref.add_to_pipe(nlp)'''

# summarizer
from summarizer import Summarizer
#from summarizer.text_processors.sentence_handler import SentenceHandler
#from spacy.lang.zh import Chinese
from transformers import *

from bert import bert

# Load model, model config and tokenizer via Transformers
modelName = "bert-base-chinese"
custom_config = AutoConfig.from_pretrained(modelName)
custom_config.output_hidden_states=True
custom_tokenizer = AutoTokenizer.from_pretrained(modelName)
custom_model = AutoModel.from_pretrained(modelName, config=custom_config)

model = bert(custom_model=custom_model,
    custom_tokenizer=custom_tokenizer)
'''model = Summarizer(
    custom_model=custom_model, 
    custom_tokenizer=custom_tokenizer,
    sentence_handler = SentenceHandler(language=Chinese)
    )'''
    
with open('1.txt', 'r') as f:
    for line in f:
        line = line.strip()
        text = line
        break
print(text)

print('--------------------------------------------------------------------')

body = text

result = model(body, min_length=4, max_length=50, ratio=0.1, use_first=True)
#full = ''.join(result)
print(result)

full = '\n'.join(result)

with open('output.txt', 'w') as f:
    for line in full:
        f.write(line)