from huggingface_hub import snapshot_download
#download llama2
_model_path = snapshot_download(repo_id='meta-llama/Llama-2-7b-chat-hf',
                               token='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')

#load in 4bit
from bigdl.llm.transformers import AutoModelForCausalLM

_model_in_4bit = AutoModelForCausalLM.from_pretrained(pretrained_model_name_or_path="meta-llama/Llama-2-7b-chat-hf",
                                                     load_in_4bit=True)

#load tokenizer
from transformers import LlamaTokenizer

_tokenizer = LlamaTokenizer.from_pretrained(pretrained_model_name_or_path="meta-llama/Llama-2-7b-chat-hf")

#save and load low bit model
_save_directory='./llama-2-7b-bigdl-llm-4-bit'
_model_in_4bit.save_low_bit(_save_directory)
del(_model_in_4bit)
_tokenizer.save_pretrained(_save_directory)

# 这里的 AutoModelForCausalLM 是从 bigdl.llm.transformers 导入的
_model_in_4bit = AutoModelForCausalLM.load_low_bit(_save_directory)
_tokenizer = LlamaTokenizer.from_pretrained(_save_directory)

#process pptx files
from pptx import Presentation

def brief_intro(current_card: card)->str:
    #generates brief introduction for a card. receives a Card class and outputs a string.
    intro='INTRODUCTION';
    return intro;


def ask_question(question:str)->str:
    #generates answer to certain questions. reveives a string and outputs a string. 
    answer='ANSWER';
    return answer;


def more_info(current_card:card)->str:
    #generates more information about a card. receives a card class and outputs a string. 
    info='MORE INDORMATION';
    return info;


def relative_questions()->list:
    #outputs a list when called.
    question_list=['Q1'];
    return question_list;


def get_sylla(syllabus:str)->dict:
    #read syllabus and outputs a list of lectures. receives a string and outputs a dictionary.
    return lec_dict;


def dump_slides(slides:Presentation,lec_dict:dict):
    #read slides and attach them to lectures. receives a .pptx file and a dictionary.
    return;


def get_card(slides:Presentation)->list:
    #generates cards. receives a .pptx file and outputs a list.
    return card_list;

