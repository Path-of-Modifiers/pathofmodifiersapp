/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $UpdatePassword = {
    properties: {
        current_password: {
            type: 'string',
            isRequired: true,
            minLength: 8,
        },
        new_password: {
            type: 'string',
            isRequired: true,
            minLength: 8,
        },
    },
} as const;
