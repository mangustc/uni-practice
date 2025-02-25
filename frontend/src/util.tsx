import { createSearchParams } from "react-router-dom";
import * as objects from "./objects.tsx";
import { toast, ToastContainer } from "react-toastify";

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

function ToastComponent({
  closeToast,
  title,
  text,
  statusClassName,
}: {
  closeToast?: any;
  title: string;
  text: string;
  statusClassName: string;
}) {
  return (
    <div className="toast-container toast-top-right">
      <div className={"toast " + statusClassName} aria-live="polite" style={{}}>
        <button
          type="button"
          className="toast-close-button"
          role="button"
          onClick={closeToast}
        >
          ×
        </button>
        <div className="toast-title">{title}</div>
        <div className="toast-message">{text}</div>
      </div>
    </div>
  );
}

export const NewNotification = {
  success: function(title: string, text: string): any {
    toast(<ToastComponent statusClassName="toast-success" title={title} text={text}/>, {
      // DO NOT TOUCH
      style: { position: "fixed", maxWidth: "0px", maxHeight: "0px", right: "-1000px"}
    })
  }
}
