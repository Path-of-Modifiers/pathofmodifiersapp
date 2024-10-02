/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class TestsService {
    /**
     * Bulk Insert Test
     * Test route for bulk inserting 100,000 account records.
     *
     * Returns a success message once the insertion is complete.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static bulkInsertTest(): CancelablePromise<Record<string, any>> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/api_v1/test/bulk-insert-test',
        });
    }
}
