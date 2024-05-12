import { Flex, Select, Text } from "@chakra-ui/react";
import { useGraphInputStore } from "../../../store/GraphInputStore";
import { BaseType } from "../../../client";

interface BaseTypeInputProps {
  baseTypes: BaseType | BaseType[];
}

// Base Type Input Component  -  This component is used to select the base type of an item.
export const BaseTypeInput = ({ baseTypes }: BaseTypeInputProps) => {
  if (!Array.isArray(baseTypes)) {
    baseTypes = [baseTypes];
  }

  const defaultValue = undefined;

  const { setBaseType } = useGraphInputStore();

  const getBaseTypeValue = () => {
    const baseType = useGraphInputStore.getState().baseSpec?.baseType;
    if (baseType) {
      return baseType;
    } else {
      return "";
    }
  };

  const handleBaseTypeChange = (
    event: React.ChangeEvent<HTMLSelectElement>
  ) => {
    const baseType = event.target.value;
    if (baseType === "Any") {
      setBaseType(undefined);
    }
    setBaseType(baseType);
  };

  let baseTypeOptions: JSX.Element[] = [];
  if (baseTypes !== undefined) {
    baseTypeOptions = baseTypes.map((baseType) => {
      return (
        <option
          value={baseType.baseType}
          key={"BaseTypeInput" + "_option_" + baseType.baseType}
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
        Item Base Type
      </Text>
      <Select
        value={getBaseTypeValue()}
        bgColor={"ui.input"}
        color={"ui.white"}
        onChange={(e) => handleBaseTypeChange(e)}
        width={150}
        focusBorderColor={"ui.white"}
        borderColor={"ui.grey"}
        mr={1}
        ml={1}
        key={"baseTypeInput"}
      >
        <option
          value={defaultValue}
          key={"baseType" + "_option_" + "any"}
          style={{ color: "white", backgroundColor: "#2d3333" }}
        >
          Any
        </option>
        {baseTypeOptions}
      </Select>
    </Flex>
  );
};
