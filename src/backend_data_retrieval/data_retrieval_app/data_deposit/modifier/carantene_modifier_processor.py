import re
from datetime import UTC, datetime
from difflib import SequenceMatcher
from typing import Any

import pandas as pd
import requests
from nltk.corpus import stopwords
from spacy.lang.en.stop_words import STOP_WORDS

from data_retrieval_app.external_data_retrieval.config import settings
from data_retrieval_app.logs.logger import data_deposit_logger as logger
from data_retrieval_app.pom_api_authentication import get_superuser_token_headers
from data_retrieval_app.utils import insert_data

NUM_PATTERN = re.compile(r"-?\d+(?:\.\d+)?")


class EmptyCarModDF(Exception):
    def __init__(self, message="Carantene modifier dataframe is empty", value=None):
        self.message = message
        self.value = value
        super().__init__(
            f"{self.message}: {self.value}" if self.value is not None else self.message
        )


def _tokenize(s: str) -> list[str]:
    return s.split()


def _lcs_len(a: list[str], b: list[str]) -> float:
    n, m = len(a), len(b)
    dp = [0] * (m + 1)
    for i in range(1, n + 1):
        prev = 0
        ai = a[i - 1]
        for j in range(1, m + 1):
            cur = dp[j]
            if ai == b[j - 1]:
                dp[j] = prev + 1
            else:
                dp[j] = max(dp[j], dp[j - 1])
            prev = cur
    return dp[m]


def _diff_chunks(a: list[str], b: list[str]) -> list[tuple[str, str, int]]:
    "Returns [(text_roll_1, text_roll_2, position), (..)] for different tokens between `a` and `b`"
    sm = SequenceMatcher(a=a, b=b, autojunk=False)
    diffs = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        base_chunk = " ".join(a[i1:i2]).strip()
        other_chunk = " ".join(b[j1:j2]).strip()
        if base_chunk and other_chunk:
            diffs.append((base_chunk, other_chunk, i1))
    return diffs


def _build_text_rolls(
    df: pd.DataFrame,
) -> pd.DataFrame:
    logger.info("Building text rolls...")
    dfx = df.copy()

    dfx["relatedUnique"] = dfx["relatedUnique"].apply(
        lambda x: x if isinstance(x, list) else [x]
    )
    dfx = dfx.explode("relatedUnique", ignore_index=True)
    dfx["textRolls"] = [[] for _ in range(len(dfx))]
    dfx["numForTextReplaced"] = dfx["effect"].str.replace(NUM_PATTERN, "d#", regex=True)

    dfx["createdAt"] = pd.to_datetime(dfx["createdAt"])

    groups = list(dfx.groupby("relatedUnique", sort=False))
    total_groups = len(groups)

    def skippable_token(t: str):
        return any(c.isdigit() or c == "#" for c in t)

    stopwords_set = (
        set(stopwords.words("english"))
        | STOP_WORDS
        | {"increased", "decreased", "reduced"}
    )

    for idx, (_, g_df) in enumerate(groups, start=1):
        logger.info(
            "Processing textrolls, related unique group %s/%s (size=%s)",
            idx,
            total_groups,
            len(g_df),
        )

        idxs: list[int] = g_df.index.tolist()
        effects_token_map: dict[int, list[str]] = {
            i: _tokenize(dfx.at[i, "numForTextReplaced"]) for i in idxs
        }
        for i in idxs:
            a_effect_tokens = [
                t for t in effects_token_map[i] if not skippable_token(t)
            ]
            if (
                len(effects_token_map[i]) < settings.MIN_WORDS_CREATE_TEXT_ROLLS
            ):  # check with skips/numbers for min words
                continue
            for j in idxs:
                if i == j:
                    continue
                b_effect_tokens = [
                    t for t in effects_token_map[j] if not skippable_token(t)
                ]
                lcs_ratio = _lcs_len(a_effect_tokens, b_effect_tokens) / max(
                    1, len(effects_token_map[i])
                )
                if lcs_ratio >= settings.MIN_OVERLAP_EFFECT_CREATE_TEXT_ROLLS:
                    diffs = _diff_chunks(a_effect_tokens, b_effect_tokens)
                    if diffs:
                        diff_rolls = [
                            diff_tuple
                            for diff_tuple in diffs
                            if all(
                                roll.lower() not in stopwords_set
                                for roll in diff_tuple[:-1]
                            )
                        ]
                        dfx.at[i, "textRolls"] = dfx.at[i, "textRolls"] + diff_rolls
    logger.info(
        "Successfully built text rolls, performing further transforms on carantene..."
    )
    return dfx


