import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv() #Loads the environment variables from .env

client = Groq() #Creates an instance of the Groq client

def continuous_conversation():
    print("Chat initiated. (Type 'sair' to terminate the program.)")

    #Read the Knowledge Base from the text file
    try:
        with open("conhecimento_otimizado.txt", "r", encoding="utf-8") as file:
            knowledge_base = file.read()
    except FileNotFoundError:
        print("Erro: O ficheiro 'conhecimento_otimizado.txt' não está na mesma pasta que o script.")
        return
    
    #Initial memory
    #List created with a the ground rules for the assistant
    history = [
        {
            "role": "system",
            "content": f"""És a 'Alma', a assistente virtual do espaço Ki Alma. 
            NUNCA te faças passar pela Liliana Carvalho. O teu tom é humano, acolhedor, empático e profissional.
            Podes usar emojis de forma moderada (🤍, ✨, 🙏).
            Trata o cliente por 'tu' por defeito, salvo se a pessoa for muito formal.
            Responde EXCLUSIVAMENTE em Português de Portugal e sê concisa.
            
            O TEU OBJETIVO: Acolher o cliente, responder às dúvidas, recolher o Nome, Serviço pretendido e Telefone. 
            No fim, deves informar que a Liliana entrará em contacto brevemente.
            
            BASE DE CONHECIMENTO (Usa apenas esta informação para responder):
            {knowledge_base}"""
        }
    ]

    #greetings message to start the conversation
    greetings = "Alma: Olá!✨ Sou a Alma, a assistente virtual do espaço Ki Alma. Como posso ajudar-te hoje?"
    print(greetings)
    history.append({"role": "assistant", "content": greetings})

    #Conversation loop
    #'while True' makes an infinite loop that keeps the program running
    while True:
        #Ask the user for input
        question = input("\nUtilizador: ")

        #Exit condition to avoid getting stuck in an infinite loop
        if question.lower() == "sair":
            print("Programa terminado.")
            break

        #Update the memory with the user's question
        #the '.append()' adds a new item to the end of our list
        history.append({"role": "user", "content": question})

        #Send the history to the Groq API
        answer = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=history,
            temperature=0.3 
            #Controls the randomness of the output. Lower values make the output more deterministic, while higher values make it more random.
        )

        #Get the response from the Groq API and print it
        answer_text = answer.choices[0].message.content
        print(f"\nAlma: {answer_text}")

        #Update the memory with the assistant's response
        history.append({"role": "assistant", "content": answer_text})

if __name__ == "__main__":
    continuous_conversation()