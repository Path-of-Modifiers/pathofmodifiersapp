// Contains env variables imported from .env in /frontend module

export const VITE_API_URL = import.meta.env.VITE_API_URL;
export const TURNSTILE_SITE_KEY = import.meta.env.VITE_APP_TURNSTILE_SITE_KEY;
export const LEAGUE_LAUNCH_TIME = import.meta.env.VITE_APP_LEAGUE_LAUNCH_TIME;

export const DEFAULT_LEAGUES = (import.meta.env.VITE_APP_DEFAULT_LEAGUES).split("|") as Array<string>;
export const ADDITIONAL_LEAGUES = (import.meta.env.VITE_APP_ADDITIONAL_LEAGUES).split("|") as Array<string>;
