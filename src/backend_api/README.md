# Path of Modifiers API documentation

This document describes and illustrates more advanced features in the API.

- [Authentication](#authentication)
- [Rate limit](#rate-limit)

Description of each route is documented in [Path of Modifiers API Docs](https://pathofmodifiers.com/docs)

## Authentication

### User session authentication

The routes produces authentication outcomes based on user roles, privileges and scope. There are two main categories for routes required during authentication:
`User required` and `Non-user required` routes. Inside `User required` routes, there are two sub categories if a user is `Superuser` or `Not superuser`.

To determine if a route is `User required` or not, the hints are to look at the dependencies of the route. Dependencies are either provided in the route decoration `@route`
or inside the route arguments with a dependency type, like `current_user: CurrentUser`.

The figure below illustrates a general action path of authenticating a user session.

![alt text](https://i.ibb.co/FJcmNpf/authentication-login-example.png)

### Different user cache token types

Async Redis cache is used to cache different types of tokens during user authentication processes. Inside module `app/core/cache/user_cache` the different cache token types are specified.

Using different types of tokens provides versatility to how long different tokens last and multiple processes happening concurrently by a user.

To see how it works, check out the `app/core/cache/user_cache` module.

## Rate limit

Uses the same Async Redis cache to track rate limit between users. It is the same cache as storing user cache tokens.

There are two rate limitting modules: `SlowAPI rate limitter` and our own custom rate limitter.

The reason we use two different modules, are due to the complexity of the rate limits in our application. Slow API has the base functionality to rate limit most of our routes. It is easy to use and requires just a decorator when applying to a route. An important thing that SlowAPI doesn't support are rate limitting based on user roles. Since most of our routes doesn't need this functionality, we use the basic SlowAPI limitter for these routes. The `/plot` route requires rate limitting based on user roles, if the user has higher or lower privileges to do an amount of requests in a time frame. A more complex custom rate limitter is used to limit this route based on the user role.

Check out module `app/core/rate_limit` to see how rate limit is set up in the application.
