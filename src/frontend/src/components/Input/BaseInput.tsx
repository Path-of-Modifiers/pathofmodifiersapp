import { Flex } from "@chakra-ui/layout";
import { useEffect } from "react";
import { BaseTypeInput, BaseType } from "./ItemBaseTypeInputComp/BaseTypeInput";
import { CategoryInput } from "./ItemBaseTypeInputComp/CategoryInput";
import { SubCategoryInput } from "./ItemBaseTypeInputComp/SubCategoryInput";
import { useGraphInputStore } from "../../store/GraphInputStore";
import { AddICheckText } from "../Icon/AddICheckText";
import { useExpandedComponentStore } from "../../store/ExpandedComponentStore";

// BaseInput component that contains the base type input, category input, and sub category input
export const BaseInput = () => {
    const { clearClicked, baseSpec, choosableItemBaseType } =
        useGraphInputStore();
    let presetBaseType: string | undefined;
    let presetCategory: string | undefined;
    let presetSubCategory: string | undefined;
    if (baseSpec) {
        if (baseSpec.baseType != null) {
            presetBaseType = baseSpec.baseType;
        }
        if (baseSpec.category != null) {
            presetCategory = baseSpec.category;
        }
        if (baseSpec.subCategory != null) {
            presetSubCategory = baseSpec.subCategory;
        }
    }

    const baseTypes: BaseType[] = choosableItemBaseType
        .filter((itemBaseType) => !itemBaseType.isNotChoosable)
        .map((itemBaseType) => ({
            itemBaseTypeId: itemBaseType.itemBaseTypeId,
            baseType: itemBaseType.baseType,
        }));
    const categories = [
        ...new Set(
            choosableItemBaseType
                .filter((itemBaseType) => !itemBaseType.isNotChoosable)
                .map((itemBaseType) => itemBaseType.category),
        ),
    ];
    const subCategories = [
        ...new Set(
            choosableItemBaseType
                .filter((itemBaseType) => !itemBaseType.isNotChoosable)
                .map((itemBaseType) => itemBaseType.subCategory)
                .filter((subCategory) => subCategory != null),
        ),
    ];

    const { expandedBaseType, setExpandedBaseType } = useExpandedComponentStore();

    const handleExpanded = () => {
        setExpandedBaseType(!expandedBaseType);
    };

    useEffect(() => {
        if (clearClicked) {
            setExpandedBaseType(false);
        }
    }, [clearClicked, setExpandedBaseType]);

    return (
        <Flex direction={"column"} width={"inputSizes.lgBox"}>
            <AddICheckText
                isChecked={expandedBaseType}
                onChange={handleExpanded}
                text="Base Type"
            />
            {expandedBaseType && choosableItemBaseType.length !== 0 && (
                <Flex flexWrap={"wrap"} justifyContent={"flex-start"} ml={10} gap={2}>
                    <BaseTypeInput baseTypes={baseTypes} presetValue={presetBaseType} />
                    <CategoryInput categories={categories} presetValue={presetCategory} />
                    <SubCategoryInput
                        subCategories={subCategories}
                        presetValue={presetSubCategory}
                    />
                </Flex>
            )}
        </Flex>
    );
};
