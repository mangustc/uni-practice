import * as requests from "../requests";
import * as util from "../util";
import React, { useState, useEffect } from "react";
import "../index.css";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [emailError, setEmailError] = useState({ isOn: false, detail: "" });
  const [passwordError, setPasswordError] = useState({ isOn: false, detail: "" });

  const handleEmailError = () => {
    if (email.length == 0) {
      setEmailError({ isOn: true, detail: "Это поле обязательно" });
      return;
    }
    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const check = pattern.test(email);
    if (check) {
      setEmailError({ isOn: true, detail: "" });
    } else {
      setEmailError({
        isOn: true,
        detail: "Введите корректный адрес эл. почты",
      });
    }
  };
  const handleEmailChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setEmail(event.target.value);
  };
  const handleEmailBlur = () => {
    if (!emailError.isOn && email.length != 0) {
      handleEmailError();
    }
  };
  useEffect(() => {
    if (emailError.isOn) {
      handleEmailError();
    }
  }, [email]);

  const handlePasswordError = () => {
    if (password.length == 0) {
      setPasswordError({ isOn: true, detail: "Это поле обязательно" });
    } else {
      setPasswordError({ isOn: true, detail: "" });
    }
  };
  const handlePasswordChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setPassword(event.target.value);
  };
  const handlePasswordBlur = () => {
    if (!passwordError.isOn && password.length != 0) {
      handlePasswordError();
    }
  };
  useEffect(() => {
    if (passwordError.isOn) {
      handlePasswordError();
    }
  }, [password]);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    let errorValues = [
      { value: emailError, handler: handleEmailError },
      { value: passwordError, handler: handlePasswordError },
    ];

    let flag = false;
    for (const el of errorValues) {
      if (!el.value.isOn) {
        flag = true;
        el.handler();
        continue;
      }
      if (el.value.detail != "") {
        flag = true;
      }
    }
    if (flag) {
      return;
    }

    requests.PUT_Login(email, password).then((obj) => {
      if (obj.status != 200) {
        util.NewNotification.error("Ошибка", obj.detail);
      } else {
        util.NewNotification.success("Успешно", "Авторизация прошла успешно"); // изменить на переход в личный кабинет
      }
    });
  };

  return (
    <div className="login-container-main">
      <div className="login-container">
        <div className="login-header">
          <a href="#" className="login__top-link login__top-link--active title">
            Вход
          </a>
          <a href="/registration" className="login__top-link  title">
            Регистрация
          </a>
        </div>

        <form
          className="login__form login__form--w293 form"
          id="js-loginForm"
          name="form_auth"
          onSubmit={handleSubmit}
        >
          <div className="field form__el">
            <span className="field__label">E-mail *</span>
            <span className="field__wrapper">
              <input
                className="field__input"
                type="email"
                value={email}
                placeholder="Введите e-mail"
                name="USER_LOGIN"
                //required=""
                onChange={handleEmailChange}
                onBlur={handleEmailBlur}
              />
            </span>
            <span className="error">{emailError.detail}</span>
          </div>

          <div className="field form__el">
            <span className="field__label">Пароль *</span>
            <span className="field__wrapper">
              <input
                className="field__input"
                type="password"
                name="USER_PASSWORD"
                placeholder="Введите пароль"
                //required=""
                onChange={handlePasswordChange}
                onBlur={handlePasswordBlur}
                value={password}
              />
            </span>
            <span className="error">{passwordError.detail}</span>
          </div>

          <button
            className="form__submit form__submit--mb20  btn btn--red"
            type="submit"
          >
            Войти
          </button>

          <div className="login__links">
            <a href="/customer/restore" className="login__link">
              Забыли пароль?
            </a>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login;
