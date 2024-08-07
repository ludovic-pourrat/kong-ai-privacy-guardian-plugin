from openai import OpenAI

client = OpenAI(
   base_url="http://localhost:8000/confidential/openai-chat",
   api_key="none",
   project="proj_UvxoZanZ3X4VO3cTE24fjQio"
)

stream = client.chat.completions.create(
   model="gpt-4o-mini",
   messages=[
      {
         "role": "system",
         "content": "You are a helpful private banker assistant"
      },
      {
         "role": "user",
         "content": "Could you provide me some investments proposal for Ludovic Pourrat who wants to invest in ESG against a 5% percent exposure to a 1 billion value portfolio ?"
      }
   ],
   stream=True,
)

print('>')
for chunk in stream:
   print(chunk.choices[0].delta.content or "", end="", flush=True)

