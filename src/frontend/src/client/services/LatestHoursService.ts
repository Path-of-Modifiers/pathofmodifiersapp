/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class LatestHoursService {
    /**
     * Get Latest Hours
     * Returns a dict mapping league id to the most recent hour relating to that league. Dict is empty if no currencies exist.
     *
     * Does not guarantee an entry for every league id.
     * @returns number Successful Response
     * @throws ApiError
     */
    public static getLatestHours({
        leagueIds,
    }: {
        leagueIds: Array<number>,
    }): CancelablePromise<Record<string, number>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/currency/latest_hours/',
            query: {
                'league_ids': leagueIds,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
