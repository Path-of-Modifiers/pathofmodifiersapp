/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $UserRegister = {
    properties: {
        username: {
            type: 'string',
            isRequired: true,
            maxLength: 255,
        },
        email: {
            type: 'string',
            isRequired: true,
            format: 'email',
            maxLength: 255,
        },
        password: {
            type: 'string',
            isRequired: true,
            maxLength: 40,
            minLength: 8,
        },
    },
} as const;
