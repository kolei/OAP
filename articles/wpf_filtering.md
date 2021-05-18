<table style="width: 100%;"><tr><td style="width: 40%;">
<a href="../articles/wpf_template.md">Каркас приложения. Модель данных. Привязка данных. Табличный вывод.
</a></td><td style="width: 20%;">
<a href="../readme.md">Содержание
</a></td><td style="width: 40%;">
<a href="../articles/wpf_filtering.md">Фильтрация данных
</a></td><tr></table>

# Фильтрация данных

В приложениях часто требуется отфильтровать данные либо по словарному полю, либо по каким-либо условиям. 

## Фильтрация по словарю

Суть фильтрации сводится к тому, что отображается не полный список объектов ("кошек"), а отфильтрованный по словарному полю (тип, категория...). Для получения фильтрованного списка реализуем геттер и сеттер для списка кошек:

```cs
public string SelectedBreed = "";

private IEnumerable<Cat> _CatList = null;
public IEnumerable<Cat> CatList {
    get
    {
        return _CatList
            .Where(c=>(SelectedBreed=="Все породы" || c.Breed==SelectedBreed));
    }
    set {
        _CatList = value;
    } 
}
```

Таким обазом, при присваивании полный список "кошек" будет сохраняться в переменной *_CatList*, а при чтении будет возвращаться отфильтрованный список

При работе с БД у нас обычно есть отдельные модели (таблицы) справочников - реализуем в нашем поставщике данных метод, возвращающий справочник пород:

1. Сначала создадим класс для элемента справочника

    ```cs
    public class CatBreed { 
        public string Title { get; set; }
    }
    ```

    >Пока в этом особого смысла нет, но при работе с БД у нас будут таки классы, поэтому сразу привыкаем к правильному коду.

2. Создаем в классе главного окна свойство для хранения справочника

    ```cs
    public List<CatBreed> CatBreedList { get; set; }
    ```

    Здесь мы выбрали тип **List**, т.к. нам нужен изменяемый список, в который мы добавим элемент "Все породы"

3. В интерфейс поставщика данных (IDataProvider) добавляем метод для получения списка пород

    ```cs
    IEnumerable<CatBreed> GetCatBreeds();
    ```

4. Реализуем этот метод в LocalDataProvider

    ```cs
    public IEnumerable<CatBreed> GetCatBreeds()
    {
        return new CatBreed[] {
            new CatBreed{ Title="Дворняжка" },
            new CatBreed{ Title="Шотландская вислоухая" },
            new CatBreed{ Title="Сиамский" },
        };
    }
    ```

5. Получаем список пород и добавляем в начало "Все породы", чтобы можно было отменить фильтрацию и отображать полный список

    ```cs
    CatBreedList = Globals.dataProvider.GetCatBreeds().ToList();
    CatBreedList.Insert(0, new CatBreed { Title = "Все породы" });
    ```

4. Теперь, имея список пород, добавляем в разметку выпадающий список для выбор породы (во WrapPanel):

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
        ItemsSource="{Binding CatBreedList}">

        <ComboBox.ItemTemplate>
            <DataTemplate>
                <Label 
                    Content="{Binding Title}"/>
            </DataTemplate>
        </ComboBox.ItemTemplate>
    </ComboBox>
    ```

    Элемент **ComboBox** предназначен для отображения списка *строк*. Для того, чтобы отобразить элементы произвольного списка используется шаблон **ComboBox.ItemTemplate**, в котором можно реализовать произвольный вид элемента списка (вставить картинки, раскрасить и т.п.) и, в нашем случае, в качестве содержимого выбрать свойство объекта для отображения. 

5. В классе главного окна в обработчике события выбора породы (*BreedFilterComboBox_SelectionChanged*) запоминаем выбранную породу

    ```cs
    SelectedBreed = (BreedFilterComboBox.SelectedItem as CatBreed).Title;
    ```

    Свойство *BreedFilterComboBox.SelectedItem* содержит выбранный элемент списка, в нашем случае это объект типа **CatBreed**.

Если сейчас запустить приложение, то выпадающий список будет отображаться, но реации на выбор не будет - дело в том, что визуальная часть не знает, что данные изменились. В одной из прошлых лекции мы упоминали про интерфейс **INotifyPropertyChanged** - реализуем его для нашего окна:

1. Добавляем интерфейс окну

    ```cs
    public partial class MainWindow : Window, INotifyPropertyChanged
    ```

2. Реализуем интерфейс

    ```cs
    public event PropertyChangedEventHandler PropertyChanged;
    ```

3. Пишем метод, который будет сообщать визуальной части что изменился список кошек

    ```cs
    private void Invalidate()
    {
        if (PropertyChanged != null)
            PropertyChanged(this, new PropertyChangedEventArgs("CatList"));
    }
    ```

4. В обработчик события выбора породы добавим вызов этого метода

    ```cs
    private void BreedFilterComboBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
    {
        SelectedBreed = (BreedFilterComboBox.SelectedItem as CatBreed).Title;
        Invalidate();
    }
    ```

## Фильтрация по условию

Иногда встречается требование сделать фильтр по условию. Сам принцип фильтрации остается прежним, только список элементов фильтра формируется программно.

Например, сделаем фильтр по возрасту кошек: котята (до года), молодые (1-10) и старые (>10)

1. Для начала сделаем класс для элементов фильтра:

    ```cs
    public class CatAge { 
        public string Title { get; set; }
        public int AgeFrom { get; set; }
        public int AgeTo { get; set; }
    }
    ```

2. Затем создадим список и переменную для хранения выбранного элемента списка. Обратите внимание, тут мы храним не строку, а весь объект.

    ```cs
    public CatAge SelectedAge = null;
    public IEnumerable<CatAge> CatAgeList { get; set; } = new CatAge[]{
        new CatAge{Title="Все возраста", AgeFrom=0, AgeTo=99},
        new CatAge{Title="Котята", AgeFrom=0, AgeTo=1},
        new CatAge{Title="Молодые", AgeFrom=1, AgeTo=10},
        new CatAge{Title="Старые", AgeFrom=10, AgeTo=99}
    };
    ```

3. В разметке меняем привязку   

    ```xml
    <ComboBox
        Name="BreedFilterComboBox"
        SelectionChanged="BreedFilterComboBox_SelectionChanged"
        VerticalAlignment="Center"
        MinWidth="100"
        SelectedIndex="0"
        ItemsSource="{Binding CatAgeList}">

        <ComboBox.ItemTemplate>
            <DataTemplate>
                <Label 
                    Content="{Binding Title}"/>
            </DataTemplate>
        </ComboBox.ItemTemplate>
    </ComboBox>
    ```

4. В обработчике события выбора элемента списка просто запоминаем выбранный элемент

    ```cs
    private void BreedFilterComboBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
    {
        SelectedAge = BreedFilterComboBox.SelectedItem as CatBreed;
        Invalidate();
    }
    ```

5. И меняем геттер списка кошек

    ```cs
    get
    {
        return _CatList
            .Where(c=>(c.Age>=SelectedAge.AgeFrom && c.Age<SelectedAge.AgeTo));
    }
    ```