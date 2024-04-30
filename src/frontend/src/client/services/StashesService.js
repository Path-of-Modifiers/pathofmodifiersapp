"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.StashesService = void 0;
var OpenAPI_1 = require("../core/OpenAPI");
var request_1 = require("../core/request");
var StashesService = /** @class */ (function () {
    function StashesService() {
    }
    /**
     * Get Stash
     * Get stash by key and value for "stashId".
     *
     * Always returns one stash.
     * @returns any Successful Response
     * @throws ApiError
     */
    StashesService.getStashApiApiV1StashStashIdGet = function (_a) {
        var stashId = _a.stashId;
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/stash/{stashId}',
            path: {
                'stashId': stashId,
            },
            errors: {
                422: "Validation Error",
            },
        });
    };
    /**
     * Update Stash
     * Update a stash by key and value for "stashId".
     *
     * Returns the updated stash.
     * @returns Stash Successful Response
     * @throws ApiError
     */
    StashesService.updateStashApiApiV1StashStashIdPut = function (_a) {
        var stashId = _a.stashId, requestBody = _a.requestBody;
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'PUT',
            url: '/api/api_v1/stash/{stashId}',
            path: {
                'stashId': stashId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: "Validation Error",
            },
        });
    };
    /**
     * Delete Stash
     * Delete a stash by key and value for "stashId".
     *
     * Returns a message that the stash was deleted successfully.
     * Always deletes one stash.
     * @returns string Successful Response
     * @throws ApiError
     */
    StashesService.deleteStashApiApiV1StashStashIdDelete = function (_a) {
        var stashId = _a.stashId;
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'DELETE',
            url: '/api/api_v1/stash/{stashId}',
            path: {
                'stashId': stashId,
            },
            errors: {
                422: "Validation Error",
            },
        });
    };
    /**
     * Get All Stashes
     * Get all stashes.
     *
     * Returns a list of all stashes.
     * @returns any Successful Response
     * @throws ApiError
     */
    StashesService.getAllStashesApiApiV1StashGet = function () {
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'GET',
            url: '/api/api_v1/stash/',
        });
    };
    /**
     * Create Stash
     * Create one or a list of new stashes.
     *
     * Returns the created stash or list of stashes.
     * @returns any Successful Response
     * @throws ApiError
     */
    StashesService.createStashApiApiV1StashPost = function (_a) {
        var requestBody = _a.requestBody;
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'POST',
            url: '/api/api_v1/stash/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: "Validation Error",
            },
        });
    };
    return StashesService;
}());
exports.StashesService = StashesService;
