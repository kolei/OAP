# Получение данных из внешних источников. CSV.

1. Для начала создаём файл с данными для импорта. Я продолжаю тему *кошек*, вы реализуете свою предметную область:

    >Мы должны уметь работать с разными типами данных, поэтому я добавил в исходные данные тип **Date** (дата прививки). Формат даты имеет множество разных форматов, но при экспорте обычно используют SQL формат (`yyyy-mm-dd`)

    ```csv
    age,breed,color,name,,dateOfLastVaccination
    1,"Дворняжка","Белый","Ириска",,2024-04-29
    2,"Шотландская вислоухая","Коричневый","Изи",,2020-01-31
    3,"Сиамский","Цветной","Макс",,2022-05-10
    ```

    * в первой строке названия полей, соответствующие модели данных
    * разделитель запятая
    * строковые литералы (текст, в котором могут встретиться спец.символы, а лучше все текстовые поля) заключаем в двойные кавычки
    * для отсутствующих полей (у меня `photo`) оставляем пустую строку

    Файл сохраняем в подкаталог `bin/debug/net8.0-windows` вашего проекта - туда, где создается исполняемый (.exe) файл (название зависит от версии .NET и платформы).

1. Правим модель (у нас добавилось свойство "Дата последней прививки")

    ```cs
    public class Cat
    {
        public string name { get; set; }
        public int age{ get; set; }
        public string color { get; set; }
        // порода
        public string breed { get; set; }
        public string photo { get; set; }
        // новое свойство
        public DateOnly dateOfLastVaccination { get; set; }  
    }
    ```

1. Загружаем данные из файла в класс поставщика данных

    >Тут есть два варианта: либо каждый раз загружать данные при вызове метода **getCats**, либо загрузить один раз при создании экземпляра класса (в конструкторе). Оба варианта имеют право на жизнь: первый имеет смысл применять, если данные часто меняются, второй, если данные статичны. Я реализую второй вариант.

    [Вспоминаем материалы лекции про типы данных](./t5_file_types.md#csv) и создаём для работы с CSV файлами класс **CSVDataProvider**, реализующий интерфейс **IDataProvider**:

    * Создаём приватную переменную для хранения загруженного списка и считываем данные в конструкторе:

        Библиотека **CsvHelper** достаточно "умная" и преобразует строку в дату автоматически

        ```cs
        public class SCVDataProvider : IDataProvider
        {
            private List<Cat> catList;

            // конструктор класса
            public CSVDataProvider()
            {
                using (var reader = new StreamReader("./cat.csv")) {
                    using (var csv = new CsvReader(
                        reader, 
                        CultureInfo.InvariantCulture))
                    {
                        catList = csv.GetRecords<Foo>();
                    }
                }
            }
        }
        ```

    * реализуем интерфейс **IDataProvider** (пишем метод **getCats**):

        ```cs
        public IEnumerable<Cat> getCats()
        {
            return catList;
        }
        ```

1. Теперь в конструкторе окна меняем класс провайдера и всё продолжает работать

    ```cs
    public MainWindow()
    {
        InitializeComponent();
        DataContext = this;
        // Globals.dataProvider = new LocalDataProvider();
        Globals.dataProvider = new CSVDataProvider();
        CatList = Globals.dataProvider.getCats();
    }
    ```

# ЗАДАНИЕ

1. Подготовить набор данных (не менее 10 записей) с разными типами (обязательно должны быть: Int, Double, String, DateTime, Boolean)

1. Реализовать класс CSVDataProvider для своей предметной области

1. Поле с датой добавить в таблицу и указать формат вывода: `Binding="{Binding YourColumn,StringFormat='dd.MM.yyyy'}"`
