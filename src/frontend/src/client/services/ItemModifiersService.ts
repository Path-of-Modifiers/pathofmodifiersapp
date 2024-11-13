/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ItemModifier } from '../models/ItemModifier';
import type { ItemModifierCreate } from '../models/ItemModifierCreate';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ItemModifiersService {
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
}
