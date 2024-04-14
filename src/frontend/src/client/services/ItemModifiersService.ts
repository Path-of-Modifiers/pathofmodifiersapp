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
     * value for "itemId", optional "modifierId" and optional "position".
     *
     * Dominant key is "itemId".
     *
     * Returns one or a list of item modifiers.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getItemModifierApiApiV1ItemModifierItemIdGet({
        itemId,
        modifierId,
        position,
    }: {
        itemId: number,
        modifierId?: (number | null),
        position?: (number | null),
    }): CancelablePromise<(ItemModifier | Array<ItemModifier>)> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/itemModifier/{itemId}',
            path: {
                'itemId': itemId,
            },
            query: {
                'modifierId': modifierId,
                'position': position,
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
    public static getAllItemModifiersApiApiV1ItemModifierGet(): CancelablePromise<(ItemModifier | Array<ItemModifier>)> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/itemModifier/',
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
    public static createItemModifierApiApiV1ItemModifierPost({
        requestBody,
    }: {
        requestBody: (ItemModifierCreate | Array<ItemModifierCreate>),
    }): CancelablePromise<(ItemModifierCreate | Array<ItemModifierCreate>)> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/api_v1/itemModifier/',
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
     * "itemId", optional "modifierId" and optional "position".
     *
     * Dominant key is "itemId".
     *
     * Returns the updated item modifier.
     * @returns ItemModifier Successful Response
     * @throws ApiError
     */
    public static updateItemModifierApiApiV1ItemModifierItemItemIdPut({
        itemId,
        modifierId,
        position,
        requestBody,
    }: {
        itemId: number,
        modifierId: number,
        position: number,
        requestBody: ItemModifierUpdate,
    }): CancelablePromise<ItemModifier> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/api_v1/itemModifier/item={itemId}',
            path: {
                'itemId': itemId,
            },
            query: {
                'modifierId': modifierId,
                'position': position,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Delete Item Modifier
     * Delete an item modifier by key and value for
     * "itemId", optional "modifierId" and optional "position".
     *
     * Dominant key is "itemId".
     *
     * Returns a message that the item modifier was deleted successfully.
     * Always deletes one item modifier.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static deleteItemModifierApiApiV1ItemModifierItemItemIdDelete({
        itemId,
        modifierId,
        position,
    }: {
        itemId: number,
        modifierId?: (number | null),
        position?: (number | null),
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/api_v1/itemModifier/item={itemId}',
            path: {
                'itemId': itemId,
            },
            query: {
                'modifierId': modifierId,
                'position': position,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
