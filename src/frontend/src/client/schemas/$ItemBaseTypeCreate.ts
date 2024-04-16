/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $ItemBaseTypeCreate = {
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
} as const;
