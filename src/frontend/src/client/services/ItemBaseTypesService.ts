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
     * Get item base type by key and value for "baseType".
     *
     * Always returns one item base type.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getItemBaseTypeApiApiV1ItemBaseTypeBaseTypeGet({
        baseType,
    }: {
        baseType: string,
    }): CancelablePromise<(ItemBaseType | Array<ItemBaseType>)> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/itemBaseType/{baseType}',
            path: {
                'baseType': baseType,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update Item Base Type
     * Update an item base type by key and value for "baseType".
     *
     * Returns the updated item base type.
     * @returns ItemBaseType Successful Response
     * @throws ApiError
     */
    public static updateItemBaseTypeApiApiV1ItemBaseTypeBaseTypePut({
        baseType,
        requestBody,
    }: {
        baseType: string,
        requestBody: ItemBaseTypeUpdate,
    }): CancelablePromise<ItemBaseType> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/api_v1/itemBaseType/{baseType}',
            path: {
                'baseType': baseType,
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
     * Delete an item base type by key and value for "baseType".
     *
     * Returns a message that the item base type was deleted successfully.
     * Always deletes one item base type.
     * @returns string Successful Response
     * @throws ApiError
     */
    public static deleteItemBaseTypeApiApiV1ItemBaseTypeBaseTypeDelete({
        baseType,
    }: {
        baseType: string,
    }): CancelablePromise<string> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/api_v1/itemBaseType/{baseType}',
            path: {
                'baseType': baseType,
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
    public static getAllItemBaseTypesApiApiV1ItemBaseTypeGet(): CancelablePromise<(ItemBaseType | Array<ItemBaseType>)> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/itemBaseType/',
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
    public static createItemBaseTypeApiApiV1ItemBaseTypePost({
        requestBody,
    }: {
        requestBody: (ItemBaseTypeCreate | Array<ItemBaseTypeCreate>),
    }): CancelablePromise<(ItemBaseTypeCreate | Array<ItemBaseTypeCreate>)> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/api_v1/itemBaseType/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
