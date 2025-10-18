export type Roles = "Administrator" | "User";

export interface Achievement {
  id: string;
  name: string;
  code: string;
  description: string;
  experience_reward: number;
}

interface UnlockedAchievement {
  level: string;
  date_earned: string;
  achievement: Achievement;
}

export interface User {
  user_id: number;
  username: string;
  email: string;
  created_at: string;
}
export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterCredentials {
  username: string;
  password: string;
  repeat_password: string;
}

export interface AuthResponse {
  username: string;
  role: string;
  permissions: string[];
}

export interface AchievementsResponse {
  user: {
    user_id: string;
    level: number;
    experience: number;
  };
  unlocked_achievements: UnlockedAchievement[];
  locked_achievements: Achievement[];
}
