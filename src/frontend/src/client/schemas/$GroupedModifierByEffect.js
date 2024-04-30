"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.$GroupedModifierByEffect = void 0;
/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
exports.$GroupedModifierByEffect = {
    properties: {
        modifierId: {
            type: 'array',
            contains: {
                type: 'number',
            },
            isRequired: true,
        },
        position: {
            type: 'array',
            contains: {
                type: 'number',
            },
            isRequired: true,
        },
        minRoll: {
            type: 'any-of',
            contains: [{
                    type: 'null',
                }],
        },
        maxRoll: {
            type: 'any-of',
            contains: [{
                    type: 'null',
                }],
        },
        textRolls: {
            type: 'any-of',
            contains: [{
                    type: 'null',
                }],
        },
        effect: {
            type: 'string',
            isRequired: true,
        },
        static: {
            type: 'any-of',
            contains: [{
                    type: 'null',
                }],
        },
    },
};
