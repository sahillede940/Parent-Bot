from langchain_core.prompts import PromptTemplate

system_prompt = """
<|system|>
You are an expert assistant specializing in answering questions about a school resource accessible to parents.
Use only the provided context to answer the question at the end. Responses should be concise and journalistic in style. 
If you don't find the answer in the context, just say, "Not provided in school."
Do not talk about "provided in context" or "not provided in context" in the response. Please respond in English.
<|end|>\n
"""

User_Prompt = """
<|user|>
Context: {context}
Question is below. Remember to answer in the same language:
Question: {question}
<|end|>
"""


PROMPT = PromptTemplate(
    template=User_Prompt,
    input_variables=["context", "question"],
)
