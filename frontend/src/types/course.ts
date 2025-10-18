export interface Course {
  id: string;
  title: string;
  description: string;
  category: string;
  experience_level: "Без опыта" | "С опытом";
  image: string;
  duration: number;
  total_lessons: number;
  completed_lessons: number;
  requirements: string[];
  whatYouWillLearn: string[];
  is_participant: boolean;
}
