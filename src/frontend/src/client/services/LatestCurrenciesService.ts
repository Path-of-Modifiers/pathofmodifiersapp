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
     * Returns a dict mapping league id to most recent currencies relating to that league. Dict is empty if no currencies exist.
     *
     * Does not guarantee an entry for every league id.
     * @returns Currency Successful Response
     * @throws ApiError
     */
    public static getLatestCurrencies({
        leagueIds,
    }: {
        leagueIds: Array<number>,
    }): CancelablePromise<Record<string, Array<Currency>>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/currency/latest_currencies/',
            query: {
                'league_ids': leagueIds,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
