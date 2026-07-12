/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Currency } from '../models/Currency';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class LatestCurrenciesService {
    /**
     * Get Latest Currencies
     * Returns a list of the latest currencies, which all share the same `createdHoursSinceLaunch` as defined by `latest_hour` endpoint.
     * @returns Currency Successful Response
     * @throws ApiError
     */
    public static getLatestCurrencies(): CancelablePromise<Array<Currency>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/currency/latest_currencies/',
        });
    }
}
