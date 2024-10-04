/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from "../core/CancelablePromise";
import { OpenAPI } from "../core/OpenAPI";
import { request as __request } from "../core/request";
export class TestsService {
  /**
   * Bulk Insert Test
   * Can only be used in `settings.ENVIRONMENT=local` environment.
   *
   * Test route for bulk inserting records.
   *
   * Returns a success message once the insertion is complete.
   * @returns any Successful Response
   * @throws ApiError
   */
  public static bulkInsertTest({
    count,
  }: {
    count: number;
  }): CancelablePromise<Record<string, any>> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/api_v1/test/bulk-insert-test",
      query: {
        count: count,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }
  /**
   * Bulk Insert Users And Verify
   * Can only be used in `settings.ENVIRONMENT=local` environment.
   *
   * Test route for bulk inserting users and verifying them.
   *
   * Returns the access tokens for the created users.
   * @returns string Successful Response
   * @throws ApiError
   */
  public static bulkInsertUsersAndVerify({
    count,
  }: {
    count: number;
  }): CancelablePromise<Array<string>> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/api_v1/test/bulk-insert-users-and-verify",
      query: {
        count: count,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }
}
