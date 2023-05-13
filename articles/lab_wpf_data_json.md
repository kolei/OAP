# Получение данных из внешних источников. JSON.

[Вспоминаем материалы лекции про типы данных](./t5_file_types.md#json)

1. Подгатавливаем файл с исходными данными:

    ```json
    [
        {
            "age": 1,
            "breed": "Дворняжка",
            "color": "Белый",
            "name": "Ириска",
            "dateOfLastVaccination": null
        },
        {
            "age": 2,
            "breed": "Шотландская вислоухая",
            "color": "Коричневый",
            "name": "Изи",
            "dateOfLastVaccination": "2020-01-31"
        },
        {
            "age": 3,
            "breed": "Сиамский",
            "color": "Цветной",
            "name": "Макс",
            "dateOfLastVaccination": "2022-05-10"
        },
    ]
    ```

    * `[]` - квадратные скобки означают, что у нас массив
    * `{}` - в фигурных скобках записана информация об объекте
    * названия полей (*age*, *bread* и т.д.) пишутся в кавычках
    * значения полей записываются в зависимости от типа данных
        * **int** - просто число
        * **double** - число с разделителем точка
        * **boolean** - литералы **true** или **false**
        * **string** - в кавычках, если в тексте есть кавычки, то они экранируются: `\"` 
        * **date** - для даты отдельного формата нет, записывается как строка

1. Импорт данных

    Для поддержки работы десериализатора и для обхода проблемы с датой в виде строки будем использовать [первый](./t5_file_types.md#работа-с-json-попытка-№2-datacontractjsonserializer) вариант десериализатора. 

    Добавляем в класс аттрибуты *[DataContract]* и *[DataMember]*:

    ```cs
    [DataContract]
    public class Cat
    {
        [DataMember]
        public string name { get; set; }
        [DataMember]
        public int age{ get; set; }
        [DataMember]
        public string color { get; set; }
        [DataMember]
        public string breed { get; set; }
        [DataMember]
        public string photo { get; set; }

        [DataMember(Name = "dateOfLastVaccination")]
        private string? stringDate { get; set; }

        [IgnoreDataMember]
        public DateTime? dateOfLastVaccination {
            get
            {
                return stringDate == null ? null : DateTime.Parse(stringDate);  
            }
            set
            {
                stringDate = value.ToString();
            } 
        }
    }
    ```

    И реализуем класс JSONDataProvider:

    ```cs
    public class JSONDataProvider
    {
        private List<Cat> _catList;
        
        public JSONDataProvider()
        {
            var serializer = new DataContractJsonSerializer(typeof(Cat[]));
            using (var sr = new StreamReader("/home/kei/temp/test.json"))
            {
                _catList = ((Cat[])serializer.ReadObject(sr.BaseStream)).ToList();
            }
        }

        public IEnumerable<Cat> getCats()
        {
            return _catList;
        }
    }
    ```

1. В классе окна меняем поставщика данных

# ЗАДАНИЕ

1. Подготовить набор данных (не менее 10 записей) с разными типами (обязательно должны быть: Int, Double, String, DateTime, Boolean)

1. Реализовать класс JSONDataProvider для своей предметной области

1. Поле с датой добавить в таблицу и указать формат вывода: `Binding="{Binding dateOfLastVaccination,StringFormat='dd.MM.yyyy'}"`

---

>Если вдруг нам приспичит делать десериализацию используя компонент **Newtonsoft.Json**, то для обхода проблемы со строковой датой можно реализовать класс-наследник **CatWithStringDates**, в котором перегрузить поле *dateOfLastVaccination*:
>```cs
>public class CatWithStringDates: Cat
>{
>    public string dateOfLastVaccination { get; set; }
>}
>```
>И при десериализации использовать этот класс:
>```cs
>var catList = JsonConvert.DeserializeObject<CatWithStringDates[]>("[{\"age\": 1, \"dateOfLastVaccination\": \"2020-01-01\"}]");
>```
>Затем, используя LINQ запрос преобразовать к нужному типу:
>```cs
>_catList = catList.Select(cat => new Cat {
>   age = cat.age,
>   dateOfLastVaccination = DateTime.Parse(cat.dateOfLastVaccination)
>}).ToList();
>```