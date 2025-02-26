import * as requests from "../requests";
import * as util from "../util";
import React, { useState, useEffect } from 'react';
import '../index.css';
import { Link } from 'react-router-dom';
import IMask from 'imask';

const Registration = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [phone, setPhone] = useState('');
  const [accountType, setAccountType] = useState('individual');
  const [organizationName, setOrganizationName] = useState('');
  const [inn, setInn] = useState('');

  const [emailError, setEmailError] = useState({isOn: false, detail: ""});
  const [passwordError, setPasswordError] = useState({isOn: false, detail: ""});
  const [confirmPasswordError, setConfirmPasswordError] = useState({isOn: false, detail: ""});
  const [phoneError, setPhoneError] = useState({isOn: false, detail: ""});
  const [organizationNameError, setOrganizationNameError] = useState({isOn: false, detail: ""});
  const [innError, setInnError] = useState({isOn: false, detail: ""});

  const [error, setError] = useState('');

  window.onload = function () {
    const phoneMask = document.querySelector("input[type='tel']");
    if (phoneMask)
      IMask(phoneMask as HTMLInputElement, {mask: "+{7} (000) 000 00 00"});
  };

  useEffect(() => {
    const phoneMask = document.querySelector("input[type='tel']");
    if (phoneMask)
      IMask(phoneMask as HTMLInputElement, {mask: "+{7} (000) 000 00 00"});
  }, [accountType]);

  
  const handleEmailError = () => {
    if (email.length == 0) {
      setEmailError({isOn: true, detail: "Это поле обязательно"});
      return;
    }
    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const check = pattern.test(email);
    if (check) {
      setEmailError({isOn: true, detail: ""});
    } else {
      setEmailError({isOn: true, detail: "Введите корректный адрес эл. почты"});
    }
  }
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
      setPasswordError({isOn: true, detail: "Это поле обязательно"});
      return;
    }
    if (password.length < 8) {
      setPasswordError({isOn: true, detail: "Пожалуйста, введите не меньше 8 символов."});
    } else {
      setPasswordError({isOn: true, detail: ""});
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


  const handleConfirmPasswordError = () => {
    if (confirmPassword.length == 0) {
      setConfirmPasswordError({isOn: true, detail: "Это поле обязательно"});
    } else {
      setConfirmPasswordError({isOn: true, detail: ""});
    }
  };
  const handleConfirmPasswordChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setConfirmPassword(event.target.value);
  };
  const handleConfirmPasswordBlur = () => {
    if (!confirmPasswordError.isOn && confirmPassword.length != 0) {
      handleConfirmPasswordError();
    }
  };
  useEffect(() => {
    if (confirmPasswordError.isOn) {
      handleConfirmPasswordError();
    }
  }, [confirmPassword]);


  const handlePhoneError = () => {
    if (phone.length == 0) {
      setPhoneError({isOn: true, detail: "Это поле обязательно"});
      return;
    } 
    if (phone.length != 18) {
      setPhoneError({isOn: true, detail: "Заполните поле до конца."});
    } else {
      setPhoneError({isOn: true, detail: ""});
    }
  }
  const handlePhoneChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setPhone(event.target.value);
  };
  const handlePhoneBlur = () => {
    if (!phoneError.isOn && phone.length != 0) {
      handlePhoneError();
    }
  };
  useEffect(() => {
    if (phoneError.isOn) {
      handlePhoneError();
    }
  }, [phone]);


  const handleOrganizationNameError = () => {
    if (organizationName.length == 0) {
      setOrganizationNameError({isOn: true, detail: "Это поле обязательно"});
    } else {
      setOrganizationNameError({isOn: true, detail: ""});
    }
  }
  const handleOrganizationNameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setOrganizationName(event.target.value);
  };
  const handleOrganizationNameBlur = () => {
    if (!organizationNameError.isOn && organizationName.length != 0) {
      handleOrganizationNameError();
    }
  };
  useEffect(() => {
    if (organizationNameError.isOn) {
      handleOrganizationNameError();
    }
  }, [organizationName]);


  const handleInnError = () => {
    if (inn.length == 0) {
      setInnError({isOn: true, detail: "Это поле обязательно"});
      return;
    }
    if (inn.length != 10) {
      setInnError({isOn: true, detail: "Введите 10 символов."});
    } else {
      setInnError({isOn: true, detail: ""});
    }
  };
  const handleInnChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = event.target.value.replace(/\D/g, '');
    setInn(newValue);
  };
  const handleInnBlur = () => {
    if (!innError.isOn && inn.length != 0) {
      handleInnError();
    }
  };
  useEffect(() => {
    if (innError.isOn) {
      handleInnError();
    }
  }, [inn]);


  const handleAccountTypeChange = (type: string) => {
    setAccountType(type);
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    let errorValues = [
      {value: emailError, handler: handleEmailError},
      {value: phoneError, handler: handlePhoneError},
      {value: passwordError, handler: handlePasswordError},
      {value: confirmPasswordError, handler: handleConfirmPasswordError}
    ];

    if (accountType != "individual") {
      errorValues.push({value: organizationNameError, handler: handleOrganizationNameError});
      errorValues.push({value: innError, handler: handleInnError});
    }

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

    if (accountType == "individual") {
      requests.POST_Register(email, password, confirmPassword, phone)
      .then((obj) => {
        if (obj.status != 201) {
          util.NewNotification.error("Ошибка", obj.detail);
        } else {
          util.NewNotification.success("Успешно", "Регистрация прошла успешно"); // изменить на переход в личный кабинет
        }
      })
    }
    if (accountType == "legal") {
      requests.POST_RegisterLegal(email, password, confirmPassword, phone, organizationName, inn)
      .then((obj) => {
        if (obj.status != 201) {
          util.NewNotification.error("Ошибка", obj.detail);
        } else {
          util.NewNotification.success("Успешно", "Регистрация прошла успешно"); // изменить на переход в личный кабинет
        }
      })
    }
    if (accountType == "ip") {
      requests.POST_RegisterIP(email, password, confirmPassword, phone, organizationName, inn)
      .then((obj) => {
        if (obj.status != 201) {
          util.NewNotification.error("Ошибка", obj.detail);
        } else {
          util.NewNotification.success("Успешно", "Регистрация прошла успешно"); // изменить на переход в личный кабинет
        }
      })
    }
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
                    placeholder="Введите e-mail"
                    name="email"
                    //required=""
                    onChange={handleEmailChange}
                    onBlur={handleEmailBlur}
                    value={email}
                  />
                </span>
                <span className="error">{emailError.detail}</span>
              </div>

              <div className="registration-new-field form__el">
                <span className="registration-new-field__label">Телефон *</span>
                <span className="registration-new-field__wrapper">
                  <input
                    className="field__input"
                    type="tel"
                    placeholder="+7 (___) ___ __ __"
                    name="phone"
                    //required=""
                    onChange={handlePhoneChange}
                    onBlur={handlePhoneBlur}
                    value={phone}
                  />
                </span>
                <span className="error">{phoneError.detail}</span>
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
                    onBlur={handleOrganizationNameBlur}
                    value={organizationName}
                  />
                </span>
                <span className="error">{organizationNameError.detail}</span>
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
                    onBlur={handleInnBlur}
                    value={inn}
                  />
                </span>
                <span className="error">{innError.detail}</span>
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
                    onBlur={handlePasswordBlur}
                    value={password}
                  />
                </span>
                <span className="error">{passwordError.detail}</span>
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
                    onBlur={handleConfirmPasswordBlur}
                    value={confirmPassword}
                  />
                </span>
                <span className="error">{confirmPasswordError.detail}</span>
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
                    placeholder="Введите e-mail"
                    name="email"
                    //required=""
                    onChange={handleEmailChange}
                    onBlur={handleEmailBlur}
                    value={email}
                  />
                </span>
                <span className="error">{emailError.detail}</span>
              </div>

              <div className="registration-new-field form__el">
                <span className="registration-new-field__label">Телефон *</span>
                <span className="registration-new-field__wrapper">
                  <input
                    className="field__input"
                    type="tel"
                    placeholder="+7 (___) ___ __ __"
                    name="phone"
                    //required=""
                    onChange={handlePhoneChange}
                    onBlur={handlePhoneBlur}
                    value={phone}
                  />
                </span>
                <span className="error">{phoneError.detail}</span>
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
                    onBlur={handlePasswordBlur}
                    value={password}
                  />
                </span>
                <span className="error">{passwordError.detail}</span>
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
                    onBlur={handleConfirmPasswordBlur}
                    value={confirmPassword}
                  />
                </span>
                <span className="error">{confirmPasswordError.detail}</span>
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