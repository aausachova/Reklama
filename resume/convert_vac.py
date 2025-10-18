import json
import asyncio
import os
import aiohttp

# Define constants used in the API function
MODEL = os.getenv("OPENAI_MODEL_NAME")
BASE_URL = os.getenv("OPENAI_BASE_URL")
PROVIDER = os.getenv("OPENAI_PROVIDER")

# The provided API function
async def call_g4f_api(prompt: str, text: str) -> tuple[str, str]:
    url = f"{BASE_URL}/chat/completions"
    body = {
        "provider": PROVIDER,
        "model": MODEL,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ],
        "stream": True,
        "stream_timeout": 120
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
        "Authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0IjoiYXUiLCJ2IjoiMC4wLjAiLCJ1dSI6InN2QzBwUHpaUlVlNkxySUJYS0xwbUE9PSIsImF1IjoiTERjcXFPKzRVNHVqM3c3N0ZUWEV6dz09IiwicyI6IkV5bDh4VXpUVmhlQkVPWnFRR3lKTVE9PSIsImlhdCI6MTc2MDgwNTcxN30.OoaNQUYuypuf3roel4E7v_JDoixzop6Wh_RC05dDpNo"  # Uncomment and set if needed
    }

    api_text = ""
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=body) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise Exception(f"Failed to send message: {resp.status} {text}")

            async for line in resp.content:
                decoded_line = line.decode('utf-8').strip()
                if decoded_line == "data: [DONE]":
                    break
                if decoded_line.startswith("data: "):
                    try:
                        data = json.loads(decoded_line[6:])
                        message = data.get("choices", [{}])[0].get("delta", {}).get("content")
                        if message:
                            api_text += message
                    except json.JSONDecodeError:
                        continue
            if 'error' in data:
                print(data['error']['message'])
                raise Exception()
            if "</think>" in api_text:
                result_text: str = api_text.split("</think>")[1].strip()
                thinking_text: str = api_text.split("</think>")[0].strip()
            else:
                result_text: str = api_text
                thinking_text: str = ""
            return result_text, thinking_text

# Main function to process the JSON file
async def process_vacancies(input_file: str, output_file: str):
    # Read the JSON file
    with open(input_file, 'r', encoding='utf-8') as f:
        vacancies = json.load(f)
    
    # System prompt for transforming requirements into skills
    system_prompt = (
        "Преобразуй список требований вакансии в структурированный набор навыков. "
        "Выдай результат в формате JSON: {\"skills\": [\"Навык 1\", \"Навык 2\", ...]}. "
        "Навыки должны быть описаны 1-3 словами. Например \"Python\", \"SQL\", \"Анализ рисков\", \"Machine Learning\"."
        "Сделай навыки краткими и уникальными, объединяя похожие если нужно. "
        "Используй русский язык."
    )
    
    processed_vacancies = []
    
    for vacancy in vacancies:
        # Prepare the text from requirements
        requirements_text = "\n".join(vacancy["requirements"])
        
        try:
            # Call the API
            result_text, thinking_text = await call_g4f_api(system_prompt, requirements_text)
            
            # Parse the result assuming it's JSON
            skills_data = json.loads(result_text)
            skills = skills_data.get("skills", [])
            
            # Add skills to the vacancy
            processed_vacancy = vacancy.copy()
            processed_vacancy["skills"] = skills
            processed_vacancies.append(processed_vacancy)
            
            print(f"Processed vacancy {vacancy['id']}: {thinking_text}")
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(processed_vacancies, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error processing vacancy {vacancy['id']}: {e}")
            # Optionally, add with empty skills
            processed_vacancy = vacancy.copy()
            processed_vacancy["skills"] = []
            processed_vacancies.append(processed_vacancy)
    
    # Write the output JSON

    
    print(f"Processed {len(processed_vacancies)} vacancies. Output saved to {output_file}")

# Run the script
if __name__ == "__main__":
    input_file = "vacancies.json"  # Replace with your input JSON file path
    output_file = "processed_vacancies.json"  # Output file path
    asyncio.run(process_vacancies(input_file, output_file))