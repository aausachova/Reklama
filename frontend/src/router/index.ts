import { createWebHistory, createRouter } from "vue-router";
import type { RouteRecordRaw } from "vue-router";

import HomePage from "@/pages/HomePage.vue";
import SettingsPage from "@/pages/SettingsPage.vue";

import DefaultLayout from "@/layouts/DefaultLayout.vue";
import GuestLayout from "@/layouts/GuestLayout.vue";
import { authMiddleware } from "@/middleware/authMiddleware";
import { titleMiddleware } from "@/middleware/titleMiddleware";
import { roleMiddleware } from "@/middleware/roleMiddleware";

import EventDetailsPage from "@/pages/events/[id].vue";
import VacansyPage from "@/pages/VacansyPage.vue";
import VacansyCreatePage from "@/pages/VacansyCreatePage.vue";
import CandidatesPage from "@/pages/CandidatesPage.vue";

const routes: RouteRecordRaw[] = [
  {
    path: "/",
    component: DefaultLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: "",
        redirect: { name: "database" },
      },
      {
        path: "/database",
        name: "database",
        meta: { title: "pages.database.title" },
        component: HomePage,
      },
      {
        path: "/vacansy",
        name: "vacansy", 
        component: VacansyPage,
      },
      {
        path:"/candidate",
        name: "candidate",
        component: CandidatesPage,
      },
      {
         path: "/vacancies/create",
        meta: { title: "Вакансии" },
        component: VacansyCreatePage,
        props: true,
      },
      {
        path: "/events/:id",
        name: "event-details",
        meta: { title: "Детали мероприятия" },
        component: EventDetailsPage,
      },
      {
        path: "/achievements",
        name: "achievements",
        meta: { title: "pages.achievements.title" },
        component: HomePage,
      },
      {
        path: "/projects",
        name: "projects",
        meta: { title: "pages.projects.title" },
        component: () => import("@/pages/ProjectsPage.vue"),
      },
      {
        path: "/dashboard",
        name: "dashboard",
        meta: {
          title: "pages.dashboard.title",
          //roles: ["admin"],
        },
        component: () => import("@/pages/DashboardPage.vue"),
      },
      {
        path: "/users",
        name: "users",
        meta: {
          title: "pages.users.title",
        },
        component: () => import("@/pages/UsersPage.vue"),
      },
      {
        path: "/profile",
        name: "profile",
        meta: { title: "pages.profile.title" },
        component: () => import("@/pages/ProfilePage.vue"),
      },
      {
        path: "/settings",
        name: "settings",
        meta: { title: "pages.settings.title" },
        component: SettingsPage,
      },
      {
        path: "/chat",
        name: "chat",
        meta: {
          title: "Чаты",
          requiresAuth: true,
        },
        component: () => import("@/pages/ChatPage.vue"),
      },
    ],
  },
  {
    path: "/auth",
    component: GuestLayout,
    meta: { requiresGuest: true },
    children: [
      {
        path: "",
        redirect: { name: "login" },
      },
      {
        path: "login",
        name: "login",
        meta: { title: "pages.login.title" },
        component: () => import("@/pages/LoginPage.vue"),
      },
      {
        path: "register",
        name: "register",
        meta: { title: "pages.register.title" },
        component: () => import("@/pages/RegistrationPage.vue"),
      },
    ],
  },
  {
    path: "/403",
    name: "403",
    component: () => import("@/pages/NotFoundPage.vue"),
    meta: { title: "error.forbidden.title" },
    props: {
      errorCode: "403",
      errorMessage: "error.forbidden.message",
      animationSrc: "/ReqectedAnimation.tgs",
    },
  },
  {
    path: "/:pathMatch(.*)*",
    name: "not-found",
    component: () => import("@/pages/NotFoundPage.vue"),
    meta: { title: "error.notFound.title" },
    props: {
      errorCode: "404",
      errorMessage: "error.notFound.message",
      animationSrc: "/DuckNothingFound.tgs",
    },
  },
];

const router = createRouter({
  history: createWebHistory(),
  scrollBehavior(_to, _from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    }
    return { top: 0 };
  },
  routes,
});

router.beforeEach(authMiddleware);
router.beforeEach(roleMiddleware);
router.beforeEach(titleMiddleware);
export default router;
