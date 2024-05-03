import { Flex, Select, Text } from "@chakra-ui/react";
import { useGraphInputStore } from "../../../store/GraphInputStore";
import { useEffect } from "react";

export const ItemRarityInput = () => {
  const defaultRarity = undefined;

  const { setItemRarity } = useGraphInputStore();

  const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const itemRarityInput = event.target.value;
    if (itemRarityInput === "Any") {
      setItemRarity(undefined);
    } else {
      setItemRarity(itemRarityInput);
      // console.log(useGraphInputStore.getState().itemSpecState);
    }
  };

  useEffect(() => {
    setItemRarity(defaultRarity);
  }, [defaultRarity, setItemRarity]);

  return (
    <Flex
      alignItems={"center"}
      color={"ui.white"}
      bgColor={"ui.secondary"}
      m={1}
    >
      <Text ml={1} width={150}>
        Item Rarity
      </Text>
      <Select
        bgColor={"ui.input"}
        color={"ui.white"}
        defaultValue={defaultRarity}
        onChange={(e) => handleChange(e)}
        width={150}
        focusBorderColor={"ui.white"}
        borderColor={"ui.grey"}
        mr={1}
        ml={1}
        key={"ItemRarityInput"}
      >
        {
          <option
            value={defaultRarity}
            key={"ItemRarityInput" + "_option_" + "Any"}
            style={{ color: "white", backgroundColor: "#2d3333" }}
          >
            Any
          </option>
        }
        {
          <option
            value={"Unique"}
            key={"ItemRarityInput" + "_option_" + "Unique"}
            style={{ color: "white", backgroundColor: "#2d3333" }}
          >
            Unique
          </option>
        }
        ,
        {
          // Future implementation for non-unique items
          // <option
          //   value={"Non_Unique"}
          //   key={"ItemRarityInput" + "_option_" + "Any Non-Unique"}
          //   style={{ color: "#B3B3B3", backgroundColor: "#2d3333" }}
          // >
          //   Any Non-Unique
          // </option>
        }
      </Select>
    </Flex>
  );
};
