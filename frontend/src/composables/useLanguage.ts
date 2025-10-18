import { useI18n } from "vue-i18n";
import { useStorage } from "@vueuse/core";
import { computed } from "vue";

export const SUPPORTED_LOCALES = ["ru", "en"] as const;
export type SupportedLocale = (typeof SUPPORTED_LOCALES)[number];

export function useLanguage() {
  const { locale } = useI18n();
  const storedLocale = useStorage<SupportedLocale>("user-locale", "ru");

  const currentLocale = computed({
    get() {
      return storedLocale.value;
    },
    set(newLocale: SupportedLocale) {
      storedLocale.value = newLocale;
      locale.value = newLocale;
    },
  });

  return {
    currentLocale,
    supportedLocales: SUPPORTED_LOCALES,
  };
}
