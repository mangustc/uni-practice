import React, { useState, useEffect } from "react";
import "../index.css";
import { Link } from 'react-router-dom';
import './ForgotPassword.css';
import { POST_RequestPasswordReset } from "../requests"; // Import the new function
import * as util from "../util";

const ForgotPassword = () => {
    const [email, setEmail] = useState("");
    const [emailError, setEmailError] = useState({ isOn: false, detail: "" });
    const [loading, setLoading] = useState(false);

    const handleEmailError = () => {
        if (email.length === 0) {
            setEmailError({ isOn: true, detail: "Это поле обязательно" });
            return;
        }
        const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const check = pattern.test(email);
        if (check) {
            setEmailError({ isOn: false, detail: "" }); // Clear error if valid
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
        if (!emailError.isOn && email.length !== 0) {
            handleEmailError();
        }
    };

    useEffect(() => {
        if (emailError.isOn) {
            handleEmailError();
        }
    }, [email]);

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();

        handleEmailError(); // Валидация email перед отправкой
        if (emailError.isOn) {
            console.log("Ошибка валидации на стороне клиента");
            return;
        }

        setLoading(true);
        try {
            const response = await POST_RequestPasswordReset(email);
            console.log("Ответ от сервера:", response);
            if (response.status === 200) {
                util.NewNotification.success("Успех", "Контрольная строка, а также ваши регистрационные данные были высланы на email. Пожалуйста, дождитесь письма, так как контрольная строка изменяется при каждом запросе.");
            } else {
                util.NewNotification.error("Ошибка", response.detail);
            }
        } catch (error) {
            console.error("Ошибка при отправке запроса:", error);
            util.NewNotification.error("Ошибка", "Не удалось отправить запрос на сброс пароля");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-container-main">
            <div className="login-container forgot_password-container">
                <h3 className="forgot_password-title">Восстановление пароля</h3>
                <p className="forgot_password-text">
                    На этот e-mail вы получите письмо для восстановления пароля
                </p>

            <form className="login__form form forgot_password-form" onSubmit={handleSubmit}>
                <div className="field form__el forgot_password-field">
                    <span className="field__label">E-mail *</span>
                    <span className="field__wrapper">
                        <input
                            className="field__input"
                            type="email"
                            value={email}
                            placeholder="Введите e-mail"
                            name="email"
                            onChange={handleEmailChange}
                            onBlur={handleEmailBlur}
                        />
                    </span>
                    <span className="error">{emailError.detail}</span>
                </div>

                <button
                    className="form__submit_forgot btn btn--red"
                    type="submit"
                    onClick={handleSubmit}
                    disabled={loading}
                >
                    {loading ? "Отправка..." : "Отправить"}
                </button>

                <div className="login__links forgot_password-links">
                    <Link to="/login" className="login__link">
                        Вход
                    </Link>
                    <Link to="/registration" className="login__link">
                        Регистрация
                    </Link>
                </div>
            </form>
        </div>
    </div>
  );
};

export default ForgotPassword;



