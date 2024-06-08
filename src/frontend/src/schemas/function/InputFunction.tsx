export type HandleChangeEventFunction = (
  event: React.ChangeEvent<HTMLSelectElement>
) => void;

export type HandleChangeStringFunction = (s: string) => void;

export type GetValueFunction = () => string | number | undefined;
