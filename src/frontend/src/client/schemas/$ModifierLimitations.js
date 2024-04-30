"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.$ModifierLimitations = void 0;
/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
exports.$ModifierLimitations = {
    properties: {
        maxRoll: {
            type: 'any-of',
            contains: [{
                    type: 'number',
                }, {
                    type: 'null',
                }],
        },
        minRoll: {
            type: 'any-of',
            contains: [{
                    type: 'number',
                }, {
                    type: 'null',
                }],
        },
        textRoll: {
            type: 'any-of',
            contains: [{
                    type: 'number',
                }, {
                    type: 'null',
                }],
        },
    },
};