def _replace_text_rolls(row):
    filled_effect: str = row["effect"]
    for group in row["textRolls"]:
        for text_roll in group[:-1]:  # group[-1] is position
            if isinstance(text_roll, str) and text_roll in filled_effect:
                filled_effect = filled_effect.replace(text_roll, "#")
    return filled_effect


def _build_counter_position(row):
    result = {}
    for pos, value, unique in zip(
        row["positionNum"], row["numValue"], row["relatedUnique"], strict=True
    ):
        mod = row["replacedNumEffect"]
        mod_unique_key = f"{mod}|{pos}|{value}|{unique}"
        if mod_unique_key not in result:
            result[mod_unique_key] = {
                "replacedNumEffect": mod,
                "positionNum": pos,
                "numValue": value,
                "relatedUnique": unique,
                "count": 0,
            }
        result[mod_unique_key]["count"] += 1
    return result


def _expand_effect(row):
    car_mod_id = row["caranteneModifierId"]
    effect = row["effect"]
    text_rolls = row["textRolls"]
    related_uniq = row["relatedUnique"]

    replaced_num_effect = NUM_PATTERN.sub("d#", effect)
    matches = list(NUM_PATTERN.finditer(effect))

    results = []
    if not matches:
        results.append(
            {
                "caranteneModifierId": car_mod_id,
                "effect": effect,
                "relatedUnique": related_uniq,
                "mutated": True,  # ToDo: adjust if this expands beyond mutated
                "replacedNumEffect": effect,
                "positionNum": 0,
                "numValue": None,
                "textRolls": text_rolls,
                "unique": bool(related_uniq),
            }
        )
        return results

    for i, m in enumerate(matches):
        group = m.group(0)

        # Decide int vs float based on the text
        if "." in group:
            num = float(group)
        else:
            num = int(group)

        results.append(
            {
                "caranteneModifierId": car_mod_id,
                "effect": effect,
                "relatedUnique": related_uniq,
                "mutated": True,  # ToDo: adjust if this expands beyond mutated
                "replacedNumEffect": replaced_num_effect,
                "positionNum": i,
                "numValue": num,
                "textRolls": text_rolls,
                "unique": bool(related_uniq),
            }
        )

    return results


def _fill_hashes(
    template: str, pos_to_value: dict[int, int | float | None]
) -> tuple[str, list[int]]:
    """Replace each # in order; only fill when mapping has a concrete value."""

    def repl(_):
        nonlocal k
        v = pos_to_value.get(k, None)
        if v is not None:
            r = str(v)
        else:
            r = "d#"
            positions.append(k)
        k += 1
        return r

    k = 0
    positions: list[int] = []
    result = re.sub(r"d#", repl, template)
    return result, positions


def _coerce_numeric(v: Any) -> int | float | Any:
    """Convert strings to int/float without destroying floats; leave non-numeric as-is."""
    if isinstance(v, int | float):
        return v

    if isinstance(v, str):
        s = v.strip()
        if not s:
            return v

        if any(c in s for c in ".eE"):
            try:
                return float(s)
            except ValueError:
                return v
        try:
            return int(s)
        except ValueError:
            try:
                return float(s)
            except ValueError:
                return v

    return v


