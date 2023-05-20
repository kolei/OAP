[Каркас приложения. Модель данных. Привязка данных. Табличный вывод.](./wpf_template.md) | [Содержание](../readme.md) | [Поиск, сортировка](./wpf_search_sort.md)

# Фильтрация данных

В приложениях часто требуется отфильтровать данные либо по словарному полю, либо по каким-либо условиям. 

## Фильтрация по словарю

Суть фильтрации сводится к тому, что отображается не полный список объектов ("кошек"), а отфильтрованный по словарному полю (тип, категория...). Для получения фильтрованного списка реализуем геттер и сеттер для списка кошек:

>Запись типа `public IEnumerable<Cat> catList { get; set; }` на самом деле является так называемым "синтаксическим сахаром", т.е. сокращённой записью для упрощения написания и повышения читабельности кода.
>
>При компиляции этот код разворачивается примерно в такой (на самом деле get и set реализуются методами getcatList(){} и setcatList(value){})
>```cs
>private IEnumerable<Cat> _catList = null;
>public IEnumerable<Cat> catList {
>   get
>   {
>       return _catList;
>   }
>   set {
>       _catList = value;
>   } 
>}
>```
>То есть создаётся приватная переменная для хранения реального значения свойства и методы **get** и **set** для, соответственно, получения и сохранения значения свойства. "value" это новое значение свойства, устанавливаемое при присваивании.

```cs
public string selectedBreed = "";

private IEnumerable<Cat> _catList = null;
public IEnumerable<Cat> catList {
    get
    {
        // возвращаем не весь список, а фильтрованный по выбранной породе
        return _catList
            .Where(c=>(selectedBreed=="Все породы" || c.breed==selectedBreed));
    }
    set {
        _catList = value;
    } 
}
```

Таким обазом, при присваивании полный список "кошек" будет сохраняться в переменной *_catList*, а при чтении будет возвращаться отфильтрованный список

При работе с БД у нас обычно есть отдельные модели (таблицы) справочников - реализуем в нашем *поставщике данных* метод, возвращающий справочник пород:

1. Сначала создадим класс для элемента справочника (по идее нам было бы достаточно просто массива строк, но мы сразу будем делать "по-взрослому", чтобы сразу пройтись по всем "граблям", которые встретятся при работе с базой данных)

    ```cs
    public class CatBreed { 
        public string title { get; set; }
    }
    ```

1. Создаем в классе главного окна свойство для хранения справочника

    ```cs
    public List<CatBreed> catBreedList { get; set; }
    ```

    Здесь мы выбрали тип **List**, т.к. нам нужен изменяемый список, в который мы добавим элемент "Все породы"

1. В **интерфейс** поставщика данных (**IDataProvider**) добавляем декларацию метода для получения списка пород

    ```cs
    IEnumerable<CatBreed> getCatBreeds();
    ```

1. Реализуем этот метод в **LocalDataProvider**

    Этот метод можно реализовать двумя вариантами:

    * можно создать список руками

        ```cs
        public IEnumerable<CatBreed> getCatBreeds()
        {
            return new CatBreed[] {
                new CatBreed{ title="Дворняжка" },
                new CatBreed{ title="Шотландская вислоухая" },
                new CatBreed{ title="Сиамский" }
            };
        }
        ```

        Из плюсов то, что в списке могут быть породы, которых нет в исходных данных (практически это аналог запроса к базе данных). Минус в том, что вы можете пропустить породу, которая есть в исходных данных.

    * можно выбрать существующие породы из исходных данных (этот вариант предпочтительнее)

        >Первоначальный вариант, как оказалось, не работает в **WPF** (видимо метод *DiastinctBy*) появился в C# более старших версий
        >
        >```cs
        >public IEnumerable<CatBreed> getCatBreeds()
        >{
        >    return _catList.DistinctBy(cat => cat.breed)
        >        .Select(cat => new CatBreed { title = cat.breed });
        >}
        >```
        >
        >Что тут происходит?
        >
        >* метод *DistinctBy* выбирает записи с уникальным значением породы
        >* метод *Select* преобразует исходный список - вместо списка кошек получаем список пород

        ```cs
        public IEnumerable<CatBreed> getCatBreeds()
        {
            return _catList
                .Select(cat => cat.breed)
                .Distinct()
                .Select(breed => new CatBreed { title = breed });
        }
        ```

        Что тут происходит?

        Допустим исходный массив выглядит так (массив объектов): 

        ```
        [
            {breed: "Порода №1", name: "Имя1"}, 
            {breed: "Порода №2", name: "Имя2"}, 
            {breed: "Порода №1", name: "Имя3"} 
        ]
        ```

        * метод *Select* преобразует элемент массива в новый объект, и т.к. мы из всего объекта вернули только одно поле, то на выходе у нас будет массив пород:

            ```
            [
                "Порода №1", 
                "Порода №2",
                "Порода №1" 
            ]
            ```

        * метод *Distinct* вернёт массив уникальных занчений:

            ```
            [
                "Порода №1", 
                "Порода №2"
            ]
            ```

        * второй вызов *Select* преобразует массив строк в массив объектов типа **CatBreed**

