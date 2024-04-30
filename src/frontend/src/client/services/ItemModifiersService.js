"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ItemModifiersService = void 0;
var OpenAPI_1 = require("../core/OpenAPI");
var request_1 = require("../core/request");
var ItemModifiersService = /** @class */ (function () {
    function ItemModifiersService() {
    }
    /**
     * Get Item Modifier
     * Get item modifier or list of item modifiers by key and
     * value for "itemId", optional "modifierId" and optional "position".
     *
     * Dominant key is "itemId".
     *
     * Returns one or a list of item modifiers.
     * @returns any Successful Response
     * @throws ApiError
     */
    ItemModifiersService.getItemModifierApiApiV1ItemModifierItemIdGet = function (_a) {
        var itemId = _a.itemId, modifierId = _a.modifierId, position = _a.position;
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/itemModifier/{itemId}',
            path: {
                'itemId': itemId,
            },
            query: {
                'modifierId': modifierId,
                'position': position,
            },
            errors: {
                422: "Validation Error",
            },
        });
    };
    /**
     * Get All Item Modifiers
     * Get all item modifiers.
     *
     * Returns a list of all item modifiers.
     * @returns any Successful Response
     * @throws ApiError
     */
    ItemModifiersService.getAllItemModifiersApiApiV1ItemModifierGet = function () {
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/itemModifier/',
        });
    };
    /**
     * Create Item Modifier
     * Create one or a list item modifiers.
     *
     * Returns the created item modifier or list of item modifiers.
     * @returns any Successful Response
     * @throws ApiError
     */
    ItemModifiersService.createItemModifierApiApiV1ItemModifierPost = function (_a) {
        var requestBody = _a.requestBody;
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'POST',
            url: '/api/api_v1/itemModifier/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: "Validation Error",
            },
        });
    };
    /**
     * Update Item Modifier
     * Update an item modifier by key and value for
     * "itemId", optional "modifierId" and optional "position".
     *
     * Dominant key is "itemId".
     *
     * Returns the updated item modifier.
     * @returns ItemModifier Successful Response
     * @throws ApiError
     */
    ItemModifiersService.updateItemModifierApiApiV1ItemModifierItemItemIdPut = function (_a) {
        var itemId = _a.itemId, modifierId = _a.modifierId, position = _a.position, requestBody = _a.requestBody;
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'PUT',
            url: '/api/api_v1/itemModifier/item={itemId}',
            path: {
                'itemId': itemId,
            },
            query: {
                'modifierId': modifierId,
                'position': position,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: "Validation Error",
            },
        });
    };
    /**
     * Delete Item Modifier
     * Delete an item modifier by key and value for
     * "itemId", optional "modifierId" and optional "position".
     *
     * Dominant key is "itemId".
     *
     * Returns a message that the item modifier was deleted successfully.
     * Always deletes one item modifier.
     * @returns any Successful Response
     * @throws ApiError
     */
    ItemModifiersService.deleteItemModifierApiApiV1ItemModifierItemItemIdDelete = function (_a) {
        var itemId = _a.itemId, modifierId = _a.modifierId, position = _a.position;
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'DELETE',
            url: '/api/api_v1/itemModifier/item={itemId}',
            path: {
                'itemId': itemId,
            },
            query: {
                'modifierId': modifierId,
                'position': position,
            },
            errors: {
                422: "Validation Error",
            },
        });
    };
    return ItemModifiersService;
}());
exports.ItemModifiersService = ItemModifiersService;