def _consistent_values_from_counter(
    counter_dict: dict[str, dict],
    template: str,
    related_unique: str,
) -> dict[int, float | int | None]:
    """
    From the counter dict, compute for one relatedUnique:
    - For each positionNum, if exactly one numValue appears -> that value (int or float)
    - Otherwise -> None (inconsistent)
    """
    by_pos: dict[int, set] = {}

    for key, info in counter_dict.items():
        # Key format expected:
        # 'replacedNumEffect|positionNum|numValue|relatedUnique'
        try:
            t, pos, val, ru = key.split("|", 3)
            pos_int = int(pos)

            if t == template and ru == related_unique and info.get("count", 0) > 0:
                # Prefer numeric from info['numValue']; fall back to val from the key
                num_val = info.get("numValue", None)
                if num_val is None:
                    num_val = val

                by_pos.setdefault(pos_int, set()).add(num_val)
        except Exception:
            # Ignore malformed keys silently
            continue

    result: dict[int, float | int | None] = {}

    for pos, vals in by_pos.items():
        # If we have exactly one distinct value, it's "consistent"
        if len(vals) == 1:
            v = next(iter(vals))
            v = _coerce_numeric(v)
            if isinstance(v, int | float):
                v = int(v) if v.is_integer() else float(v)
                result[pos] = v
            else:
                result[pos] = None
        else:
            result[pos] = None

    return result


def _apply_static_num_replacements(df: pd.DataFrame) -> pd.DataFrame:
    """
    For each input row:
      - create one output per relatedUnique
      - replace # only where (relatedUnique, positionNum) has a single numValue across the group
      - merge outputs that result in identical strings by aggregating relatedUniques
    """
    if df.empty:
        raise EmptyCarModDF

    out_rows = []

    for _, row in df.iterrows():
        carantene_mod_id = row["caranteneModifierId"]
        template = row["replacedNumEffect"]
        text_rolls = row["textRolls"]
        related_list = list(row["relatedUnique"])
        counter = row.get("counter", None)

        related_uniques = sorted(set(related_list))
        per_related_outputs = []

        for ru in related_uniques:
            pos_to_value = {}
            if isinstance(counter, dict) and counter:
                pos_to_value = _consistent_values_from_counter(counter, template, ru)

            effect_inserted, positions = _fill_hashes(template, pos_to_value)
            per_related_outputs.append(
                {
                    "caranteneModifierId": carantene_mod_id,
                    "replacedNumEffect": template,
                    "filledNumEffect": effect_inserted,
                    "relatedUnique": ru,
                    "positionNum": positions,
                    "textRolls": text_rolls,
                }
            )
        df = pd.DataFrame(per_related_outputs).explode("positionNum", ignore_index=True)
        merged = df.groupby(
            ["replacedNumEffect", "filledNumEffect"], as_index=False
        ).agg(
            {
                "caranteneModifierId": lambda s: list(s),
                "relatedUnique": lambda s: sorted(set(s)),
                "positionNum": lambda s: sorted(set(s)),
                "textRolls": lambda t: sorted(t),
            }
        )
        out_rows.append(merged)

    logger.info(
        "Successfully added static numbers replacements, performing further transforms on carantene..."
    )
    return pd.concat(out_rows, ignore_index=True)