1. Получаем список пород и добавляем в начало "Все породы", чтобы можно было отменить фильтрацию и отображать полный список

    ```cs
    catBreedList = Globals.dataProvider.getCatBreeds().ToList();
    catBreedList.Insert(0, new CatBreed { title = "Все породы" });
    ```

1. Теперь, имея список пород, добавляем в разметку (файл .xaml) выпадающий список для выбор породы (во WrapPanel):

    ```xml
    <Label 
        Content="Порода:"
        VerticalAlignment="Center"/>

    <ComboBox
        Name="BreedFilterComboBox"
        SelectionChanged="BreedFilterComboBox_SelectionChanged"
        VerticalAlignment="Center"
        MinWidth="100"
        SelectedIndex="0"
        ItemsSource="{Binding catBreedList}">

        <ComboBox.ItemTemplate>
            <DataTemplate>
                <Label 
                    Content="{Binding title}"/>
            </DataTemplate>
        </ComboBox.ItemTemplate>
    </ComboBox>
    ```

    Элемент **ComboBox** предназначен для отображения списка *строк*. Для того, чтобы отобразить элементы произвольного списка используется шаблон **ComboBox.ItemTemplate**, в котором можно реализовать произвольный вид элемента списка (вставить картинки, раскрасить и т.п.) и, в нашем случае, в качестве содержимого выбрать свойство объекта для отображения. 

    >Можно сделать проще, используя переопределение метода *getString*, но пока оставим так.

1. В классе главного окна в обработчике события выбора породы (*BreedFilterComboBox_SelectionChanged*) запоминаем выбранную породу

    ```cs
    selectedBreed = (BreedFilterComboBox.SelectedItem as CatBreed).title;
    ```

    Свойство *BreedFilterComboBox.SelectedItem* содержит выбранный элемент списка, в нашем случае это объект типа **CatBreed**.

Если сейчас запустить приложение, то выпадающий список будет отображаться, но реации на выбор не будет - дело в том, что визуальная часть не знает, что данные изменились. В одной из прошлых лекции мы упоминали про интерфейс **INotifyPropertyChanged** - реализуем его для нашего окна:

1. Добавляем интерфейс окну

    ```cs
    public partial class MainWindow : Window, INotifyPropertyChanged
                                            ^^^^^^^^^^^^^^^^^^^^^^^^
    ```

1. Реализуем интерфейс

    ```cs
    public event PropertyChangedEventHandler PropertyChanged;
    ```

1. Пишем метод, который будет сообщать визуальной части что изменился список кошек

    ```cs
    private void Invalidate()
    {
        if (PropertyChanged != null)
            PropertyChanged(this, new PropertyChangedEventArgs("catList"));
    }
    ```

1. В обработчик события выбора породы добавим вызов этого метода

    ```cs
    private void BreedFilterComboBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
    {
        selectedBreed = (BreedFilterComboBox.SelectedItem as CatBreed).title;
        Invalidate();
    }
    ```

## Фильтрация по условию

Иногда встречается требование сделать фильтр по условию. Сам принцип фильтрации остается прежним, только список элементов фильтра формируется программно.

Например, сделаем фильтр по возрасту кошек: котята (до года), молодые (1-10) и старые (>10)

1. Для начала сделаем класс для элементов фильтра:

    ```cs
    public class CatAge { 
        public string title { get; set; }
        public int ageFrom { get; set; }
        public int ageTo { get; set; }
    }
    ```

1. Затем создадим список и переменную для хранения выбранного элемента списка. Обратите внимание, тут мы храним не строку, а весь объект.

    ```cs
    private CatAge selectedAge = null;
    public IEnumerable<CatAge> catAgeList { get; set; } = new CatAge[]{
        new CatAge{title="Все возраста", ageFrom=0, ageTo=99},
        new CatAge{title="Котята", ageFrom=0, ageTo=1},
        new CatAge{title="Молодые", ageFrom=1, ageTo=10},
        new CatAge{title="Старые", ageFrom=10, ageTo=99}
    };
    ```

1. В разметке меняем привязку   

    ```xml
    <ComboBox
        Name="BreedFilterComboBox"
        SelectionChanged="BreedFilterComboBox_SelectionChanged"
        VerticalAlignment="Center"
        MinWidth="100"
        SelectedIndex="0"
        ItemsSource="{Binding catAgeList}">

        <ComboBox.ItemTemplate>
            <DataTemplate>
                <Label 
                    Content="{Binding title}"/>
            </DataTemplate>
        </ComboBox.ItemTemplate>
    </ComboBox>
    ```

1. В обработчике события выбора элемента списка просто запоминаем выбранный элемент

    ```cs
    private void BreedFilterComboBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
    {
        selectedAge = BreedFilterComboBox.SelectedItem as CatAge;
        Invalidate();
    }
    ```

1. И меняем геттер списка кошек

    ```cs
    get
    {
        return _catList
            .Where(c=>(c.age>=selectedAge.ageFrom && c.age<selectedAge.ageTo));
    }
    ```

[Каркас приложения. Модель данных. Привязка данных. Табличный вывод.](./wpf_template.md) | [Содержание](../readme.md) | [Поиск, сортировка](./wpf_search_sort.md)
