import type { Event } from "@/types/event";

const MOCK_EVENTS: Event[] = [
  {
    id: 1,
    title: "TECH SQUAD: МИССИЯ 'ИИ' от IT кластера",
    description:
      "Тебе предстоит разработать MVP системы, которая с помощью ML-моделей будет анализировать сложные промышленные изображения (например, рентгеновские снимки) и находить в них критически важные аномалии или дефекты.",
    company: {
      name: "Эвент 1",
      logo: "/img/Gazprom.svg",
    },
    endDate: "20.05.2025, 8:30",
    solutions: {
      current: 8,
      total: 30,
    },
  },
];

export const getEvents = async (): Promise<Event[]> => {
  await new Promise((resolve) => setTimeout(resolve, 500));
  return MOCK_EVENTS;
};

export const getEventById = async (id: number): Promise<Event | undefined> => {
  await new Promise((resolve) => setTimeout(resolve, 500));
  return MOCK_EVENTS.find((event) => event.id === id);
};
