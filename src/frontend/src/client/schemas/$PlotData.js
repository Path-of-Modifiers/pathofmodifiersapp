"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.$PlotData = void 0;
/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
exports.$PlotData = {
    properties: {
        valueInChaos: {
            type: 'array',
            contains: {
                type: 'number',
            },
            isRequired: true,
        },
        timeStamp: {
            type: 'array',
            contains: {
                type: 'string',
                format: 'date-time',
            },
            isRequired: true,
        },
        mostCommonCurrencyUsed: {
            type: 'string',
            isRequired: true,
        },
        conversionValue: {
            type: 'array',
            contains: {
                type: 'number',
            },
            isRequired: true,
        },
    },
};
