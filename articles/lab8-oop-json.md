# ООП. Основы (JSON)

Основано на [этой](./t5_file_types.md#вариант-попроще) лекции

1. Создание класса

    В отличие от CSV данные десериализуются в класс, т.е. этот класс должен быть объявлен заранее, например:

    ```cs
    class Student
    {
        public string firstName {get;set;}
        public int age {get;set;}
    }
    ```

2. Подготовка файла для импорта

    ```json
    [
        {
            "firstName": "Сергей", 
            "age": 18
        },
        {
            "firstName": "Богдан", 
            "age": 17
        }
    ]
    ```

3. Импорт данных

    ```cs
    var buffer = File.ReadAllText("тут имя вашего файла");
    var serializer = new JavaScriptSerializer();
    var studentList = serializer.Deserialize<Student[]>(buffer);
    ...
    ```

# Задача

* сформировать файл с данными в формате JSON для вашей предметной области
* загрузить данные с программу из подготовленного файла
