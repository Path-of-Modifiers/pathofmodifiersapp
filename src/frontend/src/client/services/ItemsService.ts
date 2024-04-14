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
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getItemApiApiV1ItemItemIdGet({
        itemId,
    }: {
        itemId: string,
    }): CancelablePromise<(Item | Array<Item>)> {
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
    public static updateItemApiApiV1ItemItemIdPut({
        itemId,
        requestBody,
    }: {
        itemId: string,
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
    public static deleteItemApiApiV1ItemItemIdDelete({
        itemId,
    }: {
        itemId: string,
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
     * Get the latest itemId
     *
     * Can only be used safely on an empty table or directly after an insertion.
     * @returns number Successful Response
     * @throws ApiError
     */
    public static getLatestItemIdApiApiV1ItemLatestItemIdGet(): CancelablePromise<number> {
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
    public static getAllItemsApiApiV1ItemGet(): CancelablePromise<(Item | Array<Item>)> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/item/',
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
    public static createItemApiApiV1ItemPost({
        requestBody,
    }: {
        requestBody: (ItemCreate | Array<ItemCreate>),
    }): CancelablePromise<(ItemCreate | Array<ItemCreate>)> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/api_v1/item/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
