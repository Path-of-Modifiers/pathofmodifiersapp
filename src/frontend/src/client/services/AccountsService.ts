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
     * Get the account by filter with key and value for "accountName" .
     *
     * Always returns one account.
     * @returns Account Successful Response
     * @throws ApiError
     */
    public static getAccount({
        accountName,
    }: {
        accountName: string,
    }): CancelablePromise<Account> {
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
    public static updateAccount({
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
    public static deleteAccount({
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
    public static getAllAccounts({
        limit,
        skip,
        sortKey,
        sortMethod,
    }: {
        limit?: (number | null),
        skip?: (number | null),
        sortKey?: (string | null),
        sortMethod?: ('asc' | 'desc' | null),
    }): CancelablePromise<(Account | Array<Account>)> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/account/',
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
     * Create Account
     * Create one or a list of accounts.
     *
     * Returns the created account or list of accounts.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static createAccount({
        requestBody,
        onDuplicatePkeyDoNothing,
        returnNothing,
    }: {
        requestBody: (AccountCreate | Array<AccountCreate>),
        onDuplicatePkeyDoNothing?: (boolean | null),
        returnNothing?: (boolean | null),
    }): CancelablePromise<(AccountCreate | Array<AccountCreate> | null)> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/api_v1/account/',
            query: {
                'on_duplicate_pkey_do_nothing': onDuplicatePkeyDoNothing,
                'return_nothing': returnNothing,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
