/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $ItemModifier = {
    properties: {
        itemId: {
            type: 'number',
            isRequired: true,
        },
        modifierId: {
            type: 'number',
            isRequired: true,
        },
        orderId: {
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
} as const;
