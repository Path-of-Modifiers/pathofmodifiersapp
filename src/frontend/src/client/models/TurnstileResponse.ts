/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { MetadataObject } from './MetadataObject';
export type TurnstileResponse = {
    success: boolean;
    error_codes?: (Array<string> | null);
    challenge_ts?: (string | null);
    hostname?: (string | null);
    action?: (string | null);
    cdata?: (string | null);
    metadata?: (MetadataObject | null);
};

