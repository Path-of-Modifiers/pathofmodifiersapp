"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.$PlotQuery = void 0;
/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
exports.$PlotQuery = {
    properties: {
        league: {
            type: 'string',
            isRequired: true,
        },
        itemSpecifications: {
            type: 'ItemSpecs',
            isRequired: true,
        },
        baseSpecifications: {
            type: 'any-of',
            contains: [{
                    type: 'BaseSpecs',
                }, {
                    type: 'null',
                }],
        },
        wantedModifiers: {
            type: 'array',
            contains: {
                type: 'WantedModifier',
            },
            isRequired: true,
        },
    },
};
