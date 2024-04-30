"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.$ItemBaseTypeUpdate = void 0;
/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
exports.$ItemBaseTypeUpdate = {
    properties: {
        baseType: {
            type: 'string',
            isRequired: true,
        },
        category: {
            type: 'string',
            isRequired: true,
        },
        subCategory: {
            type: 'any-of',
            contains: [{
                    type: 'string',
                }, {
                    type: 'null',
                }],
        },
    },
};
