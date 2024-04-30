"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ModifiersService = void 0;
var OpenAPI_1 = require("../core/OpenAPI");
var request_1 = require("../core/request");
var ModifiersService = /** @class */ (function () {
    function ModifiersService() {
    }
    /**
     * Get Modifier
     * Get modifier or list of modifiers by key and
     * value for "modifierId" and optional "position"
     *
     * Dominant key is "modifierId".
     *
     * Returns one or a list of modifiers.
     * @returns any Successful Response
     * @throws ApiError
     */
    ModifiersService.getModifierApiApiV1ModifierModifierIdGet = function (_a) {
        var modifierId = _a.modifierId, position = _a.position;
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/modifier/{modifierId}',
            path: {
                'modifierId': modifierId,
            },
            query: {
                'position': position,
            },
            errors: {
                422: "Validation Error",
            },
        });
    };
    /**
     * Update Modifier
     * Update a modifier by key and value for "modifierId" and "position".
     *
     * Dominant key is "modifierId".
     *
     * Returns the updated modifier.
     * @returns Modifier Successful Response
     * @throws ApiError
     */
    ModifiersService.updateModifierApiApiV1ModifierModifierIdPut = function (_a) {
        var modifierId = _a.modifierId, position = _a.position, requestBody = _a.requestBody;
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'PUT',
            url: '/api/api_v1/modifier/{modifierId}',
            path: {
                'modifierId': modifierId,
            },
            query: {
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
     * Delete Modifier
     * Delete a modifier by key and value for "modifierId"
     * and optional "position".
     *
     * Dominant key is "modifierId".
     *
     * Returns a message that the modifier was deleted.
     * Always deletes one modifier.
     * @returns string Successful Response
     * @throws ApiError
     */
    ModifiersService.deleteModifierApiApiV1ModifierModifierIdDelete = function (_a) {
        var modifierId = _a.modifierId, position = _a.position;
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'DELETE',
            url: '/api/api_v1/modifier/{modifierId}',
            path: {
                'modifierId': modifierId,
            },
            query: {
                'position': position,
            },
            errors: {
                422: "Validation Error",
            },
        });
    };
    /**
     * Get All Modifiers
     * Get all modifiers.
     *
     * Returns a list of all modifiers.
     * @returns any Successful Response
     * @throws ApiError
     */
    ModifiersService.getAllModifiersApiApiV1ModifierGet = function () {
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/modifier/',
        });
    };
    /**
     * Create Modifier
     * Create one or a list of new modifiers.
     *
     * Returns the created modifier or list of modifiers.
     * @returns any Successful Response
     * @throws ApiError
     */
    ModifiersService.createModifierApiApiV1ModifierPost = function (_a) {
        var requestBody = _a.requestBody;
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'POST',
            url: '/api/api_v1/modifier/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: "Validation Error",
            },
        });
    };
    /**
     * Get Grouped Modifier By Effect
     * Get all grouped modifiers by effect.
     *
     * Returns a list of all grouped modifiers by effect.
     * @returns any Successful Response
     * @throws ApiError
     */
    ModifiersService.getGroupedModifierByEffectApiApiV1ModifierGroupedModifiersByEffectGet = function () {
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/modifier/grouped_modifiers_by_effect/',
        });
    };
    return ModifiersService;
}());
exports.ModifiersService = ModifiersService;
