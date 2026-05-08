import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_huggingface import HuggingFacePipeline, ChatHuggingFace
from config import LOCAL_LLM_DIR, MAX_NEW_TOKENS, TEMPERATURE, TOP_P, REPETITION_PENALTY

def create_llm():
    print("Loading Phi-3 model...")
    tokenizer = AutoTokenizer.from_pretrained(LOCAL_LLM_DIR, trust_remote_code=False)
    model = AutoModelForCausalLM.from_pretrained(
        LOCAL_LLM_DIR,
        device_map={"": "cpu"},
        torch_dtype=torch.float32,
        low_cpu_mem_usage=True,
    )

    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=MAX_NEW_TOKENS,
        temperature=TEMPERATURE,
        top_p=TOP_P,
        repetition_penalty=REPETITION_PENALTY,
        do_sample=True,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.pad_token_id if tokenizer.pad_token_id else tokenizer.eos_token_id,
    )

    llm = HuggingFacePipeline(pipeline=pipe)
    chat_model = ChatHuggingFace(llm=llm)
    print("LLM ready.")
    return chat_model