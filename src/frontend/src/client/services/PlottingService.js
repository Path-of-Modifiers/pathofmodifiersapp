"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.PlottingService = void 0;
var OpenAPI_1 = require("../core/OpenAPI");
var request_1 = require("../core/request");
var PlottingService = /** @class */ (function () {
    function PlottingService() {
    }
    /**
     * Get Plot Data
     * Takes a query based on the 'PlotQuery' schema and retrieves data
     * to be used for plotting in the format of the 'PlotData' schema.
     *
     * The 'PlotQuery' schema allows for modifier restriction and item specifications.
     * @returns PlotData Successful Response
     * @throws ApiError
     */
    PlottingService.getPlotDataApiApiV1PlotPost = function (_a) {
        var requestBody = _a.requestBody;
        return (0, request_1.request)(OpenAPI_1.OpenAPI, {
            method: 'POST',
            url: '/api/api_v1/plot/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: "Validation Error",
            },
        });
    };
    return PlottingService;
}());
exports.PlottingService = PlottingService;
