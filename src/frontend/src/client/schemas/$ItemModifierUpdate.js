"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.$ItemModifierUpdate = void 0;
/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
exports.$ItemModifierUpdate = {
    properties: {
        itemId: {
            type: 'number',
            isRequired: true,
        },
        modifierId: {
            type: 'number',
            isRequired: true,
        },
        position: {
            type: 'number',
            isRequired: true,
        },
        roll: {
            type: 'any-of',
            contains: [{
                    type: 'number',
                }, {
                    type: 'null',
                }],
        },
    },
};
