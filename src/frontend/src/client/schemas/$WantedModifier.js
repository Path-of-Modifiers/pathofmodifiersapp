"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.$WantedModifier = void 0;
/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
exports.$WantedModifier = {
    properties: {
        modifierId: {
            type: 'number',
            isRequired: true,
        },
        position: {
            type: 'number',
            isRequired: true,
        },
        modifierLimitations: {
            type: 'any-of',
            contains: [{
                    type: 'ModifierLimitations',
                }, {
                    type: 'null',
                }],
        },
    },
};
