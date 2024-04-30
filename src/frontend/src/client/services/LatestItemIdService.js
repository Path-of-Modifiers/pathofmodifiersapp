"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.LatestItemIdService = void 0;
var OpenAPI_1 = require("../core/OpenAPI");
var request_1 = require("../core/request");
var LatestItemIdService = /** @class */ (function () {
    function LatestItemIdService() {
    }
    /**
     * Get Latest Item Id
     * Get the latest itemId
     *
     * Can only be used safely on an empty table or directly after an insertion.
     * @returns number Successful Response
     * @throws ApiError
     */
    LatestItemIdService.getLatestItemIdApiApiV1ItemLatestItemIdGet = function () {
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/item/latest_item_id/',
        });
    };
    return LatestItemIdService;
}());
exports.LatestItemIdService = LatestItemIdService;
