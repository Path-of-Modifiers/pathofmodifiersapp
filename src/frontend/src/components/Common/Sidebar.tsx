import { Button, VStack, Text } from "@chakra-ui/react";

const LinkItems = [
  {
    name: "Watcher's Eye",
    icon: "https://www.poewiki.net/images/6/63/Watcher%27s_Eye_inventory_icon.png",
  },
  {
    name: "Elegant Hubris",
    icon: "https://www.poewiki.net/images/7/75/Elegant_Hubris_inventory_icon.png",
  },
  {
    name: "Forbidden Flame",
    icon: "https://www.poewiki.net/images/6/6d/Forbidden_Flame_inventory_icon.png",
  },
  {
    name: "Glorious Vanity",
    icon: "https://www.poewiki.net/images/9/91/Glorious_Vanity_inventory_icon.png",
  },
  {
    name: "Grand Spectrum",
    icon: "https://www.poewiki.net/images/1/1d/Grand_Spectrum_%28Cobalt_Jewel%2C_power_charge%29_inventory_icon.png",
  },
  {
    name: "Impossible Escape",
    icon: "https://www.poewiki.net/images/e/eb/Impossible_Escape_inventory_icon.png",
  },
  {
    name: "Lethal Pride",
    icon: "https://www.poewiki.net/images/b/b8/Lethal_Pride_inventory_icon.png",
  },
  {
    name: "Militant Faith",
    icon: "https://www.poewiki.net/images/d/da/Militant_Faith_inventory_icon.png",
  },
  {
    name: "Sublime Vision",
    icon: "https://www.poewiki.net/images/e/eb/Sublime_Vision_inventory_icon.png",
  },
  {
    name: "That Which Was Taken",
    icon: "https://www.poewiki.net/images/5/57/That_Which_Was_Taken_inventory_icon.png",
  },
  {
    name: "Voices",
    icon: "https://www.poewiki.net/images/2/28/Voices_inventory_icon.png",
  },
];

const VerticalNavBar = () => {
  return (
    <VStack p="1rem" bg="ui.secondary" opacity={1} align="stretch">
      <Text opacity={0.7} fontSize="menu" color="ui.white">
        Jewels
      </Text>
      {LinkItems.map((item, index) => (
        <Button
          key={index}
          bg="ui.secondary"
          justifyContent="flex-start"
          p={0}
          fontSize="menu"
          fontWeight="fontWeights.normal"
          fontFamily="fonts.sidebar"
          color="ui.white"
          leftIcon={<img src={item.icon} alt={item.name} width="35px" />}
        >
          {item.name}
        </Button>
      ))}
    </VStack>
  );
}

export default VerticalNavBar;
