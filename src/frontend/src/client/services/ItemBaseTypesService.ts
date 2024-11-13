/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ItemBaseType } from '../models/ItemBaseType';
import type { ItemBaseTypeCreate } from '../models/ItemBaseTypeCreate';
import type { ItemBaseTypeUpdate } from '../models/ItemBaseTypeUpdate';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ItemBaseTypesService {
    /**
     * Get Item Base Type
     * Get item base type by key and value for "itemBaseTypeId".
     *
     * Always returns one item base type.
     * @returns ItemBaseType Successful Response
     * @throws ApiError
     */
    public static getItemBaseType({
        itemBaseTypeId,
    }: {
        itemBaseTypeId: string,
    }): CancelablePromise<ItemBaseType> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/itemBaseType/{itemBaseTypeId}',
            path: {
                'itemBaseTypeId': itemBaseTypeId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update Item Base Type
     * Update an item base type by key and value for "itemBaseTypeId".
     *
     * Returns the updated item base type.
     * @returns ItemBaseType Successful Response
     * @throws ApiError
     */
    public static updateItemBaseType({
        itemBaseTypeId,
        requestBody,
    }: {
        itemBaseTypeId: number,
        requestBody: ItemBaseTypeUpdate,
    }): CancelablePromise<ItemBaseType> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/api_v1/itemBaseType/{itemBaseTypeId}',
            path: {
                'itemBaseTypeId': itemBaseTypeId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Delete Item Base Type
     * Delete an item base type by key and value for "itemBaseTypeId".
     *
     * Returns a message that the item base type was deleted successfully.
     * Always deletes one item base type.
     * @returns string Successful Response
     * @throws ApiError
     */
    public static deleteItemBaseType({
        itemBaseTypeId,
    }: {
        itemBaseTypeId: number,
    }): CancelablePromise<string> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/api_v1/itemBaseType/{itemBaseTypeId}',
            path: {
                'itemBaseTypeId': itemBaseTypeId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get All Item Base Types
     * Get all item base types.
     *
     * Returns a list of all item base types.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getAllItemBaseTypes({
        limit,
        skip,
        sortKey,
        sortMethod,
    }: {
        limit?: (number | null),
        skip?: (number | null),
        sortKey?: (string | null),
        sortMethod?: ('asc' | 'desc' | null),
    }): CancelablePromise<(ItemBaseType | Array<ItemBaseType>)> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/itemBaseType/',
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
     * Create Item Base Type
     * Create one or a list of new item base types.
     *
     * Returns the created item base type or list of item base types.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static createItemBaseType({
        requestBody,
        onDuplicatePkeyDoNothing,
        returnNothing,
    }: {
        requestBody: (ItemBaseTypeCreate | Array<ItemBaseTypeCreate>),
        onDuplicatePkeyDoNothing?: (boolean | null),
        returnNothing?: (boolean | null),
    }): CancelablePromise<(ItemBaseTypeCreate | Array<ItemBaseTypeCreate> | null)> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/api_v1/itemBaseType/',
            query: {
                'on_duplicate_pkey_do_nothing': onDuplicatePkeyDoNothing,
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
