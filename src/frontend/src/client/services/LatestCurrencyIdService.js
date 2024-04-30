"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.LatestCurrencyIdService = void 0;
var OpenAPI_1 = require("../core/OpenAPI");
var request_1 = require("../core/request");
var LatestCurrencyIdService = /** @class */ (function () {
    function LatestCurrencyIdService() {
    }
    /**
     * Get Latest Currency Id
     * Get the latest currencyId
     *
     * Can only be used safely on an empty table or directly after an insertion.
     * @returns number Successful Response
     * @throws ApiError
     */
    LatestCurrencyIdService.getLatestCurrencyIdApiApiV1CurrencyLatestCurrencyIdGet = function () {
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/currency/latest_currency_id/',
        });
    };
    return LatestCurrencyIdService;
}());
exports.LatestCurrencyIdService = LatestCurrencyIdService;
