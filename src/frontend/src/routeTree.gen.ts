/* prettier-ignore-start */

/* eslint-disable */

// @ts-nocheck

// noinspection JSUnusedGlobalSymbols

// This file is auto-generated by TanStack Router

// Import Routes

import { Route as rootRoute } from './routes/__root'
import { Route as UserNotActivatedImport } from './routes/user-not-activated'
import { Route as UpdateUserEmailImport } from './routes/update-user-email'
import { Route as SignupImport } from './routes/signup'
import { Route as ResetPasswordImport } from './routes/reset-password'
import { Route as RecoverPasswordImport } from './routes/recover-password'
import { Route as LoginImport } from './routes/login'
import { Route as CaptchaImport } from './routes/captcha'
import { Route as ActivateAccountImport } from './routes/activate-account'
import { Route as LayoutImport } from './routes/_layout'
import { Route as LayoutIndexImport } from './routes/_layout/index'
import { Route as LayoutTermsOfUseImport } from './routes/_layout/terms-of-use'
import { Route as LayoutSettingsImport } from './routes/_layout/settings'
import { Route as LayoutPrivacyPolicyImport } from './routes/_layout/privacy-policy'
import { Route as LayoutAboutImport } from './routes/_layout/about'

// Create/Update Routes

const UserNotActivatedRoute = UserNotActivatedImport.update({
  path: '/user-not-activated',
  getParentRoute: () => rootRoute,
} as any)

const UpdateUserEmailRoute = UpdateUserEmailImport.update({
  path: '/update-user-email',
  getParentRoute: () => rootRoute,
} as any)

const SignupRoute = SignupImport.update({
  path: '/signup',
  getParentRoute: () => rootRoute,
} as any)

const ResetPasswordRoute = ResetPasswordImport.update({
  path: '/reset-password',
  getParentRoute: () => rootRoute,
} as any)

const RecoverPasswordRoute = RecoverPasswordImport.update({
  path: '/recover-password',
  getParentRoute: () => rootRoute,
} as any)

const LoginRoute = LoginImport.update({
  path: '/login',
  getParentRoute: () => rootRoute,
} as any)

const CaptchaRoute = CaptchaImport.update({
  path: '/captcha',
  getParentRoute: () => rootRoute,
} as any)

const ActivateAccountRoute = ActivateAccountImport.update({
  path: '/activate-account',
  getParentRoute: () => rootRoute,
} as any)

const LayoutRoute = LayoutImport.update({
  id: '/_layout',
  getParentRoute: () => rootRoute,
} as any)

const LayoutIndexRoute = LayoutIndexImport.update({
  path: '/',
  getParentRoute: () => LayoutRoute,
} as any)

const LayoutTermsOfUseRoute = LayoutTermsOfUseImport.update({
  path: '/terms-of-use',
  getParentRoute: () => LayoutRoute,
} as any)

const LayoutSettingsRoute = LayoutSettingsImport.update({
  path: '/settings',
  getParentRoute: () => LayoutRoute,
} as any)

const LayoutPrivacyPolicyRoute = LayoutPrivacyPolicyImport.update({
  path: '/privacy-policy',
  getParentRoute: () => LayoutRoute,
} as any)

const LayoutAboutRoute = LayoutAboutImport.update({
  path: '/about',
  getParentRoute: () => LayoutRoute,
} as any)

// Populate the FileRoutesByPath interface

declare module '@tanstack/react-router' {
  interface FileRoutesByPath {
    '/_layout': {
      preLoaderRoute: typeof LayoutImport
      parentRoute: typeof rootRoute
    }
    '/activate-account': {
      preLoaderRoute: typeof ActivateAccountImport
      parentRoute: typeof rootRoute
    }
    '/captcha': {
      preLoaderRoute: typeof CaptchaImport
      parentRoute: typeof rootRoute
    }
    '/login': {
      preLoaderRoute: typeof LoginImport
      parentRoute: typeof rootRoute
    }
    '/recover-password': {
      preLoaderRoute: typeof RecoverPasswordImport
      parentRoute: typeof rootRoute
    }
    '/reset-password': {
      preLoaderRoute: typeof ResetPasswordImport
      parentRoute: typeof rootRoute
    }
    '/signup': {
      preLoaderRoute: typeof SignupImport
      parentRoute: typeof rootRoute
    }
    '/update-user-email': {
      preLoaderRoute: typeof UpdateUserEmailImport
      parentRoute: typeof rootRoute
    }
    '/user-not-activated': {
      preLoaderRoute: typeof UserNotActivatedImport
      parentRoute: typeof rootRoute
    }
    '/_layout/about': {
      preLoaderRoute: typeof LayoutAboutImport
      parentRoute: typeof LayoutImport
    }
    '/_layout/privacy-policy': {
      preLoaderRoute: typeof LayoutPrivacyPolicyImport
      parentRoute: typeof LayoutImport
    }
    '/_layout/settings': {
      preLoaderRoute: typeof LayoutSettingsImport
      parentRoute: typeof LayoutImport
    }
    '/_layout/terms-of-use': {
      preLoaderRoute: typeof LayoutTermsOfUseImport
      parentRoute: typeof LayoutImport
    }
    '/_layout/': {
      preLoaderRoute: typeof LayoutIndexImport
      parentRoute: typeof LayoutImport
    }
  }
}

// Create and export the route tree

export const routeTree = rootRoute.addChildren([
  LayoutRoute.addChildren([
    LayoutAboutRoute,
    LayoutPrivacyPolicyRoute,
    LayoutSettingsRoute,
    LayoutTermsOfUseRoute,
    LayoutIndexRoute,
  ]),
  ActivateAccountRoute,
  CaptchaRoute,
  LoginRoute,
  RecoverPasswordRoute,
  ResetPasswordRoute,
  SignupRoute,
  UpdateUserEmailRoute,
  UserNotActivatedRoute,
])

/* prettier-ignore-end */
