/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { PlotData } from '../models/PlotData';
import type { PlotQuery } from '../models/PlotQuery';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class PlottingService {
    /**
     * Get Plot Data
     * Takes a query based on the 'PlotQuery' schema and retrieves data
     * to be used for plotting in the format of the 'PlotData' schema.
     *
     * The 'PlotQuery' schema allows for modifier restriction and item specifications.
     * @returns PlotData Successful Response
     * @throws ApiError
     */
    public static getPlotDataApiApiV1PlotPost({
        requestBody,
    }: {
        requestBody: PlotQuery,
    }): CancelablePromise<PlotData> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/api_v1/plot/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
