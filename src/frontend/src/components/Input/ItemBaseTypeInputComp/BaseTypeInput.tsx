import { useGraphInputStore } from "../../../store/GraphInputStore";
import {
    SelectBoxInput,
    SelectBoxOptionValue,
    HandleChangeEventFunction,
} from "../StandardLayoutInput/SelectBoxInput";

export interface BaseType {
    itemBaseTypeId: number;
    baseType: string;
}

interface BaseTypeInputProps {
    baseTypes: BaseType[];
    presetValue: string | undefined;
}

// Base Type Input Component  -  This component is used to select the base type of an item.
export const BaseTypeInput = (props: BaseTypeInputProps) => {
    const { setBaseType } = useGraphInputStore();

    const handleBaseTypeChange: HandleChangeEventFunction = (newValue) => {
        if (newValue) {
            const itemBaseTypeId = Number(newValue?.value);
            const baseType = newValue.label;
            if (baseType === "Any") {
                setBaseType(undefined, undefined);
            } else {
                setBaseType(itemBaseTypeId, baseType);
            }
        }
    };

    const baseTypeOptions: Array<SelectBoxOptionValue> = props.baseTypes.map(
        (baseType) => {
            return {
                value: baseType.itemBaseTypeId.toString(),
                label: baseType.baseType,
                regex: baseType.baseType,
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
