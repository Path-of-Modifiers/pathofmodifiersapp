import { Button, Flex, FlexProps } from "@chakra-ui/react";
import { capitalizeFirstLetter } from "../../hooks/utils";
import { usePlotSettingsStore } from "../../store/PlotSettingsStore";

interface PlotCustomizationButtonsProps {
  flexProps: FlexProps | undefined;
  mostCommonCurrencyUsed: string;
}

const PlotCustomizationButtons = (props: PlotCustomizationButtonsProps) => {
  const mostCommonCurrencyUsed: string = props.mostCommonCurrencyUsed;
  const renderButtons = mostCommonCurrencyUsed !== "chaos";

  const { showChaos, setShowChaos, showSecondary, setShowSecondary } = usePlotSettingsStore();

  const handleShowChaos = () => {
    setShowChaos(true);
    setShowSecondary(false);
  };
  const handleShowSecondary = () => {
    setShowChaos(false);
    setShowSecondary(true);
  };

  return (
    renderButtons && (
      <Flex
        {...props.flexProps}
        direction={["column", "row"]} // Column for small screens, row for larger screens
        maxW="98vw"
        flexWrap="wrap"
      >
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
      </Flex>
    )
  );
};

export default PlotCustomizationButtons;
