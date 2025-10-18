import apiClient from "@/lib/axios";
import type { Course } from "@/types/course";



interface CourseData {
  id: string;
  title: string;
  description : string;
  category: string;
  experience_level: "Без опыта" | "С опытом";
  image: string;
  duration: number;
  total_lessons: number;
  created_date: string;
}

interface CourseInRequest {
  requirements: string[];
  learn_points: string[];
  course: CourseData
}

interface CourseRequest {
  courses: CourseInRequest[]
}

interface UserCourseData {
  user_id: string;
  course_id: string;
  completed_lessons: number;
}

interface UserCourseRequest {
  data: UserCourseData[];
}

export const fetchCourses = async (): Promise<Course[]> => {
  const [coursesRes, userCoursesRes] = await Promise.all([
    apiClient.get<CourseRequest>("/api/courses"),
    apiClient.get<UserCourseRequest>("/api/courses/user")
  ]);

  const userProgressMap = new Map<string, number>();
  for (const entry of userCoursesRes.data.data) {
    userProgressMap.set(entry.course_id, entry.completed_lessons);
  }

  const courses: Course[] = coursesRes.data.courses.map(({ course, requirements, learn_points }) => ({
    id: course.id,
    title: course.title,
    description: course.description,
    category: course.category,
    experience_level: course.experience_level,
    image: course.image,
    duration: course.duration,
    total_lessons: course.total_lessons,
    completed_lessons: userProgressMap.get(course.id) ?? 0,
    requirements,
    whatYouWillLearn: learn_points,
    is_participant: userProgressMap.has(course.id)
  }));

  return courses;
};