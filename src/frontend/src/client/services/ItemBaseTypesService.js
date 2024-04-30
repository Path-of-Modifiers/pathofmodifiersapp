"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ItemBaseTypesService = void 0;
var OpenAPI_1 = require("../core/OpenAPI");
var request_1 = require("../core/request");
var ItemBaseTypesService = /** @class */ (function () {
    function ItemBaseTypesService() {
    }
    /**
     * Get Item Base Type
     * Get item base type by key and value for "baseType".
     *
     * Always returns one item base type.
     * @returns any Successful Response
     * @throws ApiError
     */
    ItemBaseTypesService.getItemBaseTypeApiApiV1ItemBaseTypeBaseTypeGet = function (_a) {
        var baseType = _a.baseType;
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/itemBaseType/{baseType}',
            path: {
                'baseType': baseType,
            },
            errors: {
                422: "Validation Error",
            },
        });
    };
    /**
     * Update Item Base Type
     * Update an item base type by key and value for "baseType".
     *
     * Returns the updated item base type.
     * @returns ItemBaseType Successful Response
     * @throws ApiError
     */
    ItemBaseTypesService.updateItemBaseTypeApiApiV1ItemBaseTypeBaseTypePut = function (_a) {
        var baseType = _a.baseType, requestBody = _a.requestBody;
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'PUT',
            url: '/api/api_v1/itemBaseType/{baseType}',
            path: {
                'baseType': baseType,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: "Validation Error",
            },
        });
    };
    /**
     * Delete Item Base Type
     * Delete an item base type by key and value for "baseType".
     *
     * Returns a message that the item base type was deleted successfully.
     * Always deletes one item base type.
     * @returns string Successful Response
     * @throws ApiError
     */
    ItemBaseTypesService.deleteItemBaseTypeApiApiV1ItemBaseTypeBaseTypeDelete = function (_a) {
        var baseType = _a.baseType;
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'DELETE',
            url: '/api/api_v1/itemBaseType/{baseType}',
            path: {
                'baseType': baseType,
            },
            errors: {
                422: "Validation Error",
            },
        });
    };
    /**
     * Get All Item Base Types
     * Get all item base types.
     *
     * Returns a list of all item base types.
     * @returns any Successful Response
     * @throws ApiError
     */
    ItemBaseTypesService.getAllItemBaseTypesApiApiV1ItemBaseTypeGet = function () {
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/itemBaseType/',
        });
    };
    /**
     * Create Item Base Type
     * Create one or a list of new item base types.
     *
     * Returns the created item base type or list of item base types.
     * @returns any Successful Response
     * @throws ApiError
     */
    ItemBaseTypesService.createItemBaseTypeApiApiV1ItemBaseTypePost = function (_a) {
        var requestBody = _a.requestBody;
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'POST',
            url: '/api/api_v1/itemBaseType/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: "Validation Error",
            },
        });
    };
    return ItemBaseTypesService;
}());
exports.ItemBaseTypesService = ItemBaseTypesService;
