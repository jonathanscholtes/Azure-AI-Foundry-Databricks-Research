from azure.ai.evaluation import GroundednessEvaluator,CoherenceEvaluator,RelevanceEvaluator
import json
from dotenv import load_dotenv
from os import environ
from semantic_kernel.contents import ChatHistory 


load_dotenv(override=True)


class Evaluation:
    def __init__(self):

        model_config = {
            "azure_endpoint": environ["AZURE_OPENAI_ENDPOINT"],
            "api_key": environ["AZURE_OPENAI_API_KEY"],
            "azure_deployment": environ["AZURE_OPENAI_CHAT_MODEL"],
            "api_version": environ["AZURE_OPENAI_API_VERSION"],
        }

        self.groundedness_evaluator = GroundednessEvaluator(model_config=model_config)
        self.coherence_evaluator = CoherenceEvaluator(model_config=model_config)
        self.relevance_evaluator = RelevanceEvaluator(model_config=model_config)


    def __get_conext_from_history(self, history:ChatHistory):
        context = ""
        for message in history.messages:
            if message.role != "assistant":
                continue
            context += message.content + "\n"
        return context

    def evaluate(self, user_query: str, response: str, history:ChatHistory):
        context = self.__get_conext_from_history(history)
        return self.evaluate(user_query, response, context)

    def evaluate(self, user_query: str, response: str, context: str):
        groundedness_result = self.groundedness_evaluator(
            query=user_query,
            response=response,
            context=context
        )
        coherence_result = self.coherence_evaluator(
            query=user_query,
            response=response,
            context=context
        )

        relevance_result = self.relevance_evaluator(
            query=user_query,
            response=response
        )

        return {
            "groundedness": groundedness_result,
            "coherence": coherence_result,
            "relevance": relevance_result
        }