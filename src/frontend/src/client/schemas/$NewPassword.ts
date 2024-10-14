/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $NewPassword = {
    properties: {
        token: {
            type: 'string',
            isRequired: true,
        },
        new_password: {
            type: 'string',
            isRequired: true,
            maxLength: 40,
            minLength: 8,
        },
    },
} as const;
