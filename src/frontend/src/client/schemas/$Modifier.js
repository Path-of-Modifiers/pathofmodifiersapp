"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.$Modifier = void 0;
/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
exports.$Modifier = {
    properties: {
        position: {
            type: 'number',
            isRequired: true,
        },
        minRoll: {
            type: 'any-of',
            contains: [{
                    type: 'number',
                }, {
                    type: 'null',
                }],
        },
        maxRoll: {
            type: 'any-of',
            contains: [{
                    type: 'number',
                }, {
                    type: 'null',
                }],
        },
        textRolls: {
            type: 'any-of',
            contains: [{
                    type: 'string',
                }, {
                    type: 'null',
                }],
        },
        static: {
            type: 'any-of',
            contains: [{
                    type: 'boolean',
                }, {
                    type: 'null',
                }],
        },
        effect: {
            type: 'string',
            isRequired: true,
        },
        regex: {
            type: 'any-of',
            contains: [{
                    type: 'string',
                }, {
                    type: 'null',
                }],
        },
        implicit: {
            type: 'any-of',
            contains: [{
                    type: 'boolean',
                }, {
                    type: 'null',
                }],
        },
        explicit: {
            type: 'any-of',
            contains: [{
                    type: 'boolean',
                }, {
                    type: 'null',
                }],
        },
        delve: {
            type: 'any-of',
            contains: [{
                    type: 'boolean',
                }, {
                    type: 'null',
                }],
        },
        fractured: {
            type: 'any-of',
            contains: [{
                    type: 'boolean',
                }, {
                    type: 'null',
                }],
        },
        synthesized: {
            type: 'any-of',
            contains: [{
                    type: 'boolean',
                }, {
                    type: 'null',
                }],
        },
        unique: {
            type: 'any-of',
            contains: [{
                    type: 'boolean',
                }, {
                    type: 'null',
                }],
        },
        corrupted: {
            type: 'any-of',
            contains: [{
                    type: 'boolean',
                }, {
                    type: 'null',
                }],
        },
        enchanted: {
            type: 'any-of',
            contains: [{
                    type: 'boolean',
                }, {
                    type: 'null',
                }],
        },
        veiled: {
            type: 'any-of',
            contains: [{
                    type: 'boolean',
                }, {
                    type: 'null',
                }],
        },
        modifierId: {
            type: 'number',
            isRequired: true,
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
