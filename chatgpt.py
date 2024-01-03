import pandas as pd
import openai

openai.api_base = "OpenAI API Basic URL"
openai.api_key = 'YOUR_API_KEY'

#Read CSV files containing names
df = pd.read_csv('')

for index, row in df.iterrows():
    name = row['name']
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Predict the gender of the name: {name}. Gender:"}
        ],
        max_tokens=100
    )
    reply_text = response['choices'][0]['message']['content'].lower()


    gender = reply_text.strip()

    print(gender)
    df.at[index, 'gender'] = gender

#Save updated CSV file
df.to_csv('', index=False)
