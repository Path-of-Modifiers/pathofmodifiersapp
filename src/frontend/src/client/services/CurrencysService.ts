/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Currency } from '../models/Currency';
import type { CurrencyCreate } from '../models/CurrencyCreate';
import type { CurrencyUpdate } from '../models/CurrencyUpdate';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class CurrencysService {
    /**
     * Get Currency
     * Get currency by key and value for "currencyId".
     *
     * Always returns one currency.
     * @returns Currency Successful Response
     * @throws ApiError
     */
    public static getCurrency({
        currencyId,
    }: {
        currencyId: number,
    }): CancelablePromise<Currency> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/currency/{currencyId}',
            path: {
                'currencyId': currencyId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update Currency
     * Update a currency by key and value for "currencyId".
     *
     * Returns the updated currency.
     * @returns Currency Successful Response
     * @throws ApiError
     */
    public static updateCurrency({
        currencyId,
        requestBody,
    }: {
        currencyId: number,
        requestBody: CurrencyUpdate,
    }): CancelablePromise<Currency> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/api_v1/currency/{currencyId}',
            path: {
                'currencyId': currencyId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Delete Currency
     * Delete a currency by key and value for "currencyId".
     *
     * Returns a message indicating the currency was deleted.
     * Always deletes one currency.
     * @returns string Successful Response
     * @throws ApiError
     */
    public static deleteCurrency({
        currencyId,
    }: {
        currencyId: number,
    }): CancelablePromise<string> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/api_v1/currency/{currencyId}',
            path: {
                'currencyId': currencyId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get All Currencies
     * Get all currencies.
     *
     * Returns a list of all currencies.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getAllCurrencies({
        limit,
        skip,
        sortKey,
        sortMethod,
    }: {
        limit?: (number | null),
        skip?: (number | null),
        sortKey?: (string | null),
        sortMethod?: ('asc' | 'desc' | null),
    }): CancelablePromise<(Currency | Array<Currency>)> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/currency/',
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
     * Create Currency
     * Create one or a list of currencies.
     *
     * Returns the created currency or list of currencies.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static createCurrency({
        requestBody,
        returnNothing,
    }: {
        requestBody: (CurrencyCreate | Array<CurrencyCreate>),
        returnNothing?: (boolean | null),
    }): CancelablePromise<(CurrencyCreate | Array<CurrencyCreate> | null)> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/api_v1/currency/',
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
     * Get Latest Currency Id
     * Get the latest currencyId
     *
     * Can only be used safely on an empty table or directly after an insertion.
     * @returns number Successful Response
     * @throws ApiError
     */
    public static getLatestCurrencyId(): CancelablePromise<number> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/currency/latest_currency_id/',
        });
    }
}
