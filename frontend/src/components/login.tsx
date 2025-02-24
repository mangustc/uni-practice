import * as requests from "../requests";
import React, { useState } from 'react';
import '../index.css';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleEmailChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setEmail(event.target.value);
    if (error != '')
      setError('');
  };

  const handlePasswordChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setPassword(event.target.value);
    if (error != '')
      setError('');
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    requests.PUT_Login(email, password)
    .then((obj) => {
      if (obj.status != 200) {
        setError(obj.detail);
      } else {
        setError(obj.detail); // изменить на переход в личный кабинет
      }
    })
  };

  return (
    <div className="login-container-main">
      <div className="login-container">
        <div className="login-header">
          <a href="#" className="login__top-link login__top-link--active title">Вход</a>
          <a href="/registration" className="login__top-link  title">Регистрация</a>
        </div>

        <form className="login__form login__form--w293 form" id="js-loginForm" name="form_auth" onSubmit={handleSubmit}>
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
                />
            </span>
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
                value={password}
                />
            </span>
          </div>

          <button className="form__submit form__submit--mb20  btn btn--red" type="submit">Войти</button>

          <div className="login__links">
            <a href="/customer/restore" className="login__link">Забыли пароль?</a>
            <p>{error}</p> {/*добавлено для тестирования, показ ошибки изменить*/}
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login;
