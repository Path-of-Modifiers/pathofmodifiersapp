/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Datum } from './Datum';
import type { LinkedPrices } from './LinkedPrices';
export type LeagueData = {
    league: string;
    linkedPrices?: (Array<LinkedPrices> | null);
    unlinkedPrices?: (Array<Datum> | null);
};

