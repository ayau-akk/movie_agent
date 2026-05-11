import os
from dotenv import load_dotenv

from langchain_ollama import ChatOllama
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from tools import (
    search_movie_by_title,
    search_movies_list,
    get_full_movie_plot,
    get_movie_rating,
)

load_dotenv()

MODEL_NAME = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")


def create_movie_agent():
    llm = ChatOllama(
        model=MODEL_NAME,
        temperature=0.2
    )

    tools = [
        search_movie_by_title,
        search_movies_list,
        get_full_movie_plot,
        get_movie_rating,
    ]

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    system_prompt = """
Ты — AI-агент «Киноманьяк».

Ты эксперт по фильмам, режиссёрам, актёрам, жанрам, рейтингам и рекомендациям.

Правила работы:

1. Если пользователь спрашивает факты о фильме, используй инструменты.
2. Не выдумывай рейтинг, режиссёра, актёров, награды и сюжет.
3. Если пользователь просит сравнить два фильма, вызови search_movie_by_title для каждого фильма, потом сравни результаты.
4. Если пользователь спрашивает рейтинг, используй get_movie_rating.
5. Если пользователь просит найти фильмы по ключевому слову, используй search_movies_list.
6. Если пользователь просит полный сюжет, используй get_full_movie_plot.
7. Если пользователь сообщает имя, любимые фильмы, жанры, актёров или режиссёров — запомни это из истории диалога.
8. Используй память диалога для вопросов: "Как меня зовут?", "Что я люблю?", "Какие фильмы мне посоветуешь?"
9. В ответе кратко объясняй свои действия: что ты проверил и почему.
10. Отвечай на русском языке.
"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_tool_calling_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True,
    )

    return agent_executor


def main():
    print("🎬 AI-агент «Киноманьяк» запущен!")
    print("Напиши вопрос про фильмы.")
    print("Для выхода напиши: exit")
    print("-" * 60)

    agent_executor = create_movie_agent()

    while True:
        user_input = input("\nТы: ")

        if user_input.lower() in ["exit", "quit", "выход"]:
            print("Киноманьяк: Пока! Хорошего киносеанса!")
            break

        try:
            response = agent_executor.invoke({"input": user_input})
            print("\nКиноманьяк:")
            print(response["output"])
        except Exception as error:
            print("\nПроизошла ошибка:")
            print(error)


if __name__ == "__main__":
    main()
