/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $GroupedModifierProperties = {
    properties: {
        modifierId: {
            type: 'array',
            contains: {
                type: 'number',
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
    },
} as const;
