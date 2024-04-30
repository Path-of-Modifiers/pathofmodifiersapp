"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.$Account = void 0;
/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
exports.$Account = {
    properties: {
        accountName: {
            type: 'string',
            isRequired: true,
        },
        isBanned: {
            type: 'any-of',
            contains: [{
                    type: 'boolean',
                }, {
                    type: 'null',
                }],
        },
        createdAt: {
            type: 'string',
            isRequired: true,
            format: 'date-time',
        },
        updatedAt: {
            type: 'any-of',
            contains: [{
                    type: 'string',
                    format: 'date-time',
                }, {
                    type: 'null',
                }],
        },
    },
};
