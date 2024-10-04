/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $UserRegisterPreEmailConfirmation = {
    properties: {
        username: {
            type: 'string',
            isRequired: true,
            pattern: '^[\\p{L}\\p{N}_]+$',
        },
        email: {
            type: 'string',
            isRequired: true,
            format: 'email',
        },
        password: {
            type: 'string',
            isRequired: true,
            minLength: 8,
        },
    },
} as const;
