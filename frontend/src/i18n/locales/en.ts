export default {
  language: {
    select: "Select language",
    ru: "Русский",
    en: "English",
  },
  common: {
    loading: "Loading",
    profile: "Profile",
    logout: "Logout",
  },
  sidebar: {
    control: "Control",
    dashboard: "Dashboard",
    userManagement: "User Management",
    navigation: "Navigation",
    home: "Home",
    projects: "Projects from companies",
    theory: "Theory",
    settings: "Settings",
  },
  settings: {
    title: "Settings",
    subtitle: "Manage application and account settings",
    app: {
      title: "Application",
      subtitle: "Interface settings",
      theme: {
        title: "Theme",
        subtitle: "Choose your theme",
        light: "Light",
        dark: "Dark",
        system: "System",
      },
      language: {
        title: "Interface language",
        subtitle: "Choose your preferred language",
      },
    },
    account: {
      title: "Account",
      subtitle: "Manage your account",
      logoutTitle: "Logout",
      logoutDescription: "Logout of your account",
      logout: "Logout",
    },
  },
  validation: {
    username: {
      required: "Username is required",
      min: "Username must be at least 3 characters",
      max: "Username must not exceed 20 characters",
      pattern: "Username can only contain letters, numbers, _ and -",
    },
    password: {
      required: "Password is required",
      min: "Password must be at least 6 characters",
      max: "Password must not exceed 50 characters",
      pattern:
        "Password must contain uppercase, lowercase, numbers and special characters",
    },
    repeatPassword: {
      required: "Password confirmation is required",
      mismatch: "Passwords do not match",
    },
  },
  auth: {
    register: {
      success: {
        title: "Registration successful",
        message: "Welcome to our application!",
      },
      title: "Register",
      subtitle: "Create a new account",
      hasAccount: "Already have an account?",
      login: "Login",
      form: {
        username: "Username",
        email: "Email",
        password: "Password",
        repeatPassword: "Repeat Password",
        submit: "Register",
      },
    },
    login: {
      title: "Login",
      subtitle: "Enter your credentials",
      email: "Email",
      or: "or",
      googleLogin: "Login with Google",
      noAccount: "Don't have an account?",
      createAccount: "Create an account",
      form: {
        username: "Username",
        password: "Password",
        submit: "Login",
      },
    },
  },
  profile: {
    title: "Profile",
    subtitle: "Manage your profile",
    edit: {
      button: "Edit",
      title: "Edit Profile",
      save: "Save",
      cancel: "Cancel",
    },
    avatar: {
      upload: "Upload photo",
      remove: "Remove photo",
      dropzone: "Drop image here or click to select",
    },
    fields: {
      username: "Username",
      email: "Email",
      bio: "Bio",
      location: "Location",
      website: "Website",
    },
  },
  error: {
    notFound: {
      title: "Page Not Found",
      message: "Looks like this page is lost in space",
    },
    forbidden: {
      title: "Access Denied",
      message: "You don't have access to this page",
    },
    backHome: "Back to home",
  },
  pages: {
    home: {
      title: "Home",
      welcome: {
        morning: "Good morning",
        afternoon: "Good afternoon",
        evening: "Good evening",
        night: "Good night",
        message: "{greeting}, {name}!",
      },
      subtitle: "Find your path in IT with our courses",
      stats: {
        level: {
          title: "Level",
        },
        achievements: {
          title: "Achievements",
        },
        certificates: {
          title: "Certificates",
        },
      },
    },
    dashboard: {
      title: "Dashboard",
    },
    projects: {
      title: "Projects",
    },
    profile: {
      title: "Profile",
    },
    settings: {
      title: "Settings",
    },
    login: {
      title: "Login",
    },
    register: {
      title: "Register",
    },
  },
};
