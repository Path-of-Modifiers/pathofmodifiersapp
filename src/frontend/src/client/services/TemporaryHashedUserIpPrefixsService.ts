/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { HashedUserIp } from '../models/HashedUserIp';
import type { HashedUserIpCreate } from '../models/HashedUserIpCreate';
import type { HashedUserIpUpdate } from '../models/HashedUserIpUpdate';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class TemporaryHashedUserIpPrefixsService {
    /**
     * Check Temporary Hashed User Ip
     * Takes a query based on the 'TemporaryHashedUserIp' schema and retrieves
     * whether the hashed user ip is valid.
     * @returns boolean Successful Response
     * @throws ApiError
     */
    public static checkTemporaryHashedUserIp({
        ip,
    }: {
        ip: string,
    }): CancelablePromise<boolean> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/api_v1/temporary_hashed_user_ip_prefix/check/',
            query: {
                'ip': ip,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Temporary Hashed User Ip
     * Get temporary hashed user ip by key and value for "temporaryHashedUserIp".
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getTemporaryHashedUserIp({
        temporaryHashedUserIp,
    }: {
        temporaryHashedUserIp: string,
    }): CancelablePromise<(HashedUserIp | Array<HashedUserIp>)> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/temporary_hashed_user_ip_prefix/{temporaryHashedUserIp}',
            path: {
                'temporaryHashedUserIp': temporaryHashedUserIp,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update Temporary Hashed User Ip
     * Update temporary hashed user ip by key and value for "temporaryHashedUserIp".
     * @returns any Successful Response
     * @throws ApiError
     */
    public static updateTemporaryHashedUserIp({
        temporaryHashedUserIp,
        requestBody,
    }: {
        temporaryHashedUserIp: string,
        requestBody: (HashedUserIpUpdate | Array<HashedUserIpUpdate>),
    }): CancelablePromise<(HashedUserIp | Array<HashedUserIp>)> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/api_v1/temporary_hashed_user_ip_prefix/{temporaryHashedUserIp}',
            path: {
                'temporaryHashedUserIp': temporaryHashedUserIp,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Delete Temporary Hashed User Ip
     * Delete temporary hashed user ip by key and value for "temporaryHashedUserIp".
     * @returns string Successful Response
     * @throws ApiError
     */
    public static deleteTemporaryHashedUserIp({
        temporaryHashedUserIp,
    }: {
        temporaryHashedUserIp: string,
    }): CancelablePromise<string> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/api_v1/temporary_hashed_user_ip_prefix/{temporaryHashedUserIp}',
            path: {
                'temporaryHashedUserIp': temporaryHashedUserIp,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get All Temporary Hashed User Ips
     * Get all temporary hashed user ips.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getAllTemporaryHashedUserIps(): CancelablePromise<(HashedUserIp | Array<HashedUserIp>)> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/temporary_hashed_user_ip_prefix/',
        });
    }
    /**
     * Create Temporary Hashed User Ip
     * Create temporary hashed user ip.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static createTemporaryHashedUserIp({
        requestBody,
    }: {
        requestBody: (HashedUserIpCreate | Array<HashedUserIpCreate>),
    }): CancelablePromise<(HashedUserIpCreate | Array<HashedUserIpCreate>)> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/api_v1/temporary_hashed_user_ip_prefix/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
