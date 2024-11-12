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
        roll: {
            type: 'any-of',
            contains: [{
                type: 'number',
            }, {
                type: 'null',
            }],
        },
        createdHoursSinceLaunch: {
            type: 'number',
            isRequired: true,
        },
    },
} as const;
