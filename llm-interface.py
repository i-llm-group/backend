from huggingface_hub import snapshot_download
#download llama2
model_path = snapshot_download(repo_id='meta-llama/Llama-2-7b-chat-hf',
                               token='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')

#load in 4bit
from bigdl.llm.transformers import AutoModelForCausalLM
model_in_4bit = AutoModelForCausalLM.from_pretrained(pretrained_model_name_or_path="meta-llama/Llama-2-7b-chat-hf",
                                                     load_in_4bit=True)

#load tokenizer
from transformers import LlamaTokenizer
tokenizer = LlamaTokenizer.from_pretrained(pretrained_model_name_or_path="meta-llama/Llama-2-7b-chat-hf")

#save and load low bit model
save_directory='./llama-2-7b-bigdl-llm-4-bit'
model_in_4bit.save_low_bit(save_directory)
del(model_in_4bit)
tokenizer.save_pretrained(save_directory)

# 这里的 AutoModelForCausalLM 是从 bigdl.llm.transformers 导入的
model_in_4bit = AutoModelForCausalLM.load_low_bit(save_directory)
tokenizer = LlamaTokenizer.from_pretrained(save_directory)

#process pptx files
from pptx import Presentation


def brief_intro(Card):
    intro='some brief introduction';
    return intro;

def ask_question(question):
    answer=''
    return answer;

def more_info(Card):
    info='some more information';
    return info;

def relative_questions():
    question_list=[''];
    return question_list;

def get_sylla(syllabus):
    return lec_list;

def dump_slides(slides_collection):
    return;

def get_card(slides):
    return card_list;

