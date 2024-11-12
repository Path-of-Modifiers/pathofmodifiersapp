import { useGraphInputStore } from "../../../store/GraphInputStore";
import {
    SelectBoxInput,
    SelectBoxOptionValue,
    HandleChangeEventFunction,
} from "../StandardLayoutInput/SelectBoxInput";

interface BaseTypeInputProps {
    baseTypes: string[];
    presetValue: string | undefined;
}

// Base Type Input Component  -  This component is used to select the base type of an item.
export const BaseTypeInput = (props: BaseTypeInputProps) => {
    const { choosableItemBaseType, setBaseType } = useGraphInputStore();

    const handleBaseTypeChange: HandleChangeEventFunction = (newValue) => {
        if (newValue) {
            const baseType = newValue?.value;
            const itemBaseType = choosableItemBaseType.find(
                (choosableItemBaseType) => choosableItemBaseType.baseType === baseType,
            );
            if (itemBaseType == null) {
                throw "Couldn't find the base type in choosable item base type array";
            }
            if (baseType === "Any") {
                setBaseType(undefined);
            } else {
                setBaseType(itemBaseType.itemBaseTypeId);
            }
        }
    };

    const baseTypeOptions: Array<SelectBoxOptionValue> = props.baseTypes.map(
        (baseType) => {
            return {
                value: baseType,
                label: baseType,
                regex: baseType,
            };
        },
    );

    return (
        <SelectBoxInput
            descriptionText={"Item Base Type"}
            optionsList={baseTypeOptions}
            defaultText={props.presetValue ? props.presetValue : "Any"}
            multipleValues={false}
            handleChange={handleBaseTypeChange}
            id={"baseTypeInput-0"}
            canBeAny={true}
        />
    );
};
