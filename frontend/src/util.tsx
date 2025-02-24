import { createSearchParams } from "react-router-dom";
import * as objects from "./objects.tsx";

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

export async function ResponseInfoFromResponse(response: Response): Promise<objects.ResponseInfo> {
  let info: objects.ResponseInfo;
  const data = await response.json();
  if (response.ok) {
    info = {status: response.status, detail: "Успешно"};
  } else if (response.status == 422) {
    info = {status: response.status, detail: "Ошибка валидации"};
  } else {
    info = {status: response.status, detail: data.detail ?? "Непредвиденная ошибка"};
  }
  return(info);
}
