/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $ItemModifierCreate = {
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
} as const;
