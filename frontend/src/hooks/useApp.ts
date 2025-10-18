import router from "@/router";
import { createPinia } from "pinia";
import type { App } from "vue";
import { basicSetup } from "codemirror";
import { autocompletion } from "@codemirror/autocomplete";
import piniaPluginPersistedstate from "pinia-plugin-persistedstate";
import { i18n } from "@/i18n";
import VueCodemirror from "vue-codemirror";
import { javascript } from "@codemirror/lang-javascript";
import { oneDark } from "@codemirror/theme-one-dark";
import { standardKeymap } from "@codemirror/commands";
import { keymap } from "@codemirror/view";
export const useApp = async (app: App) => {
  const pinia = createPinia();
  pinia.use(piniaPluginPersistedstate);
  app.use(pinia);
  app.use(router);
  app.use(i18n);
  app.use(VueCodemirror, {
    autofocus: true,
    disabled: false,
    indentWithTab: true,
    tabSize: 2,
    placeholder: "Code goes here...",
    extensions: [
      javascript(),
      oneDark,
      autocompletion(),
      basicSetup,
      keymap.of([...standardKeymap]),
    ],
  });
};
