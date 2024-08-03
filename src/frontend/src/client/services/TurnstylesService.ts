/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { TurnstyleQuery } from '../models/TurnstyleQuery';
import type { TurnstyleResponse } from '../models/TurnstyleResponse';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class TurnstylesService {
    /**
     * Get Turnstyle Validation
     * Takes a query based on the 'TurnstyleQuery' schema and retrieves data
     * based on the cloudfare challenge turnstyle validation response.
     *
     * Args:
     * query (schemas.TurnstyleQuery): Query based on the 'TurnstyleQuery' schema.
     * verification (bool, optional): Verification flag. Defaults to Depends(verification).
     *
     * Raises:
     * HTTPException: If verification fails.
     *
     * Returns:
     * _type_: Returns a response based on the 'TurnstyleResponse' schema.
     * @returns TurnstyleResponse Successful Response
     * @throws ApiError
     */
    public static getTurnstyleValidationApiApiV1TurnstylePost({
        requestBody,
    }: {
        requestBody: TurnstyleQuery,
    }): CancelablePromise<TurnstyleResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/api_v1/turnstyle/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