def _build_modifier_from_carantene(df: pd.DataFrame):
    if df.empty:
        raise EmptyCarModDF

    rows = []

    all_car_mod_ids = []
    for _, row in df.iterrows():
        try:
            carantene_mod_ids = row["caranteneModifierId"]
            all_car_mod_ids.extend(carantene_mod_ids)

            template = row["filledNumEffect"]
            effect = template.replace("d#", "#")

            # find hashtag placeholders in order (numeric vs text)
            kinds = []
            for m in re.finditer(r"d#|#", template):
                token = m.group()
                kinds.append("num" if token == "d#" else "text")

            # collect textRolls by token-position in filledNumEffect
            textpos_map = {}
            tr = row.get("textRolls")
            if isinstance(tr, list):
                for outer in tr:
                    for inner in outer:
                        for t1, t2, pos in inner:
                            s = textpos_map.setdefault(pos, set())
                            s.add(f"{t1}")
                            s.add(f"{t2}")
            textpos_map = {p: "|".join(sorted(v)) for p, v in textpos_map.items()}

            # map text-roll positions to hashtag indices (by order)
            text_placeholder_idx = [i for i, k in enumerate(kinds) if k == "text"]
            sorted_token_pos = sorted(textpos_map)
            pos_to_textroll = {}
            for idx, token_pos in zip(
                text_placeholder_idx, sorted_token_pos, strict=True
            ):
                pos_to_textroll[idx] = textpos_map[token_pos]

            # build regex from template using placeholder index
            parts = []
            i = 0
            h_idx = 0
            while i < len(template):
                if template.startswith("d#", i):
                    parts.append("([0-9]*[.]?[0-9]+)")
                    i += 2
                    h_idx += 1
                elif template[i] == "#":
                    texts = pos_to_textroll.get(h_idx)
                    if texts:
                        options = sorted(set(texts.split("|")))
                        parts.append("(" + "|".join(options) + ")")
                    else:
                        parts.append("(.+?)")
                    i += 1
                    h_idx += 1
                elif template[i] == "+" or template[i] == "-":
                    parts.append("[+-]")
                    i += 1
                else:
                    parts.append(template[i])
                    i += 1
            regex = "^" + "".join(parts) + "$"

            related = row.get("relatedUnique", [])
            if isinstance(related, list):
                related_str = "|".join(related)
            else:
                related_str = related if pd.notna(related) else ""

            static_val = None if ("d#" in template or "#" in template) else True
            kinds = kinds if kinds else [None]
            for pos, kind in enumerate(kinds):
                out_row = {
                    "position": pos,
                    "relatedUniques": related_str,
                    "effect": effect,
                    "regex": regex if not static_val else None,
                    "explicit": True,
                    "unique": True,
                    "static": static_val,
                    "dynamicallyCreated": True,
                }
                if kind == "num":
                    out_row["minRoll"] = -999999
                    out_row["maxRoll"] = 999999
                    out_row["textRolls"] = None
                elif kind == "text":
                    out_row["minRoll"] = None
                    out_row["maxRoll"] = None
                    out_row["textRolls"] = pos_to_textroll.get(pos)
                else:
                    out_row["minRoll"] = None
                    out_row["maxRoll"] = None
                    out_row["textRolls"] = None
                rows.append(out_row)

        except Exception as e:
            raise Exception(f"Failed to create mod on row {row}, exception: {e}")
    mod_cols = [
        "position",
        "relatedUniques",
        "minRoll",
        "maxRoll",
        "textRolls",
        "explicit",
        "unique",
        "static",
        "effect",
        "regex",
        "dynamicallyCreated",
    ]

    modifier_ids = list({int(item) for sublist in all_car_mod_ids for item in sublist})

    logger.info("Successfully built modifiers from carantene modifiers")
    return pd.DataFrame(rows, columns=mod_cols), modifier_ids


