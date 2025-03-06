import React, { useContext, useState, useEffect } from 'react';
import '../Customer.css';
import * as requests from "../requests";
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../routes/root';
import * as util from "../util";
import IMask from "imask";

const CustomerComponent = () => {
  const navigate = useNavigate();
  const { setAuthenticated } = useContext(AuthContext);
  const [customer, setCustomer] = useState({
    name: '',
    surname: '',
    email: '',
    number: '',
  });
  const [newData, setNewData] = useState({
    fullName: '',
    number: '',
    password: '',
    confirmPassword: '',
  });

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

  useEffect(() => {
    const phoneMask = document.querySelector("input[name='number']");
    if (phoneMask)
      IMask(phoneMask as HTMLInputElement, { mask: "+{7} (000) 000 00 00" });
  }, []);

  useEffect(() => {
    const fetchUserInfo = async () => {
      try {
        const userInfo = await requests.GET_GetUserInfo();
        setCustomer({
          name: userInfo.name || '',
          surname: userInfo.surname || '',
          email: userInfo.email || '',
          number: userInfo.number || '',
        });
        setNewData({
          fullName: `${userInfo.name || ''} ${userInfo.surname || ''}`,
          number: userInfo.number || '',
          password: '',
          confirmPassword: '',
        });
      } catch (error) {
        console.error('Ошибка при получении данных пользователя:', error);
      }
    };

    fetchUserInfo();
  }, []);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setNewData(prevState => ({ ...prevState, [name]: value }));
  };

  const handleSaveChanges = async () => {
    if (newData.password && newData.confirmPassword) {
      if (newData.password !== newData.confirmPassword) {
        util.NewNotification.error("Ошибка", "Пароли не совпадают");
        return;
      }
    }

    const [name, surname] = newData.fullName.trim().split(' ').filter(Boolean);
    const dataToSend = {
        name: name || '',
        surname: surname || '',
        number: newData.number,
        password: newData.password,
        confirm_password: newData.confirmPassword,
      };  
    console.log("Отправляем на сервер:", dataToSend); // Выводим данные перед отправкой
    try {
      const response = await requests.PUT_UpdateUserInfo(
        name || '',
        surname || '',
        newData.number,
        newData.password,
        newData.confirmPassword
      );
      util.NewNotification.success("Успешно", "Данные пользователя обновлены");
      const updatedUserInfo = await requests.GET_GetUserInfo();
      setCustomer({
        name: updatedUserInfo.name || '',
        surname: updatedUserInfo.surname || '',
        email: updatedUserInfo.email || '',
        number: updatedUserInfo.number || '',
      });
      setNewData({
        fullName: `${updatedUserInfo.name || ''} ${updatedUserInfo.surname || ''}`,
        number: updatedUserInfo.number || '',
        password: '',
        confirmPassword: '',
      });
    } catch (error) {
      util.NewNotification.error("Ошибка", "Не удалось обновить данные пользователя");
    }
  };

  return (
    <div className="personal-container">
      <aside className="personal-aside">
        <ul className="personal-aside-list">
          <li><a href="#" className="personal-aside-link">Личные данные</a></li>
          <li><a href="#" className="personal-aside-link">Заказы</a></li>
          <li><a href="#" className="personal-aside-link">Профили заказов</a></li>
          <li><a href="/favorites" className="personal-aside-link">Избранное</a></li>
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
              <input 
                type="text" 
                className="personal-info-form-input" 
                name="fullName" 
                value={newData.fullName} 
                onChange={handleInputChange} 
              />
            </div>
            <div className="personal-info-form-group">
              <label className="personal-info-form-label">E-mail *</label>
              <input 
                type="text" 
                className="personal-info-form-input" 
                value={customer.email} 
                readOnly 
              />
            </div>
          </div>
          <div className="personal-info-form-row">
           <div className="personal-info-form-group">
            <label className="personal-info-form-label">Телефон *</label>
             <input 
              type="text" 
              className="personal-info-form-input" 
              name="number" 
              value={newData.number} 
              onChange={handleInputChange} 
              placeholder="+7 (XXX) XXX XX XX"
             />
            </div>
         </div>
          <div className="personal-info-form-row">
            <div className="personal-info-form-group">
              <label className="personal-info-form-label">Пароль</label>
              <input 
                type="password" 
                className="personal-info-form-input" 
                name="password" 
                value={newData.password} 
                onChange={handleInputChange} 
              />
            </div>
            <div className="personal-info-form-group">
              <label className="personal-info-form-label">Подтвердите пароль</label>
              <input 
                type="password" 
                className="personal-info-form-input" 
                name="confirmPassword" 
                value={newData.confirmPassword} 
                onChange={handleInputChange} 
              />
            </div>
          </div>
          <button className="personal-save-button" onClick={handleSaveChanges}>Сохранить</button>
        </div>
        <button className="personal-delete-account-button">Удалить аккаунт</button>
      </div>
    </div>
  );
};

export default CustomerComponent;

