"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.$Currency = void 0;
/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
exports.$Currency = {
    properties: {
        tradeName: {
            type: 'string',
            isRequired: true,
        },
        valueInChaos: {
            type: 'number',
            isRequired: true,
        },
        iconUrl: {
            type: 'string',
            isRequired: true,
        },
        createdAt: {
            type: 'string',
            isRequired: true,
            format: 'date-time',
        },
        currencyId: {
            type: 'number',
            isRequired: true,
        },
    },
};
