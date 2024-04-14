/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Influences } from './Influences';
export type ItemUpdate = {
    stashId: string;
    gameItemId: string;
    name?: (string | null);
    changeId: string;
    iconUrl?: (string | null);
    league: string;
    typeLine: string;
    baseType: string;
    ilvl: number;
    rarity: string;
    identified?: boolean;
    forumNote?: (string | null);
    currencyAmount?: (number | null);
    currencyId?: (number | null);
    corrupted?: (boolean | null);
    delve?: (boolean | null);
    fractured?: (boolean | null);
    synthesized?: (boolean | null);
    replica?: (boolean | null);
    elder?: (boolean | null);
    shaper?: (boolean | null);
    influences?: (Influences | null);
    searing?: (boolean | null);
    tangled?: (boolean | null);
    isRelic?: (boolean | null);
    prefixes?: (number | null);
    suffixes?: (number | null);
    foilVariation?: (number | null);
};

