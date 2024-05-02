import { Flex, Select, Text } from "@chakra-ui/react";
import { useGraphInputStore } from "../../../store/GraphInputStore";
import { GetBaseTypes } from "../../../hooks/getBaseTypeCategories";
import { BaseType } from "../../../client";

const handleBaseTypeChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
  const baseType = event.target.value;
  useGraphInputStore.setState({ baseSpec: { baseType: baseType } });
};

export const BaseTypeInput = () => {
  const baseTypes: BaseType[] | undefined = GetBaseTypes();

  let baseTypeOptions: JSX.Element[] = [];
  if (baseTypes !== undefined) {
    baseTypeOptions = baseTypes.map((baseType) => {
      return (
        <option
          value={baseType.baseType}
          key={"ItemCategoryInput" + "_option_" + baseType.baseType}
          style={{ color: "white", backgroundColor: "#2d3333" }}
        >
          {baseType.baseType}
        </option>
      );
    });
  }

  return (
    <Flex
      alignItems={"center"}
      color={"ui.white"}
      bgColor={"ui.secondary"}
      m={1}
    >
      <Text ml={1} width={150}>
        Item Basetype
      </Text>
      <Select
        bgColor={"ui.input"}
        color={"ui.white"}
        defaultValue={"Unique"}
        onChange={(e) => handleBaseTypeChange(e)}
        width={150}
        focusBorderColor={"ui.white"}
        borderColor={"ui.grey"}
        mr={1}
        ml={1}
        key={"ItemRarityInput"}
      >
        {baseTypeOptions}
      </Select>
    </Flex>
  );
};
