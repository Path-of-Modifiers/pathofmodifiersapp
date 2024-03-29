/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class LatestItemIdService {
    /**
     * Get Latest Item Id
     * Get the latest itemId
     *
     * Can only be used safely on an empty table or directly after an insertion.
     * @returns number Successful Response
     * @throws ApiError
     */
    public static getLatestItemIdApiApiV1ItemLatestItemIdGet(): CancelablePromise<number> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/item/latest_item_id/',
        });
    }
}
