"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.DefaultService = void 0;
var OpenAPI_1 = require("../core/OpenAPI");
var request_1 = require("../core/request");
var DefaultService = /** @class */ (function () {
    function DefaultService() {
    }
    /**
     * Read Main
     * @returns any Successful Response
     * @throws ApiError
     */
    DefaultService.readMainGet = function () {
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'GET',
            url: '/',
        });
    };
    return DefaultService;
}());
exports.DefaultService = DefaultService;
