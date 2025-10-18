import json
import os
import tempfile
import aiohttp
import faiss
import fitz  # PyMuPDF
import numpy as np
from sentence_transformers import SentenceTransformer
from src.env_config import env
from src.postgre_module.models import Vacancy
from src.postgre_module.repository.vacancy_repository import VacancyRepository


class ResumeMatchingService:
    def __init__(self, vacancy_repository: VacancyRepository):
        self.model = SentenceTransformer(
            'paraphrase-multilingual-MiniLM-L12-v2')
        self.vacancy_repository = vacancy_repository

    async def extract_text_from_pdf(self, pdf_path: str) -> str:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text() + "\n"
        doc.close()
        return text.strip()

    async def call_g4f_api(self, prompt: str, text: str) -> tuple[str, str]:
        url = f"{env.model.BASE_URL}/chat/completions"
        body = {
            "provider": env.model.PROVIDER,
            "model": env.model.MODEL,
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
                    error_text = await resp.text()
                    raise Exception(
                        f"Failed to send message: {resp.status} {error_text}")

                async for line in resp.content:
                    decoded_line = line.decode('utf-8').strip()
                    if decoded_line == "data: [DONE]":
                        break
                    if decoded_line.startswith("data: "):
                        try:
                            data = json.loads(decoded_line[6:])
                            message = data.get("choices", [{}])[0].get(
                                "delta", {}).get("content")
                            if message:
                                api_text += message
                        except json.JSONDecodeError:
                            continue
                if 'error' in data:
                    raise Exception(data['error']['message'])
                if "</think>" in api_text:
                    result_text: str = api_text.split("</think>")[1].strip()
                    thinking_text: str = api_text.split("</think>")[0].strip()
                else:
                    result_text: str = api_text
                    thinking_text: str = ""
                return result_text, thinking_text

    async def parse_resume_with_ai(self, text: str) -> dict:
        prompt = f"""Извлеки из следующего текста резюме информацию в строгом JSON формате (без лишнего текста):
        {{
            "skills": ["список навыков"] например ["Оценка рисков", "Python", "SQL"],
            "education": ["строка с образованием, включая вуз, специальность и год, например: 'МГУ, Информатика, 2020-2024'"],
            "experience": ["список опытов в формате: 'Должность в Компании (годы, обязанности кратко)', например: 'Developer в Yandex (2021-2025, разработка бэкенда)'"],
            "category": "IT" // Отнеси резюме к одной из следующих категорий: Микроэлектроника, HR, IT, Административная работа, Другое, Логистика, Маркетинг, Медицина, Продажи, Производство, Финансы, Юриспруденция
        }}

        Верни ТОЛЬКО JSON."""
        result_text, _ = await self.call_g4f_api(prompt, text)  # Truncate to ~8k tokens
        try:
            parsed = json.loads(result_text)
            return parsed
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON from model")

    def prepare_resume_texts(self, resume_data: dict) -> list[str]:
        skills = " ".join(resume_data.get('skills', []))
        education = " ".join(resume_data.get('education', []))
        experience = " ".join(resume_data.get('experience', []))
        return [skills, education, experience]

    def prepare_vacancy_text(self, vacancy: Vacancy) -> str:
        return " ".join(vacancy.skills)

    def get_embeddings(self, texts: list[str]) -> np.ndarray:
        return self.model.encode(texts)

    async def find_best_vacancies(self, resume_pdf: bytes, top_n: int = 10) -> list[dict]:
        # Save uploaded PDF to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(resume_pdf)
            pdf_path = tmp_file.name

        try:
            full_text = await self.extract_text_from_pdf(pdf_path)
            resume_data = await self.parse_resume_with_ai(full_text)

            vacancies = await self.vacancy_repository.get_all()
            vacancies = [v for v in vacancies if v.direction == resume_data['category']]
            # Prepare resume embeddings (average of sections)
            resume_texts = self.prepare_resume_texts(resume_data)
            resume_embs = self.get_embeddings(resume_texts)
            resume_emb = np.mean(resume_embs, axis=0).reshape(1, -1)
            resume_emb = resume_emb / np.linalg.norm(resume_emb)  # Normalize

            # Prepare vacancy texts and embeddings
            vacancy_texts = [self.prepare_vacancy_text(
                v) for v in vacancies if v.requirements]
            if not vacancy_texts:
                return []

            vacancy_embs = self.get_embeddings(vacancy_texts)
            vacancy_embs = vacancy_embs / \
                np.linalg.norm(vacancy_embs, axis=1,
                               keepdims=True)  # Normalize

            # Create FAISS index
            dimension = vacancy_embs.shape[1]
            # Inner Product for cosine similarity
            index = faiss.IndexFlatIP(dimension)
            index.add(vacancy_embs)

            # Search for top matches
            distances, indices = index.search(resume_emb, top_n)

            # Collect results (filter to valid indices)
            best_vacancies = []
            for dist, idx in zip(distances[0], indices[0]):
                if idx < len(vacancies):
                    vac = vacancies[idx]
                    best_vacancies.append({
                        'id': str(vac.id),
                        'title': vac.title,
                        'city': vac.city,
                        'company': vac.company,
                        'type': vac.type,
                        'direction': vac.direction,
                        'experience': vac.experience,
                        'score': float(dist),  # Cosine similarity
                        'requirements': vac.requirements
                    })

            return sorted(best_vacancies, key=lambda x: x['score'], reverse=True)[:top_n]
        finally:
            os.unlink(pdf_path)
