/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $GroupedModifierByEffect = {
    properties: {
        effect: {
            type: 'string',
            isRequired: true,
        },
        regex: {
            type: 'string',
            isRequired: true,
        },
        static: {
            type: 'any-of',
            contains: [{
                type: 'boolean',
            }, {
                type: 'null',
            }],
            isRequired: true,
        },
        relatedUniques: {
            type: 'string',
            isRequired: true,
        },
        groupedModifier: {
            type: 'GroupedModifier',
            isRequired: true,
        },
    },
} as const;
