/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ItemModifier } from '../models/ItemModifier';
import type { ItemModifierCreate } from '../models/ItemModifierCreate';
import type { ItemModifierUpdate } from '../models/ItemModifierUpdate';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ItemModifiersService {
    /**
     * Get Item Modifier
     * Get item modifier or list of item modifiers by key and
     * value for optional "itemId", optional "modifierId" and optional "orderId".
     * One key must be provided.
     *
     * Returns one or a list of item modifiers.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getItemModifier({
        itemId,
        modifierId,
        orderId,
    }: {
        itemId: (number | null),
        modifierId?: (number | null),
        orderId?: (number | null),
    }): CancelablePromise<(ItemModifier | Array<ItemModifier>)> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/itemModifier/{itemId}',
            path: {
                'itemId': itemId,
            },
            query: {
                'modifierId': modifierId,
                'orderId': orderId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Delete Item Modifier
     * Delete an item modifier by key and value for "itemId", optional "modifierId" and optional "orderId".
     *
     * Can delete multiple item modifiers one one request if not modifierId or orderId is provided.
     *
     * Dominant key is "itemId".
     *
     * Returns a message that the item modifier was deleted successfully.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static deleteItemModifier({
        itemId,
        modifierId,
        orderId,
    }: {
        itemId: number,
        modifierId?: (number | null),
        orderId?: (number | null),
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/api_v1/itemModifier/{itemId}',
            path: {
                'itemId': itemId,
            },
            query: {
                'modifierId': modifierId,
                'orderId': orderId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get All Item Modifiers
     * Get all item modifiers.
     *
     * Returns a list of all item modifiers.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getAllItemModifiers({
        limit,
        skip,
        sortKey,
        sortMethod,
    }: {
        limit?: (number | null),
        skip?: (number | null),
        sortKey?: (string | null),
        sortMethod?: ('asc' | 'desc' | null),
    }): CancelablePromise<(ItemModifier | Array<ItemModifier>)> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/itemModifier/',
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
     * Create Item Modifier
     * Create one or a list item modifiers.
     *
     * Returns the created item modifier or list of item modifiers.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static createItemModifier({
        requestBody,
        returnNothing,
    }: {
        requestBody: (ItemModifierCreate | Array<ItemModifierCreate>),
        returnNothing?: (boolean | null),
    }): CancelablePromise<(ItemModifierCreate | Array<ItemModifierCreate> | null)> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/api_v1/itemModifier/',
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
    /**
     * Update Item Modifier
     * Update an item modifier by key and value for
     * "itemId", "modifierId" and "orderId".
     *
     * Returns the updated item modifier.
     * @returns ItemModifier Successful Response
     * @throws ApiError
     */
    public static updateItemModifier({
        itemId,
        modifierId,
        orderId,
        requestBody,
    }: {
        itemId: number,
        modifierId: number,
        orderId: number,
        requestBody: ItemModifierUpdate,
    }): CancelablePromise<ItemModifier> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/api_v1/itemModifier/',
            query: {
                'itemId': itemId,
                'modifierId': modifierId,
                'orderId': orderId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
