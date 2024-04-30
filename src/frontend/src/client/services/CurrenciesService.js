"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.CurrenciesService = void 0;
var OpenAPI_1 = require("../core/OpenAPI");
var request_1 = require("../core/request");
var CurrenciesService = /** @class */ (function () {
    function CurrenciesService() {
    }
    /**
     * Get Currency
     * Get currency by key and value for "currencyId".
     *
     * Always returns one currency.
     * @returns any Successful Response
     * @throws ApiError
     */
    CurrenciesService.getCurrencyApiApiV1CurrencyCurrencyIdGet = function (_a) {
        var currencyId = _a.currencyId;
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/currency/{currencyId}',
            path: {
                'currencyId': currencyId,
            },
            errors: {
                422: "Validation Error",
            },
        });
    };
    /**
     * Update Currency
     * Update a currency by key and value for "currencyId".
     *
     * Returns the updated currency.
     * @returns Currency Successful Response
     * @throws ApiError
     */
    CurrenciesService.updateCurrencyApiApiV1CurrencyCurrencyIdPut = function (_a) {
        var currencyId = _a.currencyId, requestBody = _a.requestBody;
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'PUT',
            url: '/api/api_v1/currency/{currencyId}',
            path: {
                'currencyId': currencyId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: "Validation Error",
            },
        });
    };
    /**
     * Delete Currency
     * Delete a currency by key and value for "currencyId".
     *
     * Returns a message indicating the currency was deleted.
     * Always deletes one currency.
     * @returns string Successful Response
     * @throws ApiError
     */
    CurrenciesService.deleteCurrencyApiApiV1CurrencyCurrencyIdDelete = function (_a) {
        var currencyId = _a.currencyId;
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'DELETE',
            url: '/api/api_v1/currency/{currencyId}',
            path: {
                'currencyId': currencyId,
            },
            errors: {
                422: "Validation Error",
            },
        });
    };
    /**
     * Get All Currencies
     * Get all currencies.
     *
     * Returns a list of all currencies.
     * @returns any Successful Response
     * @throws ApiError
     */
    CurrenciesService.getAllCurrenciesApiApiV1CurrencyGet = function () {
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/currency/',
        });
    };
    /**
     * Create Currency
     * Create one or a list of currencies.
     *
     * Returns the created currency or list of currencies.
     * @returns any Successful Response
     * @throws ApiError
     */
    CurrenciesService.createCurrencyApiApiV1CurrencyPost = function (_a) {
        var requestBody = _a.requestBody;
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'POST',
            url: '/api/api_v1/currency/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: "Validation Error",
            },
        });
    };
    /**
     * Get Latest Currency Id
     * Get the latest currencyId
     *
     * Can only be used safely on an empty table or directly after an insertion.
     * @returns number Successful Response
     * @throws ApiError
     */
    CurrenciesService.getLatestCurrencyIdApiApiV1CurrencyLatestCurrencyIdGet = function () {
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/currency/latest_currency_id/',
        });
    };
    return CurrenciesService;
}());
exports.CurrenciesService = CurrenciesService;
