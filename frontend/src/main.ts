import { createApp } from "vue";
import "./index.css";
import "./assets/styles/global.css";
import App from "./App.vue";
import { useApp } from "./hooks/useApp";

const app = createApp(App);
useApp(app);

app.mount("#app");
