import { Flex } from "@chakra-ui/layout";
import { useState } from "react";
import { Checkbox, CheckboxIcon, Text } from "@chakra-ui/react";
import { CategoryInput } from "./ItemBaseTypeInputComp/CategoryInput";
import { BaseTypeInput } from "./ItemBaseTypeInputComp/BaseTypeInput";
import { SubCategoryInput } from "./ItemBaseTypeInputComp/SubCategoryInput";

export const BaseInput = () => {
  const [baseExpanded, setBaseExpanded] = useState(false);

  const handleExpanded = () => {
    console.log("EXPANDED");
    setBaseExpanded(!baseExpanded);
  };

  return (
    <Flex direction={"column"}>
      <Flex>
        <Checkbox onChange={handleExpanded}>
          <CheckboxIcon />
        </Checkbox>
        <Text color={"ui.white"}>Base type</Text>
      </Flex>
      {baseExpanded && (
        <Flex flexWrap={"wrap"} width={650}>
          <BaseTypeInput />
          <CategoryInput />
          <SubCategoryInput />
        </Flex>
      )}
    </Flex>
  );
};
