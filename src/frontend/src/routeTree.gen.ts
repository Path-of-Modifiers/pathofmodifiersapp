/* eslint-disable */

// @ts-nocheck

// noinspection JSUnusedGlobalSymbols

// This file was automatically generated by TanStack Router.
// You should NOT make any changes in this file as it will be overwritten.
// Additionally, you should also exclude this file from your linter and/or formatter to prevent it from being checked or modified.

// Import Routes

import { Route as rootRoute } from './routes/__root'
import { Route as TermsOfUseImport } from './routes/terms-of-use'
import { Route as PrivacyPolicyImport } from './routes/privacy-policy'
import { Route as CaptchaImport } from './routes/captcha'
import { Route as AboutImport } from './routes/about'
import { Route as LayoutImport } from './routes/_layout'
import { Route as IndexImport } from './routes/index'

// Create/Update Routes

const TermsOfUseRoute = TermsOfUseImport.update({
  id: '/terms-of-use',
  path: '/terms-of-use',
  getParentRoute: () => rootRoute,
} as any)

const PrivacyPolicyRoute = PrivacyPolicyImport.update({
  id: '/privacy-policy',
  path: '/privacy-policy',
  getParentRoute: () => rootRoute,
} as any)

const CaptchaRoute = CaptchaImport.update({
  id: '/captcha',
  path: '/captcha',
  getParentRoute: () => rootRoute,
} as any)

const AboutRoute = AboutImport.update({
  id: '/about',
  path: '/about',
  getParentRoute: () => rootRoute,
} as any)

const LayoutRoute = LayoutImport.update({
  id: '/_layout',
  getParentRoute: () => rootRoute,
} as any)

const IndexRoute = IndexImport.update({
  id: '/',
  path: '/',
  getParentRoute: () => rootRoute,
} as any)

// Populate the FileRoutesByPath interface

declare module '@tanstack/react-router' {
  interface FileRoutesByPath {
    '/': {
      id: '/'
      path: '/'
      fullPath: '/'
      preLoaderRoute: typeof IndexImport
      parentRoute: typeof rootRoute
    }
    '/_layout': {
      id: '/_layout'
      path: ''
      fullPath: ''
      preLoaderRoute: typeof LayoutImport
      parentRoute: typeof rootRoute
    }
    '/about': {
      id: '/about'
      path: '/about'
      fullPath: '/about'
      preLoaderRoute: typeof AboutImport
      parentRoute: typeof rootRoute
    }
    '/captcha': {
      id: '/captcha'
      path: '/captcha'
      fullPath: '/captcha'
      preLoaderRoute: typeof CaptchaImport
      parentRoute: typeof rootRoute
    }
    '/privacy-policy': {
      id: '/privacy-policy'
      path: '/privacy-policy'
      fullPath: '/privacy-policy'
      preLoaderRoute: typeof PrivacyPolicyImport
      parentRoute: typeof rootRoute
    }
    '/terms-of-use': {
      id: '/terms-of-use'
      path: '/terms-of-use'
      fullPath: '/terms-of-use'
      preLoaderRoute: typeof TermsOfUseImport
      parentRoute: typeof rootRoute
    }
  }
}

// Create and export the route tree

export interface FileRoutesByFullPath {
  '/': typeof IndexRoute
  '': typeof LayoutRoute
  '/about': typeof AboutRoute
  '/captcha': typeof CaptchaRoute
  '/privacy-policy': typeof PrivacyPolicyRoute
  '/terms-of-use': typeof TermsOfUseRoute
}

export interface FileRoutesByTo {
  '/': typeof IndexRoute
  '': typeof LayoutRoute
  '/about': typeof AboutRoute
  '/captcha': typeof CaptchaRoute
  '/privacy-policy': typeof PrivacyPolicyRoute
  '/terms-of-use': typeof TermsOfUseRoute
}

export interface FileRoutesById {
  __root__: typeof rootRoute
  '/': typeof IndexRoute
  '/_layout': typeof LayoutRoute
  '/about': typeof AboutRoute
  '/captcha': typeof CaptchaRoute
  '/privacy-policy': typeof PrivacyPolicyRoute
  '/terms-of-use': typeof TermsOfUseRoute
}

export interface FileRouteTypes {
  fileRoutesByFullPath: FileRoutesByFullPath
  fullPaths:
    | '/'
    | ''
    | '/about'
    | '/captcha'
    | '/privacy-policy'
    | '/terms-of-use'
  fileRoutesByTo: FileRoutesByTo
  to: '/' | '' | '/about' | '/captcha' | '/privacy-policy' | '/terms-of-use'
  id:
    | '__root__'
    | '/'
    | '/_layout'
    | '/about'
    | '/captcha'
    | '/privacy-policy'
    | '/terms-of-use'
  fileRoutesById: FileRoutesById
}

export interface RootRouteChildren {
  IndexRoute: typeof IndexRoute
  LayoutRoute: typeof LayoutRoute
  AboutRoute: typeof AboutRoute
  CaptchaRoute: typeof CaptchaRoute
  PrivacyPolicyRoute: typeof PrivacyPolicyRoute
  TermsOfUseRoute: typeof TermsOfUseRoute
}

const rootRouteChildren: RootRouteChildren = {
  IndexRoute: IndexRoute,
  LayoutRoute: LayoutRoute,
  AboutRoute: AboutRoute,
  CaptchaRoute: CaptchaRoute,
  PrivacyPolicyRoute: PrivacyPolicyRoute,
  TermsOfUseRoute: TermsOfUseRoute,
}

export const routeTree = rootRoute
  ._addFileChildren(rootRouteChildren)
  ._addFileTypes<FileRouteTypes>()

/* ROUTE_MANIFEST_START
{
  "routes": {
    "__root__": {
      "filePath": "__root.tsx",
      "children": [
        "/",
        "/_layout",
        "/about",
        "/captcha",
        "/privacy-policy",
        "/terms-of-use"
      ]
    },
    "/": {
      "filePath": "index.tsx"
    },
    "/_layout": {
      "filePath": "_layout.tsx"
    },
    "/about": {
      "filePath": "about.tsx"
    },
    "/captcha": {
      "filePath": "captcha.tsx"
    },
    "/privacy-policy": {
      "filePath": "privacy-policy.tsx"
    },
    "/terms-of-use": {
      "filePath": "terms-of-use.tsx"
    }
  }
}
ROUTE_MANIFEST_END */
