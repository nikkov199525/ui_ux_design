@startuml

actor Пользователь as U
actor Скринридер as SR

rectangle "Веб-приложение База доступных видеоигр" {

    U -- (Открытие сайта)
    (Открытие сайта) -- (Просмотр главной страницы) : запускает
    SR -- (Просмотр главной страницы) : озвучивает

    (Просмотр главной страницы) --> (Переход к разделу Игры)
    SR -- (Переход к разделу Игры) : озвучивает
    (Переход к разделу Игры) --> (Просмотр каталога игр)
    SR -- (Просмотр каталога игр) : озвучивает

    (Просмотр каталога игр) --> (Ввод поиска)
    SR -- (Ввод поиска) : озвучивает
    (Ввод поиска) --> (Просмотр результатов поиска)
    SR -- (Просмотр результатов поиска) : озвучивает

    (Просмотр каталога игр) --> (Переход к добавлению игры)
    SR -- (Переход к добавлению игры) : озвучивает
    (Переход к добавлению игры) --> (Заполнение формы добавления игры)
    SR -- (Заполнение формы добавления игры) : озвучивает
    (Заполнение формы добавления игры) --> (Отправка формы)
    SR -- (Отправка формы) : озвучивает
    (Отправка формы) --> (Просмотр информации об игре)
    SR -- (Просмотр информации об игре) : озвучивает
    (Просмотр каталога игр) --> (Просмотр информации об игре)
    SR -- (Просмотр информации об игре) : озвучивает
    (Просмотр информации об игре) --> (Редактирование игры)
    SR -- (Редактирование игры) : озвучивает
    (Редактирование игры) --> (Отправка формы)
    SR -- (Отправка формы) : озвучивает
    (Редактирование игры) --> (Удаление игры)
    SR -- (Удаление игры) : озвучивает
    (Просмотр главной страницы) --> (Переход к регистрации)
    SR -- (Переход к регистрации) : озвучивает
    (Переход к регистрации) --> (Заполнение формы регистрации)
    SR -- (Заполнение формы регистрации) : озвучивает
    (Просмотр главной страницы) --> (Переход ко входу)
    SR -- (Переход ко входу) : озвучивает
    (Переход ко входу) --> (Заполнение формы входа)
    SR -- (Заполнение формы входа) : озвучивает
    (Просмотр главной страницы) --> (Переход к восстановлению пароля)
    SR -- (Переход к восстановлению пароля) : озвучивает
    (Переход к восстановлению пароля) --> (Заполнение формы восстановления пароля)
    SR -- (Заполнение формы восстановления пароля) : озвучивает
}

@enduml
