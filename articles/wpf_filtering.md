<table style="width: 100%;"><tr><td style="width: 40%;">
<a href="../articles/wpf_template.md">Каркас приложения. Модель данных. Привязка данных. Табличный вывод.
</a></td><td style="width: 20%;">
<a href="../readme.md">Содержание
</a></td><td style="width: 40%;">
<a href="../articles/wpf_filtering.md">Фильтрация данных
</a></td><tr></table>

# Фильтрация данных

В приложениях часто требуется отфильтровать данные либо по словарному полю, либо по каким-либо условиям. На втором варианте мы пока останавливаться не будем - сделаем фильтрацию по словарю.

Суть фильтрации сводится к тому, что возвращается не полный список объектов ("кошек"), а отфильтрованный по какому-то признаку. Для получения фильтрованного списка реализуем геттер и сеттер для списка кошек:

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

3. В интерфейс поставщика данных (IDataProvider) добавляем метод для получения списка категорий

    ```cs
    IEnumerable<CatBreed> GetCatBreeds();
    ```

4. Реализуем этот метод в LocalDataProvider

    ```cs
    public IEnumerable<Cat> GetCats()
    {
        return new Cat[]{
            new Cat{Age=1,Breed="Дворняжка", Color="Белый", Name="Ириска"},
            new Cat{Age=2,Breed="Шотландская вислоухая", Color="Коричневый", Name="Изи"},
            new Cat{Age=2,Breed="Шотландская вислоухая", Color="Коричневый", Name="Изя"},
            new Cat{Age=3,Breed="Сиамский", Color="Цветной", Name="Макс"}
        };
    }
    ```

5. Получаем список пород и добавляем в начало "Все породы"

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

5. В классе главного окна в обработчике события выбора породы запоминаем выбранную породу

    ```cs
    SelectedBreed = (BreedFilterComboBox.SelectedItem as CatBreed).Title;
    ```

Если сейчас запустить приложение, то выпадающий список будет отображаться, но реации на выбор не будет - дело в том, что визуальная часть не знает, что данные изменились. В одной из прошлых лекции мы упоминали про интерфейс INotifyPropertyChanged - реализуем его для нашего окна:

1. Добавляем интерфейс окну

    ```cs
    public partial class MainWindow : Window, INotifyPropertyChanged
    ```

2. Реализуем интерфейс

    ```cs
    public event PropertyChangedEventHandler PropertyChanged;
    ```

3. Пишем метод, который будет сообщать визуальной части что что-то изменилось

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
