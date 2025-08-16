from dotenv import dotenv_values
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage
from langchain_gigachat import GigaChat


def get_model(model_name: str = "GigaChat-2") -> BaseChatModel:
    config = dotenv_values(".env")

    giga = GigaChat(
        credentials=config["GIGACHAT_AUTHORIZATION_KEY"],
        verify_ssl_certs=False,
        scope="GIGACHAT_API_PERS",
        model=model_name,
    )
    return giga


if __name__ == "__main__":
    llm = get_model()

    messages = [
        HumanMessage(content="Hello"),
    ]

    print(llm.invoke(messages).content)
