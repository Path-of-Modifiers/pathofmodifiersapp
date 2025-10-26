A potential way to do data aggregation in pure sql. Not complete yet

```sql
WITH "baseQuery" AS
(
	SELECT item."itemId" AS "itemId", item."createdHoursSinceLaunch" AS "createdHoursSinceLaunch", item.league AS league, item."itemBaseTypeId" AS "itemBaseTypeId", item."currencyId" AS "currencyId", item."currencyAmount" AS "currencyAmount", currency."tradeName" AS "tradeName", currency."valueInChaos" AS "valueInChaos", currency."createdHoursSinceLaunch" AS "currencyCreatedHoursSinceLaunch"
	FROM item JOIN currency ON item."currencyId" = currency."currencyId"
	WHERE (item.league = 'Mercenaries')
	-- AND (item."createdHoursSinceLaunch" >3000)
	AND (
		EXISTS (
			SELECT 1
			FROM item_modifier
			WHERE item."itemId" = item_modifier."itemId" AND item_modifier."modifierId" = 2
			)
	) AND true
),
"mostCommon" AS
	(
	SELECT "baseQuery"."tradeName" AS "mostCommonTradeName", count("baseQuery"."tradeName") AS "nameCount"
	FROM "baseQuery" GROUP BY "baseQuery".league, "baseQuery"."tradeName" ORDER BY "nameCount" DESC
	LIMIT 1
 ),
"mostCommonIds" AS
(
	SELECT "baseQuery"."createdHoursSinceLaunch" AS "createdHoursSinceLaunch", max("baseQuery"."currencyId") AS "mostCommonCurrencyId"
	FROM "baseQuery"
	WHERE "baseQuery"."tradeName" = (SELECT "mostCommon"."mostCommonTradeName" FROM "mostCommon")
	GROUP BY "baseQuery"."createdHoursSinceLaunch"
),
"mostCommonPrices" AS
(
	SELECT "baseQuery"."createdHoursSinceLaunch" AS "createdHoursSinceLaunch", min("baseQuery"."valueInChaos") AS "mostCommonValueInChaos", min("baseQuery"."tradeName") AS "mostCommonCurrencyUsed"
	FROM "baseQuery" JOIN "mostCommonIds" ON "baseQuery"."createdHoursSinceLaunch" = "mostCommonIds"."createdHoursSinceLaunch" AND "baseQuery"."currencyId" = "mostCommonIds"."mostCommonCurrencyId"
	GROUP BY "baseQuery"."createdHoursSinceLaunch"
),
prices AS
(
	SELECT "baseQuery"."createdHoursSinceLaunch" AS "createdHoursSinceLaunch", "baseQuery".league AS league, "baseQuery"."currencyAmount" * "baseQuery"."valueInChaos" AS "valueInChaos", ("baseQuery"."currencyAmount" * "baseQuery"."valueInChaos") / CAST("mostCommonPrices"."mostCommonValueInChaos" AS FLOAT(4)) AS "valueInMostCommonCurrencyUsed", "mostCommonPrices"."mostCommonCurrencyUsed" AS "mostCommonCurrencyUsed"
	FROM "baseQuery" JOIN "mostCommonPrices" ON "baseQuery"."createdHoursSinceLaunch" = "mostCommonPrices"."createdHoursSinceLaunch"
),
"rankedPrices" AS
(
	SELECT
		prices."createdHoursSinceLaunch" AS "createdHoursSinceLaunch",
		prices.league AS league,
		prices."valueInChaos" AS "valueInChaos",
		prices."valueInMostCommonCurrencyUsed" AS "valueInMostCommonCurrencyUsed",
		prices."mostCommonCurrencyUsed" AS "mostCommonCurrencyUsed",
		rank() OVER (PARTITION BY prices."createdHoursSinceLaunch" ORDER BY prices."valueInChaos" ASC) AS pos
	FROM prices
),
"filteredPrices" AS
(
	SELECT "rankedPrices"."createdHoursSinceLaunch" AS "createdHoursSinceLaunch", "rankedPrices".league AS league, "rankedPrices"."valueInChaos" AS "valueInChaos", "rankedPrices"."valueInMostCommonCurrencyUsed" AS "valueInMostCommonCurrencyUsed", "rankedPrices"."mostCommonCurrencyUsed" AS "mostCommonCurrencyUsed", CASE WHEN ("rankedPrices".pos < 10) THEN 'low' WHEN ("rankedPrices".pos < 15) THEN 'medium' ELSE 'high' END AS confidence
	FROM "rankedPrices"
	WHERE "rankedPrices".pos <= 20
	ORDER BY "rankedPrices"."createdHoursSinceLaunch"
),
"jsonReady" AS
(
	SELECT
		"filteredPrices"."createdHoursSinceLaunch" AS "hoursSinceLaunch",
		"filteredPrices".league,
		avg("filteredPrices"."valueInChaos") AS "valueInChaos",
		avg("filteredPrices"."valueInMostCommonCurrencyUsed") AS "valueInMostCommonCurrencyUsed",
		min("filteredPrices"."mostCommonCurrencyUsed") AS "mostCommonCurrencyUsed",
		min("filteredPrices".confidence) AS confidence
	FROM "filteredPrices"
	GROUP BY "filteredPrices"."createdHoursSinceLaunch", "filteredPrices".league
	ORDER BY "filteredPrices"."createdHoursSinceLaunch"
),
"overallConfidence" AS
(
	SELECT
		"jsonReady".league AS "name",
		"jsonReady".confidence AS "confidenceRating",
		RANK() OVER (
			PARTITION BY "jsonReady".league
			ORDER BY COUNT("jsonReady".confidence)
			ASC
		)
	FROM "jsonReady"
	GROUP BY
		"name",
		"confidenceRating"
),
"overallMostCommonCurrencyUsed" AS (
	SELECT
		"jsonReady".league AS "name",
		"jsonReady"."mostCommonCurrencyUsed" AS "mostCommonCurrencyUsed",
		RANK() OVER (
			PARTITION BY "jsonReady".league
			ORDER BY COUNT("jsonReady"."mostCommonCurrencyUsed")
			ASC
		)
	FROM "jsonReady"
	GROUP BY
		"name",
		"mostCommonCurrencyUsed"
), "timeSeriesData" AS (
	SELECT
		"jsonReady".league AS "name",
		json_agg(
			json_build_object(
			'hoursSinceLaunch', "jsonReady"."hoursSinceLaunch",
			'valueInChaos', "jsonReady"."valueInChaos",
			'valueInMostCommonCurrencyUsed', "jsonReady"."valueInMostCommonCurrencyUsed",
			'confidence', "jsonReady"."confidence"
			)
		) AS "data",
		"overallConfidence"."confidenceRating"
	FROM "jsonReady" JOIN "overallConfidence" ON "jsonReady".league = "overallConfidence".name
	GROUP BY "jsonReady".league, "overallConfidence"."confidenceRating"
)



SELECT
	json_build_object(
		'mostCommonCurrencyUsed', MIN("overallMostCommonCurrencyUsed"."mostCommonCurrencyUsed"),
		'data', json_agg(
			json_build_object(
				'name', "timeSeriesData".name,
				'data', "timeSeriesData".data,
				'confidenceRating', "timeSeriesData"."confidenceRating"
			)
		)
	)
FROM "timeSeriesData" NATURAL JOIN "overallMostCommonCurrencyUsed"

-- SELECT *, EXP(SUM(LN(multi)) OVER (PARTITION BY league, "createdHoursSinceLaunch", "clusterId" ORDER BY "valueInChaos" RANGE UNBOUNDED PRECEDING)) AS "cumMulti"
-- FROM

-- (
-- SELECT *, SUM(is_new_cluster) OVER (PARTITION BY league, "createdHoursSinceLaunch" ORDER BY "valueInChaos" RANGE UNBOUNDED PRECEDING) AS "clusterId"
-- FROM
-- (SELECT
-- 	*,
-- 	"valueInChaos" / "valueInChaosPrev" AS multi,
-- 	"valueInChaos" / "valueInChaos2Prev" AS multi2,
-- 	CASE
-- 		WHEN (("valueInChaos" / "valueInChaosPrev") > 1.05) OR (("valueInChaos" / "valueInChaos2Prev") > 1.1)
-- 			THEN 1
-- 		ELSE
-- 			0
-- 		END AS is_new_cluster
-- FROM(
-- 	SELECT
-- 		*,
-- 		LAG("valueInChaos", CEIL("nPoints"*0.05)::INT, null) OVER (PARTITION BY league, "createdHoursSinceLaunch"  ORDER BY "valueInChaos") AS "valueInChaosPrev",
-- 		LAG(
-- 			"valueInChaos",
-- 			CEIL("nPoints"*0.1)::INT,
-- 			null
-- 		) OVER (PARTITION BY league, "createdHoursSinceLaunch"  ORDER BY "valueInChaos") AS "valueInChaos2Prev"
-- 	-- FROM prices
-- 	FROM
-- 	(
-- 	 SELECT *,
-- 	 	COUNT(*) OVER (PARTITION BY league, "createdHoursSinceLaunch") AS "nPoints"
-- 	FROM prices
-- 	)
-- 	WHERE TRUE
-- 	-- WHERE league = 'Phrecia'
-- 	AND "createdHoursSinceLaunch" = 2658
-- 	ORDER BY "createdHoursSinceLaunch"
-- )))
```
