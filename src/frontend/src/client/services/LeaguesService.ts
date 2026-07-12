/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { League } from '../models/League';
import type { LeagueCreate } from '../models/LeagueCreate';
import type { LeagueUpdate } from '../models/LeagueUpdate';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class LeaguesService {
    /**
     * Get League
     * Get league by key and value for "leagueId".
     *
     * Always returns one league.
     * @returns League Successful Response
     * @throws ApiError
     */
    public static getLeague({
        leagueId,
    }: {
        leagueId: number,
    }): CancelablePromise<League> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/league/{leagueId}',
            path: {
                'leagueId': leagueId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update Modifier
     * Update a league by key and value for "leagueId"
     *
     * Returns the updated league.
     * @returns League Successful Response
     * @throws ApiError
     */
    public static updateModifier({
        leagueId,
        requestBody,
    }: {
        leagueId: number,
        requestBody: LeagueUpdate,
    }): CancelablePromise<League> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/api_v1/league/{leagueId}',
            path: {
                'leagueId': leagueId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get All Leagues
     * Get all leagues.
     *
     * Returns a list of all leagues.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getAllLeagues({
        limit,
        skip,
        sortKey,
        sortMethod,
    }: {
        limit?: (number | null),
        skip?: (number | null),
        sortKey?: (string | null),
        sortMethod?: ('asc' | 'desc' | null),
    }): CancelablePromise<(League | Array<League>)> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/league/',
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
     * Create League
     * Create one or a list of new leagues.
     *
     * Returns the created league or list of leagues.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static createLeague({
        requestBody,
        returnNothing,
    }: {
        requestBody: (LeagueCreate | Array<LeagueCreate>),
        returnNothing?: (boolean | null),
    }): CancelablePromise<(LeagueCreate | Array<LeagueCreate> | null)> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/api_v1/league/',
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
     * Get Active Leagues
     * Get leagues that are still valid/active
     *
     * Always returns a list, but it may be empty.
     * @returns League Successful Response
     * @throws ApiError
     */
    public static getActiveLeagues(): CancelablePromise<Array<League>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/league/active_league/',
        });
    }
}
