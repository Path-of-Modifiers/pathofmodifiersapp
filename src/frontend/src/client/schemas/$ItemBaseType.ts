/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $ItemBaseType = {
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
        relatedUniques: {
            type: 'any-of',
            contains: [{
                type: 'string',
            }, {
                type: 'null',
            }],
        },
        itemBaseTypeId: {
            type: 'number',
            isRequired: true,
        },
    },
} as const;
