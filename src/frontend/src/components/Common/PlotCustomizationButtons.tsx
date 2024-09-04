import { Box, Button, Flex, FlexProps } from "@chakra-ui/react";
import { capitalizeFirstLetter } from "../../hooks/utils";
import { usePlotSettingsStore } from "../../store/PlotSettingsStore";

interface PlotCustomizationProps {
  flexProps: FlexProps | undefined;
  mostCommonCurrencyUsed: string;
}

const PlotCustomizationButtons = (props: PlotCustomizationProps) => {
  // const mostCommonCurrencyUsed: string = "chaos";
  const mostCommonCurrencyUsed: string = props.mostCommonCurrencyUsed;
  const renderSecondaryCurrency = mostCommonCurrencyUsed !== "chaos";

  const { setShowChaos, setShowSecondary } = usePlotSettingsStore();
  const showChaos = usePlotSettingsStore((state) => state.showChaos);
  const showSecondary = usePlotSettingsStore((state) => state.showSecondary);

  const handleShowChaos = () => {
    setShowChaos();
  };
  const handleShowSecondary = () => {
    setShowSecondary();
  };

  return (
    <Flex
      {...props.flexProps}
      direction={["column", "row"]} // Column for small screens, row for larger screens
      alignItems="center"
      maxW="98vw"
      flexWrap="wrap"
    >
      <Box
        width="10vw"
        flex={["none", "1"]}
        mb={[4, 20]}
        alignContent={"center"}
      ></Box>{" "}
      {/* Empty space for centering the middle item */}
      <Button
        variant="solid"
        bg={showChaos ? "#f99619" : "ui.lightInput"}
        color="#000000"
        _hover={{ bg: "ui.lightInput" }}
        onClick={handleShowChaos}
        borderWidth={1}
        borderColor="#000000"
        mb={[2, 0]}
      >
        Show price in Chaos
      </Button>
      {renderSecondaryCurrency && (
        <Button
          variant="solid"
          bg={showSecondary ? "ui.white" : "ui.lightInput"}
          color={showSecondary ? "#ff0000" : "#000000"}
          _hover={{ bg: "ui.lightInput" }}
          borderWidth={1}
          ml={[0, 2]}
          borderColor={showSecondary ? "#ff0000" : "#000000"}
          onClick={handleShowSecondary}
        >
          Show price in {capitalizeFirstLetter(mostCommonCurrencyUsed)}
        </Button>
      )}
      <Box
        width="10vw"
        flex={["none", "1"]}
        mb={[4, 20]}
        alignContent={"center"}
      ></Box>{" "}
      {/* Empty space for centering the middle item */}
    </Flex>
  );
};

export default PlotCustomizationButtons;
