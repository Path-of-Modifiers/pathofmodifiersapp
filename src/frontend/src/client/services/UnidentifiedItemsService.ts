/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { UnidentifiedItem } from '../models/UnidentifiedItem';
import type { UnidentifiedItemCreate } from '../models/UnidentifiedItemCreate';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class UnidentifiedItemsService {
    /**
     * Get Latest Item Id
     * Get the latest "itemId"
     *
     * Can only be used safely on an empty table or directly after an insertion.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getLatestItemId(): CancelablePromise<(number | null)> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/unidentifiedItem/latest_item_id/',
        });
    }
    /**
     * Get All Items
     * Get all items.
     *
     * Returns a list of all items.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getAllItems({
        limit,
        skip,
        sortKey,
        sortMethod,
    }: {
        limit?: (number | null),
        skip?: (number | null),
        sortKey?: (string | null),
        sortMethod?: ('asc' | 'desc' | null),
    }): CancelablePromise<(UnidentifiedItem | Array<UnidentifiedItem>)> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/unidentifiedItem/',
            query: {
                'limit': limit,
                'skip': skip,
                'sort_key': sortKey,
                'sort_method': sortMethod,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Create Item
     * Create one or a list of new items.
     *
     * Returns the created item or list of items.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static createItem({
        requestBody,
        returnNothing,
    }: {
        requestBody: (UnidentifiedItemCreate | Array<UnidentifiedItemCreate>),
        returnNothing?: (boolean | null),
    }): CancelablePromise<(UnidentifiedItemCreate | Array<UnidentifiedItemCreate> | null)> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/api_v1/unidentifiedItem/',
            query: {
                'return_nothing': returnNothing,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
