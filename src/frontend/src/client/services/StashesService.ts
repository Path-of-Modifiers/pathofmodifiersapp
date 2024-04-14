/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Stash } from '../models/Stash';
import type { StashCreate } from '../models/StashCreate';
import type { StashUpdate } from '../models/StashUpdate';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class StashesService {
    /**
     * Get Stash
     * Get stash by key and value for "stashId".
     *
     * Always returns one stash.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getStashApiApiV1StashStashIdGet({
        stashId,
    }: {
        stashId: string,
    }): CancelablePromise<(Stash | Array<Stash>)> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/stash/{stashId}',
            path: {
                'stashId': stashId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update Stash
     * Update a stash by key and value for "stashId".
     *
     * Returns the updated stash.
     * @returns Stash Successful Response
     * @throws ApiError
     */
    public static updateStashApiApiV1StashStashIdPut({
        stashId,
        requestBody,
    }: {
        stashId: string,
        requestBody: StashUpdate,
    }): CancelablePromise<Stash> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/api_v1/stash/{stashId}',
            path: {
                'stashId': stashId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Delete Stash
     * Delete a stash by key and value for "stashId".
     *
     * Returns a message that the stash was deleted successfully.
     * Always deletes one stash.
     * @returns string Successful Response
     * @throws ApiError
     */
    public static deleteStashApiApiV1StashStashIdDelete({
        stashId,
    }: {
        stashId: string,
    }): CancelablePromise<string> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/api_v1/stash/{stashId}',
            path: {
                'stashId': stashId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get All Stashes
     * Get all stashes.
     *
     * Returns a list of all stashes.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getAllStashesApiApiV1StashGet(): CancelablePromise<(Stash | Array<Stash>)> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/stash/',
        });
    }
    /**
     * Create Stash
     * Create one or a list of new stashes.
     *
     * Returns the created stash or list of stashes.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static createStashApiApiV1StashPost({
        requestBody,
    }: {
        requestBody: (StashCreate | Array<StashCreate>),
    }): CancelablePromise<(StashCreate | Array<StashCreate>)> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/api_v1/stash/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
