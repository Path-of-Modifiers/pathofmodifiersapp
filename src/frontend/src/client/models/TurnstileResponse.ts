/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type TurnstileResponse = {
    success: boolean;
    error_codes?: (Array<string> | null);
    challenge_ts: string;
    hostname: string;
    action: string;
    cdata: string;
    metadata: Record<string, any>;
};

