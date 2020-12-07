# Урок 3. Системы управления базами данных MongoDB и SQLite в Python

## Практическое задание

### Постановка задачи

- Источник: https://geekbrains.ru/posts/
- Необходимо обойти все записи в блоге
и извлеч из них информацию следующих полей:
  - url страницы материала
  - заголовок материала
  - первое изображение материала (cсылка)
  - дата публикации (формат datetime)
  - имя автора материала
  - ссылка на страницу автора материала
  - комментарии в виде:
    - автор
    - текст
  - список тегов
  - реализовать SQL-структуру хранения данных
  cо следующими таблицами:
    - Post
    - Comment
    - Writer
    - Tag
- Организовать реляционные связи между таблицами
- При сборе данных учесть,
что полученый из данных автор уже может быть в БД,
и значит необходимо это проверить.
- Необходимо закрывать сессию при завершении работы с ней