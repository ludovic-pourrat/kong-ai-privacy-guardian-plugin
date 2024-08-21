from openai import OpenAI

client = OpenAI(
   base_url="http://localhost:8000/investments/openai-chat",
   api_key="none",
   project="proj_UvxoZanZ3X4VO3cTE24fjQio",
   default_headers={"X-API-Key": "4255dae0-4b67-4b22-a9bf-396d894a516e"}
)

query = """Could you provide me investments proposal for me who wants to invest in ESG against
                    a 5% percent exposure to a 1 billion value portfolio ? """

stream = client.chat.completions.create(
   model="gpt-4o-mini",
   messages=[
      {
         "role": "system",
         "content": "You are a helpful private banker assistant"
      },
      {
         "role": "user",
         "content": query
      }
   ],
   stream=True,
)

print('')

for chunk in stream:
   print(chunk.choices[0].delta.content or "", end="", flush=True)

