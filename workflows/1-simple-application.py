import os
import logging
from openai import OpenAI
from dotenv import load_dotenv

# Setup environment and logging
load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Initialize the OpenAI client and define the LLM model
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "gpt-4o-mini"


class PediatricChatbotWorkflow:
    """
    This class implements an interactive pediatric diagnostic chatbot.
    
    The workflow:
      1. Begins with a static initial question.
      2. After each user response, a call is made to the LLM to ask the next clarifying question.
         The LLM is given the conversation transcript so far and is asked to respond with one question.
         If no further clarification is needed, the LLM returns "Done".
      3. Once the conversation is complete, a final LLM call generates a structured markdown report that
         includes Diagnosis, Treatment recommendations, a Disclosure reminder, and Product recommendations.
    
    The output markdown follows this structure:
    
      **Diagnosis**
      {Diagnosis}
      
      **Treatment**
      {Treatment}
      You can also check [pharmacies open now](https://www.google.com/maps/search/pharmacies+open+now/).
      
      **Disclosure reminder**
      This information is provided 100% by an AI and should not replace a consultation with a healthcare provider. (PUBLIC DISCLAIMER)[https://pedirobot.com/public-disclaimer-for-pedirobot/]
      
      **Revisit the conversation**
      Please revisit our conversation anytime if you still have questions or need another diagnostic for your child.
      
      **Product recommendations**
      {Product_recommendations}
      
      **This tool is supported by people. [Make a donation to support this tool](https://buy.stripe.com/8wM2aAacrbO36MUdQQ)**
    """

    def __init__(self):
        # The conversation is stored as a list of Q/A pairs.
        self.conversation = []
        # Begin with a static opening question.
        self.initial_question = "What seems to be the issue with the child or infant?"

    def run_conversation(self):
        # Ask the static initial question
        print(self.initial_question)
        user_response = input("Your response: ")
        self.conversation.append({"question": self.initial_question, "answer": user_response})

        # Loop to ask dynamically generated questions one at a time.
        while True:
            next_question = self.get_llm_next_question()
            # If the LLM indicates that no further questions are needed, end the conversation.
            if next_question.lower() == "done" or next_question == "":
                break

            print(next_question)
            response = input("Your response: ")
            self.conversation.append({"question": next_question, "answer": response})

        # Once done, generate a final markdown report via an LLM call.
        final_report = self.generate_final_report()
        print("\nFinal Diagnosis and Recommendations:\n")
        print(final_report)

    def get_llm_next_question(self) -> str:
        """
        Using the entire conversation transcript so far,
        this function calls the LLM to generate the next concise clarifying question.
        The LLM is instructed to ask only one question. If no further clarification is needed, it responds with "Done".
        """
        # Compose a transcript from the conversation so far.
        transcript = ""
        for pair in self.conversation:
            transcript += f"Q: {pair['question']}\nA: {pair['answer']}\n"
        # Prepare the prompt for the LLM.
        prompt = (
            "You are a pediatrician assisting in a diagnostic conversation with a parent. Based on the conversation transcript below, "
            "ask the next concise and clarifying question necessary to complete the diagnosis. "
            "Ask only one question. If no further clarification is needed, simply respond with 'Done'.\n\n"
            f"Conversation Transcript:\n{transcript}\n\n"
            "Next Question:"
        )

        # Call the LLM to get the next question.
        completion = client.beta.chat.completions.parse(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
            ],
            response_format=dict,
        )
        next_question = completion.choices[0].message.content.strip()
        logger.info(f"LLM next question: {next_question}")
        return next_question

    def generate_final_report(self) -> str:
        """
        After the conversation is complete, this method calls the LLM to generate the final report.
        The conversation transcript is injected into a prompt that instructs the LLM
        to output a markdown formatted response containing Diagnosis, Treatment,
        a disclosure, and Product recommendations.
        """
        transcript = ""
        for pair in self.conversation:
            transcript += f"Q: {pair['question']}\nA: {pair['answer']}\n"
        prompt = (
            "Based on the following conversation with a parent regarding their child's health, produce a structured, "
            "markdown formatted diagnostic report. The report must include the sections below and follow the exact format:\n\n"
            "**Diagnosis**\n{Diagnosis}\n\n"
            "**Treatment**\n{Treatment}\n\n"
            "You can also check [pharmacies open now](https://www.google.com/maps/search/pharmacies+open+now/).\n\n"
            "**Disclosure reminder**\n"
            "This information is provided 100% by an AI and should not replace a consultation with a healthcare provider. "
            "(PUBLIC DISCLAIMER)[https://pedirobot.com/public-disclaimer-for-pedirobot/]\n\n"
            "**Revisit the conversation**\n"
            "Please revisit our conversation anytime if you still have questions or need another diagnostic for your child.\n\n"
            "**Product recommendations**\n{Product_recommendations}\n\n"
            "**This tool is supported by people. [Make a donation to support this tool](https://buy.stripe.com/8wM2aAacrbO36MUdQQ)**\n\n"
            f"Conversation Transcript:\n{transcript}\n"
        )

        # Call the LLM to generate the final markdown report.
        completion = client.beta.chat.completions.parse(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
            ],
            response_format=dict,
        )
        final_report = completion.choices[0].message.content.strip()
        logger.info("Final report generated by LLM.")
        return final_report


def main():
    print("Pediatric Diagnostic Chatbot")
    print("============================\n")
    workflow = PediatricChatbotWorkflow()
    workflow.run_conversation()


if __name__ == "__main__":
    main()