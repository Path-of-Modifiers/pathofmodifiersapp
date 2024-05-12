/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $GroupedModifierByEffect = {
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
            type: 'array',
            contains: {
                type: 'any-of',
                contains: [{
                    type: 'number',
                }, {
                    type: 'null',
                }],
            },
            isRequired: true,
        },
        maxRoll: {
            type: 'array',
            contains: {
                type: 'any-of',
                contains: [{
                    type: 'number',
                }, {
                    type: 'null',
                }],
            },
            isRequired: true,
        },
        textRolls: {
            type: 'array',
            contains: {
                type: 'any-of',
                contains: [{
                    type: 'string',
                }, {
                    type: 'null',
                }],
            },
            isRequired: true,
        },
        effect: {
            type: 'string',
            isRequired: true,
        },
        static: {
            type: 'array',
            contains: {
                type: 'any-of',
                contains: [{
                    type: 'boolean',
                }, {
                    type: 'null',
                }],
            },
            isRequired: true,
        },
    },
} as const;
