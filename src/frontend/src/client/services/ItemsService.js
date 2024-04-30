"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ItemsService = void 0;
var OpenAPI_1 = require("../core/OpenAPI");
var request_1 = require("../core/request");
var ItemsService = /** @class */ (function () {
    function ItemsService() {
    }
    /**
     * Get Item
     * Get item by key and value for "itemId".
     *
     * Always returns one item.
     * @returns any Successful Response
     * @throws ApiError
     */
    ItemsService.getItemApiApiV1ItemItemIdGet = function (_a) {
        var itemId = _a.itemId;
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/item/{itemId}',
            path: {
                'itemId': itemId,
            },
            errors: {
                422: "Validation Error",
            },
        });
    };
    /**
     * Update Item
     * Update an item by key and value for "itemId".
     *
     * Returns the updated item.
     * @returns Item Successful Response
     * @throws ApiError
     */
    ItemsService.updateItemApiApiV1ItemItemIdPut = function (_a) {
        var itemId = _a.itemId, requestBody = _a.requestBody;
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'PUT',
            url: '/api/api_v1/item/{itemId}',
            path: {
                'itemId': itemId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: "Validation Error",
            },
        });
    };
    /**
     * Delete Item
     * Delete an item by key and value for "itemId".
     *
     * Returns a message indicating the item was deleted.
     * Always deletes one item.
     * @returns string Successful Response
     * @throws ApiError
     */
    ItemsService.deleteItemApiApiV1ItemItemIdDelete = function (_a) {
        var itemId = _a.itemId;
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'DELETE',
            url: '/api/api_v1/item/{itemId}',
            path: {
                'itemId': itemId,
            },
            errors: {
                422: "Validation Error",
            },
        });
    };
    /**
     * Get Latest Item Id
     * Get the latest itemId
     *
     * Can only be used safely on an empty table or directly after an insertion.
     * @returns number Successful Response
     * @throws ApiError
     */
    ItemsService.getLatestItemIdApiApiV1ItemLatestItemIdGet = function () {
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/item/latest_item_id/',
        });
    };
    /**
     * Get All Items
     * Get all items.
     *
     * Returns a list of all items.
     * @returns any Successful Response
     * @throws ApiError
     */
    ItemsService.getAllItemsApiApiV1ItemGet = function () {
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/item/',
        });
    };
    /**
     * Create Item
     * Create one or a list of new items.
     *
     * Returns the created item or list of items.
     * @returns any Successful Response
     * @throws ApiError
     */
    ItemsService.createItemApiApiV1ItemPost = function (_a) {
        var requestBody = _a.requestBody;
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'POST',
            url: '/api/api_v1/item/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: "Validation Error",
            },
        });
    };
    return ItemsService;
}());
exports.ItemsService = ItemsService;
