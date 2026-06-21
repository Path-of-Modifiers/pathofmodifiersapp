import { Box, HStack, Text, Wrap } from "@chakra-ui/layout";
import { ModifierOption } from "./ModifierInput";
import { useState } from "react";
import { FancyModifierInput } from "./FancyModifierInput";

interface FancyModifierInputProps {
    selectedModifier: ModifierOption;
    index: number;
    isDimmed?: boolean;
}
export type HandleChangeEventFunction = (
    isNumerical: boolean,
    modifierId: number,
    value: string | undefined,
    index_to_handle: number,
    numericalType?: string,
    textRolls?: string
) => void;

export const FancySelectedModifier = (props: FancyModifierInputProps) => {
    const selectedModifier = props.selectedModifier;

    const splitSelectedModiferLabel = selectedModifier.label.split("#");

    const [currentlyTakingInput, setCurrentlyTakingInput] = useState<boolean[]>(
        Array(splitSelectedModiferLabel.length).fill(false)
    );

    const changeTakingInput = (labelIndex: number) => {
        if (props.isDimmed) {
            return;
        }
        setCurrentlyTakingInput([
            ...currentlyTakingInput.slice(0, labelIndex),
            !currentlyTakingInput[labelIndex],
            ...currentlyTakingInput.slice(labelIndex + 1),
        ]);
    };

    return (
        <Box
            color="ui.white"
            display="flex"
            key={`fancyInput-${props.index}`}
            bgColor="ui.input"
            border="1px"
            borderRadius="lg"
            borderColor="ui.grey"
            p={1}
            whiteSpace="preserve"
            w="100%"
            opacity={props.isDimmed ? 0.5 : 1}
        >
            <Wrap spacing="1px">
                {splitSelectedModiferLabel.map(
                    (labelPart, labelIndex, splitSelectedModifer) => {
                        const labelPartSplit = labelPart.split(" ");
                        const isNotEnd =
                            splitSelectedModifer.length !== labelIndex + 1;
                        return labelPartSplit.map((word, wordIndex) => {
                            if (
                                wordIndex < labelPartSplit.length - 1 ||
                                !isNotEnd
                            ) {
                                return (
                                    <Text
                                        verticalAlign="center"
                                        key={`fancySelectedModifier-${props.index}-${wordIndex}`}
                                    >
                                        {word + " "}
                                    </Text>
                                );
                            } else if (isNotEnd) {
                                const textRolls =
                                    selectedModifier.groupedModifierProperties
                                        .textRolls[labelIndex] ?? undefined;
                                const modifierId =
                                    selectedModifier.groupedModifierProperties
                                        .modifierId[labelIndex];
                                return (
                                    <HStack
                                        spacing={0}
                                        verticalAlign="center"
                                        h={5}
                                        pt={1}
                                        key={`fancySelectedModifier-${props.index}-fancyInput-${wordIndex}`}
                                    >
                                        <Text verticalAlign="center">
                                            {word}
                                        </Text>
                                        <FancyModifierInput
                                            currentlyTakingInput={
                                                currentlyTakingInput[labelIndex]
                                            }
                                            modifierId={modifierId}
                                            selectedModifierIndex={props.index}
                                            textRolls={textRolls}
                                            orderIndex={labelIndex}
                                            changeTakingInput={
                                                changeTakingInput
                                            }
                                        />
                                    </HStack>
                                );
                            }
                        });
                    }
                )}
            </Wrap>
        </Box>
    );
};
