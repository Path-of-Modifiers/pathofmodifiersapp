# Testing the backend API

This document describes tests, how to run them and what the different modules are.

## Main test modules

The tests separated in two main modules: `test_real_env` and `test_simulating_env`. The `test_real_env` module tests the api environment and database that's currently in use. The `test_simulating_env` tests a simulated api and environment that are copies of the real api environment.

The purpose of `test_real_env` is to perform tests on accumulated data gathered in a more similar to production scenario. In `backend_api/app/api/routes` you will find a `test` route that this module uses to insert dummy data.

The purpose of `test_simulating_env` is to check if base case usage of all the routes are correct. These are fully automatic tests done with [pytest](https://docs.pytest.org/en/stable/).

## What is covered and how?

We test base cases and some outliers for all the crud and route models.

The routes for `account`, `currency`, `item_base_type`, `item_modifier`, `item`, `modifier` and `stash` all inherit from the same generalized crud `base` class. These uses the same test files and classes with specified fixtures for each route and crud.

There are also specialized tests for routes that doesn't use the crud `base` class. These are `login`, `user`, `plot` and `turnstile`. It doesn't make sence to inherit a base test class with these routes.

## How to run the tests?

Please see [Development documentation - Run tests](https://github.com/Path-of-Modifiers/pathofmodifiersapp/blob/main/development.md#run-tests).
