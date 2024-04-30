"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.$ValidationError = void 0;
/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
exports.$ValidationError = {
    properties: {
        loc: {
            type: 'array',
            contains: {
                type: 'any-of',
                contains: [{
                        type: 'string',
                    }, {
                        type: 'number',
                    }],
            },
            isRequired: true,
        },
        msg: {
            type: 'string',
            isRequired: true,
        },
        type: {
            type: 'string',
            isRequired: true,
        },
    },
};
