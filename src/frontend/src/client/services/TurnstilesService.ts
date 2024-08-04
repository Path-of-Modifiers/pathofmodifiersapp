/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { TurnstileQuery } from '../models/TurnstileQuery';
import type { TurnstileResponse } from '../models/TurnstileResponse';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class TurnstilesService {
    /**
     * Get Turnstile Validation
     * Takes a query based on the 'TurnstileQuery' schema and retrieves data
     * based on the cloudfare challenge turnstile validation response.
     *
     * Args:
     * query (schemas.TurnstileQuery): Query based on the 'TurnstileQuery' schema.
     * verification (bool, optional): Verification flag. Defaults to Depends(verification).
     *
     * Raises:
     * HTTPException: If verification fails.
     *
     * Returns:
     * _type_: Returns a response based on the 'TurnstileResponse' schema.
     * @returns TurnstileResponse Successful Response
     * @throws ApiError
     */
    public static getTurnstileValidationApiApiV1TurnstilePost({
        requestBody,
    }: {
        requestBody: TurnstileQuery,
    }): CancelablePromise<TurnstileResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/api_v1/turnstile/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
