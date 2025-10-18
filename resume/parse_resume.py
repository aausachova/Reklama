import asyncio
import fitz  # PyMuPDF для извлечения текста
from openai import OpenAI
import json
import os
import aiohttp

# Настройки
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Или hardcode: "sk-YourKeyHere"
# Или "gpt-4o-mini" для скорости/дешевизны
MODEL = os.getenv("OPENAI_MODEL_NAME")
BASE_URL = os.getenv("OPENAI_BASE_URL")
PROVIDER = os.getenv("OPENAI_PROVIDER")
PDF_PATH = "test_resume_2.pdf"  # Путь к файлу

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
        # "Authorization": f"Bearer {OPENAI_API_KEY}"
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
        
def extract_text_from_pdf(pdf_path):
    """Извлечение текста из PDF"""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text() + "\n"
    doc.close()
    return text.strip()


def parse_resume_with_openai(text):
    """Парсинг через OpenAI: prompt для JSON-output"""
    prompt = f"""Извлеки из следующего текста резюме информацию в строгом JSON формате (без лишнего текста):
    {{
        "skills": ["список навыков"] например ["Оценка рисков", "Python", "SQL"],
        "education": ["строка с образованием, включая вуз, специальность и год, например: 'МГУ, Информатика, 2020-2024'"],
        "experience": ["список опытов в формате: 'Должность в Компании (годы, обязанности кратко)', например: 'Developer в Yandex (2021-2025, разработка бэкенда)'"]
    }}

    Текст резюме: {text[:8000]}  # Обрезаем до ~8k токенов (для turbo)

    Верни ТОЛЬКО JSON."""

    result_text, thinking_text = asyncio.run(call_g4f_api(prompt, text))
    try:
        parsed = json.loads(result_text)
        return parsed
    except json.JSONDecodeError:
        print("Ошибка парсинга JSON:", result_text)
        return {"error": "Invalid JSON from model"}


# Запуск
if __name__ == "__main__":

    full_text = extract_text_from_pdf(PDF_PATH)
    print("Извлечённый текст (первые 500 симв.):", full_text)

    parsed_data = parse_resume_with_openai(full_text)
    print("\nПарсинг результата:")
    print(json.dumps(parsed_data, ensure_ascii=False, indent=2))

    with open('resume.json', 'w', encoding='utf-8') as f:
        json.dump(parsed_data, f, ensure_ascii=False, indent=4)
