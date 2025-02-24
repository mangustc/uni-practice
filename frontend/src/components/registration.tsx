import React, { useState } from 'react';
import '../index.css';
import { Link } from 'react-router-dom';

const Registration = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [phone, setPhone] = useState('');
  const [accountType, setAccountType] = useState('individual');
    const [organizationName, setOrganizationName] = useState('');
  const [inn, setInn] = useState('');

  const handleEmailChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setEmail(event.target.value);
  };

  const handlePasswordChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setPassword(event.target.value);
  };

  const handleConfirmPasswordChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setConfirmPassword(event.target.value);
  };

  const handlePhoneChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setPhone(event.target.value);
  };

   const handleOrganizationNameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setOrganizationName(event.target.value);
  };

  const handleInnChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInn(event.target.value);
  };

  const handleAccountTypeChange = (type: string) => {
    setAccountType(type);
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    // Логика отправки данных на сервер
  };

  return (
    <div className="registration-container-main">
      <div className="registration-container">
        <div className="login-header1">
          <Link to="/login" className="login__top-link title">Вход</Link>
          <Link to="/registration" className="login__top-link registration__top-link--active title">Регистрация</Link>
        </div>

        <div className="registration__type">
          <span
            className={`registration__type-link ${accountType === 'individual' ? 'registration__type-link--active' : ''}`}
            onClick={() => handleAccountTypeChange('individual')}
          >
            Физическое лицо
          </span>
          <span
            className={`registration__type-link ${accountType === 'legal' ? 'registration__type-link--active' : ''}`}
            onClick={() => handleAccountTypeChange('legal')}
          >
            Юридическое лицо
          </span>
          <span
            className={`registration__type-link ${accountType === 'ip' ? 'registration__type-link--active' : ''}`}
            onClick={() => handleAccountTypeChange('ip')}
          >
            ИП
          </span>
        </div>

        {accountType !== 'individual' && (
          <form className="registration__form form" onSubmit={handleSubmit}>
            <div className="registration-fields-wrapper">
              <div className="registration-new-field form__el">
                <span className="registration-new-field__label">E-mail *</span>
                <span className="registration-new-field__wrapper">
                  <input
                    className="field__input"
                    type="email"
                    value={email}
                    placeholder="Введите e-mail"
                    name="email"
                    //required=""
                    onChange={handleEmailChange}
                  />
                </span>
              </div>

              <div className="registration-new-field form__el">
                <span className="registration-new-field__label">Телефон *</span>
                <span className="registration-new-field__wrapper">
                  <input
                    className="field__input"
                    type="tel"
                    value={phone}
                    placeholder="+7 (___) ___-__-__"
                    name="phone"
                    //required=""
                    onChange={handlePhoneChange}
                  />
                </span>
              </div>
              <div className="registration-new-field form__el">
                <span className="registration-new-field__label">Наименование организации *</span>
                <span className="registration-new-field__wrapper">
                  <input
                    className="field__input"
                    type="text"
                    name="organizationName"
                    placeholder="Введите наименование организации"
                    //required=""
                    onChange={handleOrganizationNameChange}
                    value={organizationName}
                  />
                </span>
              </div>

              <div className="registration-new-field form__el">
                <span className="registration-new-field__label">ИНН *</span>
                <span className="registration-new-field__wrapper">
                  <input
                    className="field__input"
                    type="text"
                    name="inn"
                    placeholder="Введите ИНН"
                    // required=""
                    onChange={handleInnChange}
                    value={inn}
                  />
                </span>
              </div>

              <div className="registration-new-field form__el">
                <span className="registration-new-field__label">Пароль *</span>
                <span className="registration-new-field__wrapper">
                  <input
                    className="field__input"
                    type="password"
                    name="password"
                    placeholder="Введите пароль"
                    //required=""
                    onChange={handlePasswordChange}
                    value={password}
                  />
                </span>
              </div>

              <div className="registration-new-field form__el">
                <span className="registration-new-field__label">Подтвердите пароль *</span>
                <span className="registration-new-field__wrapper">
                  <input
                    className="field__input"
                    type="password"
                    name="confirmPassword"
                    placeholder="Подтвердите пароль"
                    //required=""
                    onChange={handleConfirmPasswordChange}
                    value={confirmPassword}
                  />
                </span>
              </div>
            </div>

            <button className="form__submit  btn btn--red" type="submit">Зарегистрироваться</button>

            <p className="registration__agreement">
              Нажимая на кнопку, вы соглашаетесь с
              <a href="#" className="registration__link"> Политикой конфиденциальности</a>
            </p>
          </form>
        )}
           {accountType === 'individual' && (
          <form className="registration__form form" onSubmit={handleSubmit}>
            <div className="registration-fields-wrapper">
              <div className="registration-new-field form__el">
                <span className="registration-new-field__label">E-mail *</span>
                <span className="registration-new-field__wrapper">
                  <input
                    className="field__input"
                    type="email"
                    value={email}
                    placeholder="Введите e-mail"
                    name="email"
                    //required=""
                    onChange={handleEmailChange}
                  />
                </span>
              </div>

              <div className="registration-new-field form__el">
                <span className="registration-new-field__label">Телефон *</span>
                <span className="registration-new-field__wrapper">
                  <input
                    className="field__input"
                    type="tel"
                    value={phone}
                    placeholder="+7 (___) ___-__-__"
                    name="phone"
                    //required=""
                    onChange={handlePhoneChange}
                  />
                </span>
              </div>

              <div className="registration-new-field form__el">
                <span className="registration-new-field__label">Пароль *</span>
                <span className="registration-new-field__wrapper">
                  <input
                    className="field__input"
                    type="password"
                    name="password"
                    placeholder="Введите пароль"
                    //required=""
                    onChange={handlePasswordChange}
                    value={password}
                  />
                </span>
              </div>

              <div className="registration-new-field form__el">
                <span className="registration-new-field__label">Подтвердите пароль *</span>
                <span className="registration-new-field__wrapper">
                  <input
                    className="field__input"
                    type="password"
                    name="confirmPassword"
                    placeholder="Подтвердите пароль"
                    //required=""
                    onChange={handleConfirmPasswordChange}
                    value={confirmPassword}
                  />
                </span>
              </div>
            </div>

            <button className="form__submit  btn btn--red" type="submit">Зарегистрироваться</button>

            <p className="registration__agreement">
              Нажимая на кнопку, вы соглашаетесь с
              <a href="#" className="registration__link"> Политикой конфиденциальности</a>
            </p>
          </form>
        )}
      </div>
    </div>
  );
};

export default Registration;