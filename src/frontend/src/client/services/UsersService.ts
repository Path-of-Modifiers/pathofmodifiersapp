/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Message } from '../models/Message';
import type { Token } from '../models/Token';
import type { UpdatePassword } from '../models/UpdatePassword';
import type { UserCreate } from '../models/UserCreate';
import type { UserPublic } from '../models/UserPublic';
import type { UserRegisterPreEmailConfirmation } from '../models/UserRegisterPreEmailConfirmation';
import type { UsersPublic } from '../models/UsersPublic';
import type { UserUpdate } from '../models/UserUpdate';
import type { UserUpdateMe } from '../models/UserUpdateMe';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class UsersService {
    /**
     * Get All
     * Retrieve all users.
     * @returns UsersPublic Successful Response
     * @throws ApiError
     */
    public static getAll({
        skip,
        limit = 100,
    }: {
        skip?: number,
        limit?: number,
    }): CancelablePromise<UsersPublic> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/user/',
            query: {
                'skip': skip,
                'limit': limit,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Create
     * Create new user.
     * @returns UserPublic Successful Response
     * @throws ApiError
     */
    public static create({
        requestBody,
    }: {
        requestBody: UserCreate,
    }): CancelablePromise<UserPublic> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/api_v1/user/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update Me Email Send Confirmation
     * Send confirmation to update own user.
     * @returns Message Successful Response
     * @throws ApiError
     */
    public static updateMeEmailSendConfirmation({
        requestBody,
    }: {
        requestBody: UserUpdateMe,
    }): CancelablePromise<Message> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/api_v1/user/update-me-email-pre-confirmation',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update Me Email Confirmation
     * Confirm update email.
     * @returns Message Successful Response
     * @throws ApiError
     */
    public static updateMeEmailConfirmation({
        requestBody,
    }: {
        requestBody: Token,
    }): CancelablePromise<Message> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/api_v1/user/update-me-email-confirmation',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update Me Username Send Confirmation
     * Send confirmation to update own user.
     * @returns Message Successful Response
     * @throws ApiError
     */
    public static updateMeUsernameSendConfirmation({
        requestBody,
    }: {
        requestBody: UserUpdateMe,
    }): CancelablePromise<Message> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/api_v1/user/update-me-username-pre-confirmation',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update Me Username Confirmation
     * Confirm update username.
     * @returns Message Successful Response
     * @throws ApiError
     */
    public static updateMeUsernameConfirmation({
        requestBody,
    }: {
        requestBody: Token,
    }): CancelablePromise<Message> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/api_v1/user/update-me-username-confirmation',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update Password Me
     * Update own password.
     * @returns Message Successful Response
     * @throws ApiError
     */
    public static updatePasswordMe({
        requestBody,
    }: {
        requestBody: UpdatePassword,
    }): CancelablePromise<Message> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/api_v1/user/me/password',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get User Me
     * Get current user.
     * @returns UserPublic Successful Response
     * @throws ApiError
     */
    public static getUserMe(): CancelablePromise<UserPublic> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/user/me',
        });
    }
    /**
     * Delete User Me
     * Delete own user.
     * @returns Message Successful Response
     * @throws ApiError
     */
    public static deleteUserMe(): CancelablePromise<Message> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/api_v1/user/me',
        });
    }
    /**
     * Register User Send Confirmation
     * Send email confirmation on user register. Account doesn't get created yet.
     * @returns Message Successful Response
     * @throws ApiError
     */
    public static registerUserSendConfirmation({
        requestBody,
    }: {
        requestBody: UserRegisterPreEmailConfirmation,
    }): CancelablePromise<Message> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/api_v1/user/signup-send-confirmation',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Register User Confirm
     * Confirm new user without the need to be logged in. Requires email confirmation.
     * @returns Message Successful Response
     * @throws ApiError
     */
    public static registerUserConfirm({
        requestBody,
    }: {
        requestBody: Token,
    }): CancelablePromise<Message> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/api_v1/user/signup',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get User By Id
     * Get a specific user by id.
     * @returns UserPublic Successful Response
     * @throws ApiError
     */
    public static getUserById({
        userId,
    }: {
        userId: string,
    }): CancelablePromise<UserPublic> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/user/{user_id}',
            path: {
                'user_id': userId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update User
     * Update a user.
     * @returns UserPublic Successful Response
     * @throws ApiError
     */
    public static updateUser({
        userId,
        requestBody,
    }: {
        userId: string,
        requestBody: UserUpdate,
    }): CancelablePromise<UserPublic> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/api_v1/user/{user_id}',
            path: {
                'user_id': userId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Delete User
     * Delete a user.
     * @returns Message Successful Response
     * @throws ApiError
     */
    public static deleteUser({
        userId,
    }: {
        userId: string,
    }): CancelablePromise<Message> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/api_v1/user/{user_id}',
            path: {
                'user_id': userId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Change Is Active User
     * Change activity to current user.
     * @returns Message Successful Response
     * @throws ApiError
     */
    public static changeIsActiveUser({
        userId,
        isActive,
    }: {
        userId: string,
        isActive: boolean,
    }): CancelablePromise<Message> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/api_v1/user/is_active/{user_id}',
            path: {
                'user_id': userId,
            },
            query: {
                'is_active': isActive,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Set Rate Limit Tier User
     * Set rate limit tier to current user.
     * @returns Message Successful Response
     * @throws ApiError
     */
    public static setRateLimitTierUser({
        userId,
        rateLimitTier,
    }: {
        userId: string,
        rateLimitTier: number,
    }): CancelablePromise<Message> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/api_v1/user/rate_limit_tier/{user_id}',
            path: {
                'user_id': userId,
            },
            query: {
                'rate_limit_tier': rateLimitTier,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
