import { createI18n } from "vue-i18n";
import ru from "./locales/ru";
import en from "./locales/en";
import { useStorage, useNavigatorLanguage } from "@vueuse/core";

const defaultLocale = "ru";
const supportedLocales = ["ru", "en"] as const;

function getInitialLocale() {
  const savedLocale = useStorage("user-locale", defaultLocale);
  if (
    savedLocale.value &&
    supportedLocales.includes(
      savedLocale.value as (typeof supportedLocales)[number]
    )
  ) {
    return savedLocale.value;
  }

  const { language } = useNavigatorLanguage();
  const browserLocale = language.value?.split("-")[0];
  if (
    browserLocale &&
    supportedLocales.includes(
      browserLocale as (typeof supportedLocales)[number]
    )
  ) {
    return browserLocale;
  }

  return defaultLocale;
}

export const i18n = createI18n({
  legacy: false,
  locale: getInitialLocale(),
  fallbackLocale: defaultLocale,
  messages: {
    ru,
    en,
  },
});
