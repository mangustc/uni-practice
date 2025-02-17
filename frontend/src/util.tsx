export function Num(obj: any, defaultValue = 0): number {
  const out = Number(obj);
  return out ? out : defaultValue;
}

export function Bool(obj: any, defaultValue = false): boolean {
  const out = Boolean(obj);
  return out ? out : defaultValue;
}

export function Str(obj: any, defaultValue = ""): string {
  const out = String(obj);
  return out ? out : defaultValue;
}

export function ArrFromURLSearchParam(obj: string): string[] {
  if (obj.length === 0) {
    return [];
  } else {
    return obj.split(",");
  }
}
