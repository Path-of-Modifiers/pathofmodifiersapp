"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.$AccountCreate = void 0;
/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
exports.$AccountCreate = {
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
    },
};
