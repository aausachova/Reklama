export default {
  language: {
    select: "Выберите язык",
    ru: "Русский",
    en: "English",
  },
  common: {
    loading: "Загрузка",
    profile: "Профиль",
    logout: "Выйти",
  },
  sidebar: {
    control: "Управление",
    dashboard: "Дашборд",
    userManagement: "Управление пользователями",
    navigation: "Навигация",
    home: "Главная",
    projects: "Проекты от компаний",
    theory: "Теория",
    settings: "Настройки",
  },
  settings: {
    title: "Настройки",
    subtitle: "Управление настройками приложения и аккаунта",
    app: {
      title: "Приложение",
      subtitle: "Настройки интерфейса приложения",
      theme: {
        title: "Тема приложения",
        subtitle: "Выберите тему оформления",
        light: "Светлая",
        dark: "Темная",
        system: "Системная",
      },
      language: {
        title: "Язык интерфейса",
        subtitle: "Выберите предпочитаемый язык",
      },
    },
    account: {
      title: "Аккаунт",
      subtitle: "Управление вашим аккаунтом",
      logoutTitle: "Выйти из аккаунта",
      logoutDescription: "Выйти из учетной записи",
      logout: "Выйти",
    },
  },
  profile: {
    title: "Профиль",
    subtitle: "Управление вашим профилем",
    edit: {
      button: "Редактировать",
      title: "Редактирование профиля",
      save: "Сохранить",
      cancel: "Отменить",
    },
    avatar: {
      upload: "Загрузить фото",
      remove: "Удалить фото",
      dropzone: "Перетащите изображение сюда или нажмите для выбора",
    },
    fields: {
      username: "Имя пользователя",
      email: "Email",
      bio: "О себе",
      location: "Местоположение",
      website: "Веб-сайт",
    },
  },
  validation: {
    username: {
      required: "Имя пользователя обязательно",
      min: "Имя пользователя должно содержать минимум 3 символа",
      max: "Имя пользователя не должно превышать 20 символов",
      pattern: "Имя пользователя может содержать только буквы, цифры, _ и -",
    },
    password: {
      required: "Пароль обязателен",
      min: "Пароль должен содержать минимум 6 символов",
      max: "Пароль не должен превышать 50 символов",
      pattern:
        "Пароль должен содержать заглавные, строчные буквы, цифры и специальные символы",
    },
    repeatPassword: {
      required: "Подтверждение пароля обязательно",
      mismatch: "Пароли не совпадают",
    },
  },
  auth: {
    register: {
      success: {
        title: "Регистрация успешна",
        message: "Добро пожаловать в наше приложение!",
      },
      error: {
        title: "Ошибка регистрации",
        message: "Пожалуйста, проверьте введенные данные и попробуйте снова.",
      },
      title: "Регистрация",
      subtitle: "Создать новый аккаунт",
      hasAccount: "Уже есть аккаунт?",
      login: "Войти",
      form: {
        username: "Имя пользователя",
        email: "Email",
        password: "Пароль",
        repeatPassword: "Повторите пароль",
        submit: "Зарегистрироваться",
      },
    },
    login: {
      title: "Вход",
      subtitle: "Введите ваши данные",
      email: "Email",
      or: "или",
      googleLogin: "Войти через Google",
      noAccount: "Нет аккаунта?",
      createAccount: "Создать аккаунт",
      form: {
        username: "Имя пользователя",
        password: "Пароль",
        submit: "Войти",
      },
    },
  },
  error: {
    notFound: {
      title: "Страница не найдена",
      message: "Похоже, эта страница потерялась в пространстве",
    },
    forbidden: {
      title: "Доступ запрещен",
      message: "У вас нет доступа к этой странице",
    },
    backHome: "Вернуться на главную",
  },
  pages: {
    home: {
      title: "Главная",
      welcome: {
        morning: "Доброе утро",
        afternoon: "Добрый день",
        evening: "Добрый вечер",
        night: "Доброй ночи",
        message: "{greeting}, {name}!",
      },
      subtitle: "Найдите свой путь в IT с нашими курсами",
      stats: {
        level: {
          title: "Уровень",
        },
        achievements: {
          title: "Достижения",
        },
        certificates: {
          title: "Сертификаты",
        },
      },
    },
    dashboard: {
      title: "Дашборд",
    },
    projects: {
      title: "Проекты",
    },
    profile: {
      title: "Профиль",
    },
    settings: {
      title: "Настройки",
    },
    login: {
      title: "Вход",
    },
    register: {
      title: "Регистрация",
    },
  },
};
