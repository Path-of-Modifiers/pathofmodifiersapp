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
export class CurrenciesService {
    /**
     * Get Currency
     * Get currency by key and value for "currencyId".
     *
     * Always returns one currency.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getCurrencyApiApiV1CurrencyCurrencyIdGet({
        currencyId,
    }: {
        currencyId: string,
    }): CancelablePromise<(Currency | Array<Currency>)> {
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
    public static updateCurrencyApiApiV1CurrencyCurrencyIdPut({
        currencyId,
        requestBody,
    }: {
        currencyId: string,
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
    public static deleteCurrencyApiApiV1CurrencyCurrencyIdDelete({
        currencyId,
    }: {
        currencyId: string,
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
    public static getAllCurrenciesApiApiV1CurrencyGet(): CancelablePromise<(Currency | Array<Currency>)> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/currency/',
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
    public static createCurrencyApiApiV1CurrencyPost({
        requestBody,
    }: {
        requestBody: (CurrencyCreate | Array<CurrencyCreate>),
    }): CancelablePromise<(CurrencyCreate | Array<CurrencyCreate>)> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/api_v1/currency/',
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
    public static getLatestCurrencyIdApiApiV1CurrencyLatestCurrencyIdGet(): CancelablePromise<number> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/currency/latest_currency_id/',
        });
    }
}
