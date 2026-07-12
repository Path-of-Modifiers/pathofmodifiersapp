/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class LatestHourService {
    /**
     * Get Latest Hour
     * Return -1 if database is empty
     * @returns number Successful Response
     * @throws ApiError
     */
    public static getLatestHour(): CancelablePromise<number> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/currency/latest_hour/',
        });
    }
}
