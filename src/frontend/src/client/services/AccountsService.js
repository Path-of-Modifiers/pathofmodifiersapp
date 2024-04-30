"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.AccountsService = void 0;
var OpenAPI_1 = require("../core/OpenAPI");
var request_1 = require("../core/request");
var AccountsService = /** @class */ (function () {
    function AccountsService() {
    }
    /**
     * Get Account
     * Get the account by mapping with key and value for "accountName" .
     *
     * Always returns one account.
     * @returns any Successful Response
     * @throws ApiError
     */
    AccountsService.getAccountApiApiV1AccountAccountNameGet = function (_a) {
        var accountName = _a.accountName;
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/account/{accountName}',
            path: {
                'accountName': accountName,
            },
            errors: {
                422: "Validation Error",
            },
        });
    };
    /**
     * Update Account
     * Update an account by key and value for "accountName".
     *
     * Returns the updated account.
     * @returns Account Successful Response
     * @throws ApiError
     */
    AccountsService.updateAccountApiApiV1AccountAccountNamePut = function (_a) {
        var accountName = _a.accountName, requestBody = _a.requestBody;
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'PUT',
            url: '/api/api_v1/account/{accountName}',
            path: {
                'accountName': accountName,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: "Validation Error",
            },
        });
    };
    /**
     * Delete Account
     * Delete an account by key and value "accountName".
     *
     * Returns a message indicating the account was deleted.
     * Always deletes one account.
     * @returns string Successful Response
     * @throws ApiError
     */
    AccountsService.deleteAccountApiApiV1AccountAccountNameDelete = function (_a) {
        var accountName = _a.accountName;
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'DELETE',
            url: '/api/api_v1/account/{accountName}',
            path: {
                'accountName': accountName,
            },
            errors: {
                422: "Validation Error",
            },
        });
    };
    /**
     * Get All Accounts
     * Get all accounts.
     *
     * Returns a list of all accounts.
     * @returns any Successful Response
     * @throws ApiError
     */
    AccountsService.getAllAccountsApiApiV1AccountGet = function () {
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/account/',
        });
    };
    /**
     * Create Account
     * Create one or a list of accounts.
     *
     * Returns the created account or list of accounts.
     * @returns any Successful Response
     * @throws ApiError
     */
    AccountsService.createAccountApiApiV1AccountPost = function (_a) {
        var requestBody = _a.requestBody;
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'POST',
            url: '/api/api_v1/account/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: "Validation Error",
            },
        });
    };
    return AccountsService;
}());
exports.AccountsService = AccountsService;
