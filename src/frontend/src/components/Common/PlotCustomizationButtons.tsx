import { Box, Button, Flex, FlexProps } from "@chakra-ui/react";
import { capitalizeFirstLetter } from "../../hooks/utils";
import { usePlotSettingsStore } from "../../store/PlotSettingsStore";
import { CurrencyVisuals } from "../Graph/GraphComponent";

interface PlotCustomizationProps {
  flexProps: FlexProps | undefined;
  mostCommonCurrencyUsed: string;
  chaosVisuals: CurrencyVisuals;
  secondaryVisuals: CurrencyVisuals;
}

const PlotCustomizationButtons = (props: PlotCustomizationProps) => {
  // const mostCommonCurrencyUsed: string = "chaos";
  const mostCommonCurrencyUsed: string = props.mostCommonCurrencyUsed;
  const renderSecondaryCurrency = mostCommonCurrencyUsed !== "chaos";

  const { setShowChaos, setShowSecondary } = usePlotSettingsStore();

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
        bg={props.chaosVisuals.buttonBackground}
        color={props.chaosVisuals.buttonColor}
        _hover={{ bg: "ui.lightInput" }}
        onClick={handleShowChaos}
        borderWidth={1}
        borderColor={props.chaosVisuals.buttonBorderColor}
        mb={[2, 0]}
      >
        Show price in Chaos
      </Button>
      {renderSecondaryCurrency && (
        <Button
          variant="solid"
          bg={props.secondaryVisuals.buttonBackground}
          color={props.secondaryVisuals.buttonColor}
          _hover={{ bg: "ui.lightInput" }}
          borderWidth={1}
          ml={[0, 2]}
          borderColor={props.secondaryVisuals.buttonBorderColor}
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
