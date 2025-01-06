const tg = window.Telegram.WebApp;

// Инициализация Web App
tg.expand(); // Развернуть приложение на весь экран
tg.MainButton.setText("Submit").show(); // Показать кнопку "Submit"

// Получение данных пользователя
const user = tg.initDataUnsafe.user;
document.getElementById("content").innerHTML = `
    <p>Привет, ${user.first_name}!</p>
    <p>Ваш username: ${user.username}</p>
`;

// Обработка нажатия кнопки
tg.MainButton.onClick(() => {
    tg.sendData("Данные отправлены!");
    tg.close();
});