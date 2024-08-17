/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type UserCreate = {
    username: string;
    email: string;
    hashedPassword: string;
    isActive?: (boolean | null);
    isSuperuser?: (boolean | null);
    rateLimitTier?: (number | null);
    isBanned?: (boolean | null);
    password: string;
};

