
def generate_chat_answer(message):
    result = "模拟回答：" + message
    return result
def generate_batch_chat_answers(messages):
    result = []
    for message in messages:
        result.append(generate_chat_answer(message))
    return result
        
def generate_embedding(text):

    result = [0.1, 0.2, 0.3]
    return result