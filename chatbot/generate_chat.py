from gpt4all import GPT4All
import os

model_name = 'orca-mini-3b.ggmlv3.q4_0.bin'
model_path = os.environ['MODEL']

model = GPT4All(model_name=model_name, model_path=model_path)

prompt_template = "I'm looking to purchase a new SSD and I'm deciding between two options:\n" \
                  "1. Samsung 970 SSD, which has NVMe M.2 interface and offers a read speed of 3100 MB/s and a write speed of 2300 MB/s.\n" \
                  "2. HP ESP SSD, which is also NVMe M.2 and offers a read speed of 2100 MB/s and a write speed of 1900 MB/s.\n" \
                  "Can you help me decide which one is the better choice for my needs?"
system_template = 'A chat between a curious user and an artificial intelligence assistant, and you are a marketing specialist.'
template = """
You are a marketing specialist. you have to suggest products based on this list:
1. Samsung 970 SSD, which has NVMe M.2 interface and offers a read speed of 3100 MB/s and a write speed of 2300 MB/s.
2. HP ESP SSD, which is also NVMe M.2 and offers a read speed of 2100 MB/s and a write speed of 1900 MB/s.
"""

def chatgen(query):
    with model.chat_session(system_template) as session:
        user_input= query
        response = model.generate(prompt=user_input, max_tokens=1000)
        response = model.current_chat_session[-1]['content']
    return response

