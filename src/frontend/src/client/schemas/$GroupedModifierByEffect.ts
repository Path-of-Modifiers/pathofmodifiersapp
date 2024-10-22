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
            type: 'any-of',
            contains: [{
                type: 'string',
            }, {
                type: 'null',
            }],
            isRequired: true,
        },
        groupedModifierProperties: {
            type: 'GroupedModifierProperties',
            isRequired: true,
        },
    },
} as const;
