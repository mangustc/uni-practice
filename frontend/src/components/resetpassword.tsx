import React, { useState } from "react";
import { useParams, Link, useNavigate } from 'react-router-dom';
import "../index.css";
import './ForgotPassword.css';
import * as util from "../util";
import { BACKEND_URL } from "../requests"; 

const ResetPassword = () => {
    const { token } = useParams();
    const [newPassword, setNewPassword] = useState("");
    const [reNewPassword, setReNewPassword] = useState("");
    const [passwordError, setPasswordError] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate(); 

    const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setNewPassword(e.target.value);
    };

    const handleRePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setReNewPassword(e.target.value);
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (newPassword !== reNewPassword) {
            setPasswordError("Пароли не совпадают");
            return;
        }

        setLoading(true);
        try {
            const response = await fetch(`${BACKEND_URL}/user/reset_password/${token}`, { 
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: new URLSearchParams({
                    new_password: newPassword,
                    re_new_password: reNewPassword,
                }),
            });

            const data = await response.json();

            if (response.ok) {
                util.NewNotification.success("Успех", data.message);
                navigate('/login');
            } else {
                util.NewNotification.error("Ошибка", data.detail);
            }
        } catch (error) {
            console.error("Ошибка при отправке запроса:", error);
            util.NewNotification.error("Ошибка", "Не удалось сбросить пароль");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-container-main">
            <div className="login-container forgot_password-container">
                <h3 className="forgot_password-title">Создание нового пароля</h3>

                <form className="login__form form forgot_password-form" onSubmit={handleSubmit}>
                    <div className="field form__el forgot_password-field">
                        <span className="field__label">Новый пароль *</span>
                        <span className="field__wrapper">
                            <input
                                className="field__input"
                                type="password"
                                id="new_password"
                                name="new_password"
                                value={newPassword}
                                onChange={handlePasswordChange}
                            />
                        </span>
                    </div>

                    <div className="field form__el forgot_password-field">
                        <span className="field__label">Подтвердите новый пароль *</span>
                        <span className="field__wrapper">
                            <input
                                type="password"
                                id="re_new_password"
                                name="re_new_password"
                                className="field__input"
                                value={reNewPassword}
                                onChange={handleRePasswordChange}
                            />
                        </span>
                    </div>

                    {passwordError && <div className="error">{passwordError}</div>}

                    <button
                        className="form__submit_forgot btn btn--red"
                        type="submit"
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

export default ResetPassword;

