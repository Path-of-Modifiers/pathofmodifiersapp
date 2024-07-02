export type HandleChangeEventFunction = (
  event: React.FormEvent<HTMLElement> | React.ChangeEvent<HTMLInputElement>,
  value?: string | number | undefined
) => void;

export type HandleChangeStringFunction = (s: string) => void;

export type GetValueFunction = () => string | number | undefined;
