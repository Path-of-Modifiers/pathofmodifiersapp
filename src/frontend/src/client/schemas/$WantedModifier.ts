/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $WantedModifier = {
    properties: {
        modifierId: {
            type: 'number',
            isRequired: true,
        },
        modifierLimitations: {
            type: 'any-of',
            contains: [{
                type: 'array',
                contains: {
                    type: 'ModifierLimitation',
                },
            }, {
                type: 'null',
            }],
        },
    },
} as const;
