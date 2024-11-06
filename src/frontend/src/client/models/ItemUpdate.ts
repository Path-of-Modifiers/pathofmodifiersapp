/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Influences } from './Influences';
export type ItemUpdate = {
    gameItemId: string;
    name?: (string | null);
    league: string;
    baseType: string;
    typeLine: string;
    ilvl: number;
    rarity: string;
    identified?: boolean;
    currencyAmount?: (number | null);
    currencyId?: (number | null);
    corrupted?: (boolean | null);
    delve?: (boolean | null);
    fractured?: (boolean | null);
    synthesised?: (boolean | null);
    replica?: (boolean | null);
    influences?: (Influences | null);
    searing?: (boolean | null);
    tangled?: (boolean | null);
    isRelic?: (boolean | null);
    prefixes?: (number | null);
    suffixes?: (number | null);
    foilVariation?: (number | null);
};

