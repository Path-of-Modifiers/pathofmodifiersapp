/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Account } from '../models/Account';
import type { AccountCreate } from '../models/AccountCreate';
import type { AccountUpdate } from '../models/AccountUpdate';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class AccountsService {
    /**
     * Get Account
     * Get the account by mapping with key and value for "accountName" .
     *
     * Always returns one account.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getAccountApiApiV1AccountAccountNameGet({
        accountName,
    }: {
        accountName: string,
    }): CancelablePromise<(Account | Array<Account>)> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/account/{accountName}',
            path: {
                'accountName': accountName,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update Account
     * Update an account by key and value for "accountName".
     *
     * Returns the updated account.
     * @returns Account Successful Response
     * @throws ApiError
     */
    public static updateAccountApiApiV1AccountAccountNamePut({
        accountName,
        requestBody,
    }: {
        accountName: string,
        requestBody: AccountUpdate,
    }): CancelablePromise<Account> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/api_v1/account/{accountName}',
            path: {
                'accountName': accountName,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Delete Account
     * Delete an account by key and value "accountName".
     *
     * Returns a message indicating the account was deleted.
     * Always deletes one account.
     * @returns string Successful Response
     * @throws ApiError
     */
    public static deleteAccountApiApiV1AccountAccountNameDelete({
        accountName,
    }: {
        accountName: string,
    }): CancelablePromise<string> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/api_v1/account/{accountName}',
            path: {
                'accountName': accountName,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get All Accounts
     * Get all accounts.
     *
     * Returns a list of all accounts.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getAllAccountsApiApiV1AccountGet(): CancelablePromise<(Account | Array<Account>)> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/account/',
        });
    }
    /**
     * Create Account
     * Create one or a list of accounts.
     *
     * Returns the created account or list of accounts.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static createAccountApiApiV1AccountPost({
        requestBody,
    }: {
        requestBody: (AccountCreate | Array<AccountCreate>),
    }): CancelablePromise<(AccountCreate | Array<AccountCreate>)> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/api_v1/account/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
