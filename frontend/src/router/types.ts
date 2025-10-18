import type { Roles } from "@/types/auth";

interface CustomRouteMeta {
  title?: string;
  requiresAuth?: boolean;
  requiresGuest?: boolean;
  roles?: Roles[];
}

declare module "vue-router" {
  interface RouteMeta extends CustomRouteMeta {}
}

export type { CustomRouteMeta };
