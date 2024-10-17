/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { UserInCache } from '../models/UserInCache';
import type { UserPublic } from '../models/UserPublic';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class CheckTokensService {
    /**
     * Check Access Token
     * Check access token
     * @returns UserPublic Successful Response
     * @throws ApiError
     */
    public static checkAccessToken(): CancelablePromise<UserPublic> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/api_v1/check-token/check-access-token',
        });
    }
    /**
     * Check Register Token
     * Check register token
     * @returns UserInCache Successful Response
     * @throws ApiError
     */
    public static checkRegisterToken({
        registerToken,
    }: {
        registerToken: string,
    }): CancelablePromise<UserInCache> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/api_v1/check-token/check-register-token',
            query: {
                'register_token': registerToken,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Check Password Reset Token
     * Check password reset token
     * @returns UserInCache Successful Response
     * @throws ApiError
     */
    public static checkPasswordResetToken({
        passwordResetToken,
    }: {
        passwordResetToken: string,
    }): CancelablePromise<UserInCache> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/api_v1/check-token/check-password-reset-token',
            query: {
                'password_reset_token': passwordResetToken,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Check Update Me Token
     * Check register token
     * @returns UserInCache Successful Response
     * @throws ApiError
     */
    public static checkUpdateMeToken({
        updateMeToken,
    }: {
        updateMeToken: string,
    }): CancelablePromise<UserInCache> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/api_v1/check-token/check-update-me-token',
            query: {
                'update_me_token': updateMeToken,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
