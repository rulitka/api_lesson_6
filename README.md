<h1 align="center">
Приложение для публикации комиксов в Вконтакте.
   <img src="https://github.com/rulitka/api_lesson_6/blob/master/image.jpg"> 
</h1>

## Описание проекта
Данный проект предназначен для публикации комиксов xkcd в Вконтакте. Соответственно, нужно иметь аккаунт Вконтакте, а также специально созданную группу для публикации комиксов.

## Инсталляция
Для начала нужно установить Python 3 с официального сайта Python.
После этого нужно установить все пакеты, представленные в файле requirements.txt.

```
pip install -r requirements.txt
```

Далее, для того чтобы взаимодействовать с API Вконтакте, необходимо создать приложение на странице Вконтакте для разработчиков и получить ключ доступа пользователя. 
 [Адрес страницы Вконтакте для разработчиков](https://vk.com/dev).

В качестве типа приложения следует указать standalone — это подходящий тип для приложений, которые просто запускаются на компьютере.

Для работы с приложением нам нужно будет кроме секретного ключа пользователя, еще client_id приложения.  Если нажать на кнопку "Редактировать" для нового приложения, в адресной строке вы увидите его client_id. 

Затем нужно будет получить ключ доступа пользователя. Он нужен для того, чтобы ваше приложение имело доступ к вашему аккаунту и могло публиковать сообщения в группах. Ключ можно получить вручную, не написав ни строчки кода. Вам нужно быдует в ссылку, представленную ниже  вписать client_id вашего приложения, и перейти по ней.

[Ссылка для получения секретного ключа](https://oauth.vk.com/authorize?client_id=1&display=page&scope=photos,groups,wall,offline&response_type=token&v=5.120)

В строке браузера вы увидите  access_token — строку наподобие 533bacf01e1165b57531ad114461ae8736d6506a3, это и будет ваш секретный ключ.

Кроме того, вам нужен будет group_id группы, в которой вы будете размещать комиксы.

Узнать group_id для вашей группы можно [здесь](http://regvk.com/id/)

Также, вам нужен будет user_id администратора группы, от имени которого будут размещаться комиксы.

Также нужен будет owner_id владельца группы. Это может быть user_id, либо group_id. В этом случае нужно использовать отрицательное значение для обозначения идентификатора сообщества. Напраимер: -119785763.

Все секретные данные нужно спрятать.

Для этого нужно создать файл .env в котором нужно разместить все секретные ключи от приложения API Вконтакте, в таком виде:

```
access_token=''
access_group_id_vk=''
access_user_id_vk=''
access_owner_id_vk=''
```

## Работа
После создания приложения, группы, получения всех секретных данных и записи их в файл .env, можно запускать файл main.py и при каждом запуске программы на стене группы будет появляться случайный комикс xkcd.

## Лицензия
MIT  © [Akash Nimare](http://akashnimare.in)

## Цели проекта
Этот проект был написан в образовательных целях для веб-разработки на сайте [Devman](https://www.dvmn.org).
