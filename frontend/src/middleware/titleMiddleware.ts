import { useTitle } from "@vueuse/core";
import type { RouteLocationNormalized } from "vue-router";
import { i18n } from "@/i18n";

export function titleMiddleware(
  to: RouteLocationNormalized,
  _: RouteLocationNormalized
) {
  const { t } = i18n.global;
  const title = to.meta.title
    ? `${t(to.meta.title as string)} - My App`
    : "My App";
  useTitle(title);
}
