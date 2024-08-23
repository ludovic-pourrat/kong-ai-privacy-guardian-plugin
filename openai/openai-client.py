from openai import OpenAI

client = OpenAI(
   base_url="http://localhost:8000/investments/openai-chat",
   api_key="none",
   project="proj_UvxoZanZ3X4VO3cTE24fjQio",
   default_headers={"X-API-Key": "4255dae0-4b67-4b22-a9bf-396d894a516e"}
)

query = """Could you provide an email template related to investments proposal for Ludovic Pourrat who wants to invest
           in ESG against a 5% percent exposure to a 1 billion value portfolio ?"""

system = """The AI assistant is a financial advisor with expertise in private banking and wealth management market, and investment strategies
         """

response = client.chat.completions.create(
   model="gpt-4o",
   messages=[
      {
         "role": "system",
         "content": system
      },
      {
         "role": "user",
         "content": query
      }
   ],
   stream=False,
)

message = response.choices[0].message.content
print(message)
