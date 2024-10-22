/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Item } from '../models/Item';
import type { ItemCreate } from '../models/ItemCreate';
import type { ItemUpdate } from '../models/ItemUpdate';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ItemsService {
    /**
     * Get Item
     * Get item by key and value for "itemId".
     *
     * Always returns one item.
     * @returns Item Successful Response
     * @throws ApiError
     */
    public static getItem({
        itemId,
    }: {
        itemId: number,
    }): CancelablePromise<Item> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/item/{itemId}',
            path: {
                'itemId': itemId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update Item
     * Update an item by key and value for "itemId".
     *
     * Returns the updated item.
     * @returns Item Successful Response
     * @throws ApiError
     */
    public static updateItem({
        itemId,
        requestBody,
    }: {
        itemId: number,
        requestBody: ItemUpdate,
    }): CancelablePromise<Item> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/api_v1/item/{itemId}',
            path: {
                'itemId': itemId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Delete Item
     * Delete an item by key and value for "itemId".
     *
     * Returns a message indicating the item was deleted.
     * Always deletes one item.
     * @returns string Successful Response
     * @throws ApiError
     */
    public static deleteItem({
        itemId,
    }: {
        itemId: number,
    }): CancelablePromise<string> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/api_v1/item/{itemId}',
            path: {
                'itemId': itemId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
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
            url: '/api/api_v1/item/latest_item_id/',
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
    }): CancelablePromise<(Item | Array<Item>)> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/item/',
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
        requestBody: (ItemCreate | Array<ItemCreate>),
        returnNothing?: (boolean | null),
    }): CancelablePromise<(ItemCreate | Array<ItemCreate> | null)> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/api_v1/item/',
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
