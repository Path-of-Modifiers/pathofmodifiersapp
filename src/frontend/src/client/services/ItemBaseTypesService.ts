/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { BaseType } from '../models/BaseType';
import type { ItemBaseType } from '../models/ItemBaseType';
import type { ItemBaseTypeCategory } from '../models/ItemBaseTypeCategory';
import type { ItemBaseTypeCreate } from '../models/ItemBaseTypeCreate';
import type { ItemBaseTypeSubCategory } from '../models/ItemBaseTypeSubCategory';
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
     * @returns ItemBaseType Successful Response
     * @throws ApiError
     */
    public static getItemBaseType({
        baseType,
    }: {
        baseType: string,
    }): CancelablePromise<ItemBaseType> {
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
    public static updateItemBaseType({
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
    public static deleteItemBaseType({
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
    public static getAllItemBaseTypes(): CancelablePromise<(ItemBaseType | Array<ItemBaseType>)> {
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
    /**
     * Get Base Types
     * Get all base types.
     *
     * Returns a list of all base types.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getBaseTypes(): CancelablePromise<(BaseType | Array<BaseType>)> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/itemBaseType/baseTypes/',
        });
    }
    /**
     * Get Unique Categories
     * Get all unique categories.
     *
     * Returns a list of all categories.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getUniqueCategories(): CancelablePromise<(ItemBaseTypeCategory | Array<ItemBaseTypeCategory>)> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/itemBaseType/uniqueCategories/',
        });
    }
    /**
     * Get Unique Sub Categories
     * Get all unique sub categories.
     *
     * Returns a list of all sub categories.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getUniqueSubCategories(): CancelablePromise<(ItemBaseTypeSubCategory | Array<ItemBaseTypeSubCategory>)> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/itemBaseType/uniqueSubCategories/',
        });
    }
}
