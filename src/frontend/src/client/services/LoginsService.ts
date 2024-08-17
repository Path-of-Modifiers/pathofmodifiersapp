/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_logins_login_access_token } from '../models/Body_logins_login_access_token';
import type { Message } from '../models/Message';
import type { NewPassword } from '../models/NewPassword';
import type { Token } from '../models/Token';
import type { UserPublic } from '../models/UserPublic';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class LoginsService {
    /**
     * Login Access Token
     * OAuth2 compatible token login, get an access token for future requests
     * @returns Token Successful Response
     * @throws ApiError
     */
    public static loginAccessToken({
        formData,
    }: {
        formData: Body_logins_login_access_token,
    }): CancelablePromise<Token> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/api_v1/login/access-token',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Test Token
     * Test access token
     * @returns UserPublic Successful Response
     * @throws ApiError
     */
    public static testToken(): CancelablePromise<UserPublic> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/api_v1/login/test-token',
        });
    }
    /**
     * Recover Password
     * Password Recovery
     * @returns Message Successful Response
     * @throws ApiError
     */
    public static recoverPassword({
        username,
        email,
    }: {
        username?: (string | null),
        email?: (string | null),
    }): CancelablePromise<Message> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/api_v1/login/password-recovery/',
            query: {
                'username': username,
                'email': email,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Reset Password
     * Reset password
     * @returns Message Successful Response
     * @throws ApiError
     */
    public static resetPassword({
        requestBody,
    }: {
        requestBody: NewPassword,
    }): CancelablePromise<Message> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/api_v1/login/reset-password/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Recover Password Html Content
     * HTML Content for Password Recovery
     * @returns string Successful Response
     * @throws ApiError
     */
    public static recoverPasswordHtmlContent({
        email,
    }: {
        email: string,
    }): CancelablePromise<string> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/api_v1/login/password-recovery-html-content/{email}',
            path: {
                'email': email,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}