def _transform_carantene_modifier(
    carantene_modifier_df: pd.DataFrame,
) -> tuple[pd.DataFrame, list[int]] | tuple[None, None]:
    def _expand_num_effect(df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            raise EmptyCarModDF

        return (
            df.apply(lambda row: _expand_effect(row), axis=1)
            .explode()
            .apply(pd.Series)
            .reset_index(drop=True)
        )

    def _group_and_add_counter(df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df

        grouped = df.groupby("replacedNumEffect").agg(list).reset_index()
        grouped["counter"] = grouped.apply(_build_counter_position, axis=1)

        def row_has_min_count(d, min_count=10):
            # d is the dict-of-dicts
            return any(inner.get("count", 0) >= min_count for inner in d.values())

        grouped = grouped[grouped["counter"].apply(row_has_min_count)]
        if grouped.empty:
            raise EmptyCarModDF

        logger.info(
            "Successfully grouped and added counters, performing further transforms on carantene..."
        )
        return grouped

    try:
        carantene_modifier_df, carantene_modifier_ids = (
            carantene_modifier_df.pipe(_build_text_rolls)
            .assign(effect=lambda df: df.apply(_replace_text_rolls, axis=1))
            .pipe(_expand_num_effect)
            .pipe(_group_and_add_counter)
            .pipe(_apply_static_num_replacements)
            .pipe(_build_modifier_from_carantene)
        )
    except EmptyCarModDF as e:
        logger.info(e.message)
        return None, None

    return carantene_modifier_df, carantene_modifier_ids


def _get_latest_dynamic_modifier_created_at() -> datetime:
    url = f"{settings.BACKEND_BASE_URL}/modifier/latest-dynamically-created/"
    pom_api_headers = get_superuser_token_headers(settings.BACKEND_BASE_URL)
    try:
        response = requests.get(url=url, headers=pom_api_headers, timeout=60)
        response.raise_for_status()

        latest_datetime_str = response.json()
        assert isinstance(latest_datetime_str, str)
        latest_datetime_str = latest_datetime_str.replace(
            "+00", "+00:00"
        )  # why why why

    except requests.HTTPError as e:
        raise requests.HTTPError(
            f"POM API HTTP request error, failed to create initial dynamically created modifier, error: {e}"
        )
    except Exception as e:
        raise Exception(
            f"Failed to create initial dynamically created modifier, error: {e}"
        )

    return datetime.fromisoformat(latest_datetime_str)


def _check_days_since_last_created() -> bool:
    latest_created_at = _get_latest_dynamic_modifier_created_at()
    days_since_last_created_at = (datetime.now(UTC) - latest_created_at).days
    if not days_since_last_created_at > settings.MIN_DAYS_SINCE_DYNAMICALLY_CREATED_AT:
        return False
    return True


def _get_carantene_df() -> pd.DataFrame:
    base_url = str(settings.BACKEND_BASE_URL)
    pom_auth_headers = get_superuser_token_headers(base_url)
    get_carantene_response = requests.get(
        f"{base_url}/carantene_modifier", headers=pom_auth_headers
    )

    get_carantene_response.raise_for_status()

    carantene_dump = get_carantene_response.json()

    if not carantene_dump:
        return

    carantene_df = pd.DataFrame(carantene_dump)

    return carantene_df


def _insert_modifiers_from_carantene(carantene_modifier_df: pd.DataFrame) -> None:
    base_url = str(settings.BACKEND_BASE_URL)
    pom_auth_headers = get_superuser_token_headers(base_url)

    insert_data(
        carantene_modifier_df,
        url=base_url,
        table_name="modifier",
        logger=logger,
        headers=pom_auth_headers,
        method="post",
    )


def check_carantene_modifiers() -> None:
    if not _check_days_since_last_created():
        return None

    logger.info(
        "Its been over 3 days since last created modifiers from carantene modifiers. Retrieving carantene modifiers..."
    )

    # with open("car_df_json_dump.json", "w") as f:
    #    json.dump(carantene_dump, f, indent=4)

    carantene_df = _get_carantene_df()

    logger.info("Transforming carantene modifiers...")

    carantene_modifier_df, carantene_modifier_ids = _transform_carantene_modifier(
        carantene_df
    )

    if carantene_modifier_df is not None and carantene_modifier_ids is not None:
        logger.info(
            f"Inserting {len(carantene_modifier_df)} new modifiers from carantene modifiers..."
        )

        _insert_modifiers_from_carantene(carantene_modifier_df)

        logger.info(
            f"Deleting {len(carantene_modifier_ids)} of the old carantene modifiers present"
        )

        # bulk_delete_data(
        #    primary_key="caranteneModifierId",
        #    primary_key_values=carantene_modifier_ids,
        #    table_name="carantene_modifier",
        # )


def initial_dynamically_created_modifier() -> None:
    "Creates an initial dynamically created modifier, if one does not exist in the database"

    url = f"{settings.BACKEND_BASE_URL}/modifier/initial-dynamically-created/"
    pom_api_headers = get_superuser_token_headers(settings.BACKEND_BASE_URL)
    try:
        response = requests.post(url=url, headers=pom_api_headers)
        response.raise_for_status()

    except requests.HTTPError as e:
        raise requests.HTTPError(
            f"POM API HTTP request error, failed to create initial dynamically created modifier, error: {e}"
        )
    except Exception as e:
        raise Exception(
            f"Failed to create initial dynamically created modifier, error: {e}"
        )


def delete_grouped_dupes() -> None:
    url = f"{settings.BACKEND_BASE_URL}/carantene_modifier/delete-grouped-dupes/"
    pom_api_headers = get_superuser_token_headers(settings.BACKEND_BASE_URL)
    try:
        response = requests.post(url=url, headers=pom_api_headers)
        response.raise_for_status()

    except requests.HTTPError as e:
        raise requests.HTTPError(
            f"POM API HTTP request error, failed to delete grouped dupes, error: {e}"
        )
    except Exception as e:
        raise Exception(f"Failed to delete grouped dupes, error: {e}")
