import React, { useContext } from 'react';
import '../Customer.css';
import * as requests from "../requests";
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../routes/root';
import * as util from "../util";

const CustomerComponent = () => {
    const navigate = useNavigate();
    const { setAuthenticated } = useContext(AuthContext);

    const handleLogout = async () => {
        const response = await requests.POST_Logout();
        if (response.status === 200) {
            setAuthenticated(false);
            navigate('/'); 
            util.NewNotification.success("Успешно", "Вы вышли из аккаунта");
        } else {
            util.NewNotification.error("Ошибка", "Не удалось выйти из аккаунта");
        }
    };

    return (
        <div className="personal-container">
            <aside className="personal-aside">
                <ul className="personal-aside-list">
                    <li><a href="#" className="personal-aside-link">Личные данные</a></li>
                    <li><a href="#" className="personal-aside-link">Заказы</a></li>
                    <li><a href="#" className="personal-aside-link">Профили заказов</a></li>
                    <li><a href="#" className="personal-aside-link">Избранное</a></li>
                    <button className="personal-exit-button" onClick={handleLogout}>Выход</button>
                </ul>
            </aside>
            {/* Здесь будет основная информация */}
            <div className="personal-info">
                <h1 className="personal-info-title">Личные данные</h1>
                <div className="personal-info-form">
                    <div className="personal-info-form-row">
                        <div className="personal-info-form-group">
                            <label className="personal-info-form-label">ФИО *</label>
                            <input type="text" className="personal-info-form-input" />
                        </div>
                        <div className="personal-info-form-group">
                            <label className="personal-info-form-label">E-mail *</label>
                            <input type="text" className="personal-info-form-input" />
                        </div>
                    </div>
                    <div className="personal-info-form-row">
                        <div className="personal-info-form-group">
                            <label className="personal-info-form-label">Телефон *</label>
                            <input type="text" className="personal-info-form-input" />
                        </div>
                    </div>
                    <div className="personal-info-form-row">
                        <div className="personal-info-form-group">
                            <label className="personal-info-form-label">Пароль</label>
                            <input type="password" className="personal-info-form-input" />
                        </div>
                        <div className="personal-info-form-group">
                            <label className="personal-info-form-label">Подтвердите пароль</label>
                            <input type="password" className="personal-info-form-input" />
                        </div>
                    </div>
                    <button className="personal-save-button">Сохранить</button>
                </div>
                <button className="personal-delete-account-button">Удалить аккаунт</button>
            </div>
        </div>
    );
};

export default CustomerComponent;
