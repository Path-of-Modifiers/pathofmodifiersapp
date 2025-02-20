/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_logins_login_access_session } from '../models/Body_logins_login_access_session';
import type { Token } from '../models/Token';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class LoginsService {
    /**
     * Login Access Session
     * OAuth2 compatible session login.
     * @returns Token Successful Response
     * @throws ApiError
     */
    public static loginAccessSession({
        formData,
    }: {
        formData: Body_logins_login_access_session,
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
}
