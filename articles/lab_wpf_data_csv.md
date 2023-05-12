# Получение данных из внешних источников. CSV.

1. Для начала создаём файл с данными для импорта. Я продолжаю тему *кошек*, вы реализуете свою предметную область:

    >Мы должны уметь работать с разными типами данных, поэтому я добавил в исходные данные тип **Date** (дата прививки). Формат даты имеет множество разных форматов, но при экспорте обычно используют SQL формат (yyyy-mm-dd)

    ```csv
    1,"Дворняжка","Белый","Ириска",
    2,"Шотландская вислоухая","Коричневый","Изи",2020-01-31
    3,"Сиамский","Цветной","Макс",2022-05-10
    ```

    * разделитель: запятая
    * строковые литералы (текст, в котором могут встретиться спец.символы, а лучше все текстовые поля) заключаем в двойные кавычки
    * отсутствующие данные не заполняются (дата прививки у "Ириски"), но разделители колонок при этом указываются

    Файл сохраняем в подкаталог `bin/debug` вашего проекта - туда, где создается исполняемый (.exe) файл.

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
        public DateTime dateOfLastVaccination { get; set; }  
    }
    ```

1. Загружаем данные из файла в класс поставщика данных

    >Тут есть два варианта: либо каждый раз загружать данные при вызове метода **getCats**, либо загрузить один раз при создании экземпляра класса (в конструкторе). Оба варианта имеют право на жизнь: первый имеет смысл применять, если данные часто меняются, второй, если данные статичны. Я реализую второй вариант.

    [Вспоминаем материалы лекции про типы данных](./t5_file_types.md#csv) и создаём для работы с CSV файлами класс **CSVDataProvider**, реализующий интерфейс **IDataProvider**:

    * Создаём приватную переменную для хранения загруженного списка и считываем данные в конструкторе:

        ```cs
        public class SCVDataProvider : IDataProvider
        {
            private List<Cat> catList;

            // конструктор класса
            public CSVDataProvider()
            {
                // инициализируем переменную
                catList = new List<Cat>();

                // открываем файл с данными используя класс TextFieldParser
                using (TextFieldParser parser = new TextFieldParser(@"/home/kei/temp/test.csv"))
                {
                    parser.TextFieldType = FieldType.Delimited;
                    parser.SetDelimiters(",");

                    /*
                        По-умолчанию, в качестве разделителя разрядов 
                        в числах с плавающей запятой (double) является точка
                        Но конвертер использует текущую "культурную среду", а в России
                        разделителем является запятая
                        Чтобы явно указать разделитель мы межем конвертеру указать 
                        объект NumberFormatInfo
                    */
                    NumberFormatInfo provider = new NumberFormatInfo();
                    provider.NumberDecimalSeparator = ".";

                    while (!parser.EndOfData)
                    {
                        string[] fields = parser.ReadFields();

                        // проверяем количество полей
                        if (fields.Length == 5)
                        {
                            try
                            {
                                var newCat = new Cat();
                                newCat.age = Convert.ToInt32(fields[0]);
                                newCat.breed = fields[1];
                                newCat.color = fields[2];
                                newCat.name = fields[3];
                                // пример использования конвертера с провайдером
                                // newCat.someDouble = Convert.ToDouble(fields[3], provider);
                                try
                                {
                                    // дата может быть не задана, поэтому заворачиваю в исключение
                                    // хотя проще сделать проверку
                                    newCat.dateOfLastVaccination = DateTime.Parse(fields[4]);
                                }
                                catch (Exception e)
                                {
                                    newCat.dateOfLastVaccination = null;
                                }
                                catList.Add(newCat);
                            }
                            catch (Exception e)
                            {
                            }
                        }
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